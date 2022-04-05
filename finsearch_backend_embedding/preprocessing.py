'''
Splits .jsonl relation files into index data and other data
'''
import utils
import numpy as np

data_list = [
    'data/finbert/coarse.jsonl',
    'data/finbert/granular.jsonl',
    'data/finmultiqa/coarse.jsonl',
    'data/finmultiqa/granular.jsonl',
    'data/msmarco/coarse.jsonl',
    'data/msmarco/granular.jsonl',
    'data/multiqa/coarse.jsonl',
    'data/multiqa/granular.jsonl',
]

if __name__ == "__main__":
    for dataname in data_list:
        data = utils.load_jsonl(dataname)
        dataname_value = dataname.split('.')[0]
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
        utils.save_numpy(f"{dataname_value}_train.npy", data_train)
        utils.save_jsonl(f"{dataname_value}_info.jsonl", data_info)