#########
# GLOBALS
#########


import os
import time
import pandas as pd
import numpy as np
from sklearn.feature_extraction import DictVectorizer
from sklearn import datasets


#########
# HELPERS
#########


def load_from_dict(data, orient="columns"):
    return pd.DataFrame.from_dict(data, orient=orient)

    # vec = DictVectorizer()
    # return vec.fit_transform(data).toarray()


def load_from_csv(csv_path, delimiter):
    return pd.read_csv(csv_path, sep=delimiter)

    # return np.genfromtxt(csv_path, delimiter=delimiter)


#######
# BUSES
#######


def fetch_custom_data():
    return  # TODO


def fetch_toy_data(name):
    # TODO: Add more options

    if name == "DIGITS":
        dataset = datasets.load_digits()
    elif name == "IRIS":
        dataset = datasets.load_iris()

    data = np.c_[dataset["data"], dataset["target"]]
    columns = list(range(
        1, 65)) + ["target"] if name == "DIGITS" else list(dataset["feature_names"]) + ["target"]

    return pd.DataFrame(data=data, columns=columns)


def simulate_classification_data(n_samples=100, n_features=10, n_classes=3):
    # Create a simulated feature matrix and output vector with 100 samples,
    n_informative = int(.5 * n_features)
    features, target = datasets.make_classification(
        n_samples=n_samples,
        n_features=n_features,
        n_informative=n_informative,  # Features that are actually predictive
        n_redundant=n_features - n_informative,  # Features that are random
        n_classes=n_classes
    )

    data = pd.DataFrame(features, columns=list(range(n_features)))
    data["target"] = target

    return data


######
# MAIN
######


def Dataset(name):
    if name == "MY_DATASET":  # TODO: Change to the name of your dataset
        return fetch_custom_data()
    elif name in ("DIGITS", "IRIS"):
        return fetch_toy_data(name)
    elif name == "SIMULATED":
        return simulate_classification_data()

    class InvalidDataset(Exception):
        pass

    raise InvalidDataset("The dataset named {} does not exist.".format(name))
