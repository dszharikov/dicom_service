import pydicom
from pydicom.errors import InvalidDicomError

def process_dicom_file(file_path: str) -> dict:
    try:
        # Читаем DICOM-файл
        ds = pydicom.dcmread(file_path)

        # Извлекаем необходимые метаданные
        metadata = {
            "PatientID": ds.get("PatientID", "Unknown"),
            "StudyInstanceUID": ds.get("StudyInstanceUID", "Unknown"),
            "SeriesInstanceUID": ds.get("SeriesInstanceUID", "Unknown"),
            "SOPInstanceUID": ds.get("SOPInstanceUID", "Unknown"),
            "Modality": ds.get("Modality", "Unknown"),
            "SliceThickness": ds.get("SliceThickness", "Unknown"),
            "PixelSpacing": ds.get("PixelSpacing", "Unknown"),
        }
        return metadata

    except InvalidDicomError:
        raise Exception("Файл не является корректным DICOM-файлом")
    except Exception as e:
        raise Exception(f"Ошибка при обработке DICOM-файла: {str(e)}")
