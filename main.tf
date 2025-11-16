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

resource "azurerm_resource_group" "main" {
  name     = "rg-${var.project_name}-${var.environment}"
  location = var.location

  tags = {
    Environment = var.environment
    Project     = "TravelPhotoOrganizer"
    ManagedBy   = "Terraform"
  }
}

module "network" {
  source = "./modules/network"

  resource_group_name   = azurerm_resource_group.main.name
  location              = azurerm_resource_group.main.location
  vnet_name             = "vnet-${var.project_name}"
  vnet_address_space    = var.vnet_address_space
  public_subnet_prefix  = var.public_subnet_prefix
  private_subnet_prefix = var.private_subnet_prefix

  tags = {
    Environment = var.environment
    Project     = "TravelPhotoOrganizer"
  }
}

# Storage 모듈
module "storage" {
  source = "./modules/storage"

  resource_group_name   = azurerm_resource_group.main.name
  location              = azurerm_resource_group.main.location
  storage_account_name  = "sttravelphoto${var.environment}"
  containers            = ["uploads", "albums", "archive"]

  tags = {
    Environment = var.environment
    Project     = "TravelPhotoOrganizer"
  }
}
