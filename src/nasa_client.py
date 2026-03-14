import os
import requests
from dotenv import load_dotenv

# Carrega variáveis de ambiente do .env
load_dotenv()

NASA_API_KEY = os.getenv("NASA_API_KEY", "DEMO_KEY")
APOD_URL = "https://api.nasa.gov/planetary/apod"

class NasaAPIClient:
    """Cliente para a API da NASA."""
    
    def __init__(self, api_key: str = NASA_API_KEY):
        self.api_key = api_key
        
    def get_apod(self) -> dict:
        """
        Busca a Astronomy Picture of the Day (APOD).
        
        Returns:
            dict: Dados da APOD (title, explanation, url, etc).
        """
        params = {"api_key": self.api_key}
        response = requests.get(APOD_URL, params=params)
        response.raise_for_status()
        return response.json()
        
    def search_image(self, query: str) -> dict:
        """
        Busca imagens na biblioteca da NASA (ex: para flashcards temáticos).
        
        Args:
            query: Termo de busca (ex: 'black hole').
            
        Returns:
            dict: O primeiro item de resultado válido ou None.
        """
        search_url = "https://images-api.nasa.gov/search"
        params = {"q": query, "media_type": "image"}
        response = requests.get(search_url, params=params)
        response.raise_for_status()
        
        items = response.json().get("collection", {}).get("items", [])
        if items:
            # Retorna o primeiro resultado relevante simplificado
            data = items[0].get("data", [{}])[0]
            links = items[0].get("links", [{}])
            image_url = links[0].get("href", "") if links else ""
            
            return {
                "title": data.get("title", "Sem título"),
                "explanation": data.get("description", "Sem descrição"),
                "url": image_url
            }
        return {}

# Instância padrão para uso simplificado
nasa_client = NasaAPIClient()
