# backend.tf

terraform {
  backend "azurerm" {
    resource_group_name  = "s-t-stepup-rg"
    storage_account_name = "chaelimtfstate2024"
    container_name       = "tfstate"
    key                  = "travel-photo.tfstate"
  }
}