import json
import matplotlib.pyplot as plt

if __name__ == "__main__":
    dataset_name_model = [
        ["finance_coarse_coref", "bert"], ["finance_coarse", "finbert"], \
        ["finance_granular", "bert"], ["finance_granular", "finbert"]
    ]

    for dataset_name, bert_model in dataset_name_model:
        training_f1, validation_f1, best_validation_f1 = [], [], []
        for epoch_no in range(50):
            metric_file_path = f"data/model_epochs/{dataset_name}_{bert_model}/metrics_epoch_{str(epoch_no)}.json"
            with open(metric_file_path, "r") as file:
                metric_file = json.load(file)
                training_f1.append(metric_file[f"training__{dataset_name}__relation_f1"])
                validation_f1.append(metric_file[f"validation__{dataset_name}__relation_f1"])
                best_validation_f1.append(metric_file[f"best_validation__{dataset_name}__relation_f1"])
        
        plt.figure(figsize=(10,8))
        plt.plot(training_f1, label="train")
        plt.plot(validation_f1, label="val")
        plt.plot(best_validation_f1, "k--", label="best_val")
        plt.title(f"Best Epoch: {str(metric_file['best_epoch'])}", fontsize=20)
        plt.legend(loc="upper left", fontsize=16)
        plt.xlabel("epoch", fontsize=20)
        plt.ylabel("relation f1", fontsize=20)
        plt.axvline(x=metric_file['best_epoch'], linestyle=":", color="grey")
        plt.savefig(f"data/model_epochs/{dataset_name}_{bert_model}_validation_curve.jpg")