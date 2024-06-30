from src.api_clients import HHClients


def main():
    name = input('Press enter to')
    hh_cleint = HHClients()
    result = hh_cleint.get_employer_vacancies(name)
    print(result)


if __name__ == '__main__':
    main()