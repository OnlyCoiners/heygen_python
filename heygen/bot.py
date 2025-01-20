# heygen/bot.py
import requests
from typing import List, Dict, Any
from pydantic import BaseModel, HttpUrl

class RegisterWebhookRequest(BaseModel):
    url: HttpUrl
    events: List[str]

class HeyGenClient:
    def __init__(self, api_key: str):
        """Inicializa o cliente com a chave da API."""
        self.api_key = api_key
        self.base_url = "https://api.heygen.com"

    def _build_headers(self) -> Dict[str, str]:
        """Constrói os cabeçalhos para a requisição HTTP com a chave da API."""
        return {
            "X-Api-Key": self.api_key,
            "Accept": "application/json",
        }

    def register_webhook(self, endpoint_url: str, events: List[str]) -> Dict[str, Any]:
        """Registra um webhook no serviço HeyGen."""
        url = f"{self.base_url}/v1/webhook/endpoint.add"
        # Validação dos dados de entrada usando Pydantic
        payload = RegisterWebhookRequest(url=endpoint_url, events=events).dict()

        # Fazendo a requisição POST para registrar o webhook
        response = requests.post(url, json=payload, headers=self._build_headers())

        # Verificando se a requisição foi bem-sucedida
        response.raise_for_status()
        return response.json()  # Retorna a resposta da API em formato JSON
