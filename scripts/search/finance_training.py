"""
This example loads the pre-trained SentenceTransformer model 'nli-distilroberta-base-v2' from the server.
It then fine-tunes this model for some epochs on the STS benchmark dataset.
Note: In this example, you must specify a SentenceTransformer model.
If you want to fine-tune a huggingface/transformers model like bert-base-uncased, see training_nli.py and training_stsbenchmark.py
"""
from torch.utils.data import DataLoader
import math
from sentence_transformers import SentenceTransformer, LoggingHandler, losses, InputExample
from sentence_transformers.evaluation import EmbeddingSimilarityEvaluator
import logging
import os
import sys

sys.path.append(os.getcwd())
import utils

#### Just some code to print debug information to stdout
logging.basicConfig(format='%(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO,
                    handlers=[LoggingHandler()])

# Read the dataset
model_name = 'msmarco-MiniLM-L6-cos-v5'
train_batch_size = 16
num_epochs = 4
model_save_path = 'models/fin-msmarco'

# Load a pre-trained sentence transformer model
model = SentenceTransformer(model_name)

# Convert the dataset to a DataLoader ready for training
logging.info("Read financial relation dataset")

def process_data(data):
    new_data = []
    for row in data:
        input_ab = InputExample(texts=[row['sent_a'], row['sent_b']], label=float(row['rel_ab']))
        input_ac = InputExample(texts=[row['sent_a'], row['sent_c']], label=float(row['rel_ac']))
        new_data.append(input_ab)
        new_data.append(input_ac)
    return new_data

train_samples = process_data(utils.load_json("data/finsearch/train.json"))
dev_samples = process_data(utils.load_json("data/finsearch/val.json"))
test_samples = process_data(utils.load_json("data/finsearch/test.json"))

train_dataloader = DataLoader(train_samples, shuffle=True, batch_size=train_batch_size)
train_loss = losses.CosineSimilarityLoss(model=model)

# Development set: Measure correlation between cosine score and gold labels
evaluator = EmbeddingSimilarityEvaluator.from_input_examples(dev_samples, name='sts-dev')

# Configure the training. We skip evaluation in this example
warmup_steps = math.ceil(len(train_dataloader) * num_epochs * 0.1) #10% of train data for warm-up
logging.info("Warmup-steps: {}".format(warmup_steps))

# Train the model
model.fit(train_objectives=[(train_dataloader, train_loss)],
          evaluator=evaluator,
          epochs=num_epochs,
          evaluation_steps=1000,
          warmup_steps=warmup_steps,
          output_path=model_save_path)


##############################################################################
#
# Load the stored model and evaluate its performance on STS benchmark dataset
#
##############################################################################

model = SentenceTransformer(model_save_path)
test_evaluator = EmbeddingSimilarityEvaluator.from_input_examples(test_samples, name='fin-test')
test_evaluator(model, output_path=model_save_path)