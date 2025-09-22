from fastapi import APIRouter, Depends, HTTPException
from db import db
from users import get_current_user
from bson import ObjectId

router = APIRouter()

@router.get("/", dependencies=[Depends(get_current_user)])
async def list_projects(user=Depends(get_current_user)):
    # Show all public projects and user's own private projects
    projects = await db.projects.find({
        "$or": [
            {"visibility": "public"},
            {"author": user["username"]}
        ]
    }).to_list(100)
    for project in projects:
        if "_id" in project:
            project["id"] = str(project["_id"])
            del project["_id"]
    return projects

@router.get("/public")
async def list_public_projects():
    projects = await db.projects.find({"visibility": "public"}).to_list(100)
    for project in projects:
        if "_id" in project:
            project["id"] = str(project["_id"])
            del project["_id"]
    return projects

@router.post("/", dependencies=[Depends(get_current_user)])
async def add_project(project: dict, user=Depends(get_current_user)):
    project["author"] = user["username"]
    project["visibility"] = project.get("visibility", "public")
    result = await db.projects.insert_one(project)
    return {"id": str(result.inserted_id)}

@router.put("/{project_id}", dependencies=[Depends(get_current_user)])
async def update_project(project_id: str, project: dict, user=Depends(get_current_user)):
    existing = await db.projects.find_one({"_id": ObjectId(project_id)})
    if not existing:
        raise HTTPException(status_code=404, detail="Project not found")
    if existing.get("author") != user["username"]:
        raise HTTPException(status_code=403, detail="Not allowed to update this project")
    project["author"] = user["username"]
    project["visibility"] = project.get("visibility", "public")
    await db.projects.update_one({"_id": ObjectId(project_id)}, {"$set": project})
    return {"id": project_id}

@router.get("/{project_id}")
async def get_project(project_id: str, user=Depends(get_current_user)):
    project = await db.projects.find_one({"_id": ObjectId(project_id)})
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if project.get("visibility") == "private" and (not user or project.get("author") != user["username"]):
        raise HTTPException(status_code=403, detail="Not allowed to view this project")
    project["id"] = str(project["_id"])
    del project["_id"]
    return project

# ...existing code...
