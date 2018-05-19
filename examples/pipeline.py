# TODO: Add documentation

# System modules
import sys
import os.path
import pandas as pd

sys.path.insert(0, "engine")

# Project modules
from model import Model
import preprocessing as prep
from analysis import plot_corr_matrix
import data_bus as bus


def main():
    # Fetch, preprocess, and engineer input data
    raw_data = bus.fetch_data("MNIST")
    processed_data = (
        raw_data.pipe(preproc.first_stage)
        .pipe(preproc.second_stage)
        .pipe(preproc.third_stage)
        .pipe(preproc.fourth_stage)
    )
    feature_set = (
        processed_data.pipe(augment.first_feature)
        .pipe(augment.second_feature)
        .pipe(augment.third_feature)
        .pipe(augment.fourth_feature)
    )

    # Explore and analyze the dataset
    print(processed_data.describe())
    plot_corr_matrix(processed_data)

    # Define and train your models
    log_reg = Model(
        estimator="LogisticRegression",
        features=processed_data,
        selection_algo="RFE",
        hyperparameterization=True
    )
    rand_forest = Model(
        estimator="RandomForestClassifier",
        features=processed_data,
        selection_algo="RFE",
        hyperparameterization=True
    )
    grad_boost = Model(
        estimator="GradientBoostingMachine",
        features=processed_data,
        selection_algo="RFE",
        hyperparameterization=True
    )

    # Evaluation: Logistic Regression
    log_reg.plot_cnf_matrix()
    log_reg.cross_validate(
        method="RollingWindow",
        window_size=.9,
        test_size=.1
    )

    # Evaluation: Random Forest Classifier
    rand_forest.plot_cnf_matrix()
    rand_forest.cross_validate(method="Holdout")

    # Evaluation: Gradient Boosting Machine
    grad_boost.plot_cnf_matrix()
    grad_boost.cross_validate(method="Holdout")

    # Evaluation: Find and store the highest-performing model
    best_model = get_best_model(models=[log_reg, rand_forest, grad_boost], cross_val_method="Holdout")
    best_model.serialize("my_model")


if __main__ == "__main__":
    main()
