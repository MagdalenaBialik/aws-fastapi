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
resource "aws_iam_role" "fastapi_role" {
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Sid    = ""
      Principal = {
        Service = "lambda.amazonaws.com"
      }
      }
    ]
  })

  name = "fastapi_role"

}

resource "aws_lambda_function" "fastapi" {
  function_name = "fastapi_lambda"

  role = aws_iam_role.fastapi_role.arn

  s3_bucket = "fastapi-artifacts"
  s3_key    = "${var.file_hash}.zip"

  handler = "main.handler"
  runtime = "python3.8"
}

variable "file_hash" {
  type = string
}
