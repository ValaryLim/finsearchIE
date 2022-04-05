config_name="dyfinie_coarse"

rm -r "models/${config_name}"

allennlp train "training_config/${config_name}.jsonnet" \
    --serialization-dir "models/${config_name}" \
    --include-package dygie