import os
import shutil
import errno


def main(og_path, geoclews_path, scenario):

    paths = [f'results', f'results/{scenario}']
    # Initialize output paths for data
    for output_path_raw in paths:
        output_path = f"{output_path_raw}"
        if not os.path.exists(output_path):
            try:
                os.makedirs(output_path)
            except OSError as exc:
                if exc.errno != errno.EEXIST:
                    raise
    shutil.copytree(f"{og_path}/results/{scenario}/data",
                    f'results/{scenario}/osemosys_global', dirs_exist_ok=True)
    shutil.copytree(f"{geoclews_path}/GAEZ_Processing/Data/output/{scenario}",
                    f'results/{scenario}/geoclews', dirs_exist_ok=True)


if __name__ == "__main__":
    # gets file paths
    if "snakemake" in globals():
        project_scenario = snakemake.config['scenario']
        osemosys_directory = snakemake.config["osemosys"]["dir"]
        geoclews_directory = snakemake.config["geoclews"]["dir"]
    else:
        project_scenario = "guyana"
        osemosys_directory = "../osemosys_global"
        geoclews_directory = "../CLEWs_GAEZ"
    main(osemosys_directory, geoclews_directory, project_scenario)



