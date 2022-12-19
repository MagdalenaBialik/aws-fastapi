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

resource "aws_iam_policy" "function_logging_policy" {
  name   = "function-logging-policy"
  policy = data.aws_iam_policy_document.function_logging_policy_document.json
}

resource "aws_iam_role_policy_attachment" "function_logging_policy_attachment" {
  role       = aws_iam_role.fastapi_role.id
  policy_arn = aws_iam_policy.function_logging_policy.arn
}

resource "aws_iam_policy" "dynamodb_policy" {
  name   = "dynamodb_policy"
  policy = data.aws_iam_policy_document.dynamodb_policy_document.json
}

resource "aws_iam_role_policy_attachment" "dynamodb_policy_attachment" {
  role       = aws_iam_role.fastapi_role.id
  policy_arn = aws_iam_policy.dynamodb_policy.arn
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
  role          = aws_iam_role.fastapi_role.arn

  s3_bucket = "fastapi-artifacts"
  s3_key    = "${var.file_hash}.zip"

  handler = "api.main.handler"
  runtime = "python3.8"

  environment {
    variables = {
      DYNAMODB_TABLE_NAME = var.dynamodb_table_name
    }
  }
}

module "dynamodb" {
  source   = "./modules/dynamodb"
  app_name = var.app_name
}
