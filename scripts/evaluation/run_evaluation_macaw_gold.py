import os
import sys
import pandas as pd
from sklearn.metrics import classification_report
# set working directory
sys.path.append(os.getcwd())
import utils

macaw_to_label_mapping = {
    'direct': 'DIRECT',
    'indirect': 'INDIRECT',
    'not applicable': 'NA',
    'attribute': 'ATTRIBUTE',
    'function': 'FUNCTION',
    'positive': 'POSITIVE',
    'negative': 'NEGATIVE',
    'neutral': 'NEUTRAL',
    'conditional': 'CONDITION',
    'comparison': 'COMPARISON',
    'uncertain': 'UNCERTAIN',
    'unrelated': 'NONE',
}
predictions = ["macaw_1", "macaw_1_sentence", "macaw_1_abstract", "macaw_2", "macaw_2_sentence", "macaw_2_abstract"]

if __name__ == "__main__":
    data_dirs = [
        "data/predictions/macaw/macaw-large/rel_comb/finance/coarse_coref/", "data/predictions/macaw/macaw-large/rel_comb/finance/granular_coref/", \
        "data/predictions/macaw/macaw-large/rel_comb/external_zhiren/coarse/", "data/predictions/macaw/macaw-large/rel_comb/external_zhiren/granular/", \
        "data/predictions/macaw/macaw-large/rel_perm/finance/coarse_coref/", "data/predictions/macaw/macaw-large/rel_perm/finance/granular_coref/", \
        "data/predictions/macaw/macaw-large/rel_perm/external_zhiren/coarse/", "data/predictions/macaw/macaw-large/rel_comb/external_zhiren/granular/"
    ]

    for filedir in data_dirs:
        try:
            for filename in os.listdir(filedir):
                # process predictions
                df = pd.read_csv(filedir + filename)
                for label in predictions:
                    df[label] = df[label].apply(lambda x: macaw_to_label_mapping[x] if x in macaw_to_label_mapping else 'NA')  
                df = df.fillna('NA')
                df['R_bool'] = df['R'].apply(lambda x: True if x != 'NA' else False)
                labels = list(df['R'].unique())

                # compute metrics
                all_prediction_metrics = {}
                for colname in predictions:
                    prediction_metrics = {}
                    df[f'{colname}_bool'] = df[colname].apply(lambda x: True if x != 'NA' else False)
                    
                    # compute metrics for relation identification
                    report_bool = classification_report(y_true=df['R_bool'], y_pred=df[f'{colname}_bool'], output_dict=True)
                    A_bool, P_bool, R_bool, F_bool = report_bool['accuracy'], report_bool['True']['precision'], report_bool['True']['recall'], report_bool['True']['f1-score']
                    prediction_metrics['relation'] = {
                        'accuracy': A_bool, 'precision': P_bool, 'recall': R_bool, 'f1-score': F_bool
                    }
                    # compute metrics for relation labelling
                    report = classification_report(y_true=df['R'], y_pred=df[colname], output_dict=True)
                    for label in labels:
                        prediction_metrics[f'label_{label}'] = report[label]
                    prediction_metrics['label_weighted'] = report['weighted avg']
                    
                    all_prediction_metrics[colname] = prediction_metrics

                # construct and save dataframe
                all_prediction_metrics_restruct = {}
                for method in all_prediction_metrics.keys():
                    for label in all_prediction_metrics[method].keys():
                        for metric in all_prediction_metrics[method][label].keys():
                            if metric == "support":
                                continue
                            if (label, metric) not in all_prediction_metrics_restruct:
                                all_prediction_metrics_restruct[(label, metric)] = {}
                            all_prediction_metrics_restruct[(label, metric)][method] = all_prediction_metrics[method][label][metric]

                metrics_df = pd.DataFrame.from_dict(all_prediction_metrics_restruct)
                utils.make_dir('data/evaluations/' + filedir[17:])
                metrics_df.to_csv('data/evaluations/' + filedir[17:] + filename, index=True)
        except:
            continue


