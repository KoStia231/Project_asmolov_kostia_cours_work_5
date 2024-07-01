from src.api_clients import HHClients
from src.db.loader import load_employers, load_vacancies
from src.db.manager import PostgresDBManager
from src.db.migrations import create_database, apply_migrations
from prettytable import PrettyTable

start_massage = """
Добро пожаловать для возврата на предыдущее меню введите 'q'"""
print_user_choice = """
Выберите действие :
1 - Работать с hh.ru
2 - Работать с БД
0- Выйти """

print_user_choice_hh = """
Выберите действие :
1 - Поиск компании по ключевому слову
2 - Вывести информацию по id компании
q - возврат в предыдущее меню
"""

print_user_choice_data_base = """
Выберите действие :
1 - Получить список всех компаний и количество вакансий у каждой компании
2 - Получить список всех вакансий 
3 - Получить среднюю зп по всем вакансиям
4 - Получить список всех вакансий у которых зарплата выше среднего
5 - Получить список всех вакансий по ключевому слову
q - возврат в предыдущее меню"""


def search_company_name():
    while True:
        print('-' * 37, '  ВВЕДИТЕ ИМЯ КОМПАНИИ  ', '-' * 37)
        name = input()
        if name != 'q':
            client = HHClients()
            results = client.employers_search(name)
            table = PrettyTable()
            table.field_names = ['id', 'Компания', 'Компания на hh.ru', 'Открытые вакансии']
            for result in results:
                table.add_row([result.id, result.name, result.url, result.open_vacancies])
            print(table)
            print('-' * 100)
        else:
            break


def id_company():
    while True:
        print('-' * 38, '  ВВЕДИТЕ id КОМПАНИИ  ', '-' * 37)
        name = input()
        if name != 'q':
            client = HHClients()
            results = client.get_employer_info(int(name))
            table = PrettyTable()
            table.field_names = ['id', 'Компания',
                                 'Компания на hh.ru',
                                 'Ссылка на сайт компании',
                                 'Регион',
                                 'Открытые вакансии']
            table.add_row(
                [results.id, results.name, results.url, results.site_url, results.region, results.open_vacancies])
            print(table)
            print('-' * 100)
        else:
            break


def job_hh():
    while True:
        print(print_user_choice_hh)
        user_input = input()
        if user_input == 'q':
            break
        elif user_input == '1':
            search_company_name()
        elif user_input == '2':
            id_company()


def job_bd():
    create_database()
    apply_migrations()
    load_employers()
    load_vacancies()
    data_base = PostgresDBManager()
    table = PrettyTable()
    while True:
        print(print_user_choice_data_base)
        user_input = input()
        if user_input == 'q':
            break
        elif user_input == '1':
            data = data_base.get_companies_and_vacancies_count()
            table.field_names = ['Компания', 'Количество вакансий']
            for d in data:
                table.add_row([d[0], d[1]])
            print(table)
        elif user_input == '2':
            data = data_base.get_all_vacancies()
            table.field_names = ['Компания', 'Вакансия', 'Зарплата от', 'Зарплата до', 'Ссылка']
            for d in data:
                table.add_row([d[0], d[1], d[2], d[3], d[4]])
            print(table)
        elif user_input == '3':
            data = data_base.get_avg_salary()
            print(f'Средняя зарплата по всем вакансиям: {data} руб.')
        elif user_input == '4':
            data = data_base.get_vacancies_with_higher_salary()
            table.field_names = ['Вакансия', 'Зарплата от', 'Зарплата до', 'Ссылка']
            for d in data:
                table.add_row([d[0], d[1], d[2], d[3]])
            print(table)
        elif user_input == '5':
            print('Введите ключевое слово:')
            name = input()
            data = data_base.get_vacancies_with_keyword(name)
            table.field_names = ['Вакансия', 'Зарплата от', 'Зарплата до', 'Ссылка']
            for d in data:
                table.add_row([d[0], d[1], d[2], d[3]])
            print(table)


def run() -> bool:
    print(print_user_choice)
    user_choice = int(input())
    if user_choice == 1:
        job_hh()
    elif user_choice == 2:
        job_bd()
    elif user_choice == 0:
        return True
