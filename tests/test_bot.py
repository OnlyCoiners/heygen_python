# tests/test_bot.py
import pytest
from heygen.bot import HeyGenClient
from unittest.mock import patch
import requests
from requests.models import Response

# Definindo uma fixture para criar o cliente com a chave de API
@pytest.fixture
def client():
    return HeyGenClient(api_key="fake_api_key")

# Teste para registrar webhook
def test_register_webhook(client):
    # Dados de entrada simulados
    endpoint_url = "https://api.heygen.com/v1/webhook/endpoint.add"  # URL corrigida
    events = ["video.created", "video.updated"]

    # Simulando a resposta da API com o requests-mock
    with patch('requests.post') as mock_post:
        # Criando um objeto de resposta simulada
        mock_response = Response()
        mock_response.status_code = 200
        mock_response._content = b'{"success": true, "message": "Webhook registered successfully"}'
        
        # Configurando o mock para retornar a resposta simulada
        mock_post.return_value = mock_response
        
        # Chama a função que será testada
        response = client.register_webhook(endpoint_url, events)

        # Verificando se a resposta é como esperado
        assert response['success'] == True
        assert response['message'] == "Webhook registered successfully"
        
        # Verificando se o método POST foi chamado corretamente
        mock_post.assert_called_once_with(
            'https://api.heygen.com/v1/webhook/endpoint.add',  # URL correta
            json={'url': endpoint_url, 'events': events},  # Certificando-se de passar os dados corretamente
            headers={'X-Api-Key': 'fake_api_key', 'Accept': 'application/json'}
        )
