import os

# import boto3
# from dynamodb import DynamodbDao
from fastapi import FastAPI
from mangum import Mangum

app = FastAPI()
#
# dynamodb_client = boto3.client(service_name="dynamodb")
#
# dynamodb_dao = DynamodbDao(dynamodb_client=dynamodb_client)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/variable")
def variable():
    return os.environ.get("DYNAMODB_TABLE_NAME", "fastapi_table")


#
# @app.get("/attraction")
# def attraction(city, attraction_name):
#     return dynamodb_dao.put_attraction(city, attraction_name)


handler = Mangum(app=app)
