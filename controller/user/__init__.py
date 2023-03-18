from schema.dbSchema import Customer,Position
from helpers import randomString
from env import appConfig
from sqlalchemy import select,update,delete,func,exc

def createUser(userData, connectedDB) -> bool:
    try:
        cRow = Customer(
            name=userData['name'],
            email=userData['email'],
            ref_link=randomString(50)
        )
        connectedDB.add(cRow)
        connectedDB.flush() # synchronize the session state with the database
        connectedDB.refresh(cRow) # update the cRow
        
        # TODO : update ref_by user's position if referral_link available in data
        
        totalCount,err = getPositionCount(connectedDB)
        if totalCount < 0 or err != None:
            raise Exception(err)
        
        pRow = Position(
            customer_id=cRow.id, #Last inserted id
            position=totalCount+appConfig.DEFAULT_POSITION_COUNT # To maintain the default 99 position for new positions
        )
        
        connectedDB.add(pRow)
        connectedDB.commit()
        return True
    
    except Exception as e:
        print("createUser: ",e)
        connectedDB.rollback()
        return False

#Get user data by given mail
async def getUserData(email,connectedDB)->(dict,bool):
    try:
        stmt = select([Customer.name,Customer.coupon,Customer.ref_link,Position.id.label('pos_id'),Position.position,Position.admin_priority]).\
                join(Position).\
                    where(Customer.email==email)
                        # order_by(Position.position.asc(),Position.admin_priority.asc(),Position.id.asc())
        # TODO : filter unqiue position      
        result = connectedDB.execute(stmt).fetchone()
        return result,True
    except Exception as e:
        print("getUserData: ",e)
        return None,False
    
#Return rows count of position table
def getPositionCount(connectedDB)->(int,str):
    try:
        count = connectedDB.query(Position.id).count()
        return count,None
    except Exception as e:
        print("getPositionCount: ",e)
        return -1,e