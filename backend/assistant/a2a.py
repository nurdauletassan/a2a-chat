from assistant.gemini import GeminiAssistant
from assistant.openai import OpenAIAssistant

class A2AInteraction:
    def __init__(self):
        """Initialize both assistants for A2A interaction."""
        self.gemini = GeminiAssistant()
        self.openai = OpenAIAssistant()

    async def interact(self, prompt: str) -> str:
        """
        Perform A2A interaction by combining responses from both assistants.
        
        Args:
            prompt (str): The user's input prompt
            
        Returns:
            str: The combined response from both assistants
        """
        try:
            # Get initial response from Gemini
            gemini_response = await self.gemini.generate_response(prompt)
            
            # Create a prompt for OpenAI to combine and enhance Gemini's response
            refinement_prompt = f"""
            Please combine and enhance the following response about: {prompt}
            
            Initial response:
            {gemini_response}
            
            Please create a single, comprehensive response that:
            1. Incorporates the key points from the initial response
            2. Adds relevant details and examples
            3. Maintains a natural flow and coherence
            4. Presents the information in a clear, structured way
            
            Provide the final combined response without any additional commentary or labels.
            """
            
            # Get combined response from OpenAI
            combined_response = await self.openai.generate_response(refinement_prompt)
            
            # Store both responses for reference
            self.last_gemini_response = gemini_response
            self.last_openai_response = combined_response
            
            return combined_response
            
        except Exception as e:
            return f"Error in A2A interaction: {str(e)}" 