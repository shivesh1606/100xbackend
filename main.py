from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db import connect_to_mongo, close_mongo_connection, db
from projects import router as projects_router
from users import router as users_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # adjust later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    await connect_to_mongo()

@app.on_event("shutdown")
async def shutdown():
    await close_mongo_connection()

# Routers
app.include_router(projects_router, prefix="/api/projects", tags=["projects"])
app.include_router(users_router, prefix="/api", tags=["auth"])
