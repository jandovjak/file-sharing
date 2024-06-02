from sqlalchemy.orm import Session
from uuid import UUID
import models
import schemas


def get_file(db: Session, id: UUID):
    return db.query(models.File).filter(models.File.id == id).first()


def get_files(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.File).offset(skip).limit(limit).all()


def create_file(db: Session, file: schemas.FileCreate):
    db_file = models.File(**file.model_dump())
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    return db_file


def delete_file(db: Session, id: UUID):
    db_file = db.query(models.File).filter(models.File.id == id).first()
    if db_file:
        db.delete(db_file)
        db.commit()
    return db_file
