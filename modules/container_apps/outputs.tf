output "environment_id" {
  description = "Container Apps Environment ID"
  value       = azurerm_container_app_environment.main.id
}

output "environment_name" {
  description = "Container Apps Environment 이름"
  value       = azurerm_container_app_environment.main.name
}

output "container_app_id" {
  description = "Container App ID"
  value       = azurerm_container_app.main.id
}

output "container_app_name" {
  description = "Container App 이름"
  value       = azurerm_container_app.main.name
}

output "container_app_fqdn" {
  description = "Container App URL"
  value       = azurerm_container_app.main.ingress[0].fqdn
}

output "container_app_url" {
  description = "Container App 전체 URL"
  value       = "https://${azurerm_container_app.main.ingress[0].fqdn}"
}
