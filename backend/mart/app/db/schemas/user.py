from email.mime import image
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime, date
from typing import Optional, Union


class UserBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    is_active: bool
   
class UserBasic(UserBase):
   # firstname: str
   # lastname: str
    email: str
    
       
class User(UserBase):
    first_name: Optional[str] = Field(
        title="The name of the User to do",
        description="The name has a maximum length of 50 characters",
        max_length=50,
        examples = ["John doe"]
    )
    last_name: Optional[str] = Field(
        title="The name of the User to do",
        description="The name has a maximum length of 50 characters",
        max_length=50,
        examples = ["John doe"]
    )
    email : str = Field(
        title="The email of the user",
        description="The email has a maximum length of 50 characters",
        max_length=50,
        examples = ["user@gmail.com"]
    )
    # password: str
    created_at : datetime = datetime.now()
    role: str = 'user'  # user , admin, , staff
    is_admin: Optional[bool] = False  # Default to False
    is_verified: Optional[bool] = False
    profile_picture: Optional[str] = Field(
        title="The profile picture of the user",
        description="The profile picture has a maximum length of 50 characters"
    )  
 
class UserCreate(User):
    hashed_password: str

class UserUpdate(BaseModel):
    hashed_password: str
    email: str
    updated_at: datetime = Field(default_factory=datetime.now)

class UserOut(User):
    id: int
    username: str = Field(..., alias="email")