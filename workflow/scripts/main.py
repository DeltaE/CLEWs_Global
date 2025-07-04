from pathlib import Path


def main():
    path = Path(__file__).parent.parent
    print(path)


if __name__ == '__main__':
    main()
