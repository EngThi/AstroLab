import os
import requests
from dotenv import load_dotenv

# Load environment variables from the current working directory's .env file
load_dotenv(os.path.join(os.getcwd(), '.env'))

NASA_API_KEY = os.getenv("NASA_API_KEY", "DEMO_KEY")
APOD_URL = "https://api.nasa.gov/planetary/apod"

class NasaAPIClient:
    """Client for the NASA API."""
    
    def __init__(self, api_key: str = None):
        # We evaluate the env var here again just in case it was loaded later
        self.api_key = api_key or os.getenv("NASA_API_KEY", "DEMO_KEY")
        
    def get_apod(self) -> dict:
        """
        Fetches the Astronomy Picture of the Day (APOD).
        
        Returns:
            dict: APOD data (title, explanation, url, etc).
        """
        try:
            params = {"api_key": self.api_key}
            response = requests.get(APOD_URL, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception:
            return self._fallback_apod()
            
    def _fallback_apod(self) -> dict:
        return {
            "title": "The Carina Nebula (Offline Cache)",
            "explanation": "The NASA API is currently unreachable (503 Service Unavailable). This is a cached entry. The Carina Nebula is a large, complex area of bright and dark nebulosity in the constellation Carina, located in the Carina-Sagittarius Arm of the Milky Way galaxy. It is one of the largest diffuse nebulae in our skies.",
            "url": "https://www.nasa.gov/wp-content/uploads/2023/03/359218main_hs-2009-25-e-full_full.jpg",
            "date": "Offline"
        }
        
    def search_image(self, query: str) -> dict:
        """
        Searches for images in the NASA library (e.g., for thematic flashcards).
        
        Args:
            query: Search term (e.g., 'black hole').
            
        Returns:
            dict: The first valid result item or None.
        """
        try:
            search_url = "https://images-api.nasa.gov/search"
            params = {"q": query, "media_type": "image"}
            response = requests.get(search_url, params=params, timeout=10)
            response.raise_for_status()
            
            items = response.json().get("collection", {}).get("items", [])
            if items:
                # Returns the first relevant simplified result
                data = items[0].get("data", [{}])[0]
                links = items[0].get("links", [{}])
                image_url = links[0].get("href", "") if links else ""
                
                return {
                    "title": data.get("title", "Untitled"),
                    "explanation": data.get("description", "No description"),
                    "url": image_url
                }
            return {}
        except Exception:
            return {
                "title": f"Cached Result for '{query}'",
                "explanation": "The NASA Images API is currently unreachable. This is a generic offline response.",
                "url": ""
            }

# Default instance for simplified use
nasa_client = NasaAPIClient()

