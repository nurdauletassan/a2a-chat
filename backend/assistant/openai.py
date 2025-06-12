from openai import AsyncOpenAI
from core.config import get_settings

settings = get_settings()

class OpenAIAssistant:
    def __init__(self):
        """Initialize the OpenAI assistant with API key."""
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

    async def generate_response(self, prompt: str) -> str:
        """
        Generate a response using OpenAI's GPT model.
        
        Args:
            prompt (str): The input prompt for the model
            
        Returns:
            str: The generated response
        """
        try:
            response = await self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that provides detailed and accurate information."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error generating OpenAI response: {str(e)}" 