output "container_app_id" {
  description = "Container App ID"
  value       = azurerm_container_app.main.id
}

output "fqdn" {
  description = "Container App FQDN"
  value       = "https://${azurerm_container_app.main.ingress[0].fqdn}"
}

output "container_app_name" {
  description = "Container App Name"
  value       = azurerm_container_app.main.name
}

output "environment_id" {
  description = "Container App Environment ID"
  value       = azurerm_container_app_environment.main.id
}