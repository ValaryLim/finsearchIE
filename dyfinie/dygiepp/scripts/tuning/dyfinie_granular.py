import optuna

def objective(trial: optuna.Trial) -> float:
    trial.suggest_int("hidden_size", 64, 512)
    trial.suggest_float("dropout", 0.0, 0.5)
    trial.suggest_float("learning_rate", 1e-5, 1e-2, log=True)

    executor = optuna.integration.allennlp.AllenNLPExecutor(
        trial=trial,  # trial object
        config_file="./training_config/dyfinie_granular.jsonnet",  # jsonnet path
        serialization_dir=f"./result/dyfinie_granular/{trial.number}",  # directory for snapshots and logs
        metrics='+MEAN__relation_f1',
        include_package="dygie"
    )
    return executor.run()


if __name__ == "__main__":
    study_name = "dyfinie_granular"

    study = optuna.create_study(
        storage=f"sqlite:///{study_name}.db",  # save results in DB
        sampler=optuna.samplers.TPESampler(seed=24),
        study_name=study_name,
        direction="maximize",
        pruner=optuna.pruners.HyperbandPruner()
    )

    timeout = 60 * 60 * 10  # timeout (sec): 60*60*10 sec => 10 hours

    study.optimize(
        objective,
        n_jobs=1,  # number of processes in parallel execution
        n_trials=30,  # number of trials to train a model
        timeout=timeout,  # threshold for executing time (sec)
    )

    optuna.integration.allennlp.dump_best_config(f"./training_config/{study_name}.jsonnet", f"./hyperparams/{study_name}.json", study)