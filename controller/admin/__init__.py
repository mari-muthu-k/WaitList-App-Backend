from sqlalchemy import select,update,delete,func,exc

from schema.dbSchema import Admin
from helpers import verifyHash

async def adminVerifyLogin(loginData,connectedDB)->(bool,str):
    try:
        stmt = select([Admin.id,Admin.pwd]).\
                    where(Admin.email==email)    
        result = connectedDB.execute(stmt).fetchone()
        
        verifyPass = verifyHash(loginData.password,result['pwd'])
        return verifyPass,None
    
    except Exception as e:
        print("adminVerifyLogin : ",e)
        return False,e