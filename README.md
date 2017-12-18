# SHiP_Optimization
Make sure that gpy, gpyopt, numpy, pandas are installed.
To run optimization you can use 2 options: optimize objective locally or use cluster resources.

## Local running
For this way you need to have docker installed on your machine.
1. Pull docker containing necessary scripts:
```
docker pull oleg94/worker
```
2. Clone the repository and define new environment variable (you can choose any path for this repository).
```
git clone https://github.com/AlenkinOleg/SHiP_Optimization.git
export SHIPOPT=/SHiP_Optimization
```
Now you are ready to run experiment. File config.py contains your password, login for kinit and number of events for one point calculation.
Bayesian optimization consists of 2 parts: initial random design calculation, sampling of new points. There are two different scripts for these stages.

To run initial calculations:
```
python run_initialCalculation.py --nInitial 100
```

This script generates file observations/observations.csv, containig initial design. The same file will be used for the second stage of optimization.
```
python run_newPointsCalculation.py --nPoints 500 --nInitial 100
```

This script will add new points to file observations/observations.csv

## Running on Skygrid
For this way you should have access to SkyGrid cluster and jupyter notebook should be installed.
Full pipeline of optimization on skygrid is placed at Skygrid_optimization.ipynb
