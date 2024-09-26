from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
import schemas, database, crud, oauth2, models


router = APIRouter(
    prefix="/vote",
    tags=["Vote"]
)

@router.post("/", status_code=status.HTTP_200_OK)
def vote(vote: schemas.VoteCreate, db: Session = Depends(database.get_db), user_id: str = Depends(oauth2.get_current_user)):
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == user_id)
    found_vote = vote_query.first()
    if vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User {user_id} has already voted on post {vote.post_id}")
        new_vote = models.Vote(post_id=vote.post_id, user_id=user_id)
        db.add(new_vote)
        db.commit()
        return {"message": "Successfully added vote"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User doesnt have voted on post {vote.post_id}, cant unvote")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "Successfully deleted vote"}