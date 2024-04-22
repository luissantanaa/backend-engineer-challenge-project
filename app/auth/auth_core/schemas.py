from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class UserGet(UserBase):
    model_config = ConfigDict(from_attributes=True)


class UserAuth(UserBase):
    role: str


class TokenPayload(BaseModel):
    sub: str = None
    exp: int = None


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
