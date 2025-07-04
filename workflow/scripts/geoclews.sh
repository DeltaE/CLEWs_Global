#!/usr/bin/bash

eval "$(conda shell.bash hook)"
conda activate GeoCLEWs
python ../submodules/CLEWs_GAEZ/GAEZ_Processing/main.py