from fastapi import status, HTTPException, Depends, APIRouter
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from .. import models
from ..database import get_db
from .. import schemas
from .. import oauth2


router = APIRouter(prefix="/products", tags=["Products"])


@router.get("/", response_model=List[schemas.ProductOut])
def get_products(
    db: Session = Depends(get_db),
    limit: int = 20,
    skip: int = 0,
    search: Optional[str] = "",
):
    results = (
        db.query(models.Product, func.count(models.Votes.product_id).label("votes"))
        .join(models.Votes, models.Votes.product_id == models.Product.id, isouter=True)
        .group_by(models.Product.id)
        .filter(models.Product.name.ilike(f"%{search}%"))
        .limit(limit)
        .offset(skip)
        .all()
    )
    products = [
        schemas.ProductOut(Product=schemas.Product.from_orm(product), votes=votes)
        for product, votes in results
    ]

    return products


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Product)
def post_product(
    product: schemas.ProductCreate,
    db: Session = Depends(get_db),
    current_user=Depends(oauth2.get_current_user),
):
    if not current_user.approved:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="You're not authorized yet!"
        )
    new_product = models.Product(user_id=current_user.id, **product.dict())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.ProductOut)
def get_product(id: int, db: Session = Depends(get_db)):
    product = (
        db.query(models.Product, func.count(models.Votes.product_id).label("votes"))
        .join(models.Votes, models.Votes.product_id == models.Product.id, isouter=True)
        .group_by(models.Product.id)
        .filter(models.Product.id == id)
        .first()
    )
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {id} does not exist",
        )
    return product


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    id: int,
    db: Session = Depends(get_db),
    current_user=Depends(oauth2.get_current_user),
):
    if not current_user.approved:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="You're not authorized yet!"
        )
    product_query = db.query(models.Product).filter(models.Product.id == id)
    product = product_query.first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {id} does not exist.",
        )
    product_query.delete(synchronize_session=False)
    db.commit()


@router.put(
    "/{id}",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=schemas.Product,
)
def update_product(
    id: int,
    updated_product: schemas.ProductCreate,
    db: Session = Depends(get_db),
    current_user=Depends(oauth2.get_current_user),
):
    if not current_user.approved:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="You're not authorized yet!"
        )
    product_query = db.query(models.Product).filter(models.Product.id == id)
    product = product_query.first()
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"product with id: {id} does not exist",
        )
    product_query.update(updated_product.dict(), synchronize_session=False)
    db.commit()
    return product_query.first()
