variable "resource_group_name" {
  description = "Resource Group 이름"
  type        = string
}

variable "location" {
  description = "Azure 리전"
  type        = string
}

variable "registry_name" {
  description = "Container Registry 이름"
  type        = string
}

variable "sku" {
  description = "ACR SKU"
  type        = string
  default     = "Basic"
}

variable "tags" {
  description = "태그"
  type        = map(string)
  default     = {}
}