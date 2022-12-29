from pydantic import BaseModel


class Attraction(BaseModel):
    city: str
    name: str
