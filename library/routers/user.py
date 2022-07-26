from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from ..data_base import user
from library import schemas, database

router = APIRouter(
    prefix="/user",
    tags=['Users']
)
get_db = database.get_db


@router.post("/", status_code=status.HTTP_200_OK, response_model=schemas.ShowUser)
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    return user.create(request, db)


@router.get("/{user_id}", response_model=schemas.ShowUser)
def get_user(user_id, db: Session = Depends(get_db)):
    return user.get_single(user_id, db)
