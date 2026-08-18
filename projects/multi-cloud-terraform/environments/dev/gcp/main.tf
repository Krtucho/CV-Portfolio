terraform {
  required_version = ">= 1.7.0"

  backend "gcs" {
    bucket = "terraform-state-dev-gcp"
    prefix = "gcp/terraform.tfstate"
  }

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

module "gke" {
  source = "../../../modules/gcp-gke"

  project_id      = var.project_id
  environment     = "dev"
  cluster_name    = "dev-cluster"
  region          = var.region
  network         = var.network
  subnetwork      = var.subnetwork
  pods_range_name = var.pods_range_name

  node_pools = {
    default = {
      machine_type   = "e2-standard-4"
      min_node_count = 1
      max_node_count = 3
      disk_size_gb   = 50
      disk_type      = "pd-ssd"
      spot           = true
    }
  }

  enable_private_nodes    = true
  enable_private_endpoint = false

  authorized_networks = [
    {
      cidr = var.admin_cidr
      name = "admin-vpn"
    }
  ]
}
