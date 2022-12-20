terraform {
  backend "s3" {
    bucket = "fastapi-tf-bucket"
    key    = "infra/terraform.tfstate"
    region = "eu-west-1"
  }

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

resource "aws_cloudwatch_log_group" "lambda_logs" {
  name = "/aws/lambda/${aws_lambda_function.fastapi.function_name}"

}

resource "aws_lambda_function_url" "fastapi_lambda_url" {
  function_name      = aws_lambda_function.fastapi.function_name
  authorization_type = "NONE"
}

resource "aws_lambda_function" "fastapi" {
  function_name = "fastapi_lambda"
  role          = module.iam.iam_role_arn

  s3_bucket = "fastapi-artifacts"
  s3_key    = "${var.file_hash}.zip"

  handler = "api.main.handler"
  runtime = "python3.8"

  environment {
    variables = {
      DYNAMODB_TABLE_NAME = module.dynamodb.dynamodb_table_name
    }
  }
}
