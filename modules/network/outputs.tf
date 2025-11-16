output "vnet_id" {
  description = "Virtual Network ID"
  value       = azurerm_virtual_network.main.id
}

output "vnet_name" {
  description = "Virtual Network name"
  value       = azurerm_virtual_network.main.name
}

output "public_subnet_id" {
  description = "Public Subnet ID"
  value       = azurerm_subnet.public.id
}

output "private_subnet_id" {
  description = "Private Subnet ID"
  value       = azurerm_subnet.private.id
}

output "nsg_id" {
  description = "Network Security Group ID"
  value       = azurerm_network_security_group.app_nsg.id
}
