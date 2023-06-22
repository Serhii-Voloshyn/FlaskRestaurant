from datetime import date
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, StrictInt


class User(BaseModel):
    username: str = Field(min_length=1)
    email: EmailStr
    full_name: str | None
    password: str = Field(min_length=8)


class Login(BaseModel):
    username: str
    password: str


class Restaurant(BaseModel):
    name: str = Field(min_length=1)


class Menu(BaseModel):
    restaurant_id: int
    day: date


class Employee(BaseModel):
    full_name: str = Field(min_length=1)
    email: EmailStr


class MenuItem(BaseModel):
    menu_id: int
    name: str
    price: float


StrictIntRange = type('MyStrictStr', (StrictInt,), {"ge":1, "le":5})


class Vote(BaseModel):
    menu_id: int
    employee_id: int
    score: StrictIntRange
