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
            return HTTP_RESPONSE(statusCode=401).returnErrorMessage(res,"wrong email or password")
    return HTTP_RESPONSE(statusCode=200).returnMessage(res) if status else HTTP_RESPONSE(statusCode=500).returnErrorMessage(res,"something went wrong, please try again")

@router.post("/listAll")
async def listAll(req:Request,res:Response,connectedDB:Session = Depends(get_db)):
    posList = await CustomerLogics.getAllUsers(connectedDB)
    
    if posList != None:
        nPosList = []
        #Remove Position collision using Linear probing
        positions = {}
        #Recursive function to find the available slot
        def findSlot(d,val):
            if val not in d:
                d[val] = 1
                return val
            else:
                nval = val+d[val]
                d[val] += 1
                return findSlot(d,nval)

        for i in posList:
            nI = findSlot(positions,i['position'])
            rowDict = dict(i._mapping)
            rowDict['position'] = nI
            nPosList.append(rowDict)
            
    return HTTP_RESPONSE(statusCode=200).returnCustomMessage(res,{
        "data":nPosList
    })

@router.post("/updateUser")
async def updateUser(req:Request,res:Response,reqData:formSchema.UpdateUser,connectedDB:Session = Depends(get_db)):
    reqData = reqData.dict()
    rowAffected = await CustomerLogics.updateUserData(reqData, connectedDB)

    if rowAffected == 0 :
        return HTTP_RESPONSE(statusCode=404).returnErrorMessage(res,"id doesn't exist")
    elif rowAffected == -1:
        return HTTP_RESPONSE(statusCode=409).returnErrorMessage(res, "email already exist")
    
    return HTTP_RESPONSE(statusCode=200).returnMessage(res)

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