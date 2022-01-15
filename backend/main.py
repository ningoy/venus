from typing import List

from fastapi import FastAPI, File, UploadFile, Depends, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from sqlalchemy.orm import Session
from fastapi_pagination import Page, add_pagination, paginate
from db import crud, models, schemas
from db.database import SessionLocal, engine
import hashlib
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware
from settings import Settings

origins = [
    "http://localhost",
    "http://localhost:8080",
]

models.Base.metadata.create_all(bind=engine)
settings = Settings()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
absolute_path = settings.absolute_path


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/files/")
async def create_files(files: List[bytes] = File(...)):
    return {"file_sizes": [len(file) for file in files]}


@app.get("/files/", response_model=Page[schemas.Picture])
async def get_files(db: Session = Depends(get_db)):
    db_picture = crud.get_all_picture(db)
    return paginate(db_picture)


@app.post("/renamefiles/")
def rename_file(picture: schemas.PictureRename, db: Session = Depends(get_db)):
    picture_id = picture.id
    new_name = picture.name
    db_picture = crud.update_picture(
        db, picture_id=picture_id, picture_name=new_name
    )
    return db_picture


@app.get("/deletefiles/")
def delete_file(id: int, db: Session = Depends(get_db)):
    db_picture = crud.delete_picture(db, picture_id=id)
    return db_picture


@app.get("/downloadfiles/")
def download_file(id: int, db: Session = Depends(get_db)):
    db_picture = crud.get_picture(db, picture_id=id)
    file_path = "{}/{}/{}".format(absolute_path,
                                  db_picture.create_time.strftime('%Y-%m'),
                                  db_picture.md5)
    return FileResponse(path=file_path,
                        filename=db_picture.md5,
                        media_type=db_picture.content_type)


@app.post("/uploadfiles/", response_model=schemas.Picture)
async def create_upload_files(
    files: List[UploadFile] = File(...), db: Session = Depends(get_db)
):
    for file in files:
        # todo
        contents = await file.read()
        md5 = hashlib.md5(contents).hexdigest()
        picture = schemas.PictureCreate
        picture.name = file.filename
        picture.content_type = file.content_type
        picture.md5 = md5
        db_picture = crud.get_picture_by_md5(db, md5=md5)
        if db_picture:
            raise HTTPException(
                status_code=400, detail="Picture already uploaded"
            )
        else:
            created_picture = crud.create_picture(db=db, picture=picture)
            # 从create_time中解析出年-月数据
            create_month = created_picture.create_time.strftime('%Y-%m')
            # 检测指定路径下是否有该月的目录
            tmp_dir = Path("{}/{}".format(absolute_path, create_month))
            if tmp_dir.exists():
                print("该目录已存在: {}".format(tmp_dir))
            else:
                tmp_dir.mkdir()
            # 检测指定路径下是否有该文件
            tmp_file = tmp_dir / md5
            if tmp_file.exists():
                print("该文件已存在: {}".format(tmp_file))
            else:
                with tmp_file.open('wb') as f:
                    f.write(contents)
    return created_picture


@app.get("/")
async def main():
    content = """
<body>
<form action="/files/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
<form action="/uploadfiles/" enctype="multipart/form-data" method="post">
<input name="files" type="fie" multiple>
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)


add_pagination(app)
