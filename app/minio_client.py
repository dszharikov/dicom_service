from minio import Minio
from minio.error import S3Error
import os
from app.config import Settings

settings = Settings()

# Инициализация клиента Minio
minio_client = Minio(
    endpoint=settings.MINIO_ENDPOINT,
    access_key=settings.MINIO_ACCESS_KEY,
    secret_key=settings.MINIO_SECRET_KEY,
    secure=settings.MINIO_SECURE
)

bucket_name = settings.MINIO_BUCKET

def upload_file_to_minio(file_path: str, metadata: dict):
    # Проверяем наличие бакета и создаем его при необходимости
    if not minio_client.bucket_exists(bucket_name):
        minio_client.make_bucket(bucket_name)

    # Формируем уникальное имя объекта для хранения
    object_name = f"{metadata['PatientID']}/{metadata['StudyInstanceUID']}/{os.path.basename(file_path)}"

    # Загружаем файл в Minio
    try:
        minio_client.fput_object(
            bucket_name=bucket_name,
            object_name=object_name,
            file_path=file_path,
            content_type="application/dicom"
        )
    except S3Error as err:
        raise Exception(f"Ошибка при загрузке файла в Minio: {str(err)}")
