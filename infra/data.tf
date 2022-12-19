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
