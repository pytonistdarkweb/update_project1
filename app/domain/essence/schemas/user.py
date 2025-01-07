from pydantic import BaseModel, EmailStr, Field, ConfigDict

class User(BaseModel):
    class Config(ConfigDict):
        model_config = ConfigDict(orm_mode=True)


class UserCreate(User):
    username: str = Field(..., min_length=3, max_length=50, pattern="^[a-zA-Z0-9_-]+$")
    email: EmailStr = Field(..., description="Email address must be valid")
    password: str = Field(..., min_length=8, max_length=100)
    
    
class UserLogin(User):
    email: EmailStr = Field(..., description="Email address must be valid")
    password: str = Field(..., min_length=8, max_length=100)




