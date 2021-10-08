from sqlalchemy.orm import Session

from . import models, schemas


def get_picture(db: Session, picture_id: int):
    return db.query(models.Picture).filter(
        models.Picture.id == picture_id
    ).first()


def get_all_picture(db: Session):
    return db.query(models.Picture).filter(
        models.Picture.is_valid
    ).filter(
        models.Picture.is_active
    ).all()


def update_picture(db: Session, picture_id: int, picture_name: str):
    db.query(models.Picture).filter(
        models.Picture.id == picture_id
    ).update({"name": (picture_name)})
    db.commit()
    return db.query(models.Picture).filter(
        models.Picture.id == picture_id
    ).first()


def delete_picture(db: Session, picture_id: int):
    db_picture = db.query(models.Picture).filter(
        models.Picture.id == picture_id
    ).first()
    db_picture.is_valid = False
    db.commit()
    db.refresh(db_picture)
    return db_picture


def get_picture_by_md5(db: Session, md5: str):
    return db.query(models.Picture).filter(models.Picture.md5 == md5).first()


def create_picture(db: Session, picture: schemas.PictureCreate):
    db_picture = models.Picture(name=picture.name,
                                content_type=picture.content_type,
                                md5=picture.md5)
    db.add(db_picture)
    db.commit()
    db.refresh(db_picture)
    return db_picture
