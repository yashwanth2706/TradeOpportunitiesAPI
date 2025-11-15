"""
LLM client service for AI-powered analysis
"""
import os
import logging
import asyncio
from typing import List, Dict, Optional
from datetime import datetime
from google import genai

from app.config import settings

logger = logging.getLogger(__name__)


def save_analysis_report(markdown_text: str, filename: Optional[str] = None) -> str:
    """
    Save analysis report as a markdown file
    
    Args:
        markdown_text: The markdown content to write
        filename: Optional filename. If not provided, uses a timestamp
        
    Returns:
        Path to the saved markdown file
    """
    # Clean up markdown text
    formatted_text = markdown_text.strip()

    # Generate filename with incrementing number if file exists
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"analysis_report_{timestamp}.md"
    
    # Check if file exists and increment number if needed
    reports_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "reports")
    os.makedirs(reports_dir, exist_ok=True)
    
    base_path = os.path.join(reports_dir, filename)
    if os.path.exists(base_path):
        # Split filename into name and extension
        name_parts = filename.rsplit('.', 1)
        base_name = name_parts[0]
        extension = name_parts[1] if len(name_parts) > 1 else ''
        
        # Extract the part before _by_ to insert counter
        if '_by_' in base_name:
            sector_part, model_part = base_name.rsplit('_by_', 1)
            counter = 2
            while True:
                new_filename = f"{sector_part}_({counter})_by_{model_part}.{extension}"
                file_path = os.path.join(reports_dir, new_filename)
                if not os.path.exists(file_path):
                    filename = new_filename
                    break
                counter += 1
        else:
            # Fallback: just append counter before extension
            counter = 2
            while True:
                new_filename = f"{base_name}_({counter}).{extension}"
                file_path = os.path.join(reports_dir, new_filename)
                if not os.path.exists(file_path):
                    filename = new_filename
                    break
                counter += 1

    # Write to reports directory
    reports_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "reports")
    os.makedirs(reports_dir, exist_ok=True)
    file_path = os.path.join(reports_dir, filename)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(formatted_text)

    logger.info(f"Analysis report saved to {file_path}")
    return file_path


class LLMClient:
    """
    LLM client for generating market analysis reports
    """
    
    def __init__(self):
        self.api_key = settings.LLM_API_KEY
        self.model_name = os.getenv('LLM_MODEL_NAME', 'gemini-2.0-flash-exp').strip().strip('"')
    
    async def analyze(self, sector: str, snippets: List[Dict[str, str]]) -> str:
        """
        Analyze market data and generate a report
        
        Args:
            sector: The sector to analyze
            snippets: List of data snippets collected about the sector
            
        Returns:
            Markdown formatted analysis report
        """
        if not self.api_key:
            logger.warning("GEMINI_API_KEY is not configured")
            return "Unable to perform analysis. API key is not configured."
        
        if not self.model_name:
            logger.warning("LLM_MODEL_NAME is not configured")
            return "Unable to perform analysis. Model name is not configured."
        
        # Build prompt and call Gemini API
        prompt = self._build_prompt(sector, snippets)
        
        try:
            result = await self._call_gemini(prompt)
            save_analysis_report(result, f"{sector}_sector_report_by_{self.model_name}.md")
            return result
        except Exception as e:
            logger.error("Gemini call failed: %s", e, exc_info=True)
            return f"Unable to perform analysis. Error: {str(e)}"
    
    def _build_prompt(self, sector: str, snippets: List[Dict[str, str]]) -> str:
        """Build the analysis prompt for the LLM"""
        prompt = (
            f"You are an expert market analyst. Produce a structured Markdown report "
            f"about current trade opportunities in the '{sector}' sector in India. "
            f"Use the following collected information as input and do not hallucinate facts.\n\n"
        )
        
        for i, sn in enumerate(snippets, 1):
            prompt += (
                f"Source {i}: {sn.get('title', '')}. {sn.get('snippet', '')}. "
                f"Link: {sn.get('link', '')}\n\n"
            )
        
        prompt += (
            "Produce sections: Summary, Key Drivers, Top Opportunities, Risks, "
            "Suggested Trades (long/short ideas), Data Sources."
        )
        
        return prompt
    
    async def _call_gemini(self, prompt: str) -> str:
        """Call the Gemini API asynchronously"""
        
        def sync_generate():
            client = genai.Client(api_key=self.api_key)
            response = client.models.generate_content(
                model=self.model_name,
                contents=prompt,
            )
            return response.text
        
        # Run the sync function in a thread to avoid blocking the event loop
        loop = asyncio.get_event_loop()
        text = await loop.run_in_executor(None, sync_generate)
        
        if not text:
            raise RuntimeError("No content returned from Gemini API")
        
        return text
