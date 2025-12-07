output "resource_group_name" {
  description = "Resource Group name"
  value       = azurerm_resource_group.main.name
}

output "vnet_id" {
  description = "Virtual Network ID"
  value       = module.network.vnet_id
}

output "public_subnet_id" {
  description = "Public Subnet ID"
  value       = module.network.public_subnet_id
}

output "private_subnet_id" {
  description = "Private Subnet ID"
  value       = module.network.private_subnet_id
}

output "storage_account_name" {
  description = "Storage Account name"
  value       = module.storage.storage_account_name
}

output "blob_endpoint" {
  description = "Blob endpoint"
  value       = module.storage.primary_blob_endpoint
}

output "container_names" {
  description = "Container names"
  value       = module.storage.container_names
}

output "container_app_url" {
  description = "Container App 접속 URL"
  value       = module.container_apps.container_app_url
}

output "container_app_fqdn" {
  description = "Container App FQDN"
  value       = module.container_apps.container_app_fqdn
}

output "log_analytics_workspace_id" {
  description = "Log Analytics Workspace ID"
  value       = module.log_analytics.workspace_id
}
