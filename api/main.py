from http import HTTPStatus

import boto3
from fastapi import FastAPI, HTTPException
from mangum import Mangum

from api.dynamodb.dynamodb import DynamodbDao
from api.exceptions import AttractionNotFoundError
from api.schemas import Attraction
from api.settings import get_settings

settings = get_settings()

app = FastAPI()

dynamodb_table = boto3.resource(service_name="dynamodb", region_name="eu-west-1").Table(
    settings.DYNAMODB_TABLE_NAME
)
dynamodb_dao = DynamodbDao(dynamodb_table=dynamodb_table, settings=settings)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/variable")
def variable():
    return settings.DYNAMODB_TABLE_NAME


@app.post("/put_attraction", status_code=201)
def put_attraction(attraction: Attraction):
    dynamodb_dao.put_attraction(attraction)
    return "Item successfully added"


@app.post("/get_attraction")
def get_attraction(attraction: Attraction) -> Attraction:
    try:
        response = dynamodb_dao.get_attraction(attraction)
    except AttractionNotFoundError:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Item not found")
    return response


@app.get("/get_attraction_by_city")
def get_attraction_by_city(city: str) -> Attraction:
    return dynamodb_dao.get_attraction_by_city(city)


@app.delete("/delete_attraction")
def delete_attraction(attraction: Attraction) -> Attraction:
    response = dynamodb_dao.delete_item(attraction)
    if response is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f"No {attraction.name} was found in the {attraction.city}",
        )
    return response


handler = Mangum(app=app)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, port=8080)
