## To Start 

### 1. Install Tools
- Install OSeMOSYS Global (https://github.com/OSeMOSYS/osemosys_global.git)
- Install Clewsy (https://github.com/OSeMOSYS/clewsy.git)
- Install CLEWs_GAEZ (https://github.com/OSeMOSYS/CLEWs_GAEZ.git)

### 2. Run Tools
- Use `config/osemosys-global/config.yaml` to run OSeMOSYS Global
- Use `config/geoCLEWs/GeoCLEWs.ipynb` to run GeoCLEWs (Please copy this file and paste it into `CLEWs_GAEZ/GAEZ_Processing` folder)
- Copy and paste files under `config/clewsy` to clewsy folder and run clewsy
1) ./src/build/clewsy.py CLEWS-GUY.yaml
2) otoole convert csv datafile data-out data-test.txt clewsy_otoole_config.yaml
3) python preprocess_data.py otoole data-test.txt data-test-pp.txt
4) glpsol -m OSeMOSYS-pp.txt -d data-test-pp.txt --wlp data.lp --check
5) cbc data.lp solve -solu dataGUY.sol
6) otoole -v results cbc csv dataGUY.sol results csv data-out config_otoole.yaml
