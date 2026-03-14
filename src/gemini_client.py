import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

class GeminiClient:
    """Cliente para a API do Google Gemini."""
    
    def __init__(self):
        # Utiliza o modelo gemini-1.5-flash para tarefas rápidas de texto
        if GEMINI_API_KEY:
            self.model = genai.GenerativeModel('gemini-1.5-flash')
        else:
            self.model = None
            
    def _generate_json(self, prompt: str) -> dict:
        """Helper para garantir que a resposta seja um JSON válido."""
        if not self.model:
            raise ValueError("GEMINI_API_KEY não configurada.")
            
        full_prompt = f"{prompt}\n\nResponda APENAS com um objeto JSON válido, sem formatação markdown ou texto extra."
        
        response = self.model.generate_content(full_prompt)
        text = response.text.strip()
        
        # Remove possíveis blocos de código markdown que o modelo pode retornar
        if text.startswith("```json"):
            text = text[7:]
        if text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
            
        try:
            return json.loads(text.strip())
        except json.JSONDecodeError:
            # Fallback em caso de erro na geração
            return {"error": "Falha ao decodificar JSON do Gemini", "raw_text": text}

    def generate_quiz(self, context_text: str, num_questions: int = 5) -> list:
        """
        Gera um quiz com base no texto fornecido.
        
        Args:
            context_text: O texto (ex: explicação da NASA) base para as perguntas.
            num_questions: Quantidade de perguntas.
            
        Returns:
            list: Lista de dicionários com 'question', 'options' (list), 'answer' (str), 'explanation' (str).
        """
        prompt = f"""
        Baseado no texto a seguir sobre astronomia, crie um quiz com {num_questions} perguntas de múltipla escolha.
        O nível deve ser para estudantes universitários (desafiador mas focado nos conceitos do texto).
        
        TEXTO:
        {context_text}
        
        O JSON de saída deve ser estritamente uma lista de objetos com este formato:
        [
            {{
                "question": "texto da pergunta",
                "options": ["A) op1", "B) op2", "C) op3", "D) op4"],
                "answer": "A) op1",  // DEVE ser exatamente igual a uma das strings na lista de opções
                "explanation": "Por que esta é a resposta correta baseado no texto"
            }}
        ]
        """
        try:
            result = self._generate_json(prompt)
            if isinstance(result, list):
                return result
            elif isinstance(result, dict) and "quiz" in result: # Lida com pequenas variações estruturais
                return result["quiz"]
            return []
        except Exception as e:
            print(f"Erro ao gerar quiz: {e}")
            return self._fallback_quiz()

    def generate_flashcard(self, topic: str, context_text: str) -> dict:
        """
        Gera o conteúdo de um flashcard.
        """
        prompt = f"""
        Baseado no texto da NASA sobre o tema '{topic}', crie o conteúdo para um flashcard de estudo.
        
        TEXTO:
        {context_text}
        
        O JSON de saída deve ser um objeto com este formato:
        {{
            "front": "Uma pergunta direta ou conceito chave sobre {topic}",
            "back": "A resposta detalhada, direta e fácil de memorizar"
        }}
        """
        try:
            result = self._generate_json(prompt)
            if "front" in result and "back" in result:
                return result
            return self._fallback_flashcard(topic)
        except Exception:
            return self._fallback_flashcard(topic)

    def _fallback_quiz(self) -> list:
        """Retorna um quiz fixo caso a API falhe (ex: sem internet ou sem chave)."""
        return [
            {
                "question": "[Modo Offline] O que é um buraco negro?",
                "options": ["A) Uma estrela brilhante", "B) Região do espaço onde a gravidade impede até a luz de escapar", "C) Um planeta gasoso", "D) Uma nuvem de poeira"],
                "answer": "B) Região do espaço onde a gravidade impede até a luz de escapar",
                "explanation": "Buracos negros são regiões do espaço-tempo onde a gravidade é tão forte que nada pode escapar."
            }
        ]
        
    def _fallback_flashcard(self, topic: str) -> dict:
        return {
            "front": f"Conceito: {topic} (Modo Offline)",
            "back": "Por favor, configure sua GEMINI_API_KEY para gerar flashcards dinâmicos."
        }

gemini_client = GeminiClient()
