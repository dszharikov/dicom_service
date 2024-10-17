from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_upload_dicom():
    pass
