import os
import shutil

# RULES
rule geographic_filter:
    message:
        'Applying geographic filter...'
    input: 
        csv_files = expand('workflow/submodules/osemosys_global/results/data/{csv}.csv', csv = OTOOLE_PARAMS),
    params:
        geographic_scope = config['geographic_scope'],
        res_targets = config['re_targets'],
        nodes_to_remove = config["nodes_to_remove"],
        in_dir = "workflow/submodules/osemosys_global/results/data",
        out_dir = "workflow/submodules/osemosys_global/results/{scenario}/data"
    output:
        csv_files = expand('workflow/submodules/osemosys_global/results/{{scenario}}/data/{csv}.csv', csv = OTOOLE_PARAMS),
    log:
        log = 'workflow/submodules/osemosys_global/results/{scenario}/logs/geographicFilter.log'
    script:
        '../submodules/osemosys_global/workflow/scripts/osemosys_global/geographic_filter.py'
