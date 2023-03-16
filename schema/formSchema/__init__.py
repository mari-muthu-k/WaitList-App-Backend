from pydantic import BaseModel, Field,validator


class CreateUser(BaseModel):
    name  : str
    email : str 
    referral_link : str 
    
class MyStatus(BaseModel):
    id : int 

class AdminLogin(BaseModel):
    email : str 
    password : str 

class UpdateUser(BaseModel):
    name  : str 
    email : str 
    position : int 