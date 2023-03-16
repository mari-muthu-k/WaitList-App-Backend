import os
import json
from fastapi import APIRouter,Request,Response,Depends,Path

router = APIRouter()

@router.post("/subscribe")
def subscribe(req:Request,res:Response): # have to be synchronous as move up is synchronous
    return True

@router.get("/mystatus")
async def myStatus(req:Request,res:Response):
    return True