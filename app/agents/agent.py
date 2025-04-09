import os
from typing import Optional

from google import genai


class Agent:
    def __init__(self) -> None:
        """Initialize the LLM Agent with the Gemini API client."""
        self.client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

    def generate_response(self, message: str) -> Optional[str]:
        """Generate a response using the LLM API.

        Args:
            message: The input message from the user.

        Returns:
            The generated response from the LLM.
        """
        response = self.client.models.generate_content(
            model="gemini-2.0-flash-001", contents=message  # Specify the model to use
        )
        if response and hasattr(response, "text"):
            return str(response.text)
        return None
