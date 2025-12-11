from uuid import UUID

from pydantic import BaseModel, EmailStr


class RegisterInSchema(BaseModel):
    name: str
    second_name: str
    group_number: str
    email: EmailStr
    password: str


class RegisterOutSchema(BaseModel):
    user_uid: UUID


class ConfirmInSchema(BaseModel):
    user_id: UUID
    confirm_code: str


class ConfirmOutSchema(BaseModel):
    jwt_auth_token: str


class LoginInSchema(BaseModel):
    email: str
    password: str


class LoginOutSchema(BaseModel):
    jwt_auth_token: str


class ResetPasswordInSchema(BaseModel):
    email: str
    new_password: str


class ResetPasswordOutSchema(BaseModel):
    pass


class ConfirmResetInSchema(BaseModel):
    confirm_code: str
    email: str


class ConfirmResetOutSchema(BaseModel):
    token: str