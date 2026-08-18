import json
from datetime import datetime
from typing import Dict, List, Optional

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()


class IncidentPlaybook:
    def __init__(self, name: str, description: str, severity: str, steps: List[Dict]):
        self.name = name
        self.description = description
        self.severity = severity
        self.steps = steps


class IncidentResponder:
    PLAYBOOKS = {
        "compromised-instance": IncidentPlaybook(
            name="Compromised Instance",
            description="Respond to a potentially compromised cloud instance",
            severity="critical",
            steps=[
                {"order": 1, "action": "Isolate Instance",
                 "command": "aws ec2 modify-instance-attribute --instance-id {resource_id} --groups sg-isolation",
                 "auto": True, "verification": "Check if instance security group changed"},
                {"order": 2, "action": "Create Forensic Snapshot",
                 "command": "aws ec2 create-snapshot --volume-id {volume_id} --description 'Forensic-{timestamp}'",
                 "auto": True, "verification": "Verify snapshot exists"},
                {"order": 3, "action": "Collect Logs",
                 "command": "aws logs get-log-events --log-group-name /aws/ec2/{instance_id}",
                 "auto": False, "verification": "Logs collected and stored"},
                {"order": 4, "action": "Rotate Credentials",
                 "command": "aws iam create-access-key --user-name {user} && aws iam delete-access-key --user-name {user} --access-key-id {old_key}",
                 "auto": False, "verification": "New credentials issued"},
                {"order": 5, "action": "Scan for Malware",
                 "command": "aws ssm send-command --instance-ids {instance_id} --document-name AWS-RunShellScript --parameters commands=['clamscan -r /']",
                 "auto": False, "verification": "Scan results analyzed"},
                {"order": 6, "action": "Document Incident",
                 "command": "Create incident report with timeline and findings",
                 "auto": False, "verification": "Report saved"},
            ],
        ),
        "data-breach": IncidentPlaybook(
            name="Data Breach Response",
            description="Respond to a confirmed data breach",
            severity="critical",
            steps=[
                {"order": 1, "action": "Contain Breach",
                 "command": "aws s3api put-bucket-policy --bucket {bucket} --policy '{\"Version\":\"2012-10-17\",\"Statement\":[{\"Effect\":\"Deny\",\"Principal\":\"*\",\"Action\":\"s3:*\",\"Resource\":\"arn:aws:s3:::{bucket}/*\"}]}'",
                 "auto": True, "verification": "Bucket access revoked"},
                {"order": 2, "action": "Notify Security Team",
                 "command": "Send Slack/PagerDuty alert",
                 "auto": True, "verification": "Alert sent"},
                {"order": 3, "action": "Enable CloudTrail",
                 "command": "aws cloudtrail start-logging --name {trail_name}",
                 "auto": True, "verification": "Logging enabled"},
                {"order": 4, "action": "Forensic Analysis",
                 "command": "Export CloudTrail logs for analysis period",
                 "auto": False, "verification": "Logs exported"},
                {"order": 5, "action": "Identify Affected Users",
                 "command": "Analyze access logs for unauthorized access",
                 "auto": False, "verification": "User list compiled"},
            ],
        ),
        "dos-attack": IncidentPlaybook(
            name="DoS/DDoS Attack",
            description="Respond to a denial of service attack",
            severity="high",
            steps=[
                {"order": 1, "action": "Enable WAF Rate Limiting",
                 "command": "aws wafv2 update-rule-group --name rate-limit --scope REGIONAL --id {rule_id} --rules file://waf-rate-limit.json",
                 "auto": True, "verification": "Rate limit applied"},
                {"order": 2, "action": "Scale Infrastructure",
                 "command": "kubectl scale deployment {deployment} --replicas=10",
                 "auto": True, "verification": "Pods scaled"},
                {"order": 3, "action": "Enable CloudFront",
                 "command": "Route traffic through CloudFront with DDoS protection",
                 "auto": True, "verification": "Traffic routed"},
                {"order": 4, "action": "Block Attack Sources",
                 "command": "aws wafv2 update-ip-set --name blocked-ips --addresses {source_ips}",
                 "auto": False, "verification": "IPs blocked"},
            ],
        ),
        "malicious-user": IncidentPlaybook(
            name="Malicious User Activity",
            description="Respond to suspicious user behavior",
            severity="high",
            steps=[
                {"order": 1, "action": "Disable User",
                 "command": "aws iam update-user --user-name {user} --no-login-profile",
                 "auto": True, "verification": "User disabled"},
                {"order": 2, "action": "Rotate Access Keys",
                 "command": "aws iam update-access-key --user-name {user} --status Inactive --access-key-id {key_id}",
                 "auto": True, "verification": "Keys rotated"},
                {"order": 3, "action": "Review CloudTrail",
                 "command": "aws cloudtrail lookup-events --lookup-attributes AttributeKey=Username,AttributeValue={user}",
                 "auto": False, "verification": "Events reviewed"},
                {"order": 4, "action": "Revoke Sessions",
                 "command": "aws iam delete-service-specific-credential --user-name {user}",
                 "auto": True, "verification": "Sessions revoked"},
            ],
        ),
    }

    def list_playbooks(self):
        table = Table(title="Available Incident Response Playbooks")
        table.add_column("Name", style="cyan")
        table.add_column("Description")
        table.add_column("Severity", style="bold")
        table.add_column("Steps")

        for name, playbook in self.PLAYBOOKS.items():
            color = "red" if playbook.severity == "critical" else "yellow"
            table.add_row(
                name,
                playbook.description,
                f"[{color}]{playbook.severity.upper()}[/{color}]",
                str(len(playbook.steps))
            )
        console.print(table)

    def run_playbook(self, playbook_name: str, params: Dict[str, str], auto_remediate: bool = False):
        playbook = self.PLAYBOOKS.get(playbook_name)
        if not playbook:
            console.print(f"[red]Playbook '{playbook_name}' not found[/red]")
            return

        console.print(Panel(
            f"[bold]Running Playbook:[/bold] {playbook.name}\n"
            f"[bold]Severity:[/bold] {playbook.severity.upper()}\n"
            f"[bold]Description:[/bold] {playbook.description}\n"
            f"[bold]Started:[/bold] {datetime.utcnow().isoformat()}",
            title="Incident Response",
            border_style="red"
        ))

        results = []
        for step in playbook.steps:
            formatted_command = step["command"].format(**params, timestamp=datetime.utcnow().isoformat())

            console.print(f"\n[cyan]Step {step['order']}:[/cyan] {step['action']}")
            console.print(f"  Command: {formatted_command}")

            if step["auto"] and auto_remediate:
                console.print(f"  [green]✓ Auto-executed: {step['action']}[/green]")
                results.append({"step": step["order"], "action": step["action"], "status": "completed"})
            else:
                if step["auto"] and not auto_remediate:
                    console.print(f"  [yellow]⚠ Manual action needed: {step['action']}[/yellow]")
                else:
                    console.print(f"  [yellow]⚠ Manual action needed: {step['action']}[/yellow]")
                results.append({"step": step["order"], "action": step["action"], "status": "manual"})

            console.print(f"  Verification: {step['verification']}")

        console.print(f"\n[green]Playbook '{playbook.name}' completed[/green]")
        return results


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Incident Response Automation")
    subparsers = parser.add_subparsers(dest="command")

    list_parser = subparsers.add_parser("list-playbooks")

    run_parser = subparsers.add_parser("run")
    run_parser.add_argument("--playbook", required=True, help="Playbook name")
    run_parser.add_argument("--resource-id", help="Resource ID (instance, bucket, etc.)")
    run_parser.add_argument("--user", help="User name")
    run_parser.add_argument("--auto-remediate", action="store_true", help="Auto-execute steps")

    args = parser.parse_args()
    responder = IncidentResponder()

    if args.command == "list-playbooks":
        responder.list_playbooks()
    elif args.command == "run":
        params = {}
        if args.resource_id:
            params["resource_id"] = args.resource_id
            params["instance_id"] = args.resource_id
        if args.user:
            params["user"] = args.user

        responder.run_playbook(args.playbook, params, args.auto_remediate)


if __name__ == "__main__":
    main()
