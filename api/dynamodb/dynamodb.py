import os


class DynamodbDao:
    def __init__(self, dynamodb_client):
        self.dynamodb_client = dynamodb_client

    def put_attraction(self, city: str, attraction: str):
        self.dynamodb_client.put_item(
            TableName=os.environ["DYNAMODB_TABLE_NAME"],
            Item={
                "PK": {"S": city.title()},
                "SK": {"S": attraction.title()},
            },
        )

    def get_attraction(self, city, attraction):
        return self.dynamodb_client.get_item(
            TableName=os.environ["DYNAMODB_TABLE_NAME"],
            Key={
                "PK": {"S": city},
                "SK": {"S": attraction},
            },
        )

    def get_attraction_by_city(self, city):
        return self.dynamodb_client.query(
            TableName=os.environ["DYNAMODB_TABLE_NAME"],
            Key={
                "PK": {"S": city},
            },
        )
