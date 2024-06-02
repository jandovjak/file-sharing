from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from uuid import UUID
from io import BytesIO
import crud
import schemas
import os
from database import get_db
from config import FILE_LOCATION
from app import encrypt, hash_password

router = APIRouter()


@router.post("/upload", response_model=schemas.File)
async def upload_file(file: UploadFile = File(...),
                      password: str = Form(...),
                      db: Session = Depends(get_db)):
    file_size = file.size
    file_data = schemas.FileCreate(filename=file.filename,
                                   size=file_size)
    created_file = crud.create_file(db=db, file=file_data)
    file_location = f"{FILE_LOCATION}/{created_file.id}"
    contents = await file.read()
    key = hash_password(password)
    encrypted = encrypt(contents, key)
    with open(file_location, "wb+") as file_object:
        file_object.write(encrypted)
    return created_file


@router.get("/files/{file_id}", response_model=schemas.File)
def read_file(file_id: UUID,
              password: str = Form(...),
              db: Session = Depends(get_db)):
    file = crud.get_file(db, file_id=file_id)
    if file is None:
        raise HTTPException(status_code=404, detail="File not found")
    file_location = f"{FILE_LOCATION}/{file.id}"
    with open(file_location, "rb+") as file_object:
        data = file_object.read()
        headers = {
            'Content-Disposition': f"attachment; filename={file.filename}"
        }
        return StreamingResponse(BytesIO(data),
                                 headers=headers,
                                 media_type='application/octet-stream')


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
