import asyncio

from schema.dbSchema import Customer,Position
from helpers import randomString
from env import appConfig
from sqlalchemy import select,update,delete,func,exc

class CustomerLogics():
    def createUser(userData, connectedDB) -> int:
        try:
            #return -1 if email already registered
            aloop = asyncio.new_event_loop()
            asyncio.set_event_loop(aloop)
            isEmailExist = aloop.run_until_complete(CustomerLogics.isEmailExist(userData.email,connectedDB))
            aloop.close()
            if isEmailExist:
                return -1
        
            # insert customer data
            cRow = Customer(
            name=userData.name,
            email=userData.email,
            ref_link=randomString(50)
            )
            connectedDB.add(cRow)
            connectedDB.flush() # synchronize the session state with the database
            connectedDB.refresh(cRow) # update the cRow
        
            # TODO : update ref_by user's position if referral_link available in data
        
            totalCount,err = PositionLogics.getPositionCount(connectedDB)
            if totalCount < 0 or err != None:
                raise Exception(err)
        
            pRow = Position(
            customer_id=cRow.id, #Last inserted id
            position=totalCount+appConfig.DEFAULT_POSITION_COUNT # To maintain the default 99 position for new positions
            )
        
            connectedDB.add(pRow)
            connectedDB.commit()
            return 1
    
        except Exception as e:
            print("createUser: ",e)
            connectedDB.rollback()
            return 0

    #Get user data by given mail
    async def getUserData(email,connectedDB)->(dict,bool):
        try:
            stmt = select([Customer.name,Customer.coupon,Customer.ref_link,Position.id.label('pos_id'),Position.position,Position.admin_priority]).\
                join(Position).\
                    where(Customer.email==email)
   
            result = connectedDB.execute(stmt).fetchone()
            return result,True
        except Exception as e:
            print("getUserData: ",e)
            return None,False
    
    async def isEmailExist(email,connectedDB)->bool:
        try:
            stmt = select(Customer.id).where(Customer.email == email)
            res  = connectedDB.execute(stmt).fetchone()
            return (res != None)
        except Exception as e:
            print("isEmailExist : ",e)
            return False
        
    async def MarkCustomerAsInActive(Id,connectedDB)->(int,str):
        try:
            stmt = update(Customer).values({Customer.active:False}).where(Customer.id == Id)
            res  = connectedDB.execute(stmt)
            return res.rowcount,None
        except Exception as e:
            print("MarkCustomerAsInActive : ",e)
            return -1,e
    
            

class PositionLogics():
    #Return rows count of position table
    def getPositionCount(connectedDB)->(int,str):
        try:
            count = connectedDB.query(Position.id).count()
            return count,None
        except Exception as e:
            print("getPositionCount: ",e)
            return -1,e

    async def deletePositionByCustomerId(cusID,connectedDB)->(int,str):
        try:
            stmt = delete(Position).where(Position.customer_id == cusID)
            res = connectedDB.execute(stmt)
            return res.rowcount,None
        except Exception as e:
            print("deletePositionByCustomerId : ",e)
            return -1,e