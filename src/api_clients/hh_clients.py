from src.api_clients.base import ApiClient
from src.api_clients.utils import ShortEmployersInfo


class HHClients(ApiClient):
    def __init__(self):
        self.__base_url = 'https://api.hh.ru'

    def employers_search(self, search: str, *, only_with_vacancies: bool = True) -> list[ShortEmployersInfo]:
        params = {
            'text': search,
            'only_with_vacancies': only_with_vacancies
        }

        employers = self._get_items('/employers', params)
        return [
            ShortEmployersInfo(
                id=int(employer['id']),
                name=employer['name'],
                url=employer['alternate_url'],
                open_vacancies=employer['open_vacancies'],
            )
            for employer in employers
        ]

    @property
    def base_url(self) -> str:
        return self.__base_url

    def _get_items(self, url: str, params: dict) -> list[dict]:
        """Метод для получения всех работодателей"""
        items = []
        params['page'] = 0
        params['per_page'] = 100
        while True:
            data = self._get(url, params=params)
            items.extend(data['items'])

            total_pages = data['pages']
            if total_pages == params['page']:
                break
            params['page'] += 1

            if len(items) >= 2000:
                """что-бы не падало с ошибкой"""
                break

        return items
