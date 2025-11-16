from pydantic import BaseModel, EmailStr


class RegisterInSchema(BaseModel):
    name: str
    second_name: str
    group_number: str
    email: EmailStr
    password: str


class RegisterOutSchema(BaseModel):
    token: str