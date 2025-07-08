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

include: "../submodules/osemosys_global/workflow/rules/preprocess.smk"
include: "../submodules/osemosys_global/workflow/rules/model.smk"
include: "../submodules/osemosys_global/workflow/rules/postprocess.smk"
include: "../submodules/osemosys_global/workflow/rules/retrieve.smk"
include: "../submodules/osemosys_global/workflow/rules/validate.smk"
