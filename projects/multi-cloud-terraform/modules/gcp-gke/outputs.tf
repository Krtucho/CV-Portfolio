output "cluster_endpoint" {
  value = google_container_cluster.primary.endpoint
}

output "cluster_ca_certificate" {
  value = google_container_cluster.primary.master_auth[0].cluster_ca_certificate
}

output "cluster_name" {
  value = google_container_cluster.primary.name
}

output "service_account" {
  value = google_service_account.gke.email
}

output "node_pool_names" {
  value = [for pool in google_container_node_pool.pools : pool.name]
}
