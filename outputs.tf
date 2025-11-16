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
