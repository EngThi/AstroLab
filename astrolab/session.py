import json
import os
from pathlib import Path
from datetime import datetime
from rich.console import Console
from rich.table import Table

console = Console()

ASTROLAB_DIR = Path.home() / ".astrolab"
SESSION_FILE = ASTROLAB_DIR / "history.json"

class SessionManager:
    """Manages the history of study sessions (quizzes)."""

    def __init__(self):
        # Ensures the file exists
        os.makedirs(ASTROLAB_DIR, exist_ok=True)
        if not os.path.exists(SESSION_FILE):
            with open(SESSION_FILE, "w", encoding="utf-8") as f:
                json.dump([], f)

    def save_session(self, topic: str, score: int, total_questions: int):
        """Saves a quiz result to the history."""
        try:
            with open(SESSION_FILE, "r", encoding="utf-8") as f:
                history = json.load(f)
        except json.JSONDecodeError:
            history = []

        session_data = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "topic": topic,
            "score": score,
            "total": total_questions
        }

        history.append(session_data)

        with open(SESSION_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=4, ensure_ascii=False)

    def show_stats(self):
        """Displays a stylized table with the user's progress."""
        try:
            with open(SESSION_FILE, "r", encoding="utf-8") as f:
                history = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            console.print("[bold red]No history found. Play a quiz first![/bold red]")
            return

        if not history:
            console.print("[bold yellow]Your history is empty. How about a /quiz now?[/bold yellow]")
            return

        table = Table(title="🚀 AstroLab Progress", style="cyan")
        table.add_column("Date", justify="left", style="cyan", no_wrap=True)
        table.add_column("Topic (APOD)", style="magenta")
        table.add_column("Score", justify="center", style="green")
        table.add_column("Performance", justify="left")

        for session in history:
            score = session.get('score', 0)
            total = session.get('total', 5)
            
            # Simple bar chart: █ for correct, ░ for incorrect
            bar = ("█" * score) + ("░" * (total - score))
            
            # Conditional color based on score
            color = "green" if score >= (total/2) else "red"
            
            table.add_row(
                session.get('date', 'N/A'),
                session.get('topic', 'Unknown')[:40] + "...", # Truncates long names
                f"{score}/{total}",
                f"[{color}]{bar}[/{color}]"
            )

        console.print(table)
        
        # Overall average
        total_quizzes = len(history)
        average_score = sum(s.get('score', 0) for s in history) / total_quizzes if total_quizzes > 0 else 0
        console.print(f"\n[bold white]Average Score:[/bold white] {average_score:.1f} per quiz.")

session_manager = SessionManager()

