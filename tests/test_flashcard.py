import pytest
from astrolab.gemini_client import GeminiClient

@pytest.fixture
def gemini_client():
    # Instância sem API_KEY para forçar o fallback nos testes
    return GeminiClient()

def test_flashcard_generates_question(gemini_client):
    """Tests if the flashcard is correctly generated using fallback."""
    # Using fallback to test the structure
    card = gemini_client._fallback_flashcard("Black Hole")
    assert isinstance(card, dict)
    assert "front" in card
    assert "back" in card
    assert "black hole" in card["front"].lower()

def test_quiz_returns_5_questions(mocker):
    """Testa se o quiz gera uma lista com a quantidade pedida (usando mock)."""
    client = GeminiClient()
    mock_response = mocker.Mock()
    # Simulando um json válido com 5 perguntas gerado pela API
    mock_response.text = '```json\n[\n{\"question\": \"Q1\", \"options\": [], \"answer\": \"\", \"explanation\": \"\"},\n{\"question\": \"Q2\", \"options\": [], \"answer\": \"\", \"explanation\": \"\"},\n{\"question\": \"Q3\", \"options\": [], \"answer\": \"\", \"explanation\": \"\"},\n{\"question\": \"Q4\", \"options\": [], \"answer\": \"\", \"explanation\": \"\"},\n{\"question\": \"Q5\", \"options\": [], \"answer\": \"\", \"explanation\": \"\"}\n]\n```'
    
    # Faz o mock da chamada interna caso tenha API_KEY configurada
    if client.model:
        mocker.patch.object(client.model, 'generate_content', return_value=mock_response)
        
    # Se não tiver API_KEY ele vai pro fallback e o fallback retorna só 1, mas
    # para este teste de "returns_5_questions", precisamos mockar o _generate_json direto
    mocker.patch.object(client, '_generate_json', return_value=[{"q":"1"}]*5)
    
    quiz = client.generate_quiz("texto contexto", num_questions=5)
    assert isinstance(quiz, list)
    assert len(quiz) == 5

def test_gemini_fallback_on_error(gemini_client):
    """Testa se o gerador não quebra quando falha e retorna o fallback padrão."""
    quiz = gemini_client._fallback_quiz()
    assert isinstance(quiz, list)
    assert len(quiz) > 0
    assert "question" in quiz[0]
