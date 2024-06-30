import dataclasses


@dataclasses.dataclass
class ShortEmployersInfo:
    id: int
    name: str
    url: str
    open_vacancies: int
