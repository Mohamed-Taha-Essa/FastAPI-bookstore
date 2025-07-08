from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from core.database import engine, Base
from api import bookapi

import models

#intialize app
app = FastAPI()

#mount static
app.mount("/static", StaticFiles(directory="static"), name="static")

# add router
app.include_router(bookapi.router)

# create database tables (all tables in base)
Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app",reload=True)
    