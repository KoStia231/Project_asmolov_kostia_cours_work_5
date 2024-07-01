from src.user_interactive.utils import start_massage, run


def main():
    print(start_massage)
    while True:
        result = run()
        if result:
            break


if __name__ == '__main__':
    main()
