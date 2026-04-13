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
        params = {"api_key": self.api_key}
        response = requests.get(APOD_URL, params=params)
        response.raise_for_status()
        return response.json()
        
    def search_image(self, query: str) -> dict:
        """
        Searches for images in the NASA library (e.g., for thematic flashcards).
        
        Args:
            query: Search term (e.g., 'black hole').
            
        Returns:
            dict: The first valid result item or None.
        """
        search_url = "https://images-api.nasa.gov/search"
        params = {"q": query, "media_type": "image"}
        response = requests.get(search_url, params=params)
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

# Default instance for simplified use
nasa_client = NasaAPIClient()

