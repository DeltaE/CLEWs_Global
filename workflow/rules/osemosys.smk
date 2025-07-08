import os
import yaml
from snakemake.utils import min_version
min_version("8.0")

# configuration
workdir: "workflow/submodules/osemosys_global"


module other_workflow:
    # here, plain paths, URLs and the special markers for code hosting providers (see below) are possible.
    snakefile: "workflow/snakefile"

use rule * from other_workflow as other_*

use rule some_task from other_workflow as other_all with:
    message:
        "Generating input CSV data..."
    input:
        csv_files=expand('results/{scenario}/data/{csv}.csv',scenario=config['scenario'],csv=OTOOLE_PARAMS),
