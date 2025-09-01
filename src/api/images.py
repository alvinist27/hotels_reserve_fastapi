from fastapi import APIRouter, BackgroundTasks, UploadFile

from src.services.images import ImagesService

images_router = APIRouter(prefix='/images', tags=['Images'])


@images_router.post('')
def upload_image(file: UploadFile, background_tasks: BackgroundTasks):
    ImagesService().upload_image(file, background_tasks)
