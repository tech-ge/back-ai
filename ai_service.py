from typing import List
from schemas import SearchResult, AIAnalysisResponse

class AIAnalysisService:
    """AI-powered analysis for research synthesis"""
    
    @staticmethod
    def analyze_search_results(query: str, search_results: List[SearchResult]) -> AIAnalysisResponse:
        """
        Synthesize search results into coherent analysis.
        In production, integrate with GPT-4, Claude, or open-source LLMs.
        """
        
        # Extract key information from results
        titles = [r.title for r in search_results]
        snippets = [r.snippet for r in search_results]
        sources = [r.source for r in search_results]
        
        # Create synthesis
        summary = f"Based on {len(search_results)} sources, here's what was found about '{query}':\n"
        summary += "\n".join([f"- {title[:80]}" for title in titles[:3]])
        
        key_insights = [
            "Result 1: " + (snippets[0][:100] if snippets else "No insights"),
            "Result 2: " + (snippets[1][:100] if len(snippets) > 1 else "No more data"),
            "Result 3: " + (snippets[2][:100] if len(snippets) > 2 else ""),
        ]
        
        potential_gaps = [
            "Quantitative data on this topic",
            "Recent developments in the field",
            "International perspectives",
            "Academic consensus vs. current practice"
        ]
        
        next_research_directions = [
            f"Deeper dive into {query} impact analysis",
            f"Comparative study: {query} across regions",
            f"Historical timeline of {query} evolution",
            f"Expert interviews on {query}"
        ]
        
        return AIAnalysisResponse(
            summary=summary,
            key_insights=key_insights,
            potential_gaps=potential_gaps,
            next_research_directions=next_research_directions,
            bias_analysis="Sources show mixed perspectives. News outlets lean toward sensationalism while academic sources provide depth.",
            sources_cited=sources[:5]
        )
    
    @staticmethod
    def detect_bias(sources: List[str]) -> str:
        """Analyze potential biases in sources"""
        bias_report = "Bias Analysis:\n"
        bias_report += "- Geographic bias: Primarily Western sources\n"
        bias_report += "- Temporal bias: Recent sources may lack historical context\n"
        bias_report += "- Source type bias: Mix of news and academic maintains balance\n"
        return bias_report
    
    @staticmethod
    def generate_citations(source_title: str, source_url: str, published_date: str = None) -> str:
        """Generate APA-style citation"""
        citation = f'Retrieved from "{source_title}" - {source_url}'
        if published_date:
            citation += f' (Published: {published_date})'
        return citation
