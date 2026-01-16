from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# User Models
class UserBase(BaseModel):
    email: str
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Document Models
class DocumentCreate(BaseModel):
    title: str
    content: str
    tags: Optional[List[str]] = []
    is_encrypted: bool = True

class Document(DocumentCreate):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Search Models
class SearchQuery(BaseModel):
    query: str
    sources: Optional[List[str]] = ["academic", "news", "web"]  # academic, news, web
    limit: Optional[int] = 10

class SearchResult(BaseModel):
    title: str
    url: str
    source: str
    snippet: str
    relevance_score: float
    published_date: Optional[str]
    author: Optional[str]
    citations: Optional[int]

# Research Project Models
class ResearchProjectCreate(BaseModel):
    title: str
    description: str
    category: Optional[str] = "General"

class ResearchProject(ResearchProjectCreate):
    id: int
    user_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# News Models
class NewsArticle(BaseModel):
    title: str
    description: str
    url: str
    image_url: Optional[str]
    source: str
    published_at: str
    content: str
    sentiment: Optional[str]  # positive, neutral, negative
    geographic_region: Optional[str]

# AI Analysis Models
class AIAnalysisRequest(BaseModel):
    query: str
    search_results: List[SearchResult]
    project_id: Optional[int] = None

class AIAnalysisResponse(BaseModel):
    summary: str
    key_insights: List[str]
    potential_gaps: List[str]
    next_research_directions: List[str]
    bias_analysis: Optional[str]
    sources_cited: List[str]
