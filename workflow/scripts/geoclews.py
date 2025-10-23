import os
import shutil
import pandas as pd
from constants import ROOT_DIR


def main():
    try:
        shutil.copyfile(f"{ROOT_DIR}/config/config.yaml",
                    f"{ROOT_DIR}/workflow/submodules/CLEWs_GAEZ/GAEZ_Processing/user_input/config.yaml")
        os.system(f"python {ROOT_DIR}/workflow/submodules/CLEWs_GAEZ/GAEZ_Processing/main.py")
    except shutil.SameFileError:
        os.remove(f'{ROOT_DIR}/workflow/submodules/CLEWs_GAEZ/GAEZ_Processing/user_input/config.yaml')
        shutil.copyfile(f"{ROOT_DIR}/config/config.yaml",
                    f"{ROOT_DIR}/workflow/submodules/CLEWs_GAEZ/GAEZ_Processing/user_input/config.yaml")
        os.system(f"python {ROOT_DIR}/workflow/submodules/CLEWs_GAEZ/GAEZ_Processing/main.py")



if __name__ == '__main__':
    main()
