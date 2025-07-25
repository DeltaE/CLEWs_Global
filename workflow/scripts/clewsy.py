import yaml
import pandas as pd
import numpy as np
import os
import shutil
from constants import ROOT_DIR


def modify_yaml(scenario, region_codes, timeslice, emissions):
    yaml_file =f"{ROOT_DIR}/config/clews_config/clewsy_template.yaml"
    with open(yaml_file, "r") as f:
        data = yaml.load(f, Loader=yaml.SafeLoader)
    data["Model"] = scenario
    data["otooleOutputDirectory"] = f"{ROOT_DIR}/results/{scenario}/clewsy"
    data["DataDirectoryName"] = f"{ROOT_DIR}/results/{scenario}/geoclews/summary_stats"
    data["OperationModes"] = f"{ROOT_DIR}/workflow/submodules/clewsy/optn_mds.txt"
    data["OsemosysGlobalPath"] = f"{ROOT_DIR}/results/{scenario}/osemosys_global"
    data["Years"] = pd.read_csv(f"{ROOT_DIR}/results/{scenario}/osemosys_global/YEAR.csv").VALUE.to_list()
    data["LandRegions"] = list(region_codes.keys())
    data["LandToGridMap"] = region_codes
    data["TimeSlice"] = timeslice
    for i in data["EndUseFuels"]:
        fuel_list = data["EndUseFuels"][i]
        for j in region_codes:
            fuel_list.append(f"ELC{region_codes[j]}02")
        data["EndUseFuels"][i] = fuel_list
    data["TransformationTechnologies"] = []
    for j in region_codes:
        data["TransformationTechnologies"].append([
            'PWRTRNA01', f'ELC{j}01', '1.11', f'ELC{j}02', '1', 'Power transmission Guyana', '1'])
    data["Emissions"] = {i: ['Carbon dioxide emissions.', '#000000'] for i in emissions}

    crop_list = pd.read_csv(f"{ROOT_DIR}/results/{scenario}/CROP.csv").to_dict()['FUEL'].values()
    data["CropYieldFactors"] = {
        i: 1 for i in crop_list
    }
    print(data)
    with open(f"{ROOT_DIR}/config/clews_config/clewsy.yaml", "w") as f:
        yaml.dump(data, f)


def crop_demand(scenario, country_full_name):
    def set_crop_code(row):
        if row["Item"] in other_crops:
            return "OTH"
        elif row["Item"] == np.nan:
            return "OTH"
        else:
            return row["Code"]


    data = pd.read_csv(f"{ROOT_DIR}/workflow/submodules/CLEWs_GAEZ/GAEZ_Processing/Data/FAOSTAT_2020.csv")
    filtered_data = data[data['Area'] == country_full_name]

    top_10_values = filtered_data.nlargest(10, 'Value')
    all_crops = top_10_values['Item'].tolist()

    other_crops = all_crops[5:]

    data = pd.read_csv(f"{ROOT_DIR}/data/FAOSTAT_production_2020.csv")
    filtered_data = data[data['Area'] == country_full_name]
    filtered_data = filtered_data[filtered_data['Item'].isin(all_crops)].set_index('Item')
    crop_code = pd.read_csv(
        f'{ROOT_DIR}/workflow/submodules/CLEWs_GAEZ/GAEZ_Processing/Data/Crop_code.csv').set_index('Name')
    data_classified = filtered_data.join(crop_code, how="left")[["Code", "Value"]].reset_index()
    data_classified["Code"] = data_classified.apply(set_crop_code, axis=1)
    data_summarized = data_classified.groupby(['Code']).sum('Value').to_dict()
    demand = data_summarized['Value']
    pd.DataFrame(data=demand.keys(), columns=["FUEL"]).to_csv(f"{ROOT_DIR}/results/{scenario}/CROP.csv", index=False)
    return demand


def demand_projection(demand, scenario, country_full_name, start_year, end_year):
    gdp = pd.read_excel(
        f"{ROOT_DIR}/workflow/submodules/osemosys_global/resources/data/default/iamc_db_GDPppp_Countries.xlsx",
        sheet_name="data")
    pop = pd.read_excel(
        f"{ROOT_DIR}/workflow/submodules/osemosys_global/resources/data/default/iamc_db_POP_Countries.xlsx",
        sheet_name="data")
    code = pd.read_csv(
        f'{ROOT_DIR}/workflow/submodules/CLEWs_GAEZ/GAEZ_Processing/Data/Country_code.csv').set_index(
        "Full_name").to_dict()  # More info: https://www.nationsonline.org/oneworld/country_code_list.htm
    country_code = code['country_code'][country_full_name]
    gdp = gdp[(gdp['Scenario'] == "SSP2") & (gdp['Region'] == country_code) & (gdp['Model'] == 'OECD Env-Growth')]
    pop = pop[(pop['Scenario'] == "SSP2") & (pop['Region'] == country_code) & (pop['Model'] == 'IIASA-WiC POP')]
    base_gdp = gdp.transpose().loc[[2010 + i for i in range(0, 95, 5)], ]
    base_gdp.rename(columns={base_gdp.columns[0]: 'GDP'}, inplace=True)
    base_pop = pop.transpose().loc[[2010 + i for i in range(0, 95, 5)], ]
    base_pop.rename(columns={base_pop.columns[0]: 'POP'}, inplace=True)
    df_gdp = pd.DataFrame(data=None, index=[2015 + i for i in range(end_year - 2015 + 1)])
    df_gdp = df_gdp.join(base_gdp, how="left")
    df = df_gdp.join(base_pop, how="left")
    result = df.astype(float).interpolate()
    result = result.loc[start_year:end_year]
    for column in result.columns:
        result[column] = result[column].apply(lambda x: x / result.loc[start_year, column] - 1)
    final_df = pd.DataFrame(columns=["REGION", "FUEL", "YEAR", "VALUE"])
    gdp_factor = 0
    pop_factor = 1
    for crop in demand:
        demand_data = (1 + result["GDP"] * gdp_factor + result["POP"] * pop_factor) * demand[crop]
        interim_df = pd.DataFrame({'YEAR': result.index, "VALUE": demand_data}, columns=["REGION", "FUEL", "YEAR", "VALUE"])
        interim_df["FUEL"] = f"CRP{crop}"
        final_df = pd.concat([final_df, interim_df], ignore_index=True)
    final_df["REGION"] = "GLOBAL"
    accumulated_a_demand = pd.read_csv(f"{ROOT_DIR}/results/{scenario}/clewsy/AccumulatedAnnualDemand.csv")
    final_df = pd.concat([final_df, accumulated_a_demand], ignore_index=True)
    final_df.to_csv(f"{ROOT_DIR}/results/{scenario}/clewsy/AccumulatedAnnualDemand.csv", index=False)


## TODO Make it snakemake processes
def main(scenario, region_codes, timeslice, country_full_name, emissions, start_year, end_year):

    shutil.copy(f"{ROOT_DIR}/results/{scenario}/osemosys_global/FUEL.csv",
                f"{ROOT_DIR}/results/{scenario}/osemosys_global/COMMODITY.csv")
    demand = crop_demand(scenario, country_full_name)
    modify_yaml(scenario, region_codes, timeslice, emissions)
    os.system("workflow/submodules/clewsy/src/build/clewsy.py config/clews_config/clewsy.yaml")
    with open(f"{ROOT_DIR}/results/{scenario}/clewsy/EMISSION.csv", "w") as f:
        f.write("VALUE\n")
        for i in emissions:
            f.write(f"{i}\n")

    demand_projection(demand, country_full_name, scenario, start_year, end_year)

    data_out_path = f"{ROOT_DIR}/results/{scenario}/clewsy"
    data_text = f"{ROOT_DIR}/results/{scenario}/data"
    clewsy_otoole_config = f"{ROOT_DIR}/config/clews_config/clewsy_otoole_config.yaml"
    os.system(f'otoole convert csv datafile {data_out_path} {data_text}.txt {clewsy_otoole_config}')
    os.system(f"python {ROOT_DIR}/config/clews_config/preprocess_data.py otoole {data_text}.txt {data_text}_pp.txt")

    os.system(
        f"glpsol -m {ROOT_DIR}/config/clews_config/osemosys_fast_preprocessed.txt -d {data_text}_pp.txt --wlp {data_text}.lp --check")
    os.system(f"cbc {data_text}.lp solve -solu {data_text}.sol")
    os.system(f"otoole -v results cbc csv {data_text}.sol {ROOT_DIR}/results/{scenario}/results datafile {data_text}.txt {clewsy_otoole_config}")
    print("clewsy finished successfully")


if __name__ == "__main__":
    if "snakemake" in globals():
        project_scenario = snakemake.config['scenario']
        project_region_codes = snakemake.config['region_codes']
        project_timeslice = snakemake.config['timeslice']
        project_country = snakemake.config['country_full_name']
        project_emissions = snakemake.config['emissions']
        project_start_year = snakemake.config['startYear']
        project_end_year = snakemake.config['endYear']

    else:
        project_scenario = "Guyana"
        project_region_codes = {
                  'GUY': 'GUYXX',
        }
        project_timeslice = {
              'S1D1': ['Season 1 intermediate', ''],
              'S1D2': ['Season 1 peak', ''],
              'S2D1': ['Season 2 intermediate', ''],
              'S2D2': ['Season 2 peak', '']
}
        project_country = 'Guyana'
        project_emissions = 'CO2GUY'
        project_start_year = 2021
        project_end_year = 2050
    main(project_scenario, project_region_codes, project_timeslice, project_country, project_emissions, project_start_year, project_end_year)
