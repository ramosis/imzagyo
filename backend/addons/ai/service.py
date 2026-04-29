import os
from typing import Optional
from backend.integrations.gemini.client import GeminiClient

class AIService:
    @staticmethod
    def get_response(message: str) -> str:
        client = GeminiClient()
        if not client.api_key:
            return "AI API key missing. Please configure backend environment."
        return client.generate(message)

    @staticmethod
    def translate_text(text: str, target_lang: str) -> str:
        client = GeminiClient()
        prompt = f"Translate the following text to {target_lang}: {text}"
        return client.generate(prompt)

    @staticmethod
    def summarize_property(property_data: dict) -> str:
        client = GeminiClient()
        prompt = f"""
        Bu gayrimenkul için profesyonel özet çıkar:
        Başlık: {property_data.get('title')}
        Lokasyon: {property_data.get('location')}
        Fiyat: {property_data.get('price')}
        Özellikler: {property_data.get('features')}
        """
        return client.generate(prompt)
    
    @staticmethod
    def generate_opportunity_route(criteria: dict) -> dict:
        client = GeminiClient()
        prompt = f"Return a JSON opportunity route for these criteria: {criteria}"
        return client.generate_json(prompt)
