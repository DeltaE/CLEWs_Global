import shutil
import os
from pathlib import Path


def copy_result(name):
    if not os.path.isdir(Path('results', 'data')):
        Path('results', 'data').mkdir(parents=True)
    shutil.copy(f"submodules/osemosys_global/results/{name}",
                f"results/{name}")


if __name__ == "__main__":
    if "snakemake" in globals():
        scenario = snakemake.params.scenario
        copy_result(scenario)