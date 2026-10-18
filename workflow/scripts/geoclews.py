import yaml
import subprocess
import shutil
import os


def yaml_change(geoclews_path):
    with open('config/config.yaml', 'r') as f:
        config_dict = yaml.safe_load(f)

    with open(f"{geoclews_path}/GAEZ_Processing/user_input/config.yaml", 'r') as fo:
        geoclews_config = yaml.safe_load(fo)
    for item in geoclews_config:
        geoclews_config[item] = config_dict[item]
    with open(f"{geoclews_path}/GAEZ_Processing/user_input/config.yaml", 'w') as fo:
        yaml.safe_dump(
        geoclews_config, 
        fo, 
        allow_unicode=True, 
        sort_keys=False      
    )


def user_input_copy(geoclews_path):
    shapefiles = [i for i in os.listdir("data/user_input") if i.endswith(("cpg", "dbf", "prj", "shp", "shx"))]
    for shapefile in shapefiles:
        shutil.copy(f"data/user_input/{shapefile}", f"{geoclews_path}/GAEZ_Processing/user_input/shapefile/{shapefile}")


def geoclews_run(geoclews_path):
    try:
        subprocess.run(
            ["python", "GAEZ_Processing/main.py"],
            cwd = geoclews_path,
            check = True
        )
    except subprocess.CalledProcessError as e:
        print(f"GeoCLEWs failed: {e}")
        raise


if __name__ == '__main__':
    if "snakemake" in globals():
        directory = snakemake.config["geoclews"]["dir"]
    else:
        directory = "../CLEWs_GAEZ"
    yaml_change(directory)
    user_input_copy(directory)
    geoclews_run(directory)
