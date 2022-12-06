import os

from fastapi import FastAPI
from mangum import Mangum

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/variable")
def variable():
    return os.environ.get("DYNAMODB_TABLE_NAME", "fastapi_table")


handler = Mangum(app=app)
