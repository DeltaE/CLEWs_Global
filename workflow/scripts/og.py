import yaml
import subprocess

def yaml_change(og_path):
    with open('config/config.yaml', 'r') as f:
        config_dict = yaml.safe_load(f)

    with open(f"{og_path}/config/config.yaml", 'r') as fo:
        og_config = yaml.safe_load(fo)
    for item in og_config:
        og_config[item] = config_dict[item]
    with open(f"{og_path}/config/config.yaml", 'w') as fo:
        yaml.safe_dump(
        og_config, 
        fo, 
        allow_unicode=True, 
        sort_keys=False      
    )


def og_run(og_path, jobs):
    try:
        subprocess.run(
            ["snakemake", "generate_input_data", '-j', str(jobs)],
            cwd = og_path,
            check = True
        )
    except subprocess.CalledProcessError as e:
        print(f"OSeMOSYS Global failed: {e}")
        raise


if __name__ == "__main__":
    if "snakemake" in globals():
        number_of_jobs = snakemake.config["osemosys"]["jobs"]
        osemosys_directory = snakemake.config["osemosys"]["dir"]
    else:
        number_of_jobs = 3
        osemosys_directory = "../osemosys_global"
    yaml_change(osemosys_directory)
    og_run(osemosys_directory, number_of_jobs)