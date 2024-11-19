provider "aws" {
  region = "eu-north-1"
}

terraform {
  backend "local" {
    path = "terraform/state/terraform.tfstate"
  }
}