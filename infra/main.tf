terraform {
  cloud {
    organization = "bialik-magdalena"

    workspaces {
      name = "aws-fastapi2"
    }
  }

  #  backend "s3" {
  #    bucket = "fastapi-tf-bucket"
  #    key    = "infra/terraform.tfstate"
  #    region = "eu-west-1"
  #  }

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.33.0"
    }
  }
}

provider "aws" {
  region = "eu-west-1"
}

module "dynamodb" {
  source   = "./modules/dynamodb"
  app_name = var.app_name
}

module "iam" {
  source              = "./modules/iam"
  app_name            = var.app_name
  dynamodb_table_name = module.dynamodb.dynamodb_table_name
}

module "lambda" {
  source              = "./modules/lambda"
  app_name            = var.app_name
  dynamodb_table_name = module.dynamodb.dynamodb_table_name
  lambda_role         = module.iam.iam_role_arn
  file_hash           = var.file_hash
}
