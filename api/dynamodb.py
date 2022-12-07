class DynamodbDao:
    def __init__(self, dynamodb_client):
        self.dynamodb_client = dynamodb_client

    def put_attraction(self, city, attraction):
        self.dynamodb_client.put_item(
            TableName="Travel-dynamodb-table",
            Item={"PK": {"S": city}, "SK": {"S": "1"}, "Attraction": {"S": attraction}},
        )
