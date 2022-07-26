

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. hashing import Hash
from .. import models, JWT_token


from library import database


router = APIRouter(
    prefix="/login",
    tags=['Authentication']
)
get_db = database.get_db


@router.post('/')
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Credentials are not allowed")
    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid password")
    access_token = JWT_token.create_access_token(data={"sub": user.email})

    return {"access_token": access_token, "token_type": "bearer"}


