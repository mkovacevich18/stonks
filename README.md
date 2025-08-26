# Stonks
Documenting a (mis)adventure for quantitative finance/data science. The goal of this repository is to perform analysis of various stock/options tickers and strategies. Our goal is to implement a strategy, back test it, and further develop.

## Set Up
To set up this repository and run it locally, there are two things that must occur. 
1. Create a venv via the pyproject.toml in this repository. To do so, run the command `hatch env create stonks-dev`. This will create a venv named `stonks-dev` that we can use. If on the CLI, then run `hatch shell stonks-dev` to activate the venv. In this scenario, we are running it via VScode so VScode will find the venv and allow us to use it.
2. We have a `.env` file that is stored locally and purposefully ignored when pushing to github since it contains an API key. In this `.env` place your Polygon.io API key (something like `POLYGON_API_KEY = xxxxyyyyy....`). The `options.ipynb` notebook will automatically find this key and use it in our current set up.





