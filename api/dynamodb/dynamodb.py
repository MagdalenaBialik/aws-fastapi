from boto3.dynamodb.conditions import Key

from api.exceptions import AttractionNotFoundError
from api.schemas import Attraction
from api.settings import Settings


class DynamodbDao:
    def __init__(self, dynamodb_table, settings: Settings):
        self.dynamodb_table = dynamodb_table
        self.settings = settings

    def put_attraction(self, attraction: Attraction):
        self.dynamodb_table.put_item(
            Item=self._key_from_attraction(attraction),
        )

    def _attraction_from_item(self, item: dict) -> Attraction:
        return Attraction(city=item["PK"], name=item["SK"])

    def _key_from_attraction(self, attraction: Attraction) -> dict:
        key = {"PK": attraction.city.title(), "SK": attraction.name.title()}
        return key

    def get_attraction(self, attraction: Attraction) -> Attraction:
        response = self.dynamodb_table.get_item(
            Key=self._key_from_attraction(attraction),
        )
        item = response.get("Item", None)
        if item is None:
            raise AttractionNotFoundError("Attraction not found")

        return self._attraction_from_item(item)

    def get_attraction_by_city(self, city):
        response = self.dynamodb_table.query(
            KeyConditionExpression=Key("PK").eq(city),
        )
        items = response["Items"]
        list_of_attractions = [self._attraction_from_item(item) for item in items]

        return list_of_attractions

    def delete_item(self, attraction: Attraction):
        if self.get_attraction(attraction) is None:
            return None

        response = self.dynamodb_table.delete_item(
            Key=self._key_from_attraction(attraction)
        )
        return response
