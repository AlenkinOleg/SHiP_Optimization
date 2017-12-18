min_dist = 3.6

space = [{'name': 'pitch', 'type': 'continuous', 'domain': (min_dist, min_dist)},\
         {'name': 'yoffset_layer', 'type': 'continuous', 'domain': (min_dist/2, min_dist)},\
         {'name': 'yoffset_plane', 'type': 'continuous', 'domain': (min_dist*0.25, min_dist*1.25)},\
         {'name': 'zshift_layer', 'type': 'continuous', 'domain': (1.6, 2.6)},\
         {'name': 'zshift_plane', 'type': 'continuous', 'domain': (3.8, 6.8)},\
         {'name': 'zshift_view', 'type': 'continuous', 'domain': (10, 10)},\
         {'name': 'alpha', 'type': 'discrete', 'domain': (5, 5)}]

constraints = [{'name': 'constr_1', 'constrain': '-(x[:,0]-x[:,1])**2-x[:,3]**2+2**2'},\
               {'name': 'constr_2', 'constrain': '-(x[:,1]-x[:,2])**2-(x[:,3]-x[:,4])**2+2**2'},\
               {'name': 'constr_3', 'constrain': 'x[:,3]+x[:,4]+2-x[:,5]'}]
