import os
import pynndescent
import utils
import distance_metrics

def generate_index(dataname, direction=True):
    modelname = dataname.replace('train', 'model').split('.')[0]
    modelname += '_d' if direction else '_nd'
    modelname += '.pkl'
    
    print("Loading model...", modelname)

    if os.path.exists(modelname):
        index = utils.load_pkl(modelname)
        index.prepare()
    else:
        if direction:
            index = pynndescent.NNDescent(
                utils.load_numpy(dataname), 
                metric=distance_metrics.relation_cosine
            )
        else:
            index = pynndescent.NNDescent(
                utils.load_numpy(dataname), 
                metric=distance_metrics.relation_cosine_directionless
            )
        index.prepare()
        utils.save_pkl(modelname, index)
    return index
