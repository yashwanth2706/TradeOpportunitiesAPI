"""
Data collection service for market and news data
"""
import httpx
import logging
from typing import List, Dict

logger = logging.getLogger(__name__)


class DataCollector:
    """
    Collects market/news data for a sector.
    
    This example uses DuckDuckGo HTML scraping as a simple zero-dependency method.
    In production, use a proper news API (e.g., NewsAPI, GNews) with API key.
    """

    SEARCH_URL = "https://duckduckgo.com/html/"

    async def search_news(self, query: str, limit: int = 5) -> List[Dict[str, str]]:
        """
        Search for news articles related to the query
        
        Args:
            query: Search query string
            limit: Maximum number of results to return
            
        Returns:
            List of dictionaries containing title, link, and snippet
        """
        params = {"q": query}
        
        async with httpx.AsyncClient(timeout=20.0) as client:
            try:
                r = await client.post(self.SEARCH_URL, data=params)
            except Exception as e:
                logger.error("Search request failed: %s", e)
                return []
            
            text = r.text
        
        # Parse results - crude parsing: look for "result__snippet" spans
        results: List[Dict[str, str]] = []
        parts = text.split("result__snippet")
        
        for part in parts[1: limit + 1]:
            # Find nearest <a href=
            href_idx = part.find('href="')
            if href_idx != -1:
                href_start = href_idx + 6
                href_end = part.find('"', href_start)
                href = part[href_start:href_end]
            else:
                href = ""
            
            # Extract snippet
            snippet_start = part.find('>')
            snippet_end = part.find('<', snippet_start + 1)
            snippet = part[snippet_start + 1:snippet_end].strip() if snippet_start != -1 and snippet_end != -1 else ""
            
            results.append({
                "title": snippet[:120], 
                "link": href, 
                "snippet": snippet
            })
            
            if len(results) >= limit:
                break
        
        return results
