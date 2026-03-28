from src.nasa_client import nasa_client
from src.gemini_client import gemini_client
from src.deck import deck_manager
from rich.console import Console
from rich.panel import Panel

console = Console()

class FlashcardGenerator:
    """Flashcard generator focused on space data."""
    
    def create_flashcard(self, topic: str):
        """Fetches data from NASA and generates a flashcard via AI."""
        with console.status(f"[bold cyan]Fetching NASA data about '{topic}'..."):
            nasa_data = nasa_client.search_image(topic)
            
        if not nasa_data:
            console.print(f"[bold red]No data found on NASA for '{topic}'.[/bold red]")
            return

        context = nasa_data.get("explanation", "")
        
        with console.status("[bold magenta]Gemini generating smart flashcard..."):
            flashcard = gemini_client.generate_flashcard(topic, context)
            
        self.display_flashcard(flashcard, nasa_data.get("title"))
        
        # Save generated card to the user's deck
        if "front" in flashcard and "back" in flashcard:
            deck_manager.save_card(topic, flashcard["front"], flashcard["back"])
            console.print("[dim]Card automatically saved to your deck! Use the menu to review it later.[/dim]\n")

    def display_flashcard(self, flashcard: dict, context_title: str):
        """Displays the flashcard interactively in the terminal."""
        console.print(f"\n[bold yellow]NASA Context:[/bold yellow] {context_title}")
        
        front_panel = Panel(flashcard.get("front", ""), title="[bold blue]Front (Question)[/bold blue]", expand=False)
        console.print(front_panel)
        
        input("\n[Press ENTER to flip the card...]")
        
        back_panel = Panel(flashcard.get("back", ""), title="[bold green]Back (Answer)[/bold green]", expand=False)
        console.print(back_panel)
        console.print("\n")


