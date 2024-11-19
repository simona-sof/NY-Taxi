provider aws {
    region = "eu-north-1"
}

terraform {
  backend "s3" {
    bucket         = "my-taxi-bucket-1" 
    key            = "terraform/state/terraform.tfstate"
    region         = "eu-north-1"
    encrypt        = true
  }
}