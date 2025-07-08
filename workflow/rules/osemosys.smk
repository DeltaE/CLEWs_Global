import os
import yaml
from snakemake.utils import min_version

min_version("8.0")

# configuration
workdir: "workflow/submodules/osemosys_global"
# helper functions

def get_otoole_data(otoole_config: str, var: str) -> list[str]:
    """Gets parameter/result files to be created"""

    assert var in ("param", "result", "set")

    with open(otoole_config) as f:
        otoole = yaml.safe_load(f)

    results = [x for x in otoole if otoole[x]["type"] == var]

    # no result calcualtions
    missing = [
        # storage investment not guaranteed
        "NewStorageCapacity",
        "TotalDiscountedStorageCost",
        "SalvageValueStorage",
        "CapitalInvestmentStorage",
        "DiscountedCapitalInvestmentStorage",
        "DiscountedSalvageValueStorage",
        "DiscountedCostByStorage",
        # storage levels not guaranteed
        "StorageLevelSeasonStart",
        "StorageLevelSeasonFinish",
        "StorageLevelYearStart",
        "StorageLevelYearFinish",
        "StorageLevelDayTypeStart",
        "StorageLevelDayTypeFinish",
        "StorageLowerLimit",
        "StorageUpperLimit",
        "CapitalInvestmentStorage",
        "DiscountedCapitalInvestmentStorage",
        "DiscountedCostByStorage",
        "DiscountedSalvageValueStorage",
        "NetChargeWithinDay",
        "NetChargeWithinYear",
        # other missing calcs
        "NumberOfNewTechnologyUnits",
        "Trade",
        "ModelPeriodEmissions",
    ]

    return [x for x in results if x not in missing]

OTOOLE_YAML = "resources/otoole.yaml"
OTOOLE_PARAMS = get_otoole_data(OTOOLE_YAML,"param")
OTOOLE_RESULTS = get_otoole_data(OTOOLE_YAML,"result")

COUNTRIES = config["geographic_scope"]

# rules
#
# include: "../submodules/osemosys_global/workflow/rules/preprocess.smk"
# include: "../submodules/osemosys_global/workflow/rules/model.smk"
# include: "../submodules/osemosys_global/workflow/rules/postprocess.smk"
# include: "../submodules/osemosys_global/workflow/rules/retrieve.smk"
# include: "../submodules/osemosys_global/workflow/rules/validate.smk"

module preprocess:
    snakefile: f"../submodules/osemosys_global/workflow/rules/preprocess.smk"
    prefix: "../submodules/osemosys_global/"

use rule * from preprocess as preprocess_*

module model:
    snakefile: f"../submodules/osemosys_global/workflow/rules/model.smk"
    prefix: "../submodules/osemosys_global/"

use rule * from model as model_*

module postprocess:
    snakefile: f"../submodules/osemosys_global/workflow/rules/postprocess.smk"
    prefix: "../submodules/osemosys_global/"

use rule * from postprocess as postprocess_*

module retrieve:
    snakefile: f"../submodules/osemosys_global/workflow/rules/retrieve.smk"
    prefix: "../submodules/osemosys_global/"

use rule * from retrieve as retrieve_*

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


rule generate_input_data:
    message:
        "Generating input CSV data..."
    input:
        csv_files = expand('results/{scenario}/data/{csv}.csv', scenario=config['scenario'], csv=OTOOLE_PARAMS),

rule make_dag:
    message:
        'dag created successfully and saved as docs/dag.pdf'
    shell:
        'snakemake --dag all | dot -Tpng > docs/_static/dag.png'

# rule dashboard:
#     message:
#         'Starting dashboard...'
#     shell:
#         'python workflow/scripts/osemosys_global/dashboard/app.py'

# cleaning rules

rule clean:
    message:
        'Reseting to defaults...'
    shell:
        'rm -rf results/*'

rule clean_data:
    shell:
        'rm -rf results/data/*'

rule clean_figures:
    shell:
        'rm -rf results/figs/*'
