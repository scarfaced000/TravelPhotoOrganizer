variable "resource_group_name" {
  description = "Resource Group name"
  type        = string
}

variable "location" {
  description = "Azure region"
  type        = string
}

variable "storage_account_name" {
  description = "Storage Account name (globally unique)"
  type        = string
}

variable "containers" {
  description = "List of container names"
  type        = list(string)
  default     = ["uploads", "albums", "archive"]
}

variable "tags" {
  description = "Tags"
  type        = map(string)
  default     = {}
}
