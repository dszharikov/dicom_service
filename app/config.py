from pydantic import BaseSettings

class Settings(BaseSettings):
    MINIO_ENDPOINT: str
    MINIO_ACCESS_KEY: str
    MINIO_SECRET_KEY: str
    MINIO_BUCKET: str = "dicom-files"
    MINIO_SECURE: bool = False

    class Config:
        env_file = ".env"
