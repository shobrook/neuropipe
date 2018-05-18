## Globals ##


import os
import pip
import pystache
import sys
import subprocess
import inquirer
from colorama import Fore, Style


## Helpers ##


def print_warn(warning):
    sys.stdout.write(warning) # TODO: Stylize


def print_error(error):
    sys.stdout.write(error) # TODO: Stylize


def prompt_yes_no(top_line='', bottom_line=''):
    """
    Asks user a Y/N question (stolen from @alichtman).

    @param top_line: question header/category
    @param bottom_line: the question
    @return: T/F depending on the user's answer
    """

    if top_line is '': # Only bottom_line should be printed and stylized
        questions = [inquirer.List(
            "choice",
            message=''.join([Fore.GREEN, Style.BRIGHT, bottom_line, Fore.YELLOW]),
            choices=[" Yes", " No"]
        )]
    else: # Both top and bottom_line should be printed and stylized
        sys.stdout.write(''.join([Fore.GREEN, Style.BRIGHT, ' ', top_line]))
        questions = [inquirer.List(
            "choice",
            message=''.join([Fore.GREEN, bottom_line, Fore.YELLOW]),
            choices=[" Yes", " No"]
        )]

    answers = inquirer.prompt(questions)

    return answers.get("choice").strip() == "Yes"


def decision_tree():
    """
    Questionnaire about a user's project to help select the right learning algorithms.

    @return: list of model names or None if the user's project involves unsupervised learning
    """

    # TODO: Add in the following questions:
    #   - (For classification) Are you predicting a binary class or multiple classes?
    #   -

    if prompt_yes_no(bottom_line="Are you predicting a category?"): # Classification
        if prompt_yes_no(bottom_line="Do you have labeled data?"):
            if prompt_yes_no(bottom_line="Does your dataset have less than 100K samples?"):
                return ["NaiveBayes", "KNeighbors", "SVC", "RandomForest"] # QUESTION: Include Gradient Boosting Machine?
            else:
                return ["SGDClassifier", "KernelApproximation"]
        else:
            return None
    elif prompt_yes_no(bottom_line="Are you predicting a quantity?"): # Regression
        if prompt_yes_no(bottom_line="Does your dataset have less than 100K samples?"):
            if prompt_yes_no(bottom_line="Should only a few features be important?"):
                return ["Lasso", "ElasticNet"]
            else:
                return ["RidgeRegression", "SVR"] # TODO: Add other ensemble regressors
        else:
            return ["SGDRegressor"]
    else:
        return None


def generate_project(project_name, install_dependencies=False):
    """
        Generate a project by following these steps:
            1. Iterate through the template directory
            2. Replace template variables in path names
            3. Read files
            4. Replace template variables in file contents
            5. Write files to project destination

    (stolen from @jimfleming)
    """

    project_config = {"project_name": project_name}

    # Copy template to current directory
    template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "template"))
    project_dir = os.getcwd()

    if not os.path.exists(template_dir):
        print_error(' '.join([template_dir, "containing template files does not exist"]))
        exit(1)

    # Recurse files and directories, replacing their filename with the
    # template string and the file contents with the template strings
    for root, dirs, files in os.walk(template_dir):
        rel_root = os.path.relpath(root, start=template_dir)
        for dirname in dirs:
            dest_dir = os.path.normpath(os.path.join(project_dir, rel_root, dirname))
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

            dest_path = os.path.normpath(os.path.join(project_dir, rel_root, filename))
            dest_path = pystache.render(dest_path, project_config)

            if os.path.exists(dest_path):
                print_warn(' '.join([dest_path, "already exists, skipping..."]))
                continue

            with open(src_path) as f:
                file_str = f.read()

            file_str = pystache.render(file_str, project_config)

            with open(dest_path, 'w') as f:
                f.write(file_str)

    sys.stdout.write(' '.join(["Project created:", project_dir]))

    if install_dependencies:
        pip.main(["install", '-r', "requirements.txt"])


## Main ##


def main():
    models = decision_tree()

    if models == None:
        sys.stdout.write("Sorry, neuropipe only supports supervised learning projects")
        sys.exit(0)
    else:
        generate_project("test_project")
        # TODO: Create project files


if __name__ == "__main__":
    main()
