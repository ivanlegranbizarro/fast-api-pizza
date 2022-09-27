import pydantic
import typing


class Signup(pydantic.BaseModel):
    username: str
    email: str
    password: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "username": "test",
                "email": "user@user.com",
                "password": "password"
            }
        }


class Settings(pydantic.BaseModel):
    authjwt_secret_key: str = 'a394b6f607da9f06626321ded6dab806eeae648a591a9a85d08c3cbd43a6ac51'


class Login(pydantic.BaseModel):
    username: str
    password: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "username": "test",
                "password": "password"
            }
        }


class Order(pydantic.BaseModel):
    quantity: int
    order_status: typing.Optional[str] = "PENDING"
    pizza_size: typing.Optional[str] = "MEDIUM"
    user_id: typing.Optional[int]

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "quantity": 1,
                "order_status": "PENDING",
                "pizza_size": "MEDIUM"
            }
        }

class UpdateOrder(pydantic.BaseModel):
    quantity: typing.Optional[int]
    order_status: typing.Optional[str]
    pizza_size: typing.Optional[str]
    user_id: typing.Optional[int]

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "quantity": 1,
                "order_status": "PENDING",
                "pizza_size": "MEDIUM"
            }
        }
