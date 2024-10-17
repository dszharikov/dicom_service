from fastapi import FastAPI
from app.routes import router

app = FastAPI(
    title="DICOM Upload Service",
    description="API для загрузки DICOM-файлов и их хранения в Minio",
    version="1.0.0",
)

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000)
