import numpy as np
import pandas as pd
import GPy
import GPyOpt
import os
import sys
import getopt

from optimization_space import space, constraints
from config import KINIT_USERNAME, KINIT_PASSWD, N_EVENTS
from docker_communication import objective

N_INITIAL = 100
ShipOpt = str(os.getenv('SHIPOPT'))

if __name__=='__main__':
    
    argv = sys.argv[1:]

    try:
        opts, args = getopt.getopt(argv, "", ["nInitial="])
    except getopt.GetoptError:
        print("Wrong options were used.\n")
        sys.exit(2)
        
    for opt, arg in opts:
        if opt == "--nInitial":
            N_INITIAL = int(arg)
    
    if 'observations.csv' in os.listdir(ShipOpt+'/observations/'):
        observations = pd.read_csv(ShipOpt+'/observations/observations.csv')
    else:
        observations = pd.DataFrame(columns=['pitch', 'yoffset_layer', 'yoffset_plane', 'zshift_layer',\
                                             'zshift_plane', 'zshift_view', 'angle', 'objective'])
    
    feasible_region = GPyOpt.Design_space(space=space, constraints=constraints)

    while len(observations) < N_INITIAL:
        
        new_point = GPyOpt.experiment_design.initial_design('random', feasible_region, 1)[0]
        new_value = objective(new_point)
        observations.loc[len(observations)] = list(new_point) + [new_value]
        observations.to_csv(ShipOpt+"/observations/observations.csv", index=False)