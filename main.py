from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.projects import router as projects_router
from routes.users import router as users_router
from db import db

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # or ["*"] for all origins (not recommended for production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(projects_router, prefix="/api/projects", tags=["projects"])
app.include_router(users_router, prefix="/api", tags=["auth"])

@app.on_event("startup")
async def startup_db_check():
    try:
        # The 'ping' command checks MongoDB connection
        await db.command("ping")
        print("✅ MongoDB connection successful.")
    except Exception as e:
        print("❌ MongoDB connection failed:", e)
