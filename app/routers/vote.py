from sqlalchemy.orm import Session
from fastapi.routing import APIRouter
from fastapi import status, Depends, HTTPException

from .. import schemas, database, models, oauth2, exceptions

router = APIRouter(prefix="/vote", tags=["Vote"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(
    vote: schemas.Vote,
    db: Session = Depends(database.get_db),
    user: int = Depends(oauth2.get_current_user),
):
    if not db.query(models.Post).filter(models.Post.id == vote.post_id).first():
        raise exceptions.post_does_not_exist(id=vote.post_id)

    vote_query = db.query(models.Vote).filter(
        models.Vote.post_id == vote.post_id,
        models.Vote.user_id == user.id,
    )
    existing_vote = vote_query.first()

    if vote.add:
        if existing_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"User {user.id} has already voted on post {vote.post_id}",
            )
        db.add(models.Vote(post_id=vote.post_id, user_id=user.id))
        db.commit()
        return {"message": "Successfully added vote."}

    if not existing_vote:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Vote does not exist.",
        )

    vote_query.delete(synchronize_session=False)
    db.commit()
    return {"message": "Successfully removed vote."}
