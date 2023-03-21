from fastapi import APIRouter,Request,Response,Depends,Path
from controller.http import HTTP_RESPONSE
from db import get_db
from sqlalchemy.orm import Session
from schema import formSchema
from controller.admin import adminVerifyLogin,InsertNewUser


router = APIRouter()

@router.post("/login")
async def login(req:Request,res:Response,loginData:formSchema.AdminLogin,connectedDB:Session = Depends(get_db)):
    status,err = await adminVerifyLogin(loginData, connectedDB)
    if err == None:
        if status :
            req.session['loggedIn'] = True
            return HTTP_RESPONSE(statusCode=200).returnMessage(res)
        else:
            return HTTP_RESPONSE(statusCode=401).returnErrorMessage(res,"wrong email or password")
    return HTTP_RESPONSE(statusCode=500).returnErrorMessage(res,"something went wrong, please try again")

@router.post("/createAdmin")
async def login(req:Request,res:Response,adminData:formSchema.CreateAdmin,connectedDB:Session = Depends(get_db)):
    statusCode = await InsertNewUser(adminData, connectedDB)
    
    if statusCode == 1 :
            return HTTP_RESPONSE(statusCode=200).returnMessage(res)
    elif statusCode == -1:
            return HTTP_RESPONSE(statusCode=409).returnErrorMessage(res,"email already exist")
    return HTTP_RESPONSE(statusCode=500).returnErrorMessage(res,"something went wrong, please try again")