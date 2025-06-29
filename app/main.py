#main app
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from app.routes import upload
from app.routes import upload, api
from app.middleware.logger import APILoggerMiddleware
from app.routes import ask
from app.routes import upload, api




UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)





app = FastAPI()
app.include_router(api.router, prefix="/api/secure-data")

app.include_router(ask.router)
app.add_middleware(SessionMiddleware, secret_key="upload_to_sqlite")


app.add_middleware(APILoggerMiddleware)

# Optional: Add CORS if needed
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(upload.router)
app.include_router(api.router)

