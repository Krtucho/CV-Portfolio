# Security Automation & Monitoring Toolkit

A comprehensive Python-based security toolkit for **vulnerability scanning, log monitoring, secret management, penetration testing automation, and incident response**. Designed for DevSecOps workflows with cloud-native integrations.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Modules](#modules)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
  - [Vulnerability Scanner](#1-vulnerability-scanner-sastdast)
  - [Log Monitor & SIEM](#2-log-monitor--siem-basics)
  - [Secret Manager](#3-secret-manager)
  - [Penetration Testing Toolkit](#4-penetration-testing-toolkit)
  - [Incident Response Automation](#5-incident-response-automation)
  - [Cryptography Utilities](#6-cryptography-utilities)
- [Integration with Cloud Services](#integration-with-cloud-services)
- [CI/CD Integration](#cicd-integration)
- [Extending the Toolkit](#extending-the-toolkit)
- [Security Considerations](#security-considerations)

## Overview

This toolkit provides security engineers with a unified set of tools to:

1. **Scan** codebases and containers for vulnerabilities (SAST/DAST)
2. **Monitor** logs and detect security threats (SIEM fundamentals)
3. **Manage** secrets securely (encryption, rotation, vault integration)
4. **Test** network and application security (penetration testing helpers)
5. **Respond** to incidents with automated playbooks
6. **Analyze** cryptographic implementations and attack vectors

All tools are designed to be cloud-agnostic with support for AWS, GCP, and on-premise environments.

## Features

- **SAST Scanner**: Static analysis for Python, JavaScript, and infrastructure code
- **Dependency Scanner**: Check for known CVEs in project dependencies
- **Log Monitor**: Real-time log parsing with threat detection rules (Sigma rules compatible)
- **Secret Scanner**: Detect hardcoded secrets in code and config files
- **Penetration Testing Helpers**: Port scanning, SSL/TLS analysis, brute-force protection testing
- **Incident Response**: Automated playbooks for common incident scenarios
- **Crypto Analysis**: Weak cipher detection, hash verification, certificate analysis
- **Cloud Security**: AWS IAM analyzer, GCP IAM recommender, security group auditor
- **Reporting**: Generate HTML/JSON reports with findings and remediation steps

## Project Structure

```
security-automation-toolkit/
├── scanners/
│   ├── __init__.py
│   ├── sast_scanner.py          # Static Application Security Testing
│   ├── dast_scanner.py          # Dynamic Application Security Testing
│   ├── dependency_scanner.py    # Dependency vulnerability scanning
│   ├── container_scanner.py     # Docker image vulnerability scanning
│   └── secret_scanner.py        # Hardcoded secret detection
├── monitors/
│   ├── __init__.py
│   ├── log_monitor.py           # Real-time log monitoring
│   ├── siem_engine.py           # Basic SIEM correlation engine
│   ├── threat_detector.py       # Threat detection with Sigma rules
│   └── cloudwatch_monitor.py    # AWS CloudWatch log integration
├── crypto/
│   ├── __init__.py
│   ├── cipher_analyzer.py       # Weak cipher detection
│   ├── hash_utils.py            # Hash verification and cracking
│   ├── certificate_analyzer.py  # SSL/TLS certificate analysis
│   └── key_manager.py           # Key generation and management
├── scripts/
│   ├── __init__.py
│   ├── port_scanner.py          # Network port scanner
│   ├── ssl_tester.py            # SSL/TLS configuration tester
│   ├── iam_auditor.py           # Cloud IAM policy auditor
│   ├── incident_response.py     # Incident response playbooks
│   ├── network_mapper.py        # Basic network mapping
│   └── compliance_checker.py    # SOC2 / ISO 27001 compliance checks
├── tests/
│   ├── __init__.py
│   ├── test_scanners.py
│   ├── test_monitors.py
│   └── test_crypto.py
├── rules/
│   └── sigma/                   # Sigma detection rules
│       ├── windows_events.yml
│       ├── cloud_iam_events.yml
│       └── network_attacks.yml
├── reports/                     # Generated reports directory
├── config.yaml                  # Toolkit configuration
├── requirements.txt
├── setup.py
├── Makefile
└── README.md
```

## Installation

```bash
# Clone the repository
git clone https://github.com/Krtucho/security-automation-toolkit.git
cd security-automation-toolkit

# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e .

# Copy and edit configuration
cp config.yaml.example config.yaml
```

### Dependencies

```txt
# requirements.txt
click>=8.1.0
requests>=2.31.0
cryptography>=41.0.0
pyyaml>=6.0
rich>=13.0.0  # Beautiful console output
python-dateutil>=2.8.0
boto3>=1.34.0  # AWS SDK
google-cloud-logging>=3.0.0
google-cloud-secret-manager>=2.0.0
sqlalchemy>=2.0.0
pydantic>=2.0.0
httpx>=0.25.0
paramiko>=3.4.0  # SSH
python-nmap>=0.7.0
dnspython>=2.6.0
```

## Usage

### 1. Vulnerability Scanner (SAST/DAST)

```bash
# SAST scan a Python project
python -m scanners.sast_scanner scan /path/to/project --format json --output report.json

# SAST scan with custom rules
python -m scanners.sast_scanner scan /path/to/project \
  --rules-dir custom-rules/ \
  --severity high,critical

# DAST scan a web application
python -m scanners.dast_scanner scan https://example.com \
  --endpoints /api,/login,/admin \
  --auth-token $TOKEN \
  --rate-limit 10

# Dependency scan
python -m scanners.dependency_scanner scan requirements.txt --output report.html

# Secret scan (pre-commit hook)
python -m scanners.secret_scanner scan . --exclude-dir .git,node_modules
```

**Example Output:**

```
┌──────────────────────────────────────────────────────────────────┐
│                    SAST Scan Results                              │
├──────────────────────────────────────────────────────────────────┤
│  High:      3  │  Medium:    7  │  Low:      12  │  Info:  5    │
├──────────────────────────────────────────────────────────────────┤
│  CWE-089: SQL Injection                      │ HIGH │ app/db.py │
│  CWE-079: XSS (Reflected)                   │ HIGH │ views.py  │
│  CWE-352: CSRF Token Missing                │ MED  │ forms.py  │
│  CWE-200: Information Exposure              │ MED  │ config.py │
└──────────────────────────────────────────────────────────────────┘
```

### 2. Log Monitor & SIEM Basics

```bash
# Monitor a log file in real-time
python -m monitors.log_monitor watch /var/log/nginx/access.log \
  --rules rules/sigma/ \
  --alert webhook https://hooks.slack.com/services/xxx

# Analyze logs with SIEM correlation engine
python -m monitors.siem_engine analyze \
  --log-file /var/log/auth.log \
  --timeframe 24h \
  --correlation-rules rules/sigma/network_attacks.yml

# Monitor AWS CloudWatch logs
python -m monitors.cloudwatch_monitor watch \
  --log-group /aws/eks/cluster/logs \
  --region us-east-1 \
  --filter-pattern "ERROR|CRITICAL|Unauthorized"

# Threat detection on live logs
python -m monitors.threat_detector run \
  --input /var/log/syslog \
  --output alerts.json \
  --severity high
```

**Example Threat Detection:**

```
──────────────────────────────────────────────────────────────────
🚨 ALERT: Brute Force Attack Detected
──────────────────────────────────────────────────────────────────
  Rule:     Multiple Failed SSH Logins
  Severity: HIGH
  Source:   192.168.1.100
  Target:   sshd (22)
  Events:   150 failed attempts in 5 minutes
  Time:     2024-03-15 14:23:45 UTC
──────────────────────────────────────────────────────────────────
  Action:   Block IP via AWS WAF / GCP Cloud Armor
──────────────────────────────────────────────────────────────────
```

### 3. Secret Manager

```bash
# Encrypt a sensitive value
python -m crypto.key_manager encrypt --value "my-secret-key" --key-id master-key
# Output: gAAAAAB...

# Decrypt
python -m crypto.key_manager decrypt --value "gAAAAAB..." --key-id master-key
# Output: my-secret-key

# Generate a new key pair (RSA)
python -m crypto.key_manager generate-keypair --output-dir ./keys --type rsa-2048

# Rotate secrets
python -m crypto.key_manager rotate --vault aws --secret-name db-password

# Audit secret access
python -m crypto.key_manager audit --vault gcp --secret-name api-keys
```

### 4. Penetration Testing Toolkit

```bash
# Port scan a target
python -m scripts.port_scanner scan example.com \
  --ports 1-10000 \
  --timeout 2 \
  --output scan_results.json

# SSL/TLS security test
python -m scripts.ssl_tester test https://example.com \
  --check-certificate \
  --check-ciphers \
  --check-protocols \
  --output report.html

# Network mapping
python -m scripts.network_mapper map 10.0.0.0/24 \
  --discover-hosts \
  --identify-ports \
  --detect-os

# Cloud IAM auditor
python -m scripts.iam_auditor analyze \
  --provider aws \
  --profile production \
  --check-unused-permissions \
  --check-overprivileged
```

### 5. Incident Response Automation

```bash
# List available playbooks
python -m scripts.incident_response list-playbooks

# Run an incident response playbook
python -m scripts.incident_response run \
  --playbook compromised-instance \
  --resource-id i-1234567890abcdef0 \
  --auto-remediate

# Available playbooks:
#   - compromised-instance: Isolate, snapshot, investigate
#   - data-breach:          Contain, notify, forensics
#   - dos-attack:           Rate limit, scale, block
#   - malicious-user:       Disable, audit, report

# Compliance checking
python -m scripts.compliance_checker check \
  --standard soc2 \
  --target /path/to/infrastructure \
  --report compliance_report.html
```

### 6. Cryptography Utilities

```python
from crypto.cipher_analyzer import CipherAnalyzer
from crypto.hash_utils import HashUtils
from crypto.certificate_analyzer import CertificateAnalyzer

# Analyze cipher strength
analyzer = CipherAnalyzer()
result = analyzer.analyze_cipher("AES-256-GCM")
print(result.security_level)  # "strong"
print(result.recommendations)  # []

# Check TLS configuration
cert_analyzer = CertificateAnalyzer()
result = cert_analyzer.analyze_certificate("example.com", port=443)
print(result.valid)  # True/False
print(result.weak_ciphers)  # ["TLS_RSA_WITH_AES_128_CBC_SHA", ...]
print(result.expiration_days)  # 180

# Hash verification
hash_utils = HashUtils()
is_valid = hash_utils.verify_file_hash("downloads/app.bin", "abc123...", "sha256")
print(is_valid)  # True/False

# Weak password hash detection
weak = hash_utils.detect_weak_hashes("/etc/shadow")
print(weak)  # ["user: md5 hash detected", ...]
```

## Integration with Cloud Services

### AWS Integration

```python
# monitors/cloudwatch_monitor.py
import boto3

class CloudWatchMonitor:
    def __init__(self, region="us-east-1"):
        self.logs_client = boto3.client("logs", region_name=region)
        self.guardduty = boto3.client("guardduty", region_name=region)
        self.waf = boto3.client("wafv2", region_name=region)

    def get_guardduty_findings(self, severity_threshold="HIGH"):
        response = self.guardduty.list_findings(
            DetectorId=self.detector_id,
            FindingCriteria={
                "Criterion": {
                    "severity": {"Gte": 7}
                }
            }
        )
        return response["FindingIds"]

    def block_ip_via_waf(self, ip_address: str):
        self.waf.update_ip_set(
            Name="blocked-ips",
            Scope="REGIONAL",
            Id=self.waf_ip_set_id,
            LockToken=self.get_lock_token(),
            Addresses=[f"{ip_address}/32"]
        )
```

### GCP Integration

```python
# monitors/gcp_monitor.py
from google.cloud import logging as gcp_logging
from google.cloud import secretmanager

class GCPMonitor:
    def __init__(self, project_id):
        self.logging_client = gcp_logging.Client(project=project_id)
        self.secret_client = secretmanager.SecretManagerServiceClient()

    def query_logs(self, filter_str: str, timeframe_hours: int = 24):
        logger = self.logging_client.logger("cloudaudit.googleapis.com")
        entries = logger.list_entries(
            filter_=filter_str,
            order_by="timestamp desc"
        )
        return list(entries)

    def rotate_secret(self, secret_name: str):
        parent = f"projects/{self.project_id}/secrets/{secret_name}"
        self.secret_client.add_secret_version(
            parent=parent,
            payload={"data": secrets.token_hex(32).encode()}
        )
```

## CI/CD Integration

### GitHub Actions

```yaml
# .github/workflows/security-scan.yml
name: Security Scan

on: [push, pull_request]

jobs:
  security-audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install toolkit
        run: pip install git+https://github.com/Krtucho/security-automation-toolkit.git

      - name: SAST Scan
        run: |
          python -m scanners.sast_scanner scan . \
            --severity high,critical \
            --format json \
            --output sast-report.json

      - name: Secret Scan
        run: |
          python -m scanners.secret_scanner scan . \
            --exclude-dir .git,node_modules,venv

      - name: Dependency Scan
        run: |
          python -m scanners.dependency_scanner scan requirements.txt

      - name: Upload Report
        uses: actions/upload-artifact@v4
        with:
          name: security-reports
          path: |
            sast-report.json
            secret-scan-report.json
```

### Pre-commit Hook

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/Krtucho/security-automation-toolkit
    rev: v1.0.0
    hooks:
      - id: secret-scan
        name: Scan for secrets
        entry: python -m scanners.secret_scanner scan
        language: system
        types: [text]
      - id: sast-scan
        name: SAST scan
        entry: python -m scanners.sast_scanner scan
        language: system
        types: [python]
```

## Extending the Toolkit

### Adding a New Scanner

```python
# scanners/custom_scanner.py
from scanners.base import BaseScanner
from rich.console import Console

class CustomScanner(BaseScanner):
    name = "custom"
    description = "Custom security scanner"

    def scan(self, target: str, **kwargs) -> dict:
        findings = []
        # Implement your scanning logic here
        for issue in self._find_issues(target):
            findings.append({
                "type": issue.type,
                "severity": issue.severity,
                "file": issue.file,
                "line": issue.line,
                "description": issue.description,
                "remediation": issue.remediation,
            })
        return {"findings": findings, "summary": self._summarize(findings)}

    def _find_issues(self, target):
        # Custom scanning implementation
        pass
```

### Adding Sigma Rules

```yaml
# rules/sigma/cloud_iam_events.yml
title: Suspicious IAM Policy Change
id: 8c9f5d6e-7a1b-4c3d-8e9f-0a1b2c3d4e5f
status: experimental
description: Detects modification of IAM policies that could indicate privilege escalation
logsource:
  service: cloudtrail
  product: aws
detection:
  selection:
    eventSource: iam.amazonaws.com
    eventName:
      - PutRolePolicy
      - PutUserPolicy
      - AttachRolePolicy
      - AttachUserPolicy
      - CreatePolicy
      - DeletePolicy
  condition: selection
falsepositives:
  - Legitimate administrative actions
  - Automated deployment scripts
level: high
```

## Security Considerations

1. **API Keys & Tokens**: Never hardcode credentials. Use environment variables or the built-in secret manager.
2. **Logging**: Enable audit logging for all security operations. Logs contain sensitive information — encrypt them.
3. **Network Scanning**: Always get proper authorization before scanning networks or systems.
4. **Compliance**: Ensure your security testing complies with relevant regulations (GDPR, SOC2, PCI-DSS).
5. **Rate Limiting**: Respect rate limits when scanning external services to avoid DoS.

## Example: End-to-End Security Audit

```bash
# 1. Scan code for vulnerabilities
python -m scanners.sast_scanner scan ./my-app --severity high,critical

# 2. Check for hardcoded secrets
python -m scanners.secret_scanner scan ./my-app

# 3. Analyze dependencies
python -m scanners.dependency_scanner scan ./my-app/requirements.txt

# 4. Test SSL/TLS configuration
python -m scripts.ssl_tester test https://my-app.com

# 5. Audit cloud IAM policies
python -m scripts.iam_auditor analyze --provider aws --profile prod

# 6. Check compliance
python -m scripts.compliance_checker check --standard soc2 --target ./infra

# 7. Generate comprehensive report
python -m scripts.report_generator generate \
  --reports sast.json,secrets.json,deps.json,ssl.json,iam.json,compliance.json \
  --output security-audit-report.html
```

## License

MIT
