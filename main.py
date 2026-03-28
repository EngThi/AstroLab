import argparse
import os
import sys
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from src.nasa_client import nasa_client
from src.flashcard import FlashcardGenerator
from src.quiz import QuizGenerator
from src.session import session_manager
from src.deck import deck_manager
from dotenv import load_dotenv

console = Console()

def check_env():
    """Checks if the .env file is configured."""
    load_dotenv()
    if not os.getenv("NASA_API_KEY"):
        console.print("[bold red]⚠️ Warning: NASA_API_KEY not found.[/bold red]")
        console.print("Please create a [bold white].env[/bold white] file (use .env.example as a template).")
        console.print("The project will use the DEMO_KEY, which has a very low rate limit.\n")

def show_apod():
    """Displays the Astronomy Picture of the Day."""
    with console.status("[bold cyan]Fetching APOD from NASA..."):
        try:
            data = nasa_client.get_apod()
        except Exception as e:
            console.print(f"[bold red]Error accessing NASA API: {e}[/bold red]")
            return
            
    title = data.get("title", "Untitled")
    explanation = data.get("explanation", "No description available.")
    date = data.get("date", "")
    url = data.get("url", "")
    
    console.print(f"\n[bold blue]🚀 APOD - Astronomy Picture of the Day ({date})[/bold blue]")
    console.print(f"[bold white]Title:[/bold white] {title}")
    console.print(f"[bold white]Link/Image:[/bold white] [link={url}]{url}[/link]\n")
    console.print(Panel(explanation, title="Explanation", expand=False))

def interactive_menu():
    """Main interactive menu when run without arguments."""
    
    disclaimer = """[bold yellow]💡 DEMO TIP:[/bold yellow] You are using the interactive menu. 
You can also run commands directly from your terminal!
Try: [bold cyan]./astrolab quiz[/bold cyan] or [bold cyan]./astrolab flashcard "mars"[/bold cyan]"""
    console.print(Panel(disclaimer, border_style="yellow", expand=False))
    
    console.print(Panel("[bold magenta]Welcome to AstroLab 🚀[/bold magenta]\nYour study tool powered by real NASA data.", expand=False))
    
    while True:
        console.print("\n[bold cyan]Choose an option:[/bold cyan]")
        console.print("1. 🔭 View APOD (Astronomy Picture of the Day)")
        console.print("2. 🧠 Take a Space Quiz (AI Generated)")
        console.print("3. 🃏 Generate a Flashcard (e.g., 'Black Hole')")
        console.print("4. 📊 View Study Stats & History")
        console.print("5. 🔄 Review Saved Flashcards (Deck)")
        console.print("6. 🚪 Exit")
        
        choice = Prompt.ask("\nYour choice", choices=["1", "2", "3", "4", "5", "6"])
        
        if choice == "1":
            show_apod()
        elif choice == "2":
            generator = QuizGenerator()
            generator.run_daily_quiz()
        elif choice == "3":
            tema = Prompt.ask("Enter a topic (e.g., 'gravity', 'mars')")
            generator = FlashcardGenerator()
            generator.create_flashcard(tema)
        elif choice == "4":
            session_manager.show_stats()
        elif choice == "5":
            deck_manager.review_deck()
        elif choice == "6":
            console.print("[bold green]See you on the next space journey! 🌌[/bold green]")
            sys.exit(0)

def main():
    check_env()
    
    parser = argparse.ArgumentParser(description="AstroLab: Space Pivot 🚀")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Command 'apod'
    subparsers.add_parser("apod", help="Show Astronomy Picture of the Day")
    
    # Command 'quiz'
    subparsers.add_parser("quiz", help="Generate an interactive 5-question quiz based on today's APOD")
    
    # Command 'flashcard'
    flashcard_parser = subparsers.add_parser("flashcard", help="Create a flashcard about a space topic")
    flashcard_parser.add_argument("tema", type=str, help="Topic to search on NASA (e.g., 'gravity', 'black hole')")

    # Command 'stats'
    subparsers.add_parser("stats", help="Show your study session progress history")
    
    # Command 'review'
    subparsers.add_parser("review", help="Review your personal collection of saved flashcards")
    
    args = parser.parse_args()
    
    if args.command == "apod":
        show_apod()
    elif args.command == "quiz":
        generator = QuizGenerator()
        generator.run_daily_quiz()
    elif args.command == "flashcard":
        generator = FlashcardGenerator()
        generator.create_flashcard(args.tema)
    elif args.command == "stats":
        session_manager.show_stats()
    elif args.command == "review":
        deck_manager.review_deck()
    else:
        # If no arguments are passed, open the interactive menu
        interactive_menu()

if __name__ == "__main__":
    main()

