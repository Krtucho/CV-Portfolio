resource "google_service_account" "gke" {
  account_id   = "gke-${var.environment}"
  display_name = "GKE Service Account - ${var.environment}"
  project      = var.project_id
}

resource "google_container_cluster" "primary" {
  name     = "${var.environment}-cluster"
  location = var.region

  network    = var.network
  subnetwork = var.subnetwork

  remove_default_node_pool = true
  initial_node_count       = 1

  private_cluster_config {
    enable_private_nodes    = var.enable_private_nodes
    enable_private_endpoint = var.enable_private_endpoint
    master_ipv4_cidr_block  = var.master_ipv4_cidr_block
  }

  master_authorized_networks_config {
    dynamic "cidr_blocks" {
      for_each = var.authorized_networks
      content {
        cidr_block   = cidr_blocks.value.cidr
        display_name = cidr_blocks.value.name
      }
    }
  }

  ip_allocation_policy {
    cluster_secondary_range_name  = var.pods_range_name
    services_secondary_range_name = var.services_range_name
  }

  workload_identity_config {
    workload_pool = "${var.project_id}.svc.id.goog"
  }

  addons_config {
    network_policy_config {
      disabled = false
    }
    horizontal_pod_autoscaling {
      disabled = false
    }
  }

  network_policy {
    enabled  = true
    provider = "CALICO"
  }

  cluster_autoscaling {
    enabled             = true
    autoscaling_profile = "BALANCED"
    resource_limits {
      resource_type = "cpu"
      minimum       = 1
      maximum      = 100
    }
    resource_limits {
      resource_type = "memory"
      minimum       = 1
      maximum      = 400
    }
  }

  cost_allocation_config {
    enable_cost_allocation = var.enable_cost_allocation
  }

  # Security configuration
  shielded_nodes {
    enable_secure_boot          = true
    enable_integrity_monitoring = true
  }

  workload_identity_config {
    workload_pool = "${var.project_id}.svc.id.goog"
  }

  database_encryption {
    state    = "ENCRYPTED"
    key_name = var.kms_key_name
  }

  release_channel {
    channel = "REGULAR"
  }

  maintenance_policy {
    recurring_window {
      start_time = "2024-01-01T02:00:00Z"
      end_time   = "2024-01-01T06:00:00Z"
      recurrence = "FREQ=WEEKLY;BYDAY=SA,SU"
    }
  }

  monitoring_config {
    enable_components = [
      "SYSTEM_COMPONENTS",
      "WORKLOADS",
      "APISERVER",
      "SCHEDULER",
      "CONTROLLER_MANAGER",
      "STORAGE",
      "HPA",
      "POD",
      "DAEMONSET",
      "DEPLOYMENT",
      "STATEFULSET",
    ]
    managed_prometheus {
      enabled = true
    }
  }

  logging_config {
    enable_components = [
      "SYSTEM_COMPONENTS",
      "WORKLOADS",
      "APISERVER",
      "SCHEDULER",
      "CONTROLLER_MANAGER",
    ]
  }

  node_pool_defaults {
    node_config_defaults {
      gcfs_config {
        enabled = true
      }
    }
  }

  lifecycle {
    ignore_changes = [
      node_pool,
      node_pool_defaults,
    ]
  }

  depends_on = [google_service_account.gke]
}

resource "google_container_node_pool" "pools" {
  for_each = var.node_pools

  name     = each.key
  location = var.region
  cluster  = google_container_cluster.primary.name

  initial_node_count = each.value.min_node_count

  autoscaling {
    min_node_count = each.value.min_node_count
    max_node_count = each.value.max_node_count
  }

  management {
    auto_repair  = true
    auto_upgrade = true
  }

  node_config {
    machine_type    = each.value.machine_type
    disk_size_gb    = each.value.disk_size_gb
    disk_type       = each.value.disk_type
    preemptible     = each.value.spot
    service_account = google_service_account.gke.email
    oauth_scopes    = ["https://www.googleapis.com/auth/cloud-platform"]

    shielded_instance_config {
      enable_secure_boot          = true
      enable_integrity_monitoring = true
    }

    workload_metadata_config {
      mode = "GKE_METADATA"
    }

    labels = merge(var.tags, {
      environment = var.environment
      node_pool   = each.key
    })
  }

  lifecycle {
    ignore_changes = [
      initial_node_count,
    ]
  }
}
