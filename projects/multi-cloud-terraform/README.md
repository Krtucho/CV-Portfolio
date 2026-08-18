# Multi-Cloud Infrastructure with Terraform

Infrastructure as Code (IaC) for provisioning a **secure, production-grade multi-cloud environment** across **AWS** and **Google Cloud Platform (GCP)** using Terraform. This project demonstrates advanced Terraform patterns, cloud security best practices, and cost optimization strategies.

## 📋 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [AWS Infrastructure](#aws-infrastructure)
- [GCP Infrastructure](#gcp-infrastructure)
- [Security](#security)
- [Cost Optimization](#cost-optimization)
- [CI/CD for Terraform](#cicd-for-terraform)
- [Modules](#modules)
- [Contributing](#contributing)

## Overview

This repository contains Terraform configurations to deploy a **multi-cloud infrastructure** suitable for running containerized microservices. The infrastructure is designed with security-first principles, following the AWS Well-Architected Framework and GCP best practices.

### Key Capabilities

- **AWS**: VPC, EKS (Kubernetes), RDS (PostgreSQL), ElastiCache (Redis), WAF, KMS, IAM roles/policies, S3 with encryption
- **GCP**: GKE (Kubernetes), Cloud Storage, Cloud SQL, IAM, VPC-native clusters
- **Cross-cloud**: Shared VPC connectivity, unified monitoring, consistent IAM policies
- **Security**: Encryption everywhere, least-privilege IAM, network segmentation, WAF, security scanning

## Architecture

```
                    ┌──────────────────────────────────────────────────┐
                    │                 Multi-Cloud Mesh                  │
                    │  ┌──────────────┐        ┌──────────────┐        │
                    │  │     AWS       │        │     GCP       │        │
                    │  │   (us-east-1) │        │  (us-central1)│        │
                    │  └──────┬───────┘        └──────┬────────┘        │
                    │         │                       │                  │
                    │  ┌──────▼───────┐        ┌──────▼────────┐        │
                    │  │    VPC        │        │    VPC         │        │
                    │  │  ┌─────────┐  │        │  ┌──────────┐  │        │
                    │  │  │ Public  │  │        │  │ Public   │  │        │
                    │  │  │ Subnets │  │        │  │ Subnets  │  │        │
                    │  │  └────┬────┘  │        │  └────┬─────┘  │        │
                    │  │  ┌────▼────┐  │        │  ┌────▼─────┐  │        │
                    │  │  │Private  │  │        │  │ Private  │  │        │
                    │  │  │Subnets  │  │        │  │ Subnets  │  │        │
                    │  │  └──┬──┬──┘  │        │  └──┬──┬────┘  │        │
                    │  │     │  │     │        │     │  │       │        │
                    │  │  ┌──▼──▼──┐  │        │  ┌──▼──▼────┐  │        │
                    │  │  │EKS RDS │  │        │  │GKE Cloud │  │        │
                    │  │  │    Redis│  │        │  │SQL  Redis│  │        │
                    │  │  └────────┘  │        │  └──────────┘  │        │
                    │  └──────────────┘        └──────────────┘  │        │
                    └──────────────────────────────────────────────────┘
```

## Features

### AWS Infrastructure
- **VPC** with public/private subnets across 3 AZs, NAT Gateways, VPC Flow Logs
- **EKS** cluster with managed node groups, IRSA (IAM Roles for Service Accounts), Cluster Autoscaler
- **RDS PostgreSQL** with Multi-AZ, automated backups, encryption at rest, Performance Insights
- **ElastiCache Redis** with cluster mode, encryption in transit, auto-failover
- **WAF** with rate limiting, OWASP top-10 rules, IP reputation lists
- **KMS** for encryption key management with automatic rotation
- **S3** buckets with block public access, encryption, lifecycle policies
- **IAM** with least-privilege policies, role-based access, password policies

### GCP Infrastructure
- **GKE** cluster with VPC-native, private nodes, Workload Identity, shielded nodes
- **Cloud SQL PostgreSQL** with high availability, automated backups, CMEK encryption
- **Cloud Storage** buckets with uniform bucket-level access, object versioning
- **IAM** with custom roles, service accounts, policy bindings

### Cross-Cloud Features
- Consistent tagging and naming conventions
- Unified logging and monitoring setup
- Standardized security group/firewall rules
- Cost tracking with budgets and alerts
- Disaster recovery planning

## Tech Stack

| Component | Technology |
|-----------|------------|
| IaC | Terraform 1.7+, Terragrunt |
| AWS | VPC, EKS, RDS, ElastiCache, WAF, KMS, IAM, S3 |
| GCP | GKE, Cloud SQL, Cloud Storage, IAM, VPC |
| State Management | Terraform Cloud / S3 + DynamoDB / GCS |
| CI/CD | GitHub Actions with Terraform plan/apply |
| Scanning | Checkov, tfsec, Terratest |
| Secrets | AWS Secrets Manager / GCP Secret Manager |

## Project Structure

```
multi-cloud-terraform/
├── environments/
│   ├── dev/
│   │   ├── aws/
│   │   │   ├── main.tf
│   │   │   ├── variables.tf
│   │   │   └── terraform.tfvars
│   │   └── gcp/
│   │       ├── main.tf
│   │       ├── variables.tf
│   │       └── terraform.tfvars
│   ├── staging/
│   │   ├── aws/
│   │   └── gcp/
│   └── prod/
│       ├── aws/
│       └── gcp/
├── modules/
│   ├── aws-vpc/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   ├── aws-eks/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   ├── aws-iam/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   ├── gcp-gke/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   └── gcp-storage/
│       ├── main.tf
│       ├── variables.tf
│       └── outputs.tf
├── .github/workflows/
│   └── terraform-ci.yml
├── terragrunt.hcl
├── Makefile
└── README.md
```

## Prerequisites

- Terraform 1.7+
- AWS CLI configured
- GCP SDK configured
- `gcloud auth application-default login` for GCP
- S3 bucket and DynamoDB table for Terraform state (AWS)
- GCS bucket for Terraform state (GCP)

## Quick Start

### 1. Clone and configure

```bash
git clone https://github.com/Krtucho/multi-cloud-terraform.git
cd multi-cloud-terraform

# Copy environment template
cp environments/dev/aws/terraform.tfvars.example environments/dev/aws/terraform.tfvars
```

### 2. Deploy AWS Infrastructure (Dev)

```bash
# Initialize Terraform
cd environments/dev/aws
terraform init

# Review the plan
terraform plan

# Apply infrastructure
terraform apply -auto-approve
```

### 3. Deploy GCP Infrastructure (Dev)

```bash
cd environments/dev/gcp
terraform init
terraform plan
terraform apply -auto-approve
```

### 4. Deploy with Terragrunt (all environments)

```bash
# Install Terragrunt
brew install terragrunt  # macOS

# Deploy all infrastructure
cd environments/dev
terragrunt run-all plan
terragrunt run-all apply
```

## AWS Infrastructure

### VPC Module

```hcl
module "vpc" {
  source = "../../modules/aws-vpc"

  environment       = "dev"
  cidr_block        = "10.0.0.0/16"
  availability_zones = ["us-east-1a", "us-east-1b", "us-east-1c"]

  # Subnet configuration
  public_subnet_cidrs  = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  private_subnet_cidrs = ["10.0.10.0/24", "10.0.20.0/24", "10.0.30.0/24"]

  # Security features
  enable_flow_logs           = true
  flow_logs_retention_days   = 90
  enable_nat_gateway         = true
  single_nat_gateway         = false  # One per AZ for production
  enable_vpn_gateway         = false

  tags = {
    Environment = "dev"
    ManagedBy   = "Terraform"
    CostCenter  = "engineering"
  }
}
```

### EKS Module

```hcl
module "eks" {
  source = "../../modules/aws-eks"

  environment    = "dev"
  cluster_name   = "dev-cluster"
  cluster_version = "1.29"
  vpc_id         = module.vpc.vpc_id
  subnet_ids     = module.vpc.private_subnet_ids

  # Node group configuration
  node_groups = {
    main = {
      desired_size    = 2
      min_size       = 1
      max_size       = 5
      instance_types = ["t3.medium", "t3.large"]

      # Security configuration
      use_spot_instances       = false
      enable_kms_encryption    = true
      enable_irsa              = true
      enable_cluster_logging   = true
    }
  }

  # Security features
  endpoint_private_access       = true
  endpoint_public_access        = false
  public_access_cidrs          = []
  kubernetes_network_config = {
    service_ipv4_cidr = "172.20.0.0/16"
  }
}
```

### Security Groups - Least Privilege

The security groups are configured with least-privilege access:

```
┌─────────────┐     ┌──────────────────┐     ┌──────────────────┐
│  Internet    │────▶│  ALB Security    │────▶│  EKS Node SG     │
│              │     │  Group           │     │                  │
│              │     │  In: 443 (HTTPS) │     │  In: 443 (ALB)   │
│              │     │  Out: 80 (to EKS)│     │  Out: To RDS/Redis│
└─────────────┘     └──────────────────┘     └────────┬─────────┘
                                                       │
                                               ┌───────▼──────────┐
                                               │  RDS SG           │
                                               │  In: 5432 (EKS)   │
                                               │  Out: DENY ALL    │
                                               └──────────────────┘
```

## GCP Infrastructure

### GKE Module

```hcl
module "gke" {
  source = "../../modules/gcp-gke"

  project_id      = "my-gcp-project"
  environment     = "dev"
  cluster_name    = "dev-cluster"
  region          = "us-central1"
  zones           = ["us-central1-a", "us-central1-b", "us-central1-c"]

  # Node pool configuration
  node_pools = {
    default = {
      machine_type      = "e2-standard-4"
      min_node_count   = 1
      max_node_count   = 5
      disk_size_gb     = 100
      disk_type        = "pd-ssd"
      spot             = false  # Use preemptible for cost savings
    }
  }

  # Security features
  private_cluster              = true
  enable_private_nodes        = true
  enable_private_endpoint     = true
  master_ipv4_cidr_block      = "172.16.0.0/28"
  enable_shielded_nodes       = true
  enable_workload_identity    = true
  enable_intranode_visibility = true
  enable_cost_allocation      = true
}
```

## Security

### IAM Policies

The IAM module implements least-privilege access:

```hcl
# AWS IAM role for EKS service account
resource "aws_iam_role" "app_role" {
  name = "app-${var.environment}"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Federated = module.eks.oidc_provider_arn
        }
        Action = "sts:AssumeRoleWithWebIdentity"
        Condition = {
          StringEquals = {
            "${module.eks.oidc_provider}:sub" : "system:serviceaccount:production:app-sa"
          }
        }
      }
    ]
  })
}

# Minimal permissions for the application
resource "aws_iam_policy" "app_policy" {
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:PutObject",
        ]
        Resource = "${module.storage.data_bucket_arn}/*"
      },
      {
        Effect = "Allow"
        Action = [
          "kms:Decrypt",
          "kms:GenerateDataKey",
        ]
        Resource = module.kms.key_arn
      }
    ]
  })
}
```

### Encryption

| Resource | Encryption Type | Key Management |
|----------|----------------|----------------|
| EBS Volumes | AES-256 | AWS KMS (auto-rotate) |
| RDS | AES-256 | AWS KMS (auto-rotate) |
| S3 | SSE-S3 / SSE-KMS | AWS KMS |
| Cloud SQL | CMEK | GCP Cloud KMS |
| GKE Secrets | envelope encryption | GCP Cloud KMS |
| etcd in EKS/Kubernetes | AES-256 | AWS KMS |

### Network Security

- **VPC Flow Logs** enabled in all environments
- **Security Groups** with explicit allow rules only
- **Network Policies** in Kubernetes for pod-level segmentation
- **Private subnets** for all workloads
- **NAT Gateways** for outbound traffic (no public IPs)
- **WAF** with OWASP Top 10 and rate limiting rules

### Compliance Controls

| Control | Implementation |
|---------|---------------|
| SOC 2 | Encryption at rest & transit, access logging, change management |
| ISO 27001 | IAM policies, security groups, network segmentation, audit logging |
| GDPR | Data classification tags, encryption, access controls |
| CIS Benchmarks | Hardened AMIs, Kubernetes CIS benchmark, restricted pod security |

## Cost Optimization

### AWS Cost Optimization Strategies

#### 1. Compute Optimization

```hcl
# Use Spot Instances for non-critical workloads
node_groups = {
  spot-workers = {
    instance_types  = ["t3.medium", "t3.large", "m5.large"]
    use_spot       = true
    spot_allocation_strategy = "capacity-optimized"
  }
}
```

#### 2. Storage Optimization

- S3 lifecycle policies to transition to Infrequent Access after 30 days
- EBS gp3 volumes (better price/performance than gp2)
- RDS storage auto-scaling
- Delete unused EBS snapshots automatically

#### 3. Network Optimization

- Use VPC endpoints (Gateway + Interface) to reduce NAT Gateway costs
- Enable S3 Transfer Acceleration for large transfers
- Use CloudFront for content delivery (reduces origin load)

#### 4. Monitoring & Budgets

```hcl
# Budget alert
resource "aws_budgets_budget" "monthly" {
  name         = "monthly-budget-${var.environment}"
  budget_type  = "COST"
  limit_amount = var.monthly_budget_limit
  time_unit    = "MONTHLY"

  notification {
    comparison_operator = "GREATER_THAN"
    threshold          = 80
    threshold_type     = "PERCENTAGE"
    notification_type  = "ACTUAL"
    subscriber_email_addresses = ["team@company.com"]
  }
}
```

### GCP Cost Optimization

- Use committed use discounts (1 or 3 year commitments)
- Preemptible VMs for batch workloads
- Cloud Storage lifecycle policies (Nearline → Coldline → Archive)
- VPC-native clusters (reduces load balancer costs)

## CI/CD for Terraform

The GitHub Actions workflow (`terraform-ci.yml`) validates all infrastructure changes:

```yaml
name: Terraform CI

on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: hashicorp/setup-terraform@v3
        with:
          terraform_version: 1.7.0

      - name: Terraform fmt
        run: terraform fmt -check -recursive

      - name: Terraform init
        run: terraform init

      - name: Terraform validate
        run: terraform validate

  security-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run Checkov scan
        uses: bridgecrewio/checkov-action@master
        with:
          directory: ./
          framework: terraform
          soft_fail: false

      - name: Run tfsec scan
        uses: aquasecurity/tfsec-action@master
        with:
          working_directory: ./

  plan:
    if: github.event_name == 'pull_request'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: hashicorp/setup-terraform@v3

      - name: Terraform plan (AWS Dev)
        run: |
          cd environments/dev/aws
          terraform init
          terraform plan -out=tfplan
          terraform show -no-color tfplan > plan.txt

      - uses: actions/github-script@v7
        with:
          script: |
            const fs = require('fs');
            const plan = fs.readFileSync('environments/dev/aws/plan.txt', 'utf8');
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: `## Terraform Plan (AWS Dev)\n\`\`\`\n${plan}\n\`\`\``
            });
```

## Modules

### AWS VPC Module (`modules/aws-vpc/`)

```
Inputs:
  - cidr_block, environment, availability_zones
  - public_subnet_cidrs, private_subnet_cidrs
  - enable_flow_logs, enable_nat_gateway

Outputs:
  - vpc_id, public_subnet_ids, private_subnet_ids
  - nat_gateway_ips, flow_log_group
```

### AWS EKS Module (`modules/aws-eks/`)

```
Inputs:
  - cluster_name, cluster_version, vpc_id, subnet_ids
  - node_groups (map with instance_types, sizes, spot config)
  - enable_kms_encryption, enable_irsa

Outputs:
  - cluster_endpoint, cluster_ca_certificate
  - oidc_provider_arn, node_role_arn
```

### GCP GKE Module (`modules/gcp-gke/`)

```
Inputs:
  - project_id, cluster_name, region, zones
  - node_pools, private_cluster, enable_workload_identity

Outputs:
  - cluster_endpoint, cluster_ca_certificate
  - service_account, node_pool_names
```

## Best Practices Demonstrated

1. **Modular Architecture** - Each cloud resource is a reusable module
2. **Remote State** with locking (S3+DynamoDB / GCS)
3. **Environment Separation** - dev, staging, prod with different configurations
4. **Security Scanning** - Checkov, tfsec in CI pipeline
5. **Least Privilege IAM** - Every role has minimum required permissions
6. **Encryption Everywhere** - At rest and in transit
7. **Cost Tracking** - Budgets, tags, and alerts
8. **Immutable Infrastructure** - No manual changes, always through Terraform

## License

MIT
