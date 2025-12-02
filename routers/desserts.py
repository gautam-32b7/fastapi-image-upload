from typing import Annotated
import shutil
import os
import tempfile

from fastapi import APIRouter, Depends, Path, UploadFile, Form, HTTPException, File
from starlette import status
from sqlalchemy.orm import Session

from imagekitio import ImageKit
from imagekitio.models.UploadFileRequestOptions import UploadFileRequestOptions

from database import session_local
from models.dessert import Dessert
from config import PRIVATE_KEY, PUBLIC_KEY, URL_ENDPOINT

router = APIRouter()


# Provide a database session and ensures it's closed after use
def get_session():
    session = session_local()
    try:
        yield session
    finally:
        session.close()


# Defines a dependency that provides a database session to routes
session_dep = Annotated[Session, Depends(get_session)]


# SDK initialization
imagekit = ImageKit(
    private_key=PRIVATE_KEY,
    public_key=PUBLIC_KEY,
    url_endpoint=URL_ENDPOINT
)


# Retrieve list of all desserts
@router.get('/desserts', status_code=status.HTTP_200_OK)
async def list_desserts(session: session_dep):
    return session.query(Dessert).all()


# Retrieve a single dessert by its ID
@router.get('/desserts/{dessert_id}', status_code=status.HTTP_200_OK)
async def retrieve_dessert(dessert_id: int = Path(gt=0)):
    return 'DESSERT'


# Create a new dessert entry
@router.post('/desserts/create-dessert', status_code=status.HTTP_201_CREATED)
async def create_dessert(session: session_dep, dessert_name: str = Form(...), description: str = Form(...), price: float = Form(...), image: UploadFile = File(...)):
    temp_file_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(image.filename)[1]) as temp_file:
            temp_file_path = temp_file.name
            shutil.copyfileobj(image.file, temp_file)

            upload_result = imagekit.upload_file(
                file=open(temp_file_path, 'rb'),
                file_name=image.filename,
                options=UploadFileRequestOptions(
                    use_unique_file_name=True, tags=['backend-upload'])
            )

            if upload_result.response_metadata.http_status_code == 200:
                dessert_model = Dessert(
                    dessert_name=dessert_name,
                    description=description,
                    price=price,
                    image_url=upload_result.url
                )
                session.add(dessert_model)
                session.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            os.unlink(temp_file_path)
        image.file.close()


# Update an existing dessert by its ID
@router.put('/desserts/{dessert_id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_dessert(dessert_id: int = Path(gt=0)):
    return 'UPDATE DESSERT'


# Delete a dessert by its ID
@router.delete('/desserts/{dessert_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_dessert(dessert_id: int = Path(gt=0)):
    return 'DELETE DESSERT'
