import re
import json
from pathlib import Path
from typing import List, Optional

import yaml
from rich.console import Console
from rich.table import Table

console = Console()


class SecretPattern:
    def __init__(self, name: str, pattern: str, severity: str, verification_hint: str):
        self.name = name
        self.pattern = pattern
        self.severity = severity
        self.verification_hint = verification_hint


class SecretFinding:
    def __init__(self, pattern: SecretPattern, file_path: str, line_number: int, match: str):
        self.pattern = pattern
        self.file_path = file_path
        self.line_number = line_number
        self.match = match[:80]


class SecretScanner:
    PATTERNS = [
        SecretPattern("AWS Access Key", r"(?i)AKIA[0-9A-Z]{16}", "CRITICAL",
                       "Check if key is active in AWS IAM"),
        SecretPattern("AWS Secret Key", r"(?i)(?<![A-Za-z0-9])[A-Za-z0-9\/+=]{40}(?![A-Za-z0-9\/+=])", "CRITICAL",
                       "Try using the key with AWS CLI"),
        SecretPattern("GitHub Token", r"(?i)(ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9_]{36,}", "CRITICAL",
                       "Check GitHub for associated account"),
        SecretPattern("Generic API Key", r"(?i)(api[_-]?key|apikey|api[_-]?secret|api_secret)\s*[=:]\s*['\"][A-Za-z0-9_\-\.]{16,}['\"]",
                       "HIGH", "Verify with the API provider"),
        SecretPattern("JWT Token", r"eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}",
                       "HIGH", "Decode JWT payload to check"),
        SecretPattern("Private Key", r"-----BEGIN\s?(RSA|DSA|EC|OPENSSH|PGP)?\s?PRIVATE KEY-----",
                       "CRITICAL", "Check if key is used in production"),
        SecretPattern("Password in Code", r"(?i)(password|passwd|pwd)\s*[=:]\s*['\"][^'\"]{8,}['\"]",
                       "HIGH", "Check if credential is valid"),
        SecretPattern("Slack Token", r"xox[baprs]-[0-9a-zA-Z-]{10,}", "HIGH",
                       "Check Slack workspace for token"),
        SecretPattern("GCP Service Account", r"\"type\":\s*\"service_account\"", "CRITICAL",
                       "Check GCP IAM for service account key"),
        SecretPattern("Connection String", r"(?i)(mongodb|postgresql|mysql|redis)://[^@]+@", "CRITICAL",
                       "Test connection to database"),
    ]

    def __init__(self, custom_patterns: Optional[List[SecretPattern]] = None):
        self.patterns = custom_patterns or self.PATTERNS

    def scan_file(self, file_path: Path) -> List[SecretFinding]:
        findings = []
        try:
            content = file_path.read_text(errors="ignore")
            lines = content.split("\n")

            for pattern in self.patterns:
                for i, line in enumerate(lines, 1):
                    matches = re.findall(pattern.pattern, line)
                    for match in matches:
                        findings.append(SecretFinding(pattern, str(file_path), i, match))
        except Exception:
            pass

        return findings

    def scan_directory(self, directory: Path, exclude_dirs: Optional[List[str]] = None) -> List[SecretFinding]:
        exclude_dirs = exclude_dirs or [".git", "node_modules", "venv", "__pycache__", ".venv"]
        findings = []

        for file_path in directory.rglob("*"):
            if any(excluded in file_path.parts for excluded in exclude_dirs):
                continue
            if file_path.is_file() and not file_path.suffix in {".pyc", ".jpg", ".png", ".gif", ".ico", ".woff", ".woff2", ".eot", ".ttf"}:
                findings.extend(self.scan_file(file_path))

        return findings

    def generate_report(self, findings: List[SecretFinding]) -> str:
        table = Table(title="Secret Scan Results")
        table.add_column("Severity", style="bold")
        table.add_column("Pattern", style="cyan")
        table.add_column("File", style="green")
        table.add_column("Line", style="yellow")
        table.add_column("Match", style="white")
        table.add_column("Verification", style="dim")

        for f in findings:
            color = "red" if f.pattern.severity == "CRITICAL" else "yellow"
            table.add_row(f"[{color}]{f.pattern.severity}[/{color}]",
                          f.pattern.name,
                          f.file_path,
                          str(f.line_number),
                          f.match,
                          f.pattern.verification_hint)

        return table


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Secret Scanner - Detect hardcoded secrets in code")
    parser.add_argument("target", help="File or directory to scan")
    parser.add_argument("--exclude-dir", nargs="*", default=[".git", "node_modules", "venv"],
                        help="Directories to exclude")
    parser.add_argument("--output", help="Output JSON file path")

    args = parser.parse_args()
    target = Path(args.target)
    scanner = SecretScanner()

    if target.is_file():
        findings = scanner.scan_file(target)
    else:
        findings = scanner.scan_directory(target, args.exclude_dir)

    report = scanner.generate_report(findings)
    console.print(report)
    console.print(f"\nTotal secrets found: {len(findings)}")
    critical = len([f for f in findings if f.pattern.severity == "CRITICAL"])
    high = len([f for f in findings if f.pattern.severity == "HIGH"])
    console.print(f"[red]Critical: {critical}[/red] | [yellow]High: {high}[/yellow]")

    if args.output:
        report_json = json.dumps([
            {
                "pattern": f.pattern.name,
                "severity": f.pattern.severity,
                "file": f.file_path,
                "line": f.line_number,
                "match": f.match,
            }
            for f in findings
        ], indent=2)
        Path(args.output).write_text(report_json)
        console.print(f"[green]Report saved to {args.output}[/green]")

    return len(findings)


if __name__ == "__main__":
    main()
