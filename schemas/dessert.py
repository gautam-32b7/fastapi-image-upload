from pydantic import BaseModel


# Pydantic: dessert data schema for request
class RequestDessert(BaseModel):
    id: int | None = None
    dessert_name: str
    description: str
    price: int
    image_url: str
