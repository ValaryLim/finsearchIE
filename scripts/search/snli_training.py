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
from datasets import load_dataset

#### Just some code to print debug information to stdout
logging.basicConfig(format='%(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO,
                    handlers=[LoggingHandler()])
#### /print debug information to stdout

# load dataset
snli_dataset = load_dataset('snli')

# Read the dataset
model_name = 'models/stsb-multi-qa-MiniLM-L6-cos-v1'
train_batch_size = 16
num_epochs = 4
model_save_path = 'models/snli-'+model_name

# Load a pre-trained sentence transformer model
model = SentenceTransformer(model_name)

# Convert the dataset to a DataLoader ready for training
logging.info("Read SNLI train dataset")

samples = {
    'train': [], 'validation': [], 'test': []
}

for sample in snli_dataset:
    for row in snli_dataset[sample]:
        score = abs(row['label']-2)/2
        print(row['premise'], row['hypothesis'])
        inp_example = InputExample(texts=[row['premise'], row['hypothesis']], label=score)
        samples[sample].append(inp_example)


# train_dataloader = DataLoader(samples['train'], shuffle=True, batch_size=train_batch_size)
# train_loss = losses.CosineSimilarityLoss(model=model)


# # Development set: Measure correlation between cosine score and gold labels
# logging.info("Read SNLI dev dataset")
# evaluator = EmbeddingSimilarityEvaluator.from_input_examples(samples['validation'], name='snli-dev')


# # Configure the training. We skip evaluation in this example
# warmup_steps = math.ceil(len(train_dataloader) * num_epochs * 0.1) #10% of train data for warm-up
# logging.info("Warmup-steps: {}".format(warmup_steps))


# # Train the model
# model.fit(train_objectives=[(train_dataloader, train_loss)],
#           evaluator=evaluator,
#           epochs=num_epochs,
#           evaluation_steps=1000,
#           warmup_steps=warmup_steps,
#           output_path=model_save_path)


# ##############################################################################
# #
# # Load the stored model and evaluate its performance on STS benchmark dataset
# #
# ##############################################################################

# model = SentenceTransformer(model_save_path)
# test_evaluator = EmbeddingSimilarityEvaluator.from_input_examples(samples['test'], name='snli-test')
# test_evaluator(model, output_path=model_save_path)