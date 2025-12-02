from fastapi import FastAPI

from imagekitio import ImageKit

from database import engine
from models import dessert
from routers import desserts

app = FastAPI()

dessert.Base.metadata.create_all(bind=engine)




app.include_router(desserts.router)
