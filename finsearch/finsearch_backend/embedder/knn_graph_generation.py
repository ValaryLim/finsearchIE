'''
Preprocessing Step to Generate k-Nearest Neighbours Graph

Reads coarse.jsonl and granular.jsonl relation files
Splits files into graph data and miscellaneous (author, date, etc) data
Saves data into same file directory

To run this file, call:
python preprocessing.py (model_name)
'''
import os
import sys
import utils
import numpy as np

if __name__ == "__main__":
    # retrieve input embedder name
    embedder_name = sys.argv[1]
    
    # generate embedder path
    embedder_path = f"finsearch_embedder/data/{embedder_name}/"

    # return error if does not exist
    if not os.path.exists(embedder_path):
        raise NameError("Embedder path does not exist. Embedder is not valid name.")
    
    # generate data paths
    data_names = [f"{embedder_path}/coarse.jsonl", f"{embedder_path}/granular.jsonl"]
    info_names = [f"{embedder_path}/coarse_info.jsonl", f"{embedder_path}/granular_info.jsonl"]
    embd_names = [f"{embedder_path}/coarse_train.npy", f"{embedder_path}/granular_train.npy"]
    
    for i in range(len(data_names)):
        # extract info
        dataname, infoname, embdname = data_names[i], info_names[i], embd_names[i]

        # retrieve data
        data = utils.load_jsonl(dataname)

        # convert to array
        data_train = np.array([np.array(x['E1_CODE'] + x['E2_CODE']) for x in data])
        data_info = [{
            'E1': x['E1'], 
            'E2': x['E2'], 
            'E1_START': x['E1_START'], 
            'E1_END': x['E1_END'], 
            'E2_START': x['E2_START'], 
            'E2_END': x['E2_END'], 
            'REL': x['REL'], 
            'DOC_KEY': x['DOC_KEY']
        } for x in data]

        # save split data
        utils.save_numpy(embdname, data_train)
        utils.save_jsonl(infoname, data_info)