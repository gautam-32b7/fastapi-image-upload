from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from starlette import status
from fastapi.middleware.cors import CORSMiddleware

from database import engine
from models import dessert
from routers import desserts

app = FastAPI()

dessert.Base.metadata.create_all(bind=engine)


# Origin -> CORS
origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:5173",   # <-- Vite dev server

    'https://fastapi-image-upload-m1b1.onrender.com'  # backend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root route


@app.get('/', status_code=status.HTTP_200_OK, include_in_schema=False)
def root():
    return RedirectResponse(url='/desserts')


app.include_router(desserts.router)
