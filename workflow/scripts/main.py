import os
from pathlib import Path
ROOT_DIR = Path(__file__).parent.parent.parent



def main():
    os.chdir(f'{ROOT_DIR}/submodules/osemosys_global')
    os.system("snakemake -j 10")


if __name__ == '__main__':
    main()
