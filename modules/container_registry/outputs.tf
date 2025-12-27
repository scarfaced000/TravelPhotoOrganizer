output "registry_id" {
  description = "Container Registry ID"
  value       = azurerm_container_registry.main.id
}

output "registry_name" {
  description = "Container Registry 이름"
  value       = azurerm_container_registry.main.name
}

output "login_server" {
  description = "로그인 서버"
  value       = azurerm_container_registry.main.login_server
}

output "admin_username" {
  description = "Admin 사용자명"
  value       = azurerm_container_registry.main.admin_username
  sensitive   = true
}

output "admin_password" {
  description = "Admin 비밀번호"
  value       = azurerm_container_registry.main.admin_password
  sensitive   = true
}