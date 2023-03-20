import asyncio

from schema.dbSchema import Customer,Position,Referral
from helpers import randomString
from env import appConfig
from sqlalchemy import select,update,delete,func,exc
from controller import email
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
        
            #Run referral logics
            if userData.referral_link :
                nloop = asyncio.new_event_loop()
                asyncio.set_event_loop(nloop)
                nloop.run_until_complete(ReferralLogics.rewardReferrer(userData.referral_link,cRow.id,connectedDB))
                nloop.close()
        
            totalCount,err = PositionLogics.getPositionCount(connectedDB)
            if totalCount < 0 or err != None:
                raise Exception(err)
        
            pRow = Position(
            customer_id=cRow.id, #Last inserted id
            position=totalCount+appConfig.DEFAULT_POSITION_COUNT, # To maintain the default 99 position for new positions
            admin_priority = userData.admin_created
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
    
    async def getCusByRefLink(refLink,connectedDB)->dict:
        try:
            stmt = select([Customer.id,Customer.name,Customer.email,Position.position,Position.ref_score]).\
                join(Position).\
                    where(Customer.ref_link == refLink)
            res  = connectedDB.execute(stmt).fetchone()
            return res
        except Exception as e:
            print("getCusIdByRefLink : ",e)
            return None    
          
    async def updateCouponCode(code,cusID,connectedDB)->bool:
        try:
            stmt = update(Customer).values({Customer.coupon:code}).where(Customer.id == cusID)
            res = connectedDB.execute(stmt)
            return True
        
        except Exception as e:
            print("updateCouponCode : ",e)
            return False
        
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
    
    async def rewardPositionForReferral(cusID,currPos,ref_score,connectedDB)->(bool,str):
        try:
            stmt = update(Position).values({Position.position:currPos-1,Position.ref_score:ref_score+1}).where(Position.customer_id==cusID)
            res = connectedDB.execute(stmt)
            return True,None
        
        except Exception as e:
            print("rewardPositionForReferral : ",e)
            return False,e


class ReferralLogics():
    async def insertReferral(refID,refById,connectedDB)->bool:
         try:
             ref = Referral(
                 ref = refID,
                 ref_by = refById
             )
             connectedDB.add(ref)
             connectedDB.commit()
             return True
         except Exception as e:
             print("insertReferral : ",e)
             return False
         
    async def rewardReferrer(refLink,refID,connectedDB)->bool:
        try:
            refCus = await CustomerLogics.getCusByRefLink(refLink,connectedDB)
            if refCus != None :
                # insert the relation
                await ReferralLogics.insertReferral(refID, refCus['id'], connectedDB)
                
                if refCus['position'] == 2 : # will be 1 after the reward
                    coupon = randomString(50)
                    #update the coupon code in customer table
                    if not await CustomerLogics.updateCouponCode(coupon,refCus['id'] ,connectedDB):
                        return False 
                    await PositionLogics.deletePositionByCustomerId(refCus['id'], connectedDB) # no longer needed for position calculation
                    await ReferralLogics.sendCoupon(refCus['name'],refCus['email'], coupon)
                else:
                    await PositionLogics.rewardPositionForReferral(refCus['id'],refCus['position'],refCus['ref_score'],connectedDB)
            return True
        except Exception as e:
            print("rewardReferrer : ",e)
            return False 
    
    async def sendCoupon(name,email,code)->bool:
        try : 
            if appConfig.CONNECT_MAIL:
                content = email.returnCouponMail(name, code)
                await email.sendEmail(email, content['subject'], content['message'])
                return True
            print('email connection not enabled')
            print('email : ',email,' name : ',name, ' coupon : ',code)
            return False
        except Exception as e:
            print("sendCoupon : ",e)
            return False