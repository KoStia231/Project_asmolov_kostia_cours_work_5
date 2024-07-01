from abc import ABC, abstractmethod
import requests


class ApiClient(ABC):
    @property
    @abstractmethod
    def base_url(self) -> str:
        pass

    def _get(self, url: str, params: dict = {}) -> dict:
        full_url = self.base_url + url
        response = requests.get(full_url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
