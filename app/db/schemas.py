from pydantic import BaseModel
from uuid import UUID


class UserBase(BaseModel):

    first_name: str
    las_name: str
    email: str
