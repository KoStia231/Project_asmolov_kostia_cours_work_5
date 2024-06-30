from src.api_clients import HHClients


def main():
    w = HHClients()
    q = w.employers_search('VK')
    print(q)


if __name__ == '__main__':
    main()