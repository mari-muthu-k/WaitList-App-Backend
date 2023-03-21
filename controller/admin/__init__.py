from fastapi import Request,Response
from sqlalchemy import select,update,delete,func,exc


from schema.dbSchema import Admin
from helpers import verifyHash,hashThis
from controller.http import http_codes
from exception import customException

async def adminVerifyLogin(loginData,connectedDB)->(bool,str):
    try:
        stmt = select([Admin.id,Admin.pwd]).\
                    where(Admin.email==loginData.email)    
        result = connectedDB.execute(stmt).fetchone()
        if result == None:
            return False,None
        
        verifyPass = verifyHash(loginData.password,result['pwd'])
        return verifyPass,None
    
    except Exception as e:
        print("adminVerifyLogin : ",e)
        return False,e

def AuthCheck(request:Request,response:Response):
    if request.session == None or request.session.get('loggedIn') == None or not request.session['loggedIn']:
         raise customException(status_code=401, message=http_codes[401])
    return request

async def InsertNewUser(adminData,connectedDB)->int:
    try:
        if await isEmailExist(adminData.email, connectedDB):
            return -1
        
        row = Admin(
            name = adminData.name,
            email = adminData.email,
            pwd   = hashThis(adminData.password)
        )
        connectedDB.add(row)
        connectedDB.commit()
        return 1
    except Exception as e:
        print("insertNewUser : ",e)
        return 0

async def isEmailExist(email,connectedDB)->bool:
    try:
        row = select([Admin.id]).where(Admin.email == email)
        res = connectedDB.execute(row).fetchone()
        return (res != None)
    except Exception as e:
        print("isEmailExist : ",e)
        return False