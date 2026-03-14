import argparse
from rich.console import Console
from rich.panel import Panel
from src.nasa_client import nasa_client
from src.flashcard import FlashcardGenerator
from src.quiz import QuizGenerator

console = Console()

def show_apod():
    """Mostra a Astronomy Picture of the Day e uma curiosidade se possível."""
    with console.status("[bold cyan]Buscando APOD na NASA..."):
        try:
            data = nasa_client.get_apod()
        except Exception as e:
            console.print(f"[bold red]Erro ao acessar a API da NASA: {e}[/bold red]")
            return
            
    title = data.get("title", "Sem título")
    explanation = data.get("explanation", "Sem descrição")
    date = data.get("date", "")
    url = data.get("url", "")
    
    console.print(f"\n[bold blue]🚀 APOD - Astronomy Picture of the Day ({date})[/bold blue]")
    console.print(f"[bold white]Título:[/bold white] {title}")
    console.print(f"[bold white]Link/Imagem:[/bold white] [link={url}]{url}[/link]\n")
    console.print(Panel(explanation, title="Explicação", expand=False))

def main():
    parser = argparse.ArgumentParser(description="Study-Lab-Core: Space Pivot 🚀")
    subparsers = parser.add_subparsers(dest="command", help="Comandos disponíveis")
    
    # Comando 'apod'
    subparsers.add_parser("apod", help="Mostra Astronomy Picture of the Day")
    
    # Comando 'quiz'
    subparsers.add_parser("quiz", help="Gera um quiz interativo de 5 perguntas sobre o APOD do dia")
    
    # Comando 'flashcard'
    flashcard_parser = subparsers.add_parser("flashcard", help="Cria um flashcard sobre um tema espacial")
    flashcard_parser.add_argument("tema", type=str, help="Tema para buscar na NASA (ex: 'gravidade', 'black hole')")
    
    args = parser.parse_args()
    
    if args.command == "apod":
        show_apod()
    elif args.command == "quiz":
        generator = QuizGenerator()
        generator.run_daily_quiz()
    elif args.command == "flashcard":
        generator = FlashcardGenerator()
        generator.create_flashcard(args.tema)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
