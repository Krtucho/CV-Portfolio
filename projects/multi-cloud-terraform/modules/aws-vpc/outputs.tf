output "vpc_id" {
  value = aws_vpc.main.id
}

output "public_subnet_ids" {
  value = aws_subnet.public[*].id
}

output "private_subnet_ids" {
  value = aws_subnet.private[*].id
}

output "nat_gateway_ips" {
  value = aws_eip.nat[*].public_ip
}

output "flow_log_group" {
  value = var.enable_flow_logs ? aws_cloudwatch_log_group.flow_logs[0].name : null
}
