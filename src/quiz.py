from src.nasa_client import nasa_client
from src.gemini_client import gemini_client
from src.session import session_manager
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm

console = Console()

class QuizGenerator:
    """Gerador e executor de quizzes baseados em dados da NASA."""
    
    def run_daily_quiz(self):
        """Busca o APOD do dia e gera um quiz interativo de 5 perguntas."""
        with console.status("[bold cyan]Buscando Foto Astronômica do Dia (APOD)..."):
            try:
                apod_data = nasa_client.get_apod()
            except Exception as e:
                console.print(f"[bold red]Erro ao buscar dados da NASA: {e}[/bold red]")
                return
                
        title = apod_data.get("title", "Desconhecido")
        explanation = apod_data.get("explanation", "")
        
        console.print(Panel(f"[italic]{explanation}[/italic]", title=f"🔭 {title}"))
        
        with console.status("[bold magenta]IA gerando 5 perguntas baseadas no texto acima..."):
            questions = gemini_client.generate_quiz(explanation, num_questions=5)
            
        if not questions:
            console.print("[bold red]Falha ao gerar o quiz.[/bold red]")
            return
            
        self._execute_quiz(questions, title)

    def _execute_quiz(self, questions: list, topic_title: str):
        score = 0
        wrong_answers = []
        console.print("\n[bold green]--- 🚀 INICIANDO SPACE QUIZ ---[/bold green]\n")
        
        for i, q in enumerate(questions, 1):
            console.print(f"[bold cyan]Pergunta {i}:[/bold cyan] {q.get('question')}")
            for opt in q.get('options', []):
                console.print(f"  {opt}")
                
            resposta_usuario = Prompt.ask("\nSua resposta (ex: A, B, C, D)").strip().upper()
            
            # Pega apenas a letra da resposta correta (ex: "A) texto" -> "A")
            resposta_correta = q.get('answer', '')
            letra_correta = resposta_correta[0].upper() if resposta_correta else ''
            
            if resposta_usuario == letra_correta:
                console.print("[bold green]✅ Correto![/bold green]")
                score += 1
            else:
                console.print(f"[bold red]❌ Incorreto.[/bold red] A resposta certa era: {resposta_correta}")
                wrong_answers.append(q)
                
            console.print(f"[italic]Explicação: {q.get('explanation')}[/italic]\n")
            
        console.print(f"[bold yellow]--- Fim do Quiz! Sua pontuação: {score}/{len(questions)} ---[/bold yellow]\n")
        
        # Salva o resultado no histórico de sessões
        session_manager.save_session(topic_title, score, len(questions))
        console.print(f"[dim]Sessão salva no histórico. Use 'main.py stats' para ver seu progresso.[/dim]")
        
        if wrong_answers and Confirm.ask("\n[bold cyan]Você errou algumas perguntas. Deseja uma explicação aprofundada (Deep Dive) da IA sobre os seus erros?[/bold cyan]"):
            with console.status("[bold magenta]Analisando seus erros e gerando Deep Dive educacional..."):
                deep_dive_text = gemini_client.generate_deep_dive(wrong_answers)
            console.print(Panel(deep_dive_text, title="[bold blue]🧠 Deep Dive: Revisão Focada[/bold blue]", border_style="blue"))

