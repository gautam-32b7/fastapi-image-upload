from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from starlette import status

from database import engine
from models import dessert
from routers import desserts

app = FastAPI()

dessert.Base.metadata.create_all(bind=engine)

# Root route


@app.get('/', status_code=status.HTTP_200_OK, include_in_schema=False)
def root():
    return RedirectResponse(url='/desserts')


app.include_router(desserts.router)
