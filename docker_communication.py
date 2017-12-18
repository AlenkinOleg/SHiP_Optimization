import os
import numpy as np
import pandas as pd

from config import KINIT_USERNAME, KINIT_PASSWD, N_EVENTS

ShipOpt = str(os.getenv('SHIPOPT'))

def send_command(pitch, yoffset_layer, yoffset_plane, zshift_layer, zshift_plane, zshift_view, alpha):
    
    #send commands to docker container
    logining = "docker run --rm -v "+ShipOpt+"/output:/output oleg94/worker /bin/bash -c 'echo "+KINIT_PASSWD+" | kinit "+KINIT_USERNAME+"; "
    sourcing = "source /opt/FairShipRun/config.sh; "
    simulation = "python $SHIPOPT/code/objective.py --pitch "+str(pitch)+" --yoffset_layer "+str(yoffset_layer)+\
    " --yoffset_plane "+str(yoffset_plane)+" --zshift_layer "+str(zshift_layer)+" --zshift_plane "+\
    str(zshift_plane)+" --zshift_view "+str(zshift_view)+" --alpha "+str(int(alpha))+\
    " --nEvents "+str(N_EVENTS)+" --output /output/output.txt'"

    os.system(logining+sourcing+simulation)
    
    metrics = pd.read_csv(ShipOpt+"/output/output.txt", header=None)
    value = metrics[0][0]
    

    os.system("rm -rf "+ShipOpt+"/output/*")
    return value

def objective(point):

    pitch, yoffset_layer, yoffset_plane, zshift_layer, zshift_plane, zshift_view, alpha = list(point)      
    value = send_command(pitch, yoffset_layer, yoffset_plane, zshift_layer, zshift_plane, zshift_view, alpha)
    
    return value