from .base import DBManager
import psycopg2


class PostgresDBManager(DBManager):

    def connect(self) -> None:
        if self.connection is None:
            self.connection = psycopg2.connect(
                dbname=self.db_name,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )

    def disconnect(self) -> None:
        if self.connection is not None:
            self.connection.close()
            self.connection = None

    def get_companies_and_vacancies_count(self) -> list[tuple[str, int]]:
        """получает список всех компаний и количество вакансий у каждой компании."""
        sql = """
            SELECT e.name, COUNT(*) as vacancies_count
            FROM employers as e
            LEFT JOIN vacancies as vc ON e.id = vc.employer_id
            GROUP BY e.name;
        """

        self.connect()

        with self.connection.cursor() as cursor:
            cursor.execute(sql)
            return cursor.fetchall()

    def get_all_vacancies(self) -> list:
        """Получает список всех вакансий с указанием названия компании, названия вакансии, зарплаты и ссылки на вакансию."""
        sql = """
            SELECT e.name, v.name, v.salary_from, v.salary_to, v.url
            FROM vacancies as v
            JOIN employers as e ON v.employer_id = e.id;
        """

        self.connect()

        with self.connection.cursor() as cursor:
            cursor.execute(sql)
            return cursor.fetchall()

    def get_avg_salary(self) -> float:
        """получает среднюю зарплату по вакансиям"""
        sql = """
        SELECT avg(v.salary_from), avg(v.salary_to) FROM vacancies as v;
        """

        self.connect()

        with self.connection.cursor() as cursor:
            cursor.execute(sql)
            min_salary, max_salary = cursor.fetchone()
            avg_salary = (min_salary + max_salary) / 2
            return round(avg_salary, 2)

    def get_vacancies_with_higher_salary(self) -> list:
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        sql = """
            SELECT v.name, v.salary_from, v.salary_to, v.url
            FROM vacancies as v
            WHERE (v.salary_from + v.salary_to) / 2 > (
                SELECT AVG((salary_from + salary_to) / 2) 
                FROM vacancies
                WHERE salary_from IS NOT NULL AND salary_to IS NOT NULL
            );
        """

        self.connect()

        with self.connection.cursor() as cursor:
            cursor.execute(sql)
            return cursor.fetchall()

    def get_vacancies_with_keyword(self, keyword):
        """Получает список всех вакансий, в названии которых содержатся переданные в метод слова."""
        sql = """
            SELECT v.name, v.salary_from, v.salary_to, v.url
            FROM vacancies as v
            WHERE v.name LIKE %s;
        """

        self.connect()

        with self.connection.cursor() as cursor:
            search_keyword = f'%{keyword}%'
            cursor.execute(sql, (search_keyword,))
            return cursor.fetchall()
