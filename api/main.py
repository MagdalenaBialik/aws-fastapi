import os

from fastapi import FastAPI
from mangum import Mangum

app = FastAPI()

table_name = os.environ.get("DYNAMODB_TABLE_NAME", "fastapi_table")


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/variable")
def variable():
    return table_name


handler = Mangum(app=app)
