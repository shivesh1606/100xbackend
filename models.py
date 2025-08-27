from pydantic import BaseModel
from typing import List, Optional

class User(BaseModel):
    username: str
    password: str  # hashed in DB

class ProjectFile(BaseModel):
    name: str
    url: str
    type: str

class Project(BaseModel):
    id: Optional[str]
    title: str
    description: str
    mediumUrl: Optional[str]
    executiveSummary: Optional[str]
    liveDemoUrl: Optional[str]
    files: List[ProjectFile]
    author: Optional[str]
