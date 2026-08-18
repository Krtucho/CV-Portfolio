import ast
import json
import re
from pathlib import Path
from typing import List, Optional

import yaml
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()


class SASTRule:
    def __init__(self, rule_id: str, name: str, severity: str, pattern: str, cwe: str, description: str, remediation: str):
        self.rule_id = rule_id
        self.name = name
        self.severity = severity
        self.pattern = pattern
        self.cwe = cwe
        self.description = description
        self.remediation = remediation


class Finding:
    def __init__(self, rule: SASTRule, file_path: str, line_number: int, snippet: str):
        self.rule = rule
        self.file_path = file_path
        self.line_number = line_number
        self.snippet = snippet


class SASTScanner:
    RULES = [
        SASTRule("S001", "Hardcoded Password", "HIGH",
                 r"(password|passwd|pwd|secret|token|api_key|apikey)\s*[=:]\s*['\"][^'\"]+['\"]",
                 "CWE-798", "Hardcoded credentials found", "Use environment variables or a secret manager"),
        SASTRule("S002", "SQL Injection", "HIGH",
                 r"execute\s*\(\s*['\"].*\{.*\}.*['\"]", "CWE-89",
                 "String interpolation in SQL query", "Use parameterized queries with placeholders"),
        SASTRule("S003", "Debug Code", "MEDIUM",
                r"(print|console\.log|debugger|var_dump|dd\()", "CWE-489",
                "Debug code left in production", "Remove debug statements before deployment"),
        SASTRule("S004", "Weak Hash Algorithm", "MEDIUM",
                 r"(md5|sha1)\s*\(", "CWE-327",
                 "Weak cryptographic hash function", "Use SHA-256 or stronger"),
        SASTRule("S005", "Command Injection", "HIGH",
                 r"(os\.system|subprocess\.call|subprocess\.Popen|eval|exec)\s*\(",
                 "CWE-78", "Potential command injection", "Use safe APIs and validate input"),
    ]

    def __init__(self, rules: Optional[List[SASTRule]] = None):
        self.rules = rules or self.RULES

    def scan_file(self, file_path: Path) -> List[Finding]:
        findings = []
        try:
            content = file_path.read_text(errors="ignore")
            lines = content.split("\n")

            for rule in self.rules:
                for i, line in enumerate(lines, 1):
                    if re.search(rule.pattern, line, re.IGNORECASE):
                        findings.append(Finding(rule, str(file_path), i, line.strip()))
        except Exception as e:
            console.print(f"[yellow]Warning:[/yellow] Could not scan {file_path}: {e}")

        return findings

    def scan_directory(self, directory: Path, exclude_dirs: Optional[List[str]] = None) -> List[Finding]:
        exclude_dirs = exclude_dirs or [".git", "node_modules", "venv", "__pycache__", ".venv"]
        findings = []

        for file_path in directory.rglob("*"):
            if any(excluded in file_path.parts for excluded in exclude_dirs):
                continue
            if file_path.suffix in {".py", ".js", ".ts", ".jsx", ".tsx", ".php", ".java", ".go", ".rb", ".sh", ".yaml", ".yml", ".tf"}:
                findings.extend(self.scan_file(file_path))

        return findings

    def generate_report(self, findings: List[Finding], output_format: str = "table") -> str:
        if output_format == "json":
            return json.dumps([
                {
                    "rule_id": f.rule.rule_id,
                    "name": f.rule.name,
                    "severity": f.rule.severity,
                    "cwe": f.rule.cwe,
                    "file": f.file_path,
                    "line": f.line_number,
                    "snippet": f.snippet,
                    "description": f.rule.description,
                    "remediation": f.rule.remediation,
                }
                for f in findings
            ], indent=2)

        table = Table(title="SAST Scan Results")
        table.add_column("Severity", style="bold")
        table.add_column("Rule", style="cyan")
        table.add_column("File", style="green")
        table.add_column("Line", style="yellow")
        table.add_column("Snippet", style="white")

        for f in findings:
            color = "red" if f.rule.severity == "HIGH" else "yellow" if f.rule.severity == "MEDIUM" else "blue"
            table.add_row(f"[{color}]{f.rule.severity}[/{color}]",
                          f.rule.name,
                          f.file_path,
                          str(f.line_number),
                          f.snippet[:80])

        return table


def main():
    import argparse
    parser = argparse.ArgumentParser(description="SAST Scanner - Static Application Security Testing")
    parser.add_argument("target", help="File or directory to scan")
    parser.add_argument("--severity", choices=["low", "medium", "high", "critical"], default="medium",
                        help="Minimum severity level")
    parser.add_argument("--format", choices=["table", "json"], default="table",
                        help="Output format")
    parser.add_argument("--output", help="Output file path")
    parser.add_argument("--exclude-dir", nargs="*", default=[".git", "node_modules", "venv"],
                        help="Directories to exclude")

    args = parser.parse_args()
    target = Path(args.target)
    scanner = SASTScanner()

    if target.is_file():
        findings = scanner.scan_file(target)
    else:
        findings = scanner.scan_directory(target, args.exclude_dir)

    if args.severity == "high":
        findings = [f for f in findings if f.rule.severity == "HIGH"]
    elif args.severity == "medium":
        findings = [f for f in findings if f.rule.severity in {"HIGH", "MEDIUM"}]

    report = scanner.generate_report(findings, args.format)

    if args.output:
        Path(args.output).write_text(report)
        console.print(f"[green]Report saved to {args.output}[/green]")
    else:
        if args.format == "json":
            console.print(report)
        else:
            console.print(report)
            console.print(f"\nTotal findings: {len(findings)}")
            high = len([f for f in findings if f.rule.severity == "HIGH"])
            medium = len([f for f in findings if f.rule.severity == "MEDIUM"])
            low = len([f for f in findings if f.rule.severity == "LOW"])
            console.print(f"[red]High: {high}[/red] | [yellow]Medium: {medium}[/yellow] | [blue]Low: {low}[/blue]")


if __name__ == "__main__":
    main()
