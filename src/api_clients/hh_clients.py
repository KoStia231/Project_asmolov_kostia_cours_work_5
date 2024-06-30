from src.api_clients.base import ApiClient
from src.api_clients.utils import ShortEmployersInfo, FullEmployersInfo, VacanciesInfo, VacanciesType


class HHClients(ApiClient):
    def __init__(self):
        self.__base_url = 'https://api.hh.ru'

    def employers_search(self, search: str, *, only_with_vacancies: bool = True) -> list[ShortEmployersInfo]:
        """Поиск компании по имени"""
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

    def get_employer_info(self, employer_id: int) -> FullEmployersInfo:
        """"Получение инфы о компании"""
        employer_info = self._get(f'/employers/{employer_id}')
        return FullEmployersInfo(
            id=employer_id,
            name=employer_info['name'],
            url=employer_info['alternate_url'],
            site_url=employer_info['site_url'],
            region=employer_info['area']['name'],
            open_vacancies=employer_info['open_vacancies'],
        )

    def get_employer_vacancies(self, employer_id) -> list[VacanciesInfo]:
        """Получение инфы вакансии"""
        params = {
            'employer_id': employer_id,
            'only_with_salary': True
        }
        vacancies = self._get_items('/vacancies', params=params)
        return [
            VacanciesInfo(
                id=int(vacancy['id']),
                name=vacancy['name'],
                url=vacancy['alternate_url'],
                salary_from=vacancy['salary'].get('from'),
                salary_to=vacancy['salary'].get('to'),
                employer_id=employer_id,
                type=VacanciesType[vacancy['type']['id']],
            )
            for vacancy in vacancies
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
