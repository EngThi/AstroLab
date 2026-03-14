from src.nasa_client import nasa_client
from src.gemini_client import gemini_client
from rich.console import Console
from rich.panel import Panel

console = Console()

class FlashcardGenerator:
    """Gerador de flashcards focado em dados espaciais."""
    
    def create_flashcard(self, topic: str):
        """Busca dados na NASA e gera um flashcard via IA."""
        with console.status(f"[bold cyan]Buscando dados da NASA sobre '{topic}'..."):
            nasa_data = nasa_client.search_image(topic)
            
        if not nasa_data:
            console.print(f"[bold red]Nenhum dado encontrado na NASA para '{topic}'.[/bold red]")
            return

        context = nasa_data.get("explanation", "")
        
        with console.status("[bold magenta]Gemini gerando flashcard inteligente..."):
            flashcard = gemini_client.generate_flashcard(topic, context)
            
        self.display_flashcard(flashcard, nasa_data.get("title"))

    def display_flashcard(self, flashcard: dict, context_title: str):
        """Mostra o flashcard de forma interativa no terminal."""
        console.print(f"\n[bold yellow]Contexto da NASA:[/bold yellow] {context_title}")
        
        front_panel = Panel(flashcard.get("front", ""), title="[bold blue]Frente (Pergunta)[/bold blue]", expand=False)
        console.print(front_panel)
        
        input("\n[Pressione ENTER para virar o card...]")
        
        back_panel = Panel(flashcard.get("back", ""), title="[bold green]Verso (Resposta)[/bold green]", expand=False)
        console.print(back_panel)
        console.print("\n")
