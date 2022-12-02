data "aws_region" "current"{
}
resource "aws_api_gateway_rest_api" "fastapi" {
  name          = "fastapi_gateway"
  body = jsonencode({
    openapi = "3.0.2"
    info = {
      title   = "fastapi"
      version = "1.0.1"
    }
    paths = {
      "/" = {
        get = {
          x-amazon-apigateway-integration = {
            httpMethod           = "GET"
            payloadFormatVersion = "1.0"
            type                 = "AWS_PROXY"
            uri                  = "arn:aws:apigateway:${data.aws_region.current.name}:lambda:path/2015-03-31/functions/${aws_lambda_function.fastapi.arn}/invocations"
          }
//          responses = {
//            200 = {
//              description: "200 Response",
//              content: {
//                application/json: {
//                  schema: {
//                    $ref: "#/"
//                  }
//                }
//              }
//            }
//          }
        }

      }
    }
  })

  endpoint_configuration {
    types = ["REGIONAL"]
  }
}

resource "aws_api_gateway_gateway_response" "this" {
  rest_api_id   = aws_api_gateway_rest_api.fastapi.id
  status_code   = "200"

  response_templates = {
    "application/json" = "{\"message\":$context.error.messageString}"
  }

  response_parameters = {
    "gatewayresponse.header.Authorization" = "'Basic'"
  }
  response_type = ""
}

resource "aws_api_gateway_deployment" "this" {
  rest_api_id = aws_api_gateway_rest_api.fastapi.id

  triggers = {
    redeployment = sha1(jsonencode(aws_api_gateway_rest_api.fastapi.body))
  }

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_api_gateway_stage" "this" {
  deployment_id = aws_api_gateway_deployment.this.id
  rest_api_id   = aws_api_gateway_rest_api.fastapi.id
  stage_name    = "dev"
}
