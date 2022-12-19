resource "aws_dynamodb_table" "dynamodb_table" {
  name           = "${var.app_name}-table"
  read_capacity  = 5
  write_capacity = 5
  hash_key       = "PK"

  attribute {
    name = "PK"
    type = "S"
  }
}
