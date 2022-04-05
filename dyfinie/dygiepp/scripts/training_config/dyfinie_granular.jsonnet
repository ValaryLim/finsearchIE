local template = import "template.libsonnet";
local ffwd_hidden_size = std.parseInt(std.extVar('hidden_size'));
local ffwd_dropout = std.parseJson(std.extVar('dropout'));
local opt_lr = std.parseJson(std.extVar('learning_rate'));

template.DyGIE {
    bert_model: "ProsusAI/finbert",
    cuda_device: -1,
    data_paths: {
        train: "data/dyfinie_granular/normalized_data/train.json",
        validation: "data/dyfinie_granular/normalized_data/dev.json",
        test: "data/dyfinie_granular/normalized_data/test.json",
    },
    loss_weights: {
        ner: 0.2,
        relation: 1.0,
        coref: 1.0,
        events: 0.0
    },
    model +: {
        modules +: {
            coref +: {
                coref_prop: 1,
            }
        },
        feedforward_params +: {
            hidden_dims +: ffwd_hidden_size,
            dropout +: ffwd_dropout,
        }
    },
    trainer +: {
        optimizer +: {
            lr +: opt_lr,
        }
    },
    target_task: "relation",
}