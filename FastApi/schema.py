from pydantic import BaseModel
from typing import Optional, List
from schema import CreateAndUpdateUser

class User(BaseModel):
    id = int
    name = str

    class Config:
        orm_mode = True


# TO support list and get APIs
class User(CreateAndUpdateUser):
    id: int

    class Config:
        orm_mode = True


# To support list cars API
class PaginatedUserInfo(BaseModel):
    limit: int
    offset: int
    data: List[User]

