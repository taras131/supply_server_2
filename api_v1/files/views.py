from fastapi import APIRouter, UploadFile, File, HTTPException
import shutil
from pathlib import Path
from fastapi.responses import FileResponse
import uuid

router = APIRouter(tags=["File Upload"])

UPLOAD_DIRECTORY = "uploaded_files"  # Локальная папка для хранения загруженных файлов
Path(UPLOAD_DIRECTORY).mkdir(exist_ok=True)  # Убедимся, что папка существует


@router.post("/")
async def upload_file(file: UploadFile = File(...)):
    try:
        unique_filename = f"{uuid.uuid4().hex}_{file.filename}"
        file_path = Path(UPLOAD_DIRECTORY) / unique_filename
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        return {"filename": unique_filename, "detail": "File uploaded successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")


@router.get("/{filename}")
async def get_photo(filename: str):
    file_path = Path(UPLOAD_DIRECTORY) / filename
    if not file_path.exists() or not file_path.is_file():  # Если файл не найден
        raise HTTPException(status_code=404, detail="Photo not found")

    return FileResponse(file_path, media_type="image/jpeg")


@router.delete("/{filename}")
async def delete_file(filename: str):
    file_path = Path(UPLOAD_DIRECTORY) / filename
    if (
        not file_path.exists() or not file_path.is_file()
    ):  # Проверяем, существует ли файл
        raise HTTPException(status_code=404, detail="File not found")
    try:
        file_path.unlink()  # Удаляем файл
        return {"filename": filename, "detail": "File deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
