# variables.tf

variable "subscription_id" {
  description = "Azure Subscription ID"
  type        = string
}

variable "location" {
  description = "Azure Region"
  type        = string
  default     = "Korea Central"
}

variable "project_name" {
  description = "Project name"
  type        = string
  default     = "travelphoto"
}

variable "environment" {
  description = "Environment"
  type        = string
  default     = "dev"
}

# Network 설정
variable "vnet_address_space" {
  description = "VNet address space"
  type        = list(string)
  default     = ["10.0.0.0/16"]
}

variable "public_subnet_prefix" {
  description = "Public subnet"
  type        = string
  default     = "10.0.1.0/24"
}

variable "private_subnet_prefix" {
  description = "Private subnet"
  type        = string
  default     = "10.0.2.0/24"
}