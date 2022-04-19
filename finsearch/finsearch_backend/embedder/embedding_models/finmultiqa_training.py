"""
This example loads the pre-trained SentenceTransformer model 'multi-qa-MiniLM-L6-cos-v1' from the server.
It then fine-tunes this model for some epochs on the FinSemantic.
"""
import utils
import math
from torch.utils.data import DataLoader
from sentence_transformers import SentenceTransformer, losses, InputExample
from sentence_transformers.evaluation import EmbeddingSimilarityEvaluator
import logging

def process_data(data):
    new_data = []
    for row in data:
        input_ab = InputExample(texts=[row['sent_a'], row['sent_b']], label=float(row['rel_ab']))
        input_ac = InputExample(texts=[row['sent_a'], row['sent_c']], label=float(row['rel_ac']))
        new_data.append(input_ab)
        new_data.append(input_ac)
    return new_data

if __name__ == "__main__":
    # retrieve inputs
    model_save_path = f"../finsearch_embedder/models/finmultiqa"

    # create directory if does not exist
    utils.make_directory(model_save_path)

    # retrieve training data
    train_samples = process_data(utils.load_json("finsemantic/train.json"))
    dev_samples = process_data(utils.load_json("finsemantic/val.json"))
    test_samples = process_data(utils.load_json("finsemantic/test.json"))

    # Load pre-trained sentence transformer model
    model_name = 'multi-qa-MiniLM-L6-cos-v1'
    model = SentenceTransformer(model_name)

    # Set training batch size and epoch size
    train_batch_size = 16
    num_epochs = 4

    # Convert the dataset to a DataLoader ready for training
    logging.info("Read financial relation dataset")

    # generate train dataset
    train_dataloader = DataLoader(train_samples, shuffle=True, batch_size=train_batch_size)
    train_loss = losses.CosineSimilarityLoss(model=model)

    # Development set: Measure correlation between cosine score and gold labels
    evaluator = EmbeddingSimilarityEvaluator.from_input_examples(dev_samples, name='sts-dev')

    # Configure the training. We skip evaluation in this example
    warmup_steps = math.ceil(len(train_dataloader) * num_epochs * 0.1) #10% of train data for warm-up
    logging.info("Warmup-steps: {}".format(warmup_steps))

    # Train the model
    model.fit(
        train_objectives=[(train_dataloader, train_loss)],
        evaluator=evaluator,
        epochs=num_epochs,
        evaluation_steps=1000,
        warmup_steps=warmup_steps,
        output_path=model_save_path
    )

    # Load the stored model and evaluate its performance against test set
    model = SentenceTransformer(model_save_path)
    test_evaluator = EmbeddingSimilarityEvaluator.from_input_examples(test_samples, name='finsemantic-test')
    test_evaluator(model, output_path=model_save_path)