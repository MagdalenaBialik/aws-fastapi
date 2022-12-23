import os

from boto3.dynamodb.conditions import Key


class DynamodbDao:
    def __init__(self, dynamodb_table):
        self.dynamodb_table = dynamodb_table

    def put_attraction(self, city: str, attraction: str):
        self.dynamodb_table.put_item(
            TableName=os.environ["DYNAMODB_TABLE_NAME"],
            Item={
                "PK": city.title(),
                "SK": attraction.title(),
            },
        )

    def get_attraction(self, city, attraction):
        response = self.dynamodb_table.get_item(
            TableName=os.environ["DYNAMODB_TABLE_NAME"],
            Key={
                "PK": city,
                "SK": attraction,
            },
        )
        return response.get("Item", None)

    def get_attraction_by_city(self, city):
        response = self.dynamodb_table.query(
            TableName=os.environ["DYNAMODB_TABLE_NAME"],
            KeyConditionExpression=Key("PK").eq(city),
        )
        return response["Items"]
