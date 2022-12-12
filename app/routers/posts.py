from msilib import schema
from typing import Optional

from sqlalchemy import func
from sqlalchemy.orm import Session
from fastapi import Response, status, Depends, APIRouter

from ..database import get_db
from .. import models, schemas, oauth2, exceptions

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/", response_model=list[schemas.PostGet])
def get_posts(
    db: Session = Depends(get_db),
    user=Depends(oauth2.get_current_user),
    title: Optional[str] = "",
    limit: int = 10,
    offset: int = 0,
):
    # in sqlalchemy, default join is left inner, whereas most are default left outer.
    # offset skips the first <offset> posts in the result and returns everything after.
    return (
        db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
        .join(
            models.Vote,
            models.Post.id == models.Vote.post_id,
            isouter=True,
        )
        .filter(models.Post.title.contains(title))
        .group_by(models.Post.id)
        .limit(limit)
        .offset(offset)
        .all()
    )


@router.get("/{id}", response_model=schemas.PostGet)
def get_post(
    id: int,
    db: Session = Depends(get_db),
    user=Depends(oauth2.get_current_user),
):
    post = (
        db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
        .join(
            models.Vote,
            models.Post.id == models.Vote.post_id,
            isouter=True,
        )
        .filter(models.Post.id == id)
        .group_by(models.Post.id)
        .first()
    )
    if not post:
        raise exceptions.post_does_not_exist(id=id)
    return post


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.Post,
)
def create_post(
    post: schemas.PostBase,
    db: Session = Depends(get_db),  # Force connection to database.
    user=Depends(oauth2.get_current_user),  # Force login
):
    # post = models.Post(
    #     title=post.title,
    #     content=post.content,
    #     published=post.published,
    # )
    post = models.Post(owner_id=user.id, **post.dict())
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int,
    db: Session = Depends(get_db),
    user=Depends(oauth2.get_current_user),
):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if not post:
        raise exceptions.post_does_not_exist(id=id)
    if post.owner_id != user.id:
        raise exceptions.not_authorized()
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Post)
def update_post(
    id: int,
    updated_post: schemas.PostBase,
    db: Session = Depends(get_db),
    user=Depends(oauth2.get_current_user),
):
    query = db.query(models.Post).filter(models.Post.id == id)
    current_post = query.first()
    if not current_post:
        raise exceptions.post_does_not_exist(id=id)
    if current_post.owner_id != user.id:
        raise exceptions.not_authorized()
    query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return query.first()
