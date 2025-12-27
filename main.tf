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
  features {}
  subscription_id = var.subscription_id
}

# 로컬 변수
locals {
  # Workspace에 따라 environment 자동 설정
  environment = terraform.workspace == "default" ? var.environment : terraform.workspace

  common_tags = {
    Environment = local.environment
    Project     = "TravelPhotoOrganizer"
    ManagedBy   = "Terraform"
  }
}
# Resource Group
resource "azurerm_resource_group" "main" {
  name     = "rg-${var.project_name}-${local.environment}"
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

  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location

  # workspace별로 완전히 다른 이름
  storage_account_name = local.environment == "prod" ? "sttravelphotoprod" : "sttravelphotodev"

  containers = ["uploads", "albums", "archive"]

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

# Container Registry 모듈 
module "container_registry" {
  source = "./modules/container_registry"

  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  registry_name       = "acr${var.project_name}${local.environment}"
  sku                 = "Basic"

  tags = local.common_tags
}

# Container Apps 모듈 (수정)
module "container_apps" {
  source = "./modules/container_apps"

  resource_group_name        = azurerm_resource_group.main.name
  location                   = azurerm_resource_group.main.location
  environment_name           = "cae-${var.project_name}-${var.environment}"
  log_analytics_workspace_id = module.log_analytics.workspace_id

  container_app_name = "ca-${var.project_name}-api-${var.environment}"
  container_name     = "fastapi-app"
  container_image    = "${module.container_registry.login_server}/travel-photo-api:latest"
  container_cpu      = 0.5
  container_memory   = "1Gi"

  min_replicas = 1
  max_replicas = 3

  ingress_external_enabled = true
  ingress_target_port      = 8000

  # ✅ ACR 인증 추가
  registry_server               = module.container_registry.login_server
  registry_username             = module.container_registry.admin_username
  registry_password_secret_name = "acr-password"

  environment_variables = {
    ENVIRONMENT          = var.environment
    STORAGE_ACCOUNT_NAME = module.storage.storage_account_name
    AZURE_REGION         = var.location
  }

  # ✅ Secrets에 ACR 비밀번호 추가
  secrets = {
    storage-account-key = module.storage.primary_access_key
    acr-password        = module.container_registry.admin_password
  }

  tags = local.common_tags
}