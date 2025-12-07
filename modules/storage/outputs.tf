output "storage_account_id" {
  description = "Storage Account ID"
  value       = azurerm_storage_account.main.id
}

output "storage_account_name" {
  description = "Storage Account name"
  value       = azurerm_storage_account.main.name
}

output "primary_blob_endpoint" {
  description = "Primary Blob endpoint"
  value       = azurerm_storage_account.main.primary_blob_endpoint
}

output "connection_string" {
  description = "Storage connection string"
  value       = azurerm_storage_account.main.primary_connection_string
  sensitive   = true
}

output "container_names" {
  description = "Created container names"
  value       = [for c in azurerm_storage_container.containers : c.name]
}
output "primary_access_key" {
  description = "Storage Account Primary Access Key"
  value       = azurerm_storage_account.main.primary_access_key
  sensitive   = true
}