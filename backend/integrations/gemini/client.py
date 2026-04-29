import os
import google.generativeai as genai

class GeminiClient:
    """Sadece ham Gemini API istemcisi. İş mantığı YOK."""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if self.api_key:
            genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-pro')
    
    def generate(self, prompt: str, temperature: float = 0.7) -> str:
        """Prompt gönder, ham yanıtı döndür."""
        if not self.api_key:
            return "Simulated Gemini Response (API Key not configured)"
        response = self.model.generate_content(
            prompt,
            generation_config={"temperature": temperature}
        )
        return response.text
    
    def generate_json(self, prompt: str) -> dict:
        """JSON formatında yanıt iste."""
        if not self.api_key:
            return {"simulated": True, "message": "API Key not configured"}
        response = self.model.generate_content(prompt)
        import json
        try:
            return json.loads(response.text)
        except Exception:
            return {"raw_text": response.text}
