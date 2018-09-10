import os
import analysis
import preprocessing as pp
import matplotlib.pyplot as plt
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.externals import joblib
from sklearn.feature_selection import RFE

PARENT_DIR = os.path.dirname(os.getcwd())

class Model(object):
    def __init__(self, estimator, features, balance, normalize=True, feature_selection=None, hyperparameterization=False):
        self.estimator, self.balance = estimator, balance
        self.x_train, self.x_test, self.y_train, self.y_test = self.__split(features, test_size=.2)

        self.scaler = StandardScaler()
        self.scalar.fit(self.x_train)

        self.hyperparameterization, self.feature_selection = hyperparameterization, feature_selection

        self.__fit_model()

        self.y_pred = self.model.predict(self.scaler.transform(self.x_test))

    def __fit_model(self):
        if self.estimator == "LogisticRegression":
            if self.hyperparameterization:
                # Fit a model using a hyperparameter grid search
            else:
                self.model = LogisticRegression()
        elif self.estimator == "RandomForest":
            if self.hyperparameterization:
                # Fit a model using a hyperparameter grid search
            else:
                self.model = RandomForestClassifier()
        else:
            print("\tError: '%s' is not a valid model" % self.estimator)

    def _holdout_test(self):
        """Calculates the model's classification accuracy, sensitivity, precision, and specificity."""
        print("\t\tHoldout Validation Results:")

        print("\t\t\tAccuracy: ", analysis.accuracy(self.y_pred, self.y_test))
        print("\t\t\tPrecision: ", analysis.precision(self.y_pred, self.y_test))
        print("\t\t\tSpecificity: ", analysis.specificity(self.y_pred, self.y_test))
        print("\t\t\tSensitivity: ", analysis.sensitivity(self.y_pred, self.y_test))


    def _rolling_window_test(self, window_size, test_size, step=1):
        print("\t\tRolling Window Validation Results:")

        # TODO: Hide the STDOUT of pp.split() and _fit_model(), and prevent _fit_model() from saving a .pkl on each run

        windows = [self.features.loc[idx * step:(idx * step) + round(window_size * len(self.features))] for idx in range(int((len(self.features) - round(window_size * len(self.features))) / step))]
        decoupled_windows = [pp.split(window, test_size=test_size, balanced=False) for window in windows] # TODO: Do a nonrandom split to respect the temporal order of observations

        results = {"accuracy": [], "precision": [], "specificity": [], "sensitivity": []}
        for feature_set in decoupled_windows:
            self.x_train, self.x_test, self.y_train, self.y_test = feature_set

            self.scaler = StandardScaler()
            self.scaler.fit(self.x_train)

            self._fit_model()

            self.y_pred = self.model.predict(self.scaler.transform(self.x_test))

            results["accuracy"].append(analysis.accuracy(self.y_pred, self.y_test))
            results["precision"].append(analysis.precision(self.y_pred, self.y_test))
            results["specificity"].append(analysis.specificity(self.y_pred, self.y_test))
            results["sensitivity"].append(analysis.sensitivity(self.y_pred, self.y_test))

        print("\t\t\tAccuracy: ", str(sum(results["accuracy"]) / float(len(results["accuracy"]))))
        print("\t\t\tPrecision: ", str(sum(results["precision"]) / float(len(results["precision"]))))
        print("\t\t\tSpecificity: ", str(sum(results["specificity"]) / float(len(results["specificity"]))))
        print("\t\t\tSensitivity: ", str(sum(results["sensitivity"]) / float(len(results["sensitivity"]))))


    def _select_features(self):
        # Create a list of possible dataframes
        # For each df, split into train/test,


        return

    def cross_validate(self, method, window_size=.9, test_size=.1, step=1):
        if method == "Holdout":
            self._holdout_test()
        elif method == "RollingWindow":
            self._rolling_window_test(window_size, test_size, step)
        else:
            print("\t\tError: Invalid cross-validation method")


    """
    def print_feature_importances(self, data):
        for feat, importance in zip(data.drop(["Date", "Trend"], axis=1).columns, self.model.feature_importances_):
            print("\t\t\t" + feat + ": " + importance)
    """
