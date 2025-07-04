import os
from pathlib import Path
ROOT_DIR = Path(__file__).parent.parent.parent


def main():
    os.system(f"python {ROOT_DIR}/submodules/CLEWs_GAEZ/GAEZ_Processing/main.py")


if __name__ == '__main__':
    main()
