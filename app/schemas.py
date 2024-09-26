from pydantic import BaseModel

from pydantic import BaseModel
from typing import Optional

class CreateUserRequest(BaseModel):
    name: str
    email: str
    age: Optional[int] = None
    address: Optional[str] = None
    phone_number: Optional[str] = None
    gender: str
    membership_status: Optional[str] = 'Active'

class UpdateUserRequest(BaseModel):
    name: Optional[str]
    email: Optional[str]
    age: Optional[int]
    address: Optional[str]
    phone_number: Optional[str]
    gender: Optional[str]
    membership_status: Optional[str]


class RespValidation(BaseModel):
    status: str
    message: str
    data: dict = None
