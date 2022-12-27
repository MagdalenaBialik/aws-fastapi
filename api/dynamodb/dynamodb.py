from boto3.dynamodb.conditions import Key

from api.settings import Settings


class DynamodbDao:
    def __init__(self, dynamodb_table, settings: Settings):
        self.dynamodb_table = dynamodb_table
        self.settings = settings

    def put_attraction(self, city: str, attraction: str):
        self.dynamodb_table.put_item(
            Item={
                "PK": city.title(),
                "SK": attraction.title(),
            },
        )

    def get_attraction(self, city, attraction):
        response = self.dynamodb_table.get_item(
            Key={
                "PK": city,
                "SK": attraction,
            },
        )
        return response.get("Item", None)

    def get_attraction_by_city(self, city):
        response = self.dynamodb_table.query(
            KeyConditionExpression=Key("PK").eq(city),
        )
        return response["Items"]

    def delete_item_(self, city, attraction):
        self.dynamodb_table.delete_item(
            Key={
                "PK": city,
                "SK": attraction,
            }
        )
