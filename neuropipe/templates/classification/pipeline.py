# TODO: Add documentation

from engine.data_bus import Dataset
from engine.transformers import Transformer
from engine.analysis import Analyze
from engine.model import Model, get_best_model

def main():
    # Fetch and preprocess your dataset
    raw_data = Dataset("MNIST") # TODO: Replace MNIST with your desired dataset name
    processed_data = (
        raw_data.pipe(Transformer("MY_FIRST_TRANSFORM"))
        .pipe(Transformer("MY_SECOND_TRANSFORM"))
        .pipe(Transformer("MY_THIRD_TRANSFORM"))
    )

    # Explore and visualize your dataset
    Analyze(processed_data, type="CorrelationMatrix")

    # TODO: Train models in parallel

    # Define and train your models
    rand_forest = Model(
        estimator="RandomForestClassifier",
        features=processed_data,
        balance=True,
        normalize=True,
        feature_selection="RFE",
        hyperparameterization=True
    )
    grad_boost = Model(
        estimator="GradientBoostingMachine",
        features=processed_data,
        balance=False,
        normalize=True,
        feature_selection="RFE",
        hyperparameterization=True
    )
    log_reg = Model(
        estimator="LogisticRegression",
        features=processed_data,
        balance=True,
        normalize=True,
        feature_selection="RFE",
        hyperparameterization=True
    )

    # Evaluation: Confusion Matrices
    rand_forest_conf_matrix = ConfusionMatrix(rand_forest)
    grad_boost_conf_matrix = ConfusionMatrix(grad_boost)
    log_reg_conf_matrix = ConfusionMatrix(log_reg)

    # Evaluation: Cross Validation
    rand_forest_eval = CrossValidate(model=rand_forest, method="Holdout")
    grad_boost_eval = CrossValidate(model=grad_boost, method="Holdout")
    log_reg_eval = CrossValidate(
        model=log_reg,
        method="RollingWindow",
        window_size=.9,
        test_size=.1
    )

    # Find and store the highest-performing model
    best_model = BestModel()
    best_model = BestModel([log_reg_eval, rand_forest_eval, grad_boost_eval])
    best_model.serialize("my_model")

if __main__ == "__main__":
    main()
