resource "aws_lambda_function_url" "fastapi_lambda_url" {
  function_name      = aws_lambda_function.fastapi.function_name
  authorization_type = "NONE"
}

resource "aws_cloudwatch_log_group" "lambda_logs" {
  name = "/aws/lambda/${aws_lambda_function.fastapi.function_name}"

}

resource "aws_lambda_function" "fastapi" {
  function_name = "fastapi_lambda"
  role          = var.lambda_role
  s3_bucket     = "fastapi-artifacts"
  s3_key        = "${var.file_hash}.zip"

  handler = "api.main.handler"
  runtime = "python3.8"

  environment {
    variables = {
      DYNAMODB_TABLE_NAME = var.dynamodb_table_name
    }
  }
}
