# outputs.tf

output "resource_group_name" {
  description = "Resource Group name"
  value       = azurerm_resource_group.main.name
}

output "resource_group_location" {
  description = "Resource Group location"
  value       = azurerm_resource_group.main.location
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

output "container_registry_login_server" {
  description = "Container Registry 로그인 서버"
  value       = module.container_registry.login_server
}

output "container_registry_name" {
  description = "Container Registry 이름"
  value       = module.container_registry.registry_name
}

output "container_app_url" {
  description = "Container App FQDN"
  value       = module.container_apps.fqdn
}

output "container_app_name" {
  description = "Container App Name"
  value       = module.container_apps.container_app_name
}