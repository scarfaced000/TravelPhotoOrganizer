# main.tf

terraform {
  required_version = ">= 1.0"
  
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}

provider "azurerm" {
  features {
    resource_group {
      prevent_deletion_if_contains_resources = false
    }
  }
  subscription_id = var.subscription_id
}

# 로컬 변수
locals {
  common_tags = {
    Environment = var.environment
    Project     = "TravelPhotoOrganizer"
    ManagedBy   = "Terraform"
  }
}

# Resource Group
resource "azurerm_resource_group" "main" {
  name     = "rg-${var.project_name}-${var.environment}"
  location = var.location
  tags     = local.common_tags
}

# Network 모듈
module "network" {
  source = "./modules/network"

  resource_group_name   = azurerm_resource_group.main.name
  location              = azurerm_resource_group.main.location
  vnet_name             = "vnet-${var.project_name}"
  vnet_address_space    = var.vnet_address_space
  public_subnet_prefix  = var.public_subnet_prefix
  private_subnet_prefix = var.private_subnet_prefix

  tags = local.common_tags
}

# Storage 모듈
module "storage" {
  source = "./modules/storage"

  resource_group_name  = azurerm_resource_group.main.name
  location             = azurerm_resource_group.main.location
  storage_account_name = "st${var.project_name}${var.environment}"
  containers           = ["uploads", "albums", "archive"]

  tags = local.common_tags
}

# Log Analytics 모듈
module "log_analytics" {
  source = "./modules/log_analytics"

  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  workspace_name      = "log-${var.project_name}-${var.environment}"
  retention_in_days   = 30

  tags = local.common_tags
}

# Container Apps 모듈
module "container_apps" {
  source = "./modules/container_apps"

  resource_group_name        = azurerm_resource_group.main.name
  location                   = azurerm_resource_group.main.location
  environment_name           = "cae-${var.project_name}-${var.environment}"
  log_analytics_workspace_id = module.log_analytics.workspace_id
  
  container_app_name = "ca-${var.project_name}-api-${var.environment}"
  container_name     = "fastapi-app"
  container_image    = var.container_image
  container_cpu      = 0.5
  container_memory   = "1Gi"
  
  min_replicas = 1
  max_replicas = 3
  
  ingress_external_enabled = true
  ingress_target_port      = 8000
  
  environment_variables = {
    ENVIRONMENT          = var.environment
    STORAGE_ACCOUNT_NAME = module.storage.storage_account_name
    AZURE_REGION         = var.location
  }
  
  secrets = {
    storage-account-key = module.storage.primary_access_key
  }
  
  tags = local.common_tags
}
