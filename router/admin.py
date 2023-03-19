import os
import json
from fastapi import APIRouter,Request,Response,Depends,Path
from controller.http import HTTP_RESPONSE
from db import get_db
from sqlalchemy.orm import Session
from schema import formSchema
from controller.admin import adminVerifyLogin
from controller.user import CustomerLogics,PositionLogics

router = APIRouter()

@router.post("/login")
async def login(req:Request,res:Response,loginData:formSchema.AdminLogin,connectedDB:Session = Depends(get_db)):
    status,err = await adminVerifyLogin(loginData, connectedDB)
    if err == None:
        if status :
            return HTTP_RESPONSE(statusCode=200).returnMessage(res)
        else:
            return HTTP_RESPONSE(statusCode=401).returnCustomMessage(res,"wrong email or password")
    return HTTP_RESPONSE(statusCode=200).returnMessage(res) if status else HTTP_RESPONSE(statusCode=500).returnCustomMessage(res,"something went wrong, please try again")

@router.get("/listAll")
async def listAll(req:Request,res:Response):
    return True

@router.post("/getUser")
async def getUser(req:Request,res:Response,reqData:formSchema.MyStatus,connectedDB:Session=Depends(get_db)):
    resultData,status = await CustomerLogics.getUserData(reqData.email,connectedDB)
    if status:
        if resultData == None:
            return HTTP_RESPONSE(statusCode=404).returnCustomMessage(res,{
            "data" : "email doesn't exist"
            })
        else:
            return HTTP_RESPONSE(statusCode=200).returnCustomMessage(res,{
            "data" : resultData
            })
    return HTTP_RESPONSE(statusCode=500).returnCustomMessage(res,"Something went wrong")

@router.post("/updateUser")
async def updateUser(req:Request,res:Response):
    return True

@router.delete("/deleteUser")
async def deleteUser(req:Request,res:Response,delData:formSchema.DeleteUser,connectedDB:Session = Depends(get_db)):
    rowCount,cErr = await CustomerLogics.MarkCustomerAsInActive(delData.id, connectedDB)
    if cErr != None:
        return HTTP_RESPONSE(statusCode=500).returnCustomMessage(res,"something went wrong, please try again")
    elif rowCount < 1:
        return  HTTP_RESPONSE(statusCode=404).returnCustomMessage(res,"customer id doesn't exist")
    
    _,pErr = await PositionLogics.deletePositionByCustomerId(delData.id, connectedDB)
    if pErr != None:
        return HTTP_RESPONSE(statusCode=500).returnCustomMessage(res,"something went wrong, please try again")
    
    return  HTTP_RESPONSE(statusCode=200).returnMessage(res)