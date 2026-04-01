import json
import os
import random
from pathlib import Path
from rich.console import Console
from rich.panel import Panel

console = Console()
ASTROLAB_DIR = Path.home() / ".astrolab"
DECK_FILE = ASTROLAB_DIR / "deck.json"

class DeckManager:
    """Manages the collection of saved flashcards."""

    def __init__(self):
        os.makedirs(ASTROLAB_DIR, exist_ok=True)
            
        if not os.path.exists(DECK_FILE):
            with open(DECK_FILE, "w", encoding="utf-8") as f:
                json.dump([], f)

    def save_card(self, topic: str, front: str, back: str):
        """Saves a generated flashcard into the personal deck."""
        try:
            with open(DECK_FILE, "r", encoding="utf-8") as f:
                deck = json.load(f)
        except json.JSONDecodeError:
            deck = []

        # Avoid exact duplicates
        if not any(card.get('front') == front for card in deck):
            deck.append({
                "topic": topic,
                "front": front,
                "back": back
            })
            with open(DECK_FILE, "w", encoding="utf-8") as f:
                json.dump(deck, f, indent=4, ensure_ascii=False)

    def review_deck(self):
        """Starts a review session for saved flashcards."""
        try:
            with open(DECK_FILE, "r", encoding="utf-8") as f:
                deck = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            console.print("[bold red]Error reading the deck.[/bold red]")
            return

        if not deck:
            console.print("[bold yellow]Your deck is empty! Generate some flashcards first using option 3 from the menu.[/bold yellow]")
            return

        console.print(f"\n[bold green]--- 📚 STARTING REVIEW ({len(deck)} cards) ---[/bold green]\n")
        
        # Shuffle cards for review
        random.shuffle(deck)

        for i, card in enumerate(deck, 1):
            console.print(f"[bold cyan]Card {i}/{len(deck)} | Topic: {card.get('topic', 'N/A')}[/bold cyan]")
            
            front_panel = Panel(card.get("front", ""), title="[bold blue]Front (Question)[/bold blue]", expand=False)
            console.print(front_panel)
            
            input("\nPress ENTER to reveal the answer...")
            
            back_panel = Panel(card.get("back", ""), title="[bold green]Back (Answer)[/bold green]", expand=False)
            console.print(back_panel)
            
            if i < len(deck):
                cont = input("\nPress ENTER for the next card or 'q' to quit the review...").strip().lower()
                if cont == 'q':
                    break
            console.print("\n")
            
        console.print("[bold yellow]--- Review Finished! ---[/bold yellow]\n")

deck_manager = DeckManager()

