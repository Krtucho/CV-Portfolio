terraform {
  required_version = ">= 1.7.0"

  backend "s3" {
    bucket         = "terraform-state-dev"
    key            = "aws/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-state-lock"
    encrypt        = true
  }

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Environment = "dev"
      ManagedBy   = "Terraform"
      Project     = "MultiCloudInfra"
    }
  }
}

module "vpc" {
  source = "../../../modules/aws-vpc"

  environment       = "dev"
  cidr_block        = var.vpc_cidr
  availability_zones = var.availability_zones

  public_subnet_cidrs  = var.public_subnet_cidrs
  private_subnet_cidrs = var.private_subnet_cidrs

  enable_flow_logs         = true
  flow_logs_retention_days = 30
  single_nat_gateway       = true
}

module "eks" {
  source = "../../../modules/aws-eks"

  environment    = "dev"
  cluster_name   = "dev-cluster"
  cluster_version = "1.29"
  vpc_id         = module.vpc.vpc_id
  subnet_ids     = module.vpc.private_subnet_ids

  node_groups = {
    main = {
      desired_size    = 2
      min_size       = 1
      max_size       = 3
      instance_types = ["t3.medium"]
      use_spot       = true
    }
  }

  endpoint_private_access = true
  endpoint_public_access  = false
}
