import json
import os
from datetime import datetime
from rich.console import Console
from rich.table import Table

console = Console()
SESSION_FILE = "data/sessions/history.json"

class SessionManager:
    """Gerencia o histórico de sessões de estudo (quizzes)."""

    def __init__(self):
        # Garante que o arquivo existe
        if not os.path.exists(SESSION_FILE):
            with open(SESSION_FILE, "w", encoding="utf-8") as f:
                json.dump([], f)

    def save_session(self, topic: str, score: int, total_questions: int):
        """Salva o resultado de um quiz no histórico."""
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
        """Exibe uma tabela estilizada com o progresso do usuário."""
        try:
            with open(SESSION_FILE, "r", encoding="utf-8") as f:
                history = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            console.print("[bold red]Nenhum histórico encontrado. Jogue um quiz primeiro![/bold red]")
            return

        if not history:
            console.print("[bold yellow]Seu histórico está vazio. Que tal um /quiz agora?[/bold yellow]")
            return

        table = Table(title="🚀 Progresso no AstroLab", style="cyan")
        table.add_column("Data", justify="left", style="cyan", no_wrap=True)
        table.add_column("Tópico (APOD)", style="magenta")
        table.add_column("Acertos", justify="center", style="green")
        table.add_column("Desempenho", justify="left")

        for session in history:
            score = session.get('score', 0)
            total = session.get('total', 5)
            
            # Gráfico de barras simples: █ para acerto, ░ para erro
            bar = ("█" * score) + ("░" * (total - score))
            
            # Cor condicional baseada na nota
            color = "green" if score >= (total/2) else "red"
            
            table.add_row(
                session.get('date', 'N/A'),
                session.get('topic', 'Desconhecido')[:40] + "...", # Trunca nomes longos
                f"{score}/{total}",
                f"[{color}]{bar}[/{color}]"
            )

        console.print(table)
        
        # Média geral
        total_quizzes = len(history)
        media_acertos = sum(s.get('score', 0) for s in history) / total_quizzes if total_quizzes > 0 else 0
        console.print(f"\n[bold white]Média de Acertos:[/bold white] {media_acertos:.1f} por quiz.")

session_manager = SessionManager()
