import google.generativeai as genai
from core.config import get_settings

settings = get_settings()

class GeminiAssistant:
    def __init__(self):
        """Initialize the Gemini assistant with API key."""
        genai.configure(api_key=settings.GEMINI_API_KEY)
        # Используем стандартную модель gemini-pro
        self.model = genai.GenerativeModel('gemini-2.0-flash')

    async def generate_response(self, prompt: str) -> str:
        """
        Generate a response using Google's Gemini model.
        
        Args:
            prompt (str): The input prompt for the model
            
        Returns:
            str: The generated response
        """
        try:
            response = await self.model.generate_content_async(prompt)
            return response.text
        except Exception as e:
            return f"Error generating Gemini response: {str(e)}" 