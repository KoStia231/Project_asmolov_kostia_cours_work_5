from dataclasses import dataclass
from enum import Enum


@dataclass
class ShortEmployersInfo:
    id: int
    name: str
    url: str
    open_vacancies: int


@dataclass
class FullEmployersInfo:
    id: int
    name: str
    url: str
    site_url: str
    region: str
    open_vacancies: int


class VacanciesType(Enum):
    open = 'Открытая'
    closed = 'Закрытая'
    anonymous = 'Анонимная'
    direct = 'Рекламная'


@dataclass
class VacanciesInfo:
    id: int
    name: str
    url: str
    salary_from: int | None
    salary_to: int | None
    employer_id: int
    type: VacanciesType | None
