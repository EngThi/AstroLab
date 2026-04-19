import argparse
import os
import sys
import webbrowser
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from astrolab.nasa_client import nasa_client
from astrolab.flashcard import FlashcardGenerator
from astrolab.quiz import QuizGenerator
from astrolab.session import session_manager
from astrolab.deck import deck_manager
from dotenv import load_dotenv

console = Console()

def check_env():
    """Checks if the .env file is configured."""
    load_dotenv(os.path.join(os.getcwd(), '.env'))
    if not os.getenv("NASA_API_KEY") or not os.getenv("GEMINI_API_KEY"):
        console.print("[bold yellow]Notice: Local API keys not detected.[/bold yellow]")
        console.print("Running in interactive demo mode using cached data.\n")

def show_apod():
    """Displays the Astronomy Picture of the Day."""
    with console.status("[bold cyan]Accessing NASA database..."):
        try:
            data = nasa_client.get_apod()
        except Exception as e:
            console.print(f"[bold red]Connection error: {e}[/bold red]")
            return
            
    title = data.get("title", "Untitled")
    explanation = data.get("explanation", "No description available.")
    date = data.get("date", "")
    url = data.get("url", "")
    
    console.print(f"\n[bold blue]NASA APOD - {date}[/bold blue]")
    console.print(f"[bold white]Title:[/bold white] {title}")
    console.print(f"[bold white]URL:[/bold white] [link={url}]{url}[/link]\n")
    console.print(Panel(explanation, title="Summary", expand=False))

    if url and Confirm.ask("\nOpen this image/video in your browser?"):
        webbrowser.open(url)

def interactive_menu():
    """Main interactive menu."""
    console.print(f"[dim]Tip: You can also run commands directly via './astrolab quiz'[/dim]")
    console.print(Panel("[bold magenta]AstroLab[/bold magenta]\nInteractive space science study tool.", expand=False))
    
    while True:
        console.print("\n[bold cyan]Select an activity:[/bold cyan]")
        console.print("1. 🔭 View Astronomy Picture of the Day")
        console.print("2. 🧠 Start Space Quiz")
        console.print("3. 🃏 Generate Study Flashcard")
        console.print("4. 📊 Performance Stats")
        console.print("5. 🔄 Review Your Deck")
        console.print("6. 🩺 System Health Check")
        console.print("7. 🚪 Exit")
        
        choice = Prompt.ask("\nAction", choices=["1", "2", "3", "4", "5", "6", "7"])
        
        if choice == "1":
            show_apod()
        elif choice == "2":
            generator = QuizGenerator()
            generator.run_daily_quiz()
        elif choice == "3":
            topic = Prompt.ask("Enter a space topic (e.g. 'jupiter', 'apollo 11')")
            generator = FlashcardGenerator()
            generator.create_flashcard(topic)
        elif choice == "4":
            session_manager.show_stats()
        elif choice == "5":
            deck_manager.review_deck()
        elif choice == "6":
            run_health_check()
        elif choice == "7":
            console.print("[bold green]Closing system. Fly safe![/bold green]")
            sys.exit(0)

def run_health_check():
    """Simple diagnostic to check environment setup."""
    from pathlib import Path
    import platform
    
    table = Table(title="🔧 AstroLab System Health", show_header=False, border_style="dim")
    table.add_row("Python Version", platform.python_version())
    table.add_row("OS", platform.system())
    
    nasa_key = "Detected" if os.getenv("NASA_API_KEY") else "Missing (Using Demo)"
    gemini_key = "Detected" if os.getenv("GEMINI_API_KEY") else "Missing (Using Cache)"
    
    table.add_row("NASA API Key", nasa_key)
    table.add_row("Gemini API Key", gemini_key)
    
    storage_path = Path.home() / ".astrolab"
    table.add_row("Storage Path", str(storage_path))
    table.add_row("Storage Ready", "Yes" if storage_path.exists() else "No")
    
    console.print(table)

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

    # Command 'check'
    subparsers.add_parser("check", help="Run a system health check")
    
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
    elif args.command == "check":
        run_health_check()
    else:
        # If no arguments are passed, open the interactive menu
        interactive_menu()

if __name__ == "__main__":
    main()

