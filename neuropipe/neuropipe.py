#########
# GLOBALS
#########


import os
import pip
import pystache
import sys
import subprocess
import inquirer
from colorama import Fore, Style


#########
# HELPERS
#########


def print_warn(warning):
    print(warning)  # TODO: Stylize


def print_error(error):
    print(error)  # TODO: Stylize


def prompt_yes_no(prompt):
    """
    Asks user a Y/N question (written by @alichtman).

    @param prompt: Prompt message to display.
    @return: T/F depending on the user's answer
    """

    question = [inquirer.List(
        "choice",
        message=''.join([Fore.GREEN, Style.BRIGHT, prompt, Fore.YELLOW]),
        choices=[" Yes", " No"]
    )]
    answer = inquirer.prompt(question)

    return answer.get("choice").strip() == "Yes"


def decision_tree():
    """
    Questionnaire about a user's project to help select the right learning
    algorithms.

    @return: list of model names or None if the user's project involves
    unsupervised learning.
    """

    if prompt_yes_no("Are you predicting a category?"):  # Classification
        if prompt_yes_no("Do you have labeled data?"):
            if prompt_yes_no("Does your dataset have less than 100K samples?"):
                # QUESTION: Include Gradient Boosting Machine?
                return ["NaiveBayes", "KNeighbors", "SVC", "RandomForest"]
            else:
                return ["SGDClassifier", "KernelApproximation"]
        else:
            return None
    elif prompt_yes_no("Are you predicting a quantity?"):  # Regression
        if prompt_yes_no("Does your dataset have less than 100K samples?"):
            if prompt_yes_no("Should only a few features be important?"):
                return ["Lasso", "ElasticNet"]
            else:
                # TODO: Add other ensemble regressors
                return ["RidgeRegression", "SVR"]
        else:
            return ["SGDRegressor"]
    else:
        return None


def generate_project(project_name, models, install_dependencies=False):
    """
    Generates template files for a specific project (written by @jimfleming).

    @param project_name:
    @param install_dependencies:
    """

    project_config = {"project_name": project_name}

    # Copy template to current directory
    template_dir = os.path.abspath(os.path.join(
        os.path.dirname(__file__), "template"))
    project_dir = os.getcwd()

    if not os.path.exists(template_dir):
        print_error(
            ' '.join([template_dir, "containing template files does not exist"]))
        exit(1)

    # Recurse files and directories, replacing their filename with the
    # template string and the file contents with the template strings
    for root, dirs, files in os.walk(template_dir):
        rel_root = os.path.relpath(root, start=template_dir)
        for dirname in dirs:
            dest_dir = os.path.normpath(
                os.path.join(project_dir, rel_root, dirname))
            dest_dir = pystache.render(dest_dir, project_config)

            if os.path.exists(dest_dir):
                print_warn(' '.join([dest_dir, "already exists, skipping..."]))
                continue

            os.mkdir(dest_dir)

        for filename in files:
            _, extension = os.path.splitext(filename)
            if extension == ".pyc":
                continue

            src_path = os.path.join(root, filename)

            dest_path = os.path.normpath(
                os.path.join(project_dir, rel_root, filename))
            dest_path = pystache.render(dest_path, project_config)

            if os.path.exists(dest_path):
                print_warn(' '.join([dest_path, "already exists, skipping..."]))
                continue

            with open(src_path) as f:
                file_str = f.read()

            file_str = pystache.render(file_str, project_config)

            with open(dest_path, 'w') as f:
                f.write(file_str)

    print(' '.join(["Project created:", project_dir, '\n']))

    if install_dependencies:
        pip.main(["install", '-r', "requirements.txt"])


## Main ##


def main():
    models = decision_tree()

    if models:
        print_error(
            "Sorry, neuropipe only supports supervised learning projects")
        sys.exit(0)
    else:
        generate_project(sys.argv[1])


if __name__ == "__main__":
    main()
