import os


class DynamodbDao:
    def __init__(self, dynamodb_client):
        self.dynamodb_client = dynamodb_client

    def put_attraction(self, country, city, attraction):
        self.dynamodb_client.put_item(
            TableName=os.environ["DYNAMODB_TABLE_NAME"],
            Item={
                "PK": {"S": country},
                "SK": {"S": city},
                "Attraction": {"S": attraction},
            },
        )
