from src.api_clients import HHClients
from src.config import settings


def search():
    while True:
        print('-'*37, '  ВВЕДИТЕ ИМЯ КОМПАНИИ  ', '-'*37)
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
    print(settings.get_employee_ids())



if __name__ == '__main__':
    main()