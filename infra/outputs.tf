output "lambda_url" {
  description = "URL of fastapi lambda"
  value       = aws_lambda_function_url.fastapi_lambda_url.function_url
}
