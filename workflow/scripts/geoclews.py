import os
from pathlib import Path
import shutil
ROOT_DIR = Path(__file__).parent.parent.parent


def main():
    shutil.copy(f". {ROOT_DIR}/config/config.yaml", f".{ROOT_DIR}/workflow/submodules/CLEWs_GAEZ/GAEZ_Processing/user_input/config.yaml")
    os.system(f"python {ROOT_DIR}/workflow/submodules/CLEWs_GAEZ/GAEZ_Processing/main.py")


if __name__ == '__main__':
    main()
