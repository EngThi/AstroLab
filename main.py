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
from dotenv import load_dotenv

console = Console()

def check_env():
    """Verifica se o arquivo .env foi configurado."""
    load_dotenv()
    if not os.getenv("NASA_API_KEY"):
        console.print("[bold red]⚠️ Atenção: NASA_API_KEY não encontrada.[/bold red]")
        console.print("Por favor, crie um arquivo [bold white].env[/bold white] (use o .env.example como base).")
        console.print("O projeto usará a chave DEMO_KEY, que tem limite baixo de requisições.\n")

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

def interactive_menu():
    """Menu interativo principal para quando rodar sem argumentos."""
    console.print(Panel("[bold magenta]Bem-vindo ao AstroLab 🚀[/bold magenta]\nSua ferramenta de estudo com dados reais da NASA.", expand=False))
    
    while True:
        console.print("\n[bold cyan]Escolha uma opção:[/bold cyan]")
        console.print("1. 🔭 Ver APOD (Astronomy Picture of the Day)")
        console.print("2. 🧠 Fazer Quiz Espacial (Gerado por IA)")
        console.print("3. 🃏 Gerar Flashcard (ex: 'Black Hole')")
        console.print("4. 📊 Ver Histórico de Estudos (Stats)")
        console.print("5. 🚪 Sair")
        
        choice = Prompt.ask("\nSua escolha", choices=["1", "2", "3", "4", "5"])
        
        if choice == "1":
            show_apod()
        elif choice == "2":
            generator = QuizGenerator()
            generator.run_daily_quiz()
        elif choice == "3":
            tema = Prompt.ask("Digite o tema em inglês (ex: 'gravity', 'mars')")
            generator = FlashcardGenerator()
            generator.create_flashcard(tema)
        elif choice == "4":
            session_manager.show_stats()
        elif choice == "5":
            console.print("[bold green]Até a próxima jornada espacial! 🌌[/bold green]")
            sys.exit(0)

def main():
    check_env()
    
    parser = argparse.ArgumentParser(description="AstroLab: Space Pivot 🚀")
    subparsers = parser.add_subparsers(dest="command", help="Comandos disponíveis")
    
    # Comando 'apod'
    subparsers.add_parser("apod", help="Mostra Astronomy Picture of the Day")
    
    # Comando 'quiz'
    subparsers.add_parser("quiz", help="Gera um quiz interativo de 5 perguntas sobre o APOD do dia")
    
    # Comando 'flashcard'
    flashcard_parser = subparsers.add_parser("flashcard", help="Cria um flashcard sobre um tema espacial")
    flashcard_parser.add_argument("tema", type=str, help="Tema para buscar na NASA (ex: 'gravidade', 'black hole')")

    # Comando 'stats'
    subparsers.add_parser("stats", help="Mostra o histórico de progresso das suas sessões de estudo")
    
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
    else:
        # Se não passar argumentos via CLI, abre o menu interativo lindão
        interactive_menu()

if __name__ == "__main__":
    main()
