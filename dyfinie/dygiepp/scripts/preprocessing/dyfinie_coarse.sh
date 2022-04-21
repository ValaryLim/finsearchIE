config_name="dyfinie_coarse"
out_dir="data/dyfinie_coarse"

mkdir $out_dir

# Normalize by adding dataset name.
python scripts/data/shared/normalize.py \
    $out_dir/processed_data/json \
    $out_dir/normalized_data/json \
    --file_extension=json \
    --max_tokens_per_doc=0 \
    --dataset=$config_name

# Collate for more efficient non-coref training.
python scripts/data/shared/collate.py \
    $out_dir/processed_data/json \
    $out_dir/collated_data/json \
    --file_extension=json \
    --dataset=$config_name


# # Train DyFinIE Model (No Tuning)
# rm -r "models/${config_name}"
# allennlp train "training_config/${config_name}.jsonnet" \
#     --serialization-dir "models/${config_name}" \
#     --include-package dygie