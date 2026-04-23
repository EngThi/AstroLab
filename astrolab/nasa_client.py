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
            "title": "Saturn at Equinox (Offline/Rate-Limited Cache)",
            "explanation": "The NASA API is currently unreachable or you have exceeded the DEMO_KEY rate limit (30 requests/hour). Please add your own NASA_API_KEY to the .env file! Meanwhile, enjoy this cached image of Saturn illuminated by sunlight exactly edge-on to its rings.",
            "url": "https://images-assets.nasa.gov/image/PIA12235/PIA12235~orig.jpg",
            "date": "Offline Cache"
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

