from src.api_clients.base import ApiClient


class HHClients(ApiClient):
    def __init__(self):
        self.__base_url = 'https://api.hh.ru'

    @property
    def base_url(self) -> str:
        return self.__base_url

