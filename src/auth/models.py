from uuid import UUID
from pydantic import BaseModel
from datetime import date, datetime


class RegisterAdmin(BaseModel):
    firstname: str
    lastname: str
    phone: str
    email: str
    username: str
    password: str
    position: str
    time_created: datetime



class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    admin_id: str | None = None

    def get_uuid(self) -> UUID | None:
        if self.admin_id:
            return UUID(self.admin_id)
        return None
    

    