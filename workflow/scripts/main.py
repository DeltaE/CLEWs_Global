import os
from pathlib import Path
ROOT_DIR = Path(__file__).parent.parent.parent



def main():
    os.chdir(f'{ROOT_DIR}')


if __name__ == '__main__':
    main()
