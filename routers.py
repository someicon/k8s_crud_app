from typing import Generator
from fastapi import APIRouter, Request, HTTPException, status, Depends, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import text
from sqlalchemy.orm import Session
from database.engine import engine, sessionlocal
from database import models

router = APIRouter()

templates = Jinja2Templates(directory="templates/")

models.Base.metadata.create_all(bind=engine)


def get_db() -> Generator[Session, None, None]:
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/testdb")
def test_db():
    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT 'PostgreSQL connection successful!'")
        )
    return result


@router.get("/")
def home_page(request: Request, db: Session = Depends(get_db)):
    users = db.query(models.User).order_by(models.User.id.desc())
    return templates.TemplateResponse("index.html", {"request": request, "users": users})


@router.get("/addnew")
def new_item(request: Request):
    return templates.TemplateResponse("addnew.html", {"request": request})


@router.post("/add")
async def add_user(
        name: str = Form(...),
        surname: str = Form(...),
        age: str = Form(...),
        email: str = Form(...),
        password: str = Form(...),
        db: Session = Depends(get_db)):

    user = models.User(name=name, surname=surname, age=age,
                       email=email, password=password)
    db.add(user)
    db.commit()
    return RedirectResponse(url=router.url_path_for("home_page"), status_code=status.HTTP_303_SEE_OTHER)


@router.get("/edit/{user_id}")
async def edit_user(request: Request, user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if user:
        return templates.TemplateResponse("edit.html", {"request": request, "user": user})

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User with supplied id doesn`t exist"
    )


@router.post("/update/{user_id}")
async def update_user(
        user_id: int,
        db: Session = Depends(get_db),
        name: str = Form(...),
        surname: str = Form(...),
        age: str = Form(...),
        email: str = Form(...),
        password: str = Form(...)):

    user = db.query(models.User).filter(models.User.id == user_id).first()

    if user:
        user.name = name
        user.surname = surname
        user.age = age
        user.email = email
        user.password = password
        db.commit()
        return RedirectResponse(url=router.url_path_for("home_page"), status_code=status.HTTP_303_SEE_OTHER)

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User with supplied id doensn`t exit"
    )


@router.get("/delete/{user_id}")
async def delete_user(user_id: int, db: Session = Depends(get_db)) -> RedirectResponse:
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if user:
        db.delete(user)
        db.commit()
        return RedirectResponse(url=router.url_path_for("home_page"), status_code=status.HTTP_303_SEE_OTHER)

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User with supplied id doesn`t exit"
    )
