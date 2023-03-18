import os
import json
from fastapi import APIRouter,Request,Response,Depends,Path
from schema.formSchema import CreateUser as CreateUserSchema,MyStatus as MyStatusSchema
from controller.user import createUser,getUserData
from controller.http import HTTP_RESPONSE
from db import get_db
from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/subscribe")
def subscribe(req:Request,res:Response,userData:CreateUserSchema,connectedDB:Session=Depends(get_db)): # have to be synchronous as move up is synchronous
    userData = userData.dict() # Convert class obj to dict
    status = createUser(userData,connectedDB)
    return HTTP_RESPONSE(statusCode=200).returnMessage(res) if status else HTTP_RESPONSE(statusCode=500).returnCustomMessage(res,"Something went wrong, please try again")

@router.post("/mystatus")
async def myStatus(req:Request,res:Response,reqData:MyStatusSchema,connectedDB:Session=Depends(get_db)):
    resultData,status = await getUserData(reqData.email,connectedDB)
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