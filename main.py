from env import appConfig as config
from fastapi import FastAPI,Request,Response,Depends
from fastapi.responses import JSONResponse

from schema.dbSchema import Base
from db import engine

from fastapi.middleware.cors import CORSMiddleware
from starlette_session import SessionMiddleware

from controller import http,admin as adminController
from router import user,admin,authAdmin
from exception import customException

app = FastAPI() if config.LIST_ENDPOINTS else FastAPI(openapi_url="")

#Create DB schema
Base.metadata.create_all(bind=engine)

#Session config
app.add_middleware(
    SessionMiddleware,
    secret_key = config.COOKIE_SECRET_KEY,
    cookie_name = config.COOKIE_NAME,
    max_age = config.COOKIE_MAX_AGE,
    same_site = config.COOKIE_SAME_SITE,
    domain = config.COOKIE_DOMAIN
    )

#CORS config
app.add_middleware( 
    CORSMiddleware, 
    allow_origins=config.AUTH_DOMAINS, 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"]
    )

app.include_router(user.router,prefix="/api")
app.include_router(admin.router,prefix="/api/admin")
app.include_router(authAdmin.router,prefix="/api/admin",dependencies=[Depends(adminController.AuthCheck)])

@app.exception_handler(customException)
async def exception_handler(request: Request, exc: customException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message":exc.message},
    )