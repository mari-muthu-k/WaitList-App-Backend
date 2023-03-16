import os
import json
from fastapi import APIRouter,Request,Response,Depends,Path

router = APIRouter()

@router.post("/login")
async def login(req:Request,res:Response):
    return True

@router.get("/listAll")
async def listAll(req:Request,res:Response):
    return True

@router.get("/getUser")
async def getUser(req:Request,res:Response):
    return True

@router.post("/updateUser")
async def updateUser(req:Request,res:Response):
    return True

@router.delete("/deleteUser")
async def deleteUser(req:Request,res:Response):
    return True