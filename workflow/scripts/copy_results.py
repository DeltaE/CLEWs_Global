import os
import shutil
import errno
from constants import ROOT_DIR


def main(scenario):

    paths = [f'{ROOT_DIR}/results', f'{ROOT_DIR}/results/{scenario}']
    # Initialize output paths for data
    for output_path_raw in paths:
        output_path = f"{output_path_raw}"
        if not os.path.exists(output_path):
            try:
                os.makedirs(output_path)
            except OSError as exc:
                if exc.errno != errno.EEXIST:
                    raise
    shutil.copytree(ROOT_DIR / f"workflow/submodules/osemosys_global/results/{scenario}/data",
                    ROOT_DIR / f'results/{scenario}/osemosys_global', dirs_exist_ok=True)
    shutil.copytree(ROOT_DIR / f"workflow/submodules/CLEWs_GAEZ/GAEZ_Processing/Data/output/{scenario}",
                    ROOT_DIR / f'results/{scenario}/geoclews', dirs_exist_ok=True)


if __name__ == "__main__":
    # gets file paths
    if "snakemake" in globals():
        project_scenario = snakemake.config['scenario']
    else:
        project_scenario = "guyana"
    main(project_scenario)



