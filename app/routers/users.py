from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Depends, APIRouter

from ..database import get_db
from .. import models, schemas, utils

router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.UserResponse,
)
def create_post(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # hash the users password
    user.password = utils.hash(user.password)
    user = models.User(**user.dict())
    db.add(user)
    db.commit()
    # Apparently calling commit gets rid of the user variable
    # so you need to use refresh to get it back.
    db.refresh(user)
    return user


@router.get("/{id}", response_model=schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id: {id} does not exist.",
        )
    return user
