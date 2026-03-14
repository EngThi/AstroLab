import pytest
from src.nasa_client import NasaAPIClient

@pytest.fixture
def mock_nasa_client(mocker):
    # Mock para não bater na API real durante os testes
    client = NasaAPIClient(api_key="DEMO_KEY")
    mock_response = mocker.Mock()
    mock_response.json.return_value = {
        "title": "Mock APOD Title",
        "explanation": "This is a mock explanation for testing purposes.",
        "url": "https://example.com/image.jpg",
        "date": "2026-02-12"
    }
    mocker.patch("requests.get", return_value=mock_response)
    return client

def test_nasa_client_returns_apod_dict(mock_nasa_client):
    """Testa se o client retorna um dicionário ao chamar a API."""
    data = mock_nasa_client.get_apod()
    assert isinstance(data, dict)

def test_apod_has_required_fields(mock_nasa_client):
    """Testa se o retorno da APOD contém os campos essenciais."""
    data = mock_nasa_client.get_apod()
    assert "title" in data
    assert "explanation" in data
    assert "url" in data