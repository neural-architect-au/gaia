#!/bin/bash
source ~/.authenticate/authenticate.sh
authenticate --to=innovations-dev-au --artifactory=false > /dev/null 2>&1

pkill -f climate_runtime.py
python3 climate_runtime.py
