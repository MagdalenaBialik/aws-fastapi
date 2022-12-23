import os
from http import HTTPStatus

import boto3
from fastapi import FastAPI, HTTPException
from mangum import Mangum

from api.dynamodb.dynamodb import DynamodbDao

app = FastAPI()

dynamodb_table = boto3.resource(service_name="dynamodb", region_name="eu-west-1").Table(
    os.environ["DYNAMODB_TABLE_NAME"]
)
dynamodb_dao = DynamodbDao(dynamodb_table=dynamodb_table)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/variable")
def variable():
    return os.environ["DYNAMODB_TABLE_NAME"]


@app.post("/put_attraction", status_code=201)
def put_attraction(city, attraction_name):
    dynamodb_dao.put_attraction(city, attraction_name)
    return "Item successfully added"


@app.get("/get_attraction")
def get_attraction(city, attraction_name):
    response = dynamodb_dao.get_attraction(city, attraction_name)
    if response is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Item not found")

    return response


@app.get("/get_attraction_by_city")
def get_attraction_by_city(city):
    return dynamodb_dao.get_attraction_by_city(city)


handler = Mangum(app=app)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, port=8080)
