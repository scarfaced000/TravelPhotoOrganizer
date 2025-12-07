variable "resource_group_name" {
  description = "Resource Group 이름"
  type        = string
}

variable "location" {
  description = "Azure 리전"
  type        = string
}

variable "workspace_name" {
  description = "Log Analytics Workspace 이름"
  type        = string
}

variable "sku" {
  description = "SKU"
  type        = string
  default     = "PerGB2018"
}

variable "retention_in_days" {
  description = "로그 보관 일수"
  type        = number
  default     = 30
}

variable "tags" {
  description = "리소스 태그"
  type        = map(string)
  default     = {}
}
