import os
import yaml
from snakemake.utils import min_version

min_version("8.0")

# configuration
workdir: "workflow/submodules/osemosys_global"
# helper functions



# rules
#
# include: "../submodules/osemosys_global/workflow/rules/preprocess.smk"
# include: "../submodules/osemosys_global/workflow/rules/model.smk"
# include: "../submodules/osemosys_global/workflow/rules/postprocess.smk"
# include: "../submodules/osemosys_global/workflow/rules/retrieve.smk"
# include: "../submodules/osemosys_global/workflow/rules/validate.smk"

for module_name in ["preprocess", "model", "retrieve", "postprocess", "validation"]:

    module:
        name: module_name
        snakefile: f"../submodules/osemosys_global/workflow/rules/{module_name}.smk"
        prefix: "../submodules/osemosys_global/"

    use rule * from module_name as module_name*


# handlers

onsuccess:
    shell(f"python workflow/scripts/osemosys_global/check_backstop.py {config['scenario']}")
    print('Workflow finished successfully!')

    # Will fix this in next update so that preprocessing steps dont always need to be rerun
    [f.unlink() for f in Path('results','data').glob("*") if f.is_file()]

onerror:
    print('An error occurred, please submit issue to '
          'https://github.com/OSeMOSYS/osemosys_global/issues')

# file creation check

if not os.path.isdir(Path('results','data')):
    Path('results','data').mkdir(parents=True)

# target rules

wildcard_constraints:
    scenario="[A-Za-z0-9]+"

