from src.api_clients import HHClients
from src.config import settings
from src.db.manager import PostgresDBManager

api_clients = HHClients()


def load_employers():
    """загрузка компаний в базу данных"""
    employer_ids = settings.get_employee_ids()
    sql = """
    INSERT INTO employers(id, name, url, site_url, region)
    VALUES(%s, %s, %s, %s, %s);
    """

    db_manager = PostgresDBManager()
    db_manager.connect()
    try:
        with db_manager.connection.cursor() as cursor:
            for employer_id in employer_ids:
                emp = api_clients.get_employer_info(employer_id)
                cursor.execute(sql, (emp.id, emp.name, emp.url, emp.site_url, emp.region))
            db_manager.commit()
    finally:
        db_manager.disconnect()


def load_vacancies():
    """загрузка вакансий в базу"""
    employer_ids = settings.get_employee_ids()
    sql = """
    INSERT INTO vacancies(id, name, url, type, salary_from, salary_to, employer_id)
    VALUES(%s, %s, %s, %s, %s, %s, %s);
    """

    db_manager = PostgresDBManager()
    db_manager.connect()
    try:
        with db_manager.connection.cursor() as cursor:
            for employer_id in employer_ids:
                vacancies = api_clients.get_employer_vacancies(employer_id)
                data = (
                    (vac.id, vac.name, vac.url, vac.type.name, vac.salary_from, vac.salary_to, employer_id)
                    for vac in vacancies
                )
                cursor.executemany(sql, data)

            db_manager.commit()
    finally:
        db_manager.disconnect()
