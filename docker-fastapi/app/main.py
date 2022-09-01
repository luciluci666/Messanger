from email.mime import application
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.handlers import router

def get_application() -> FastAPI:
    application = FastAPI()

    # test parameters
    application.add_middleware(CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


    application.include_router(router=router)
    return application

app = get_application()