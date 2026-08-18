# Secure FastAPI Microservice with DevSecOps Pipeline

A production-ready microservice built with **FastAPI** featuring a complete **DevSecOps** pipeline — from automated CI/CD with security scanning to cloud infrastructure provisioning and observability.

## 📋 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Quick Start](#quick-start)
- [API Endpoints](#api-endpoints)
- [DevSecOps Pipeline](#devsecops-pipeline)
- [Infrastructure](#infrastructure)
- [Security](#security)
- [Observability](#observability)
- [Contributing](#contributing)

## Overview

This project demonstrates a **full DevSecOps workflow**:

- **FastAPI** microservice with JWT-based authentication, role-based access control (RBAC), rate limiting, and input validation
- **GitHub Actions** CI/CD pipeline with SAST (Bandit, Semgrep), DAST (OWASP ZAP), dependency scanning (Snyk/Dependabot), and container scanning (Trivy)
- **Docker & Kubernetes** deployment with security-hardened containers (distroless images, non-root users, read-only filesystems)
- **Terraform** provisioning on AWS (VPC, EKS, RDS, ElastiCache, WAF, KMS)
- **Sentry** integration for real-time error tracking and performance monitoring
- **Secret management** with HashiCorp Vault (or AWS Secrets Manager)
- **Helm charts** for Kubernetes deployment with security contexts and network policies

## Architecture

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   Client    │────▶│  CloudFront  │────▶│    WAF      │
└─────────────┘     │    / ALB     │     │ (Rate Limit)│
                    └──────────────┘     └──────┬──────┘
                                               │
                                        ┌──────▼──────┐
                                        │  FastAPI     │
                                        │  (EKS Pods)  │
                                        └──┬───────┬──┘
                                           │       │
                                   ┌───────▼┐ ┌────▼────────┐
                                   │  RDS   │ │ ElastiCache  │
                                   │(Postgres)│ │   (Redis)    │
                                   └────────┘ └─────────────┘
```

## Features

### API Security
- **JWT-based authentication** with access & refresh tokens
- **Role-based access control** (admin, user, read-only)
- **Rate limiting** per endpoint and per user (Redis-backed)
- **Input validation** with Pydantic (strict type checking)
- **SQL injection prevention** via parameterized queries (SQLAlchemy)
- **CORS** configuration with strict origin whitelist
- **Helmet-style** security headers
- **Request logging** with sensitive data masking

### CI/CD Pipeline
- **Lint & Type Check**: ruff, mypy
- **SAST**: Bandit + Semgrep for Python security analysis
- **Dependency Scan**: pip-audit + Snyk
- **Tests**: pytest with coverage (≥90%)
- **Container Scan**: Trivy on Docker images
- **DAST**: OWASP ZAP in staging environment
- **Infrastructure Scan**: Checkov/Terraform validate
- **Deploy**: Automatic deployment to EKS staging, manual approval for production

### Infrastructure
- **Terraform modules** for VPC, EKS, RDS, ElastiCache, WAF, KMS
- **Security groups** with least-privilege rules
- **Encryption at rest** (RDS, EBS, S3) with KMS
- **Encryption in transit** (TLS 1.3)
- **VPC flow logs** for network monitoring
- **Private subnets** for databases and application tier
- **Auto-scaling** based on CPU/memory metrics

## Tech Stack

| Component | Technology |
|-----------|------------|
| API Framework | FastAPI (Python 3.12) |
| Database | PostgreSQL 16 (via SQLAlchemy + Alembic) |
| Cache | Redis 7 (via redis-py) |
| Auth | PyJWT + python-jose |
| Container | Docker (distroless images) |
| Orchestration | Kubernetes (EKS) |
| IaC | Terraform + Terragrunt |
| CI/CD | GitHub Actions |
| SAST | Bandit, Semgrep |
| DAST | OWASP ZAP |
| Container Security | Trivy |
| Dependency Scanning | Snyk, pip-audit, Dependabot |
| IaC Scanning | Checkov, tfsec |
| Secrets | HashiCorp Vault / AWS Secrets Manager |
| Monitoring | Sentry, CloudWatch |
| Logging | structlog + CloudWatch Logs |

## Project Structure

```
secure-fastapi-devsecops/
├── .github/
│   └── workflows/
│       ├── ci.yml                 # CI: lint, test, security scan
│       ├── cd-staging.yml         # CD: deploy to staging
│       └── cd-production.yml      # CD: deploy to production (manual approval)
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI application entry point
│   ├── api/
│   │   ├── __init__.py
│   │   ├── dependencies.py        # Dependency injection (auth, rate-limit)
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── auth.py            # Login, register, refresh
│   │       ├── users.py           # User CRUD (admin)
│   │       ├── items.py           # Resource endpoints
│   │       └── health.py          # Health check endpoint
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py              # Pydantic Settings (env-based config)
│   │   ├── security.py            # JWT, hashing, encryption
│   │   └── rate_limit.py          # Redis-backed rate limiter
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py                # SQLAlchemy User model
│   │   └── item.py                # SQLAlchemy Item model
│   └── services/
│       ├── __init__.py
│       ├── auth_service.py        # Business logic for auth
│       └── item_service.py        # Business logic for items
├── infra/
│   ├── terraform/
│   │   ├── main.tf                # Root Terraform configuration
│   │   ├── variables.tf
│   │   ├── outputs.tf
│   │   ├── modules/
│   │   │   ├── vpc/               # VPC with public/private subnets
│   │   │   ├── eks/               # EKS cluster with managed node groups
│   │   │   ├── rds/               # PostgreSQL RDS instance
│   │   │   ├── redis/             # ElastiCache Redis cluster
│   │   │   ├── waf/               # WAF with rate limiting rules
│   │   │   └── kms/               # KMS keys for encryption
│   │   └── environments/
│   │       ├── dev/
│   │       ├── staging/
│   │       └── prod/
│   └── k8s/
│       ├── namespace.yaml
│       ├── deployment.yaml        # Kubernetes Deployment
│       ├── service.yaml           # Kubernetes Service
│       ├── ingress.yaml           # Ingress with TLS
│       ├── configmap.yaml         # App configuration
│       ├── network-policy.yaml    # Network policies
│       ├── hpa.yaml               # Horizontal Pod Autoscaler
│       └── pdb.yaml               # Pod Disruption Budget
├── tests/
│   ├── __init__.py
│   ├── conftest.py                # Pytest fixtures with test containers
│   ├── test_auth.py
│   ├── test_users.py
│   └── test_items.py
├── Dockerfile                     # Multi-stage build (distroless)
├── docker-compose.yml             # Local development environment
├── .env.example
├── requirements.txt
├── requirements-dev.txt
├── pyproject.toml
└── Makefile
```

## Quick Start

### Prerequisites

- Python 3.12+
- Docker & Docker Compose
- Terraform 1.7+
- kubectl
- AWS CLI configured

### Local Development

```bash
# Clone the repository
git clone https://github.com/Krtucho/secure-fastapi-devsecops.git
cd secure-fastapi-devsecops

# Set up environment
cp .env.example .env
python -m venv .venv && source .venv/bin/activate

# Install dependencies
pip install -r requirements-dev.txt

# Run with Docker Compose (PostgreSQL, Redis, app)
docker compose up -d

# Run database migrations
alembic upgrade head

# Run tests
pytest --cov=app --cov-report=term-missing

# Start the development server
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`. Interactive docs at `http://localhost:8000/docs`.

### Docker Build

```bash
# Build security-hardened image
docker build -t secure-fastapi:latest .

# Scan image for vulnerabilities
trivy image secure-fastapi:latest

# Run container
docker run -p 8000:8000 secure-fastapi:latest
```

### Kubernetes Deployment

```bash
# Deploy with kubectl
kubectl apply -f infra/k8s/namespace.yaml
kubectl apply -f infra/k8s/

# Or deploy with Helm
helm upgrade --install secure-fastapi ./charts/fastapi-service
```

## API Endpoints

### Authentication

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/api/v1/auth/register` | Register new user | None |
| POST | `/api/v1/auth/login` | Login, returns JWT | None |
| POST | `/api/v1/auth/refresh` | Refresh access token | Bearer |
| POST | `/api/v1/auth/logout` | Invalidate token | Bearer |

### Users (Admin only)

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/api/v1/users/` | List all users | Admin |
| GET | `/api/v1/users/{id}` | Get user by ID | Admin |
| PUT | `/api/v1/users/{id}` | Update user | Admin |
| DELETE | `/api/v1/users/{id}` | Delete user | Admin |

### Items

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/api/v1/items/` | List items (paginated) | Bearer |
| GET | `/api/v1/items/{id}` | Get item by ID | Bearer |
| POST | `/api/v1/items/` | Create item | Bearer |
| PUT | `/api/v1/items/{id}` | Update item | Bearer |
| DELETE | `/api/v1/items/{id}` | Delete item | Bearer |

### Health

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/health/` | Health check (includes DB, Redis status) |
| GET | `/api/v1/health/ready` | Readiness probe |
| GET | `/api/v1/health/live` | Liveness probe |

## DevSecOps Pipeline

### CI Pipeline (`.github/workflows/ci.yml`)

The CI pipeline runs on every push and pull request:

```yaml
name: CI Pipeline

on: [push, pull_request]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pip install ruff mypy
      - run: ruff check app/
      - run: mypy app/

  sast:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pip install bandit semgrep
      - run: bandit -r app/ -f json
      - run: semgrep --config=auto app/

  dependency-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pip install pip-audit
      - run: pip-audit
      - uses: snyk/actions/python@master
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
        with:
          args: --severity-threshold=high

  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_DB: test
          POSTGRES_USER: test
          POSTGRES_PASSWORD: test
        ports:
          - 5432:5432
      redis:
        image: redis:7
        ports:
          - 6379:6379
    steps:
      - uses: actions/checkout@v4
      - run: pip install -r requirements-dev.txt
      - run: pytest --cov=app --cov-report=xml --cov-fail-under=90
      - uses: codecov/codecov-action@v3

  container-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: docker build -t app:latest .
      - run: |
          docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
          aquasec/trivy image app:latest \
          --severity HIGH,CRITICAL --exit-code 1
```

### CD Pipeline (`.github/workflows/cd-staging.yml`)

- Triggers on merge to `main`
- Builds and pushes Docker image to ECR
- Scans infrastructure with Checkov
- Deploys to staging EKS cluster
- Runs OWASP ZAP DAST scan against staging
- Sends notification to Slack/Teams

### Production Deployment

- Requires manual approval via GitHub Environments
- Blue/Green deployment on EKS
- Automatically rolls back on health check failure
- Post-deployment smoke tests

## Infrastructure

### Terraform Modules

```hcl
# VPC Module
module "vpc" {
  source = "./modules/vpc"
  environment = var.environment
  cidr_block  = "10.0.0.0/16"
  availability_zones = ["us-east-1a", "us-east-1b", "us-east-1c"]
  private_subnets  = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  public_subnets   = ["10.0.101.0/24", "10.0.102.0/24", "10.0.103.0/24"]
  enable_flow_logs = true
}

# EKS Module
module "eks" {
  source = "./modules/eks"
  environment      = var.environment
  vpc_id          = module.vpc.vpc_id
  private_subnets = module.vpc.private_subnet_ids
  node_group_config = {
    min_size     = 2
    max_size     = 10
    instance_types = ["t3.medium"]
  }
  cluster_version = "1.29"
  enable_kms_encryption = true
}
```

### Security Groups

The infrastructure enforces least-privilege networking:

| Component | Ingress Rules | Egress Rules |
|-----------|--------------|--------------|
| ALB | 443 from 0.0.0.0/0 | To EKS nodes (80) |
| EKS Nodes | 443 from ALB SG | To RDS (5432), Redis (6379) |
| RDS | 5432 from EKS SG | None (deny all) |
| Redis | 6379 from EKS SG | None (deny all) |

## Security

### Implemented Security Controls

1. **Authentication & Authorization**
   - JWT with RS256 signing
   - Short-lived access tokens (15 min)
   - Refresh token rotation
   - RBAC with least-privilege principle

2. **API Security**
   - Rate limiting (100 req/min per user, 1000 req/min per IP)
   - Request size limits (1 MB)
   - Input validation with Pydantic
   - SQLAlchemy parameterized queries
   - CORS with strict origin validation

3. **Container Security**
   - Distroless base images (Google's distroless)
   - Non-root user execution
   - Read-only root filesystem
   - No shell or package manager in production image
   - Regular vulnerability scanning

4. **Infrastructure Security**
   - Encryption at rest (KMS)
   - Encryption in transit (TLS 1.3)
   - VPC with private subnets
   - VPC flow logs enabled
   - Security groups with minimal rules
   - WAF with rate limiting and OWASP rules

5. **Secret Management**
   - No secrets in code or config files
   - All secrets via Vault or AWS Secrets Manager
   - Automatic secret rotation
   - Audit logging for secret access

6. **Monitoring & Incident Response**
   - Sentry for error tracking
   - CloudWatch for metrics and logs
   - VPC flow logs for network monitoring
   - GuardDuty for threat detection
   - Automated incident response playbooks

## Observability

### Sentry Integration

```python
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration

sentry_sdk.init(
    dsn=settings.SENTRY_DSN,
    environment=settings.ENVIRONMENT,
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
    integrations=[
        FastApiIntegration(),
        SqlalchemyIntegration(),
    ],
)
```

### Structured Logging

```python
import structlog

logger = structlog.get_logger()

# Automatically includes correlation IDs, request IDs
logger.info("user.login", user_id=user.id, ip_address="*** masked ***")
```

### Health Checks

- `/health/ready`: Returns 200 when DB and Redis are reachable
- `/health/live`: Returns 200 always (simple process check)
- All health checks exclude sensitive data from responses

## Makefile

```makefile
.PHONY: install lint test security docker-up docker-down deploy

install:
	pip install -r requirements-dev.txt

lint:
	ruff check app/ tests/
	mypy app/

test:
	pytest --cov=app --cov-report=term-missing

security:
	bandit -r app/
	pip-audit

docker-up:
	docker compose up -d

docker-down:
	docker compose down

deploy-staging:
	@echo "Deploying to staging..."
	kubectl apply -f infra/k8s/

deploy-prod:
	@echo "Deploying to production..."
	kubectl apply -f infra/k8s/ --namespace=production
```

## License

MIT
