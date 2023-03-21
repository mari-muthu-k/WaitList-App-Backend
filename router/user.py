import os
import json
from fastapi import APIRouter,Request,Response,Depends,Path
from schema.formSchema import CreateUser as CreateUserSchema,MyStatus as MyStatusSchema
from controller.user import CustomerLogics
from controller.http import HTTP_RESPONSE
from db import get_db
from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/subscribe")
def subscribe(req:Request,res:Response,userData:CreateUserSchema,connectedDB:Session=Depends(get_db)): # have to be synchronous as move up is synchronous
    status = CustomerLogics.createUser(userData,connectedDB)
    if status == -1:
        return HTTP_RESPONSE(statusCode=409).returnErrorMessage(res, "email already exist")

    return HTTP_RESPONSE(statusCode=200).returnMessage(res) if status == 1 else HTTP_RESPONSE(statusCode=500).returnErrorMessage(res,"something went wrong, please try again")

@router.post("/mystatus")
async def myStatus(req:Request,res:Response,reqData:MyStatusSchema,connectedDB:Session=Depends(get_db)):
    resultData,status = await CustomerLogics.getUserData(reqData.email,connectedDB)
    if status:
        if resultData == None:
            return HTTP_RESPONSE(statusCode=404).returnErrorMessage(res, "email doesn't exist")
        else:
            return HTTP_RESPONSE(statusCode=200).returnCustomMessage(res,{
            "data" : resultData
            })
    return HTTP_RESPONSE(statusCode=500).returnCustomMessage(res,"Something went wrong")