# Neuropipe

A beginner-friendly command-line tool for quickly setting up modular machine learning pipelines. Answer a series of questions about your project in the command-line, and a custom template will be created. The questions are based on the Scikit-Learn cheatsheet for selecting a learning algorithm:

![Scikit-Learn Cheatsheet](docs/cheatsheet.png)

Neuropipe was developed specifically for projects using Scikit-Learn.

<!--__Notable projects using neuropipe:__
* Poirot – plagiarism detection software
* BitVision – Bitcoin trading CLI that uses machine learning to predict price movements
* Sediment – program that predicts the quality of a wine given its physicochemical properties
* Aaron's LING 406 Project – program that classifies the sentiment of Bitcoin-related news headlines-->

## Usage

Install `neuropipe` with pip:

```
$ pip3 install neuropipe
 ```

Create an empty project directory:

```
$ mkdir my_project/
$ cd my_project/
```

Run `neuropipe my_project` and go through the decision tree to create your custom environment:

```
$ neuropipe my_project
```

## Workflow

A new project has the following file structure:

```bash
├── pipeline.py
├── engine/
│   ├── data_bus.py
│   ├── preprocessing.py
│   ├── model.py
│   └── analytics.py
├── data/
│   ├── raw.csv
│   └── processed.csv
├── models/
└── figures/
```

Where:
* `pipeline.py`: defines the entire pipeline, from fetching raw data to model evaluation – you run this
* `engine/`: holds all of the modules used in your pipeline
* `engine/data_bus.py`: 
* `engine/preprocessing.py`:
* `engine/model.py`:
* `engine/analytics.py`:
* `data/`:
* `models/`:
* `figures/`: 

Neuropipe adheres to the canonical model for a machine learning pipeline.

<!--## Pending Features
There's a lot of potential for this project. I'd like to turn this into a robust tool for easily scaffolding Scikit-Learn pipelines. Right now, the command-line questionnaire helps with generating custom `model.py` and `analytics.py` files, but in the future a user could provide more information about their dataset (i.e. if it's structured or unstructured, text, image, time series, etc.) and problem domain. That way, `preprocessing.py` could be populated with common preprocessing and data wrangling functions tailored to the user's task at hand. 
I'd also like to add more options for exploratory data analysis, feature selection, model evaluation, and cloud deployment.
* Easily generate random datasets, convert CSVs or dictionaries into dataframes, load toy datasets, or wrap your own functions for loading data
* Automatic caching for pre and post-processed datasets, so data doesn't have to be re-fetched (or scraped) on each run
* Use common data wrangling operations, such as breaking a list into n-sized sublists
* Answer a command-line questionnaire to automatically narrow down the learning algorithms available for you to test
* Use common model evaluation methods and metrics
* Visualize your dataset, the training process, and your results
* Serialize your pipeline and model
* Deploy as a Flask app
* Run preprocessing and training functions in parallel
