from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import get_db


router = APIRouter(prefix="/vote", tags=["Votes"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(
    vote: schemas.Vote,
    db: Session = Depends(get_db),
    current_user=Depends(oauth2.get_current_user),
):
    product = db.query(models.Product).filter(models.Product.id==vote.product_id).first()
    if not product:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"Product with id {vote.product_id} doesn't exist")
    vote_query = db.query(models.Votes).filter(
        models.Votes.product_id == vote.product_id,
        models.Votes.user_id == current_user.id,
    )
    found_vote = vote_query.first()

    if vote.dir:
        if found_vote:
            raise HTTPException(
                status.HTTP_409_CONFLICT,
                detail=f"User {current_user.id} has already voted on product {vote.product_id}",
            )
        new_vote = models.Votes(product_id=vote.product_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "Successfully added vote"}
    else:
        if not found_vote:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Vote does not exist")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "Successfully deleted vote"}
