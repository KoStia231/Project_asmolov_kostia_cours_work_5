from src.api_clients import HHClients
from src.db.loader import load_employers, load_vacancies
from src.db.manager import PostgresDBManager
from src.db.migrations import create_database, apply_migrations


def search():
    while True:
        print('-'*33, '  ДЛЯ ОСТАНОВКИ ВВЕДИТЕ "стоп"  ', '-'*33)
        print('-' * 37, '  ВВЕДИТЕ ИМЯ КОМПАНИИ  ', '-' * 37)
        name = input()
        if name != 'стоп'.lower():
            client = HHClients()
            results = client.employers_search(name)
            for result in results:
                print(result)
            print('-' * 100)
        else:
            break


def main():
    create_database()
    apply_migrations()
    load_employers()
    load_vacancies()
    db = PostgresDBManager()
    res = db.get_companies_and_vacancies_count()
    print(res)




if __name__ == '__main__':
    main()

