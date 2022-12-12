from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, status, HTTPException

from .. import database, schemas, models, utils, oauth2

router = APIRouter(tags=["Authentification"])


@router.post("/login", response_model=schemas.Token)
def login(
    # OAuth2PasswordRequestForm allows you to use form-data in postman
    # (different format input than raw json body)
    credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(database.get_db),
) -> None:
    where = models.User.email == credentials.username
    user = db.query(models.User).filter(where).first()
    if not user and utils.verify(credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Invalid Credentials.",
        )
    access_token = oauth2.create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}
