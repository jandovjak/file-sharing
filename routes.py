from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from fastapi.responses import Response, StreamingResponse
from sqlalchemy.orm import Session
from uuid import UUID
from io import BytesIO
from database import get_db
from config import FILE_LOCATION
from app import decrypt, encrypt, hash_password

import crud
import schemas
import os

router = APIRouter()


def is_valid_uuid(uuid: str) -> bool:
    try:
        uuid_object = UUID(uuid)
    except ValueError:
        return False
    return str(uuid_object) == uuid


@router.post("/upload", response_model=schemas.File)
async def upload_file(file: UploadFile = File(...),
                      password: str = Form(...),
                      db: Session = Depends(get_db)):
    file_data = schemas.FileCreate(filename=file.filename,
                                   size=file.size)
    created_file = crud.create_file(db=db, file=file_data)
    file_location = f"{FILE_LOCATION}/{created_file.id}"
    file_content = await file.read()
    key = hash_password(password)
    encrypted = encrypt(file_content, key)
    try:
        with open(file_location, "wb") as file_object:
            file_object.write(encrypted)
            return created_file
    except FileNotFoundError:
        raise HTTPException(status_code=404,
                            detail="File could not be created")
    except PermissionError:
        raise HTTPException(status_code=404,
                            detail="File could not be created")
    except Exception:
        raise HTTPException(status_code=500,
                            detail="Unexpected error happened")


@router.post("/download")
def read_file(id: str = Form(...),
              password: str = Form(...),
              decrypt_file: bool = Form(None),
              db: Session = Depends(get_db)):
    if not is_valid_uuid(id):
        raise HTTPException(status_code=404, detail="Invalid ID")
    file = crud.get_file(db, id=id)
    if file is None:
        raise HTTPException(status_code=404, detail="File not found")
    file_location = f"{FILE_LOCATION}/{file.id}"
    try:
        with open(file_location, "rb") as file_object:
            key = hash_password(password)
            data = file_object.read()
            if decrypt_file is not None and decrypt_file:
                data = decrypt(data, key)
            headers = {
                'Content-Disposition': f"attachment; filename={file.filename}"
            }
            return StreamingResponse(BytesIO(data),
                                     headers=headers,
                                     media_type='application/octet-stream')
    except FileNotFoundError:
        raise HTTPException(status_code=404,
                            detail="File does not exist")
    except PermissionError:
        raise HTTPException(status_code=404,
                            detail="Unable to delete file")
    except Exception:
        raise HTTPException(status_code=500,
                            detail="Unexpected error happened")


@router.post("/delete", response_model=schemas.File)
def delete_file(id: str = Form(...),
                db: Session = Depends(get_db)):
    if not is_valid_uuid(id):
        raise HTTPException(status_code=404, detail="Invalid ID")
    file = crud.delete_file(db, id=id)
    if file is None:
        raise HTTPException(status_code=404,
                            detail="File not found")
    file_location = f"{FILE_LOCATION}/{file.id}"
    try:
        os.remove(file_location)
        return Response(status_code=204)
    except FileNotFoundError:
        raise HTTPException(status_code=404,
                            detail="File does not exist")
    except PermissionError:
        raise HTTPException(status_code=404,
                            detail="Unable to delete file")
    except Exception:
        raise HTTPException(status_code=500,
                            detail="Unexpected error happened")
