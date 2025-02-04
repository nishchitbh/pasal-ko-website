from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ProductBase(BaseModel):
    name: str
    price: int
    is_available: Optional[bool] = None


class UserCreate(BaseModel):
    username: str
    password: str


class UserEdit(UserCreate):
    username: str
    password: str
    approved: bool
    admin: bool


class UserPatch(BaseModel):
    approved: bool
    admin: bool


class UserOut(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    username: str
    password: str


class ProductCreate(ProductBase):
    pass


class Product(ProductBase):
    id: int
    created_at: datetime
    user_id: int
    user: UserOut

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str

    class Config:
        orm_mode = True


class TokenData(BaseModel):
    id: str


class Vote(BaseModel):
    product_id: int
    dir: bool

class ProductOut(BaseModel):
    Product: Product
    votes: int
    class Config:
        from_attributes = True

class AdminCreate(UserCreate):
    admin:Optional[bool] = True
    approved:Optional[bool] = True