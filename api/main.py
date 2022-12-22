import os

import boto3
from fastapi import FastAPI
from mangum import Mangum

from api.dynamodb.dynamodb import DynamodbDao

app = FastAPI()

dynamodb_client = boto3.client(service_name="dynamodb", region_name="eu-west-1")
dynamodb_dao = DynamodbDao(dynamodb_client=dynamodb_client)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/variable")
def variable():
    return os.environ["DYNAMODB_TABLE_NAME"]


@app.get("/attraction")
def attraction(country, city, attraction_name):
    return dynamodb_dao.put_attraction(country, city, attraction_name)


handler = Mangum(app=app)
