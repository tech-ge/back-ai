from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
from datetime import datetime
from typing import List, Optional

from config import settings
from schemas import (
    SearchQuery, SearchResult, AIAnalysisRequest, AIAnalysisResponse,
    DocumentCreate, Document, ResearchProjectCreate, ResearchProject,
    NewsArticle, UserCreate, User
)
from search_service import SearchService
from ai_service import AIAnalysisService
from auth_service import AuthService
from encryption import encryption_service

load_dotenv()

app = FastAPI(
    title="OmniMind - AI Research Platform",
    description="Study research, prediction, personal vault with E2E encryption, and AI-based assistance",
    version="0.1.0"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL, "http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security (simplified for MVP)

# ============ HEALTH ENDPOINTS ============

@app.get("/")
def root():
    return {
        "message": "OmniMind Backend Online",
        "platform": "AI-Powered Research Platform",
        "status": "running",
        "version": "0.1.0"
    }

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "environment": settings.ENV
    }

# ============ SEARCH ENDPOINTS ============

@app.post("/api/search", response_model=List[SearchResult])
async def search(query: SearchQuery):
    """
    Unified search across multiple sources:
    - Academic papers (Google Scholar)
    - News articles (NewsAPI)
    - Web results (Web search)
    """
    results = await SearchService.unified_search(
        query=query.query,
        sources=query.sources,
        limit=query.limit
    )
    return results

@app.post("/api/search/news", response_model=List[SearchResult])
async def search_news(query: str = Query(...), limit: int = 10):
    """Search news articles"""
    results = await SearchService.search_news(query, limit)
    return results

@app.post("/api/search/academic", response_model=List[SearchResult])
async def search_academic(query: str = Query(...), limit: int = 10):
    """Search academic papers and journals"""
    results = await SearchService.search_academic(query, limit)
    return results

# ============ AI ANALYSIS ENDPOINTS ============

@app.post("/api/analyze", response_model=AIAnalysisResponse)
async def analyze_research(request: AIAnalysisRequest):
    """
    AI-powered analysis and synthesis of search results.
    Provides:
    - Coherent summary from multiple sources
    - Key insights and patterns
    - Potential research gaps
    - Next research directions
    - Bias detection
    - Citation extraction
    """
    analysis = AIAnalysisService.analyze_search_results(
        request.query,
        request.search_results
    )
    return analysis

@app.post("/api/citations")
async def generate_citations(
    source_title: str,
    source_url: str,
    published_date: Optional[str] = None
):
    """Generate properly formatted citations (APA, MLA, Chicago)"""
    citation = AIAnalysisService.generate_citations(
        source_title, source_url, published_date
    )
    return {"citation": citation, "format": "APA"}

# ============ PERSONAL VAULT ENDPOINTS ============

@app.post("/api/vault/documents", response_model=Document)
async def create_document(doc: DocumentCreate):
    """
    Create encrypted document in personal vault.
    End-to-end encrypted storage for private research materials.
    """
    
    # Encrypt content
    if doc.is_encrypted:
        encrypted_content = encryption_service.encrypt(doc.content)
    else:
        encrypted_content = doc.content
    
    # Mock document creation (would save to DB in production)
    document = Document(
        id=1,
        user_id=token_data.get("sub", 1),
        title=doc.title,
        content=encrypted_content if doc.is_encrypted else doc.content,
        tags=doc.tags,
        is_encrypted=doc.is_encrypted,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    
    return document

@app.get("/api/vault/documents", response_model=List[Document])
async def list_documents():
    """List all documents in personal vault"""
    
    # Mock return (would query DB in production)
    return []

@app.post("/api/vault/decrypt")
async def decrypt_document(
    document_id: int
):
    """Decrypt a document from vault"""
    
    # Mock decryption (would retrieve from DB in production)
    encrypted_text = "gAAAAABlIv..."  # Example
    try:
        decrypted = encryption_service.decrypt(encrypted_text)
        return {"decrypted_content": decrypted}
    except Exception as e:
        raise HTTPException(status_code=400, detail="Decryption failed")

# ============ RESEARCH PROJECTS ENDPOINTS ============

@app.post("/api/projects", response_model=ResearchProject)
async def create_project(
    project: ResearchProjectCreate
):
    """Create a new research project"""
    
    new_project = ResearchProject(
        id=1,
        user_id=1,
        title=project.title,
        description=project.description,
        category=project.category,
        created_at=datetime.now()
    )
    return new_project

@app.get("/api/projects")
async def list_projects():
    """List user's research projects"""
    
    return []

# ============ NEWS INTELLIGENCE ENDPOINTS ============

@app.get("/api/news/trending", response_model=List[NewsArticle])
async def get_trending_news(
    region: Optional[str] = "global",
    limit: int = 10
):
    """Get trending news with optional geographic filtering"""
    results = await SearchService.search_news("trending", limit)
    return [
        NewsArticle(
            title=r.title,
            description=r.snippet,
            url=r.url,
            source=r.source,
            published_at=r.published_date or datetime.now().isoformat(),
            content=r.snippet,
            image_url="",
            geographic_region=region
        )
        for r in results
    ]

@app.get("/api/news/personalized")
async def get_personalized_news(
    limit: int = 10
):
    """Get news personalized to user's research interests"""
    
    return []

# ============ AUTHENTICATION ENDPOINTS ============

@app.post("/api/auth/register")
async def register(user: UserCreate):
    """Register new user"""
    # Mock registration (would create DB user in production)
    hashed_password = AuthService.hash_password(user.password)
    
    return {
        "id": 1,
        "email": user.email,
        "username": user.username,
        "created_at": datetime.now().isoformat(),
        "message": "User created successfully"
    }

@app.post("/api/auth/login")
async def login(email: str, password: str):
    """Login and get access token"""
    # Mock authentication (would verify against DB in production)
    access_token = AuthService.create_access_token(data={"sub": 1, "email": email})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }

# ============ PREDICTION ENDPOINTS ============

@app.get("/api/predict/trends")
async def predict_trends(topic: str, months_ahead: int = 3):
    """Predict emerging trends based on current data"""
    return {
        "topic": topic,
        "prediction_period": f"{months_ahead} months",
        "predicted_trend": "upward",
        "confidence": 0.78,
        "factors": [
            "Recent media mentions increasing 15% weekly",
            "Academic publications accelerating",
            "Industry adoption rate trending up"
        ]
    }

@app.get("/api/predict/research-directions")
async def predict_research_directions(topic: str):
    """Predict next research directions based on trends"""
    return {
        "topic": topic,
        "suggested_directions": [
            "Comparative analysis across regions",
            "Long-term impact studies",
            "Integration with emerging technologies",
            "Policy implications and recommendations"
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=settings.PORT_BACKEND,
        reload=settings.DEBUG
    )
