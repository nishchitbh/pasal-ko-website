from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas
from .. import utils
from .. import models
from .. import oauth2

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    userexists = db.query(models.User).filter(models.User.username==user.username).first()
    if userexists:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail=f"User with username {user.username} already exists!")
    user.password = utils.hash(user.password)
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {id} does not exist",
        )
    return user


@router.get("/", status_code=status.HTTP_200_OK)
def get_users(
    db: Session = Depends(get_db), current_user=Depends(oauth2.get_current_user)
):
    if not current_user.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action",
        )
    users = db.query(models.User).all()
    return users


@router.patch("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_user(
    id: int,
    updated_user: schemas.UserPatch,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    user_query = db.query(models.User).filter(models.User.id == id)
    user = user_query.first()

    if not current_user.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action",
        )
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"product with id: {id} does not exist",
        )
    user_query.update(updated_user.dict(), synchronize_session=False)
    db.commit()
    return user_query.first()


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    id: int,
    db: Session = Depends(get_db),
    current_user=Depends(oauth2.get_current_user),
):
    if not current_user.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="You're not authorized yet!"
        )
    user_query = db.query(models.User).filter(models.User.id == id)
    user = user_query.first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {id} does not exist.",
        )
    user_query.delete(synchronize_session=False)
    db.commit()


@router.post("/admin", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_admin(user: schemas.AdminCreate, db: Session = Depends(get_db)):
    userexists = db.query(models.User).filter(models.User.username==user.username).first()
    if userexists:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail=f"User with username {user.username} already exists!")
    user.password = utils.hash(user.password)
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
