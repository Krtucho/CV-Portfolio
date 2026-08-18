variable "project_id" {
  description = "GCP Project ID"
  type        = string
}

variable "environment" {
  description = "Environment name"
  type        = string
}

variable "cluster_name" {
  description = "GKE Cluster name"
  type        = string
}

variable "region" {
  description = "GCP region"
  type        = string
}

variable "network" {
  description = "VPC network name"
  type        = string
}

variable "subnetwork" {
  description = "VPC subnetwork name"
  type        = string
}

variable "pods_range_name" {
  description = "Secondary range name for pods"
  type        = string
  default     = "pods"
}

variable "services_range_name" {
  description = "Secondary range name for services"
  type        = string
  default     = "services"
}

variable "node_pools" {
  description = "Node pool configurations"
  type = map(object({
    machine_type    = string
    min_node_count  = number
    max_node_count  = number
    disk_size_gb    = number
    disk_type       = string
    spot            = bool
  }))
}

variable "enable_private_nodes" {
  description = "Enable private nodes"
  type        = bool
  default     = true
}

variable "enable_private_endpoint" {
  description = "Enable private endpoint"
  type        = bool
  default     = true
}

variable "master_ipv4_cidr_block" {
  description = "CIDR block for master"
  type        = string
  default     = "172.16.0.0/28"
}

variable "authorized_networks" {
  description = "Authorized networks for master access"
  type = list(object({
    cidr = string
    name = string
  }))
  default = []
}

variable "enable_cost_allocation" {
  description = "Enable cost allocation"
  type        = bool
  default     = true
}

variable "kms_key_name" {
  description = "KMS key name for etcd encryption"
  type        = string
  default     = ""
}

variable "tags" {
  description = "Tags to apply"
  type        = map(string)
  default     = {}
}
