import json
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional

import yaml
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()


class SigmaRule:
    def __init__(self, title: str, id: str, description: str, level: str,
                 logsource: dict, detection: dict, falsepositives: List[str]):
        self.title = title
        self.id = id
        self.description = description
        self.level = level
        self.logsource = logsource
        self.detection = detection
        self.falsepositives = falsepositives


class Alert:
    def __init__(self, rule: SigmaRule, source: str, timestamp: datetime,
                 fields: Dict[str, str]):
        self.rule = rule
        self.source = source
        self.timestamp = timestamp
        self.fields = fields


class ThreatDetector:
    def __init__(self, rules_dir: Optional[Path] = None):
        self.rules = []
        if rules_dir:
            self.load_rules(rules_dir)

    def load_rules(self, rules_dir: Path):
        for rule_file in rules_dir.glob("*.yml"):
            try:
                data = yaml.safe_load(rule_file.read_text())
                self.rules.append(SigmaRule(
                    title=data.get("title", "Unknown"),
                    id=data.get("id", ""),
                    description=data.get("description", ""),
                    level=data.get("level", "medium"),
                    logsource=data.get("logsource", {}),
                    detection=data.get("detection", {}),
                    falsepositives=data.get("falsepositives", []),
                ))
            except Exception as e:
                console.print(f"[yellow]Warning:[/yellow] Could not load rule {rule_file}: {e}")

    def analyze_log_line(self, line: str, source: str) -> Optional[Alert]:
        for rule in self.rules:
            selection = rule.detection.get("selection", {})
            matches = True

            for key, value in selection.items():
                if isinstance(value, str):
                    if value not in line:
                        matches = False
                        break
                elif isinstance(value, list):
                    if not any(v in line for v in value):
                        matches = False
                        break

            if matches:
                return Alert(
                    rule=rule,
                    source=source,
                    timestamp=datetime.utcnow(),
                    fields={"raw": line[:200]}
                )
        return None

    def monitor_log_file(self, log_path: Path, callback=None):
        console.print(f"[green]Monitoring {log_path}...[/green]")
        alerts = []

        with open(log_path) as f:
            f.seek(0, 2)
            while True:
                line = f.readline()
                if line:
                    alert = self.analyze_log_line(line.strip(), str(log_path))
                    if alert:
                        alerts.append(alert)
                        if callback:
                            callback(alert)
                        self.display_alert(alert)
                else:
                    import time
                    time.sleep(0.1)

        return alerts

    def display_alert(self, alert: Alert):
        panel = Panel(
            f"[red]Rule:[/red] {alert.rule.title}\n"
            f"[yellow]Severity:[/yellow] {alert.rule.level.upper()}\n"
            f"[cyan]Source:[/cyan] {alert.source}\n"
            f"[green]Time:[/green] {alert.timestamp.isoformat()}\n"
            f"[white]Description:[/white] {alert.rule.description}",
            title=f"🚨 Alert: {alert.rule.title}",
            border_style="red"
        )
        console.print(panel)

    def search_logs(self, log_path: Path, timeframe_hours: int = 24) -> List[Alert]:
        alerts = []
        cutoff = datetime.utcnow() - timedelta(hours=timeframe_hours)
        log_path = Path(log_path)

        if log_path.is_file():
            for line in log_path.read_text().split("\n"):
                alert = self.analyze_log_line(line, str(log_path))
                if alert:
                    alerts.append(alert)
        elif log_path.is_dir():
            for f in log_path.glob("*.log"):
                alerts.extend(self.search_logs(f, timeframe_hours))

        return alerts

    def generate_report(self, alerts: List[Alert]) -> str:
        table = Table(title="Thint Detection Report")
        table.add_column("Timestamp", style="cyan")
        table.add_column("Severity", style="bold")
        table.add_column("Rule", style="green")
        table.add_column("Source")
        table.add_column("Description")

        for alert in sorted(alerts, key=lambda a: a.timestamp, reverse=True):
            color = "red" if alert.rule.level in {"high", "critical"} else "yellow"
            table.add_row(
                alert.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                f"[{color}]{alert.rule.level.upper()}[/{color}]",
                alert.rule.title,
                alert.source,
                alert.rule.description[:60]
            )

        return table


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Threat Detector - Log-based threat detection")
    parser.add_argument("--input", required=True, help="Log file or directory to analyze")
    parser.add_argument("--rules", default="rules/sigma", help="Sigma rules directory")
    parser.add_argument("--timeframe", type=int, default=24, help="Timeframe in hours")
    parser.add_argument("--watch", action="store_true", help="Watch mode (follow log)")
    parser.add_argument("--output", help="Output file path")

    args = parser.parse_args()
    detector = ThreatDetector(rules_dir=Path(args.rules))
    input_path = Path(args.input)

    if args.watch:
        detector.monitor_log_file(input_path)
    else:
        alerts = detector.search_logs(input_path, args.timeframe)
        report = detector.generate_report(alerts)

        if args.output:
            Path(args.output).write_text(str(report))
        else:
            console.print(report)

        console.print(f"\nTotal alerts: {len(alerts)}")
        high = len([a for a in alerts if a.rule.level in {"high", "critical"}])
        medium = len([a for a in alerts if a.rule.level == "medium"])
        console.print(f"[red]High/Critical: {high}[/red] | [yellow]Medium: {medium}[/yellow]")


if __name__ == "__main__":
    main()
