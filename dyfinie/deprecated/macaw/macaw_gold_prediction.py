import os
import sys
import pandas as pd
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
# set working directory
sys.path.append(os.getcwd())
import utils

def generate_macaw_pred(model, tokenizer, input_string):
    try:
        input_ids = tokenizer.encode(input_string, return_tensors="pt")
        output = model.generate(input_ids, max_length=200)
        result = tokenizer.batch_decode(output, skip_special_tokens=True)
        return result[0].split('= ')[1] 
    except:
        return ''

def relation_twostep(model, tokenizer, e1, e2, context='', coarse=True):
    # generate mc options 
    if coarse:
        mcoptions = "(A) direct (B) indirect"
    else:
        mcoptions = "(A) attribute (B) function (C) positive (D) negative (E) neutral (F) unrelated (G) uncertain (H) comparison (I) conditional"
    
    # STEP 1: IDENTIFY IF RELATION EXISTS
    if len(context) != 0:
        input1 = f"$answer$ ; $question$ = Are {e1} and {e2} related? ; $context$ = {context} ; $mcoptions$ = (A) yes (B) no"
    else:
        input1 = f"$answer$ ; $question$ = Are {e1} and {e2} related? ; $mcoptions$ = (A) yes (B) no"
    
    # STEP 2: IDENTIFY EXACT RELATION (IF EXISTS)
    pred1 = generate_macaw_pred(model, tokenizer, input1)
    if pred1 == "yes":
        if len(context) != 0:
            input2 = f"$answer$ ; $question$ = What is the relation between {e1} and {e2}? ; $context$ = {context} ; $mcoptions$ = {mcoptions}"
        else:
            input2 = f"$answer$ ; $question$ = What is the relation between {e1} and {e2}? ; $mcoptions$ = {mcoptions}"
        pred2 = generate_macaw_pred(model, tokenizer, input2)
        return pred2
    return '' # no prediction

def relation_onestep(model, tokenizer, e1, e2, context='', coarse=True):
    # generate mc options
    if coarse: 
        mcoptions = "(A) direct (B) indirect (C) not applicable"
    else:
        mcoptions = "(A) attribute (B) function (C) positive (D) negative (E) neutral (F) unrelated (G) uncertain (H) comparison (I) conditional (J) not applicable"
    
    if len(context) != 0:
        input =  f"$answer$ ; $question$ = What is the relation between {e1} and {e2}? ; $context$ = {context} ; $mcoptions$ = {mcoptions}"
    else: 
        input = f"$answer$ ; $question$ = What is the relation between {e1} and {e2}? ; $mcoptions$ = {mcoptions}"
    return generate_macaw_pred(model, tokenizer, input)

if __name__ == "__main__":
    model_options = ["allenai/macaw-large", "allenai/macaw-answer-11b", "allenai/macaw-11b", "allenai/macaw-3b"]
    data_dirs = [
        "data/macaw/rel_comb/finance/coarse_coref/", "data/macaw/rel_comb/finance/granular_coref/", \
        "data/macaw/rel_comb/external_zhiren/coarse/", "data/macaw/rel_comb/external_zhiren/granular/", \
        "data/macaw/rel_perm/finance/coarse_coref/", "data/macaw/rel_perm/finance/granular_coref/", \
        "data/macaw/rel_perm/external_zhiren/coarse/", "data/macaw/rel_comb/external_zhiren/granular/"
    ]
    coarse_data = [True if "coarse" in x else False for x in data_dirs]
    
    for model_option in model_options:
        # load model
        tokenizer = AutoTokenizer.from_pretrained(model_option)
        model = AutoModelForSeq2SeqLM.from_pretrained(model_option)
        
        # predict on datasets
        for dir in data_dirs: 
            # create directory for predictions
            save_dir = "data/predictions/macaw/" + model_option.split('/')[-1] + dir[10:]
            utils.make_dir(save_dir)
            # check if coarse dataset
            is_coarse = True if "coarse" in dir else False
            # load all datasets
            for file in os.listdir(dir):
                # load data
                df = pd.read_csv(dir + file)
                # generate predictions 
                df["macaw_1"] = df.apply(lambda x: relation_onestep(model, tokenizer, x["E1"], x["E2"], coarse=is_coarse), axis=1)
                df["macaw_1_sentence"] = df.apply(lambda x: relation_onestep(model, tokenizer, x["E1"], x["E2"], context=x["sentence"], coarse=is_coarse), axis=1)
                df["macaw_1_abstract"] = df.apply(lambda x: relation_onestep(model, tokenizer, x["E1"], x["E2"], context=x["abstract"], coarse=is_coarse), axis=1)
                df["macaw_2"] = df.apply(lambda x: relation_twostep(model, tokenizer, x["E1"], x["E2"], coarse=is_coarse), axis=1)
                df["macaw_2_sentence"] = df.apply(lambda x: relation_twostep(model, tokenizer, x["E1"], x["E2"], context=x["sentence"], coarse=is_coarse), axis=1)
                df["macaw_2_abstract"] = df.apply(lambda x: relation_twostep(model, tokenizer, x["E1"], x["E2"], context=x["abstract"], coarse=is_coarse), axis=1)
                # save df
                df.to_csv(save_dir + file, index=False)
