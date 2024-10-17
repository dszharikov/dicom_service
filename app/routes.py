from fastapi import APIRouter, UploadFile, File, HTTPException
from app.minio_client import upload_file_to_minio
from app.dicom_processor import process_dicom_file
import os
import shutil

router = APIRouter()

@router.post("/upload/", summary="Загрузить DICOM-файл", tags=["Загрузка"])
async def upload_dicom(file: UploadFile = File(...)):
    # Проверяем расширение файла
    if not file.filename.lower().endswith(('.dcm', '.dicom')):
        raise HTTPException(status_code=400, detail="Недопустимый формат файла. Требуется DICOM-файл.")

    # Создаем временный путь для хранения файла
    temp_dir = "/tmp/dicom_uploads"
    os.makedirs(temp_dir, exist_ok=True)
    temp_file_path = os.path.join(temp_dir, file.filename)

    # Сохраняем файл во временное хранилище
    with open(temp_file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        # Обрабатываем DICOM-файл и извлекаем метаданные
        dicom_metadata = process_dicom_file(temp_file_path)

        # Загружаем файл в Minio
        upload_file_to_minio(temp_file_path, dicom_metadata)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Удаляем временный файл
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

    return {"message": "DICOM-файл успешно загружен", "metadata": dicom_metadata}
