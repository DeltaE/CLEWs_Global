
# Installation  
  
## Installation Steps  
  
> CLEWs Global is currently tested on **UNIX** systems. If you are using  Windows, we suggest you install [Windows Subsystem for Linux](https://docs.microsoft.com/en-us/windows/wsl/install)  
  
### 1. Clone Repository  
  
Users can clone the the CLEWs Global GitHub repository using HTTPS, SSH, or via the GitHub CLI. See GitHub docs for information on the different cloning methods.  
Using HTTPS  
  
```bash  
$ git clone https://github.com/DeltaE/CLEWs_Global.git --recurse-submodules
```  
  
### 2. Install Miniconda   
  
CLEWs Global uses `conda` to manage project dependencies. We recommend installing [miniconda](https://www.anaconda.com/docs/getting-started/miniconda/install). To verify that miniconda is installed, runt the command `conda info`. Information about your conda environment will be printed out. 

```bash
(base) $ conda info           
     active environment : base
    active env location : /home/xxx/miniconda3
            shell level : 1
       user config file : /home/xxx/.condarc
 populated config files : /home/xxx/miniconda3/.condarc
          conda version : 25.5.1
    conda-build version : not installed
         python version : 3.13.5.final.0
                 solver : libmamba (default)

...
```

### 3. Create the Environment 

CLEWs Global uses two conda environments, since it was built upon OSeMOSYS Global and GeoCLEWs. OSeMOSYS Global and GeoCLEWs are the submodules, which mange the project dependencies in a file that miniconda can read to create a new environment. Run command below from the root of CLEWs Global directory to create new environments called `osemosys-global` and `GeoCLEWs`.

```bash
(base) $ conda env create -f workflow/submodules/osemosys_global/workflow/envs/osemosys-global.yaml  

(base) $ conda env create -f workflow/submodules/CLEWs_GAEZ/environment.yml

```

Once installed, activate the new `osemosys-global` environment. You will now see `(osemosys-global)` at the start of your command prompt.

```bash
(base) $ conda activate osemosys-global
(osemosys-global) $ 
```

### 4. Install a Solver 

CLEWs Global supports `CBC` as its solver. Moreover, CLEWs Global uses `GLPK` to generate solver independent linear programming file. To run CLEWs Global, you **must** install `GLPK` and `CBC`. 

#### 4.1. Install GLPK

[GNU GLPK](https://www.gnu.org/software/glpk/) is an open-source linear programming package that **will be installed with the environment**. CLEWs Global uses it to create a linear programming files. To confirm that `GLPK` installed correctly, run the command `glpsol` in the command line. The following message should display. 

```bash 
(osemosys-global) $ glpsol

GLPSOL: GLPK LP/MIP Solver, v4.65
No input problem file specified; try glpsol --help
```

>If for any reason you need to install `GLPK`, you can do so using the command `conda install glpk`.

#### 4.2. Install CBC

[`CBC`](https://github.com/coin-or/Cbc) is open-source solver that **will be installed with the environment**. To confirm that `CBC` installed correctly, run the command `cbc` in the command line. The following message should display. Type `quit` to exit `CBC`.

```bash
(osemosys-global) $ cbc

Welcome to the CBC MILP Solver 
Version: 2.10.3 
Build Date: Mar 24 2020 

CoinSolver takes input from arguments ( - switches to stdin)
Enter ? for list of commands or help
Coin:
 ```

### 5. Prepare for Input Data

#### 5.1 Configuration
CLEWs Global uses `yaml` file for configuration. Modify `config/config.yaml` file to set up your model.

#### 5.2 Download Shapefiles 

GeoCLEWs with its adaptable design allows for running with any arbitrary shape and incorporating the geospatial characteristics of any geographical region. Additionally, users have the option to utilize the open-source [GADM](https://gadm.org/download_country.html) dataset , which provides various levels of administrative boundaries for all countries. With this flexibility, users can seamlessly tailor the analysis to their specific needs and explore a wide range of geospatial data. It is essential to make sure to follow the same naming format as provided in the examples.

- The 'GAEZ_Processing' folder includes the Jupyter Notebook code (GeoCLEWs.ipynb), required GAEZ and FAOSTAT resources in CSV format, and the 'Data' folder corresponding to the input and output data. Please ensure that all files within the 'GAEZ_Processing' folder are placed in the same directory in your local machine for seamless execution of the GeoCLEWs code.
- Download the shapefile for administrative boundary at level 0 from the [GADM](https://gadm.org/download_country.html) or any other sources. Place the file inside the 'Data/input' directory and rename it to "..._ adm0" where "..." represents the 3-letter ISO [country code](https://www.nationsonline.org/oneworld/country_code_list.htm). For instance, "KEN_adm0.shp" indicates the shapefile for the administrative boundary of Kenya. Admin level 0 is essential to include in all projects as it provides the outer boundary of the region.

Please note: Ensure that all necessary files, such as .shx, .shp, etc., are included. For example, for Kenya, you’ll need to input the following files: KEN_adm0.gpkg, KEN_adm0.prj, KEN_adm0.shp, KEN_adm0.shx, and so on.

- The second required shapefile for clustering can also be obtained from [GADM](https://gadm.org/download_country.html). Depending on the project specifications, users can download either the administrative level 0 or higher. The GAEZ data will be processed based on the admin level selected by the user in this step. Please store the shapefiles in the `workflow/submodules/CLEWs_GAEZ/GAEZ_Processing/user_input/shapefile` folder.

Note: Two datasets (two collections of shapefiles including "..._ adm0" and “…admX”) corresponding to the selected country need to be downloaded and placed inside the 'Data/input' folder. If processing at administrative level 0, the same dataset with different naming formats should be used and placed together in the same directory.

### 6. Run a Model

Run the command `snakemake -j6 --use-conda`. The time to build and solve the model will vary depending on your computer, but in general, this example will finish within minutes.

```bash
(base) ~/CLEWs_Global$ conda activate osemosys-global
(osemosys-global) ~/CLEWs_Global$
```
