from typing import Optional

from pydantic import BaseModel, UUID4, EmailStr, model_validator, ConfigDict


class UserBase(BaseModel):
    email: EmailStr
    first_name: str
    last_name: Optional[str] | None = None


    #model_config = ConfigDict(from_attributes=True)


class UserCreate(UserBase):
    username: str
    age: int
    password: str
    password_confirm: str

    @model_validator(mode='after')
    def check_password_match(cls, values):
        if values.password != values.password_confirm:
            raise ValueError('Password do not match')
        return values


#class User(UserBase):
    #id: UUID4

    #class Config:
    #    from_attributes = True

    #@field_validator("id", pre=True)
    #def convert_to_str(cls, v, values, **kwargs):
    #    return str(v) if v else v


#class UserLogin(BaseModel):
#    email: EmailStr
#    password: str


class UserResponse(BaseModel):
    first_name: str
    last_name: str
    age: int
    email: str

    class Config:
        from_attributes = True



