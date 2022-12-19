data "aws_region" "current" {

}

data "aws_caller_identity" "current" {

}

data "aws_iam_policy_document" "dynamodb_policy_document" {
  statement {
    actions = [
      "dynamodb:PutItem",
    ]
    resources = ["arn:aws:dynamodb:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:table/${aws_dynamodb_table.dynamodb_table.name}"]

    effect = "Allow"
  }
}

data "aws_iam_policy_document" "function_logging_policy_document" {
  statement {
    actions = [
      "logs:CreateLogStream",
      "logs:PutLogEvents"
    ]
    resources = ["arn:aws:logs:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:${aws_cloudwatch_log_group.lambda_logs.name}"]
    effect    = "Allow"
  }
}
