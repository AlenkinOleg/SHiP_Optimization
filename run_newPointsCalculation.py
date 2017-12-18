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

N_POINTS = 100
N_INITIAL = 100
ShipOpt = str(os.getenv('SHIPOPT'))

if __name__=='__main__':
    
    argv = sys.argv[1:]

    try:
        opts, args = getopt.getopt(argv, "", ["nEvents=", "nPoints=", "nInitial="])
    except getopt.GetoptError:
        print("Wrong options were used.\n")
        sys.exit(2)
        
    for opt, arg in opts:
        if opt == "--nEvents":
            N_EVENTS = int(arg)
        elif opt == "--nPoints":
            N_POINTS = int(arg)
        elif opt == "--nInitial":
            N_Initial = int(arg)
    
    if 'observations.csv' in os.listdir(ShipOpt+'/observations/'):
        observations = pd.read_csv(ShipOpt+'/observations/observations.csv')
    else:
        observations = pd.DataFrame(columns=['pitch', 'yoffset_layer', 'yoffset_plane', 'zshift_layer',\
                                             'zshift_plane', 'zshift_view', 'angle', 'objective'])
    
    feasible_region = GPyOpt.Design_space(space=space, constraints=constraints)

    for num_i in range(N_POINTS):

        step_X = observations[observations.columns[:-1]].values
        #because we want to maximize
        step_Y = -observations[observations.columns[-1:]].values
        ignored_X = step_X[np.isnan(step_Y.ravel(), dtype=np.float64)]
        step_X = step_X[~np.isnan(step_Y.ravel(), dtype=np.float64)]
        step_Y = step_Y[~np.isnan(step_Y.ravel(), dtype=np.float64)]
        bo = GPyOpt.methods.BayesianOptimization(f=None, domain=space, constraints=constraints, X=step_X,\
                                                 Y=step_Y, de_duplication=True, initial_design_numdata=N_INITIAL)
        new_point = bo.suggest_next_locations(ignored_X=ignored_X)[0]
        new_value = objective(new_point)
        observations.loc[len(observations)] = list(new_point) + [new_value]
        observations.to_csv(ShipOpt+"/observations/observations.csv", index=False)