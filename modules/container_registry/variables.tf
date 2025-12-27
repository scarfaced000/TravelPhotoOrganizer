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
  description = "ACR SKU (Basic, Standard, Premium)"
  type        = string
  default     = "Basic"
}

variable "tags" {
  description = "리소스 태그"
  type        = map(string)
  default     = {}
}