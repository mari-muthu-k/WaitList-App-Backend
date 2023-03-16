import os
from fastapi_mail import FastMail, MessageSchema,ConnectionConfig
from env import appConfig as mailConfig

if mailConfig.CONNECT_MAIL :
  conf = ConnectionConfig(
    MAIL_USERNAME = mailConfig.MAIL_USERNAME,
    MAIL_PASSWORD = mailConfig.MAIL_PASSWORD,
    MAIL_FROM = mailConfig.MAIL_FROM,
    MAIL_PORT = 587, #Encrypted SMTP port
    MAIL_SERVER = mailConfig.MAIL_SERVER,
    MAIL_TLS = True,
    MAIL_SSL = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True)


def returnCouponMail(name,code):
    couponMail = {
    'subject': "Congratulations! You're at the top of the waiting list",
    'message': "<p>Dear {name}</p><br/><p>We're excited to announce that you have reached the top of our waiting list and are now eligible to purchase our new product</p><p>Please use the code {code} at checkout to apply the discount.</p><br/><p>Best regards,</p><br/><p>Cartrabbit</p>"
    }
    return couponMail

async def sendEmail(email,subject,message):
        message = MessageSchema(
        subject=subject,
        recipients=[email],
        html=message,
        subtype="html"
        )
        fm = FastMail(conf)
        await fm.send_message(message)
        return True