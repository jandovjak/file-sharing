from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import shutil
from uuid import UUID
import crud
import schemas
import os
from database import get_db
from config import FILE_LOCATION

router = APIRouter()


@router.post("/upload", response_model=schemas.File)
def upload_file(file: UploadFile = File(...),
                db: Session = Depends(get_db)):
    file_size = file.size
    file_data = schemas.FileCreate(filename=file.filename,
                                   size=file_size)
    created_file = crud.create_file(db=db, file=file_data)
    file_location = f"{FILE_LOCATION}/{created_file.id}"
    with open(file_location, "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)
    return created_file


@router.get("/files/{file_id}", response_model=schemas.File)
def read_file(file_id: UUID, db: Session = Depends(get_db)):
    file = crud.get_file(db, file_id=file_id)
    if file is None:
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(f"{FILE_LOCATION}/{file.id}",
                        media_type='application/octet-stream',
                        filename=file.filename)


@router.delete("/files/{file_id}", response_model=schemas.File)
def delete_file(file_id: UUID, db: Session = Depends(get_db)):
    file = crud.delete_file(db, file_id=file_id)
    if file is None:
        raise HTTPException(status_code=404, detail="File not found")
    file_location = f"{FILE_LOCATION}/{file.id}"
    try:
        os.remove(file_location)
        print(f"The file {file_location} has been removed successfully.")
    except FileNotFoundError:
        print(f"The file {file_location} does not exist.")
    except PermissionError:
        print(f"Permission denied: unable to delete {file_location}.")
    except Exception as e:
        print(f"Error occurred: {e}")
    return file
