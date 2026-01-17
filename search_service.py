import httpx
from typing import List
from schemas import SearchResult
from config import settings
import json
 
class SearchService:
    """Multi-source search aggregator for OmniMind"""
    
    @staticmethod
    async def search_news(query: str, limit: int = 5) -> List[SearchResult]:
        """Search news using NewsAPI"""
        if not settings.NEWSAPI_KEY:
            return []
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    "https://newsapi.org/v2/everything",
                    params={
                        "q": query,
                        "sortBy": "relevancy",
                        "language": "en",
                        "pageSize": limit,
                        "apiKey": settings.NEWSAPI_KEY
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    results = []
                    for article in data.get("articles", []):
                        results.append(SearchResult(
                            title=article.get("title", ""),
                            url=article.get("url", ""),
                            source=article.get("source", {}).get("name", "News"),
                            snippet=article.get("description", ""),
                            relevance_score=0.8,
                            published_date=article.get("publishedAt"),
                            author=article.get("author"),
                            citations=None
                        ))
                    return results
        except Exception as e:
            print(f"News search error: {e}")
        
        return []
    
    @staticmethod
    async def search_web(query: str, limit: int = 5) -> List[SearchResult]:
        """Placeholder for web search - integrate with Bing/Google API"""
        # This would integrate with a search engine API
        return []
    
    @staticmethod
    async def search_academic(query: str, limit: int = 5) -> List[SearchResult]:
        """Placeholder for academic search - integrate with Google Scholar API"""
        # This would integrate with academic paper databases
        return []
    
    @staticmethod
    async def unified_search(query: str, sources: List[str] = None, limit: int = 10) -> List[SearchResult]:
        """Perform unified search across multiple sources"""
        if sources is None:
            sources = ["news", "web", "academic"]
        
        all_results = []
        
        if "news" in sources:
            news_results = await SearchService.search_news(query, limit=limit)
            all_results.extend(news_results)
        
        if "web" in sources:
            web_results = await SearchService.search_web(query, limit=limit)
            all_results.extend(web_results)
        
        if "academic" in sources:
            academic_results = await SearchService.search_academic(query, limit=limit)
            all_results.extend(academic_results)
        
        # Sort by relevance score
        all_results.sort(key=lambda x: x.relevance_score, reverse=True)
        return all_results[:limit]
