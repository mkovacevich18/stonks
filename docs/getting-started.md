#Overview

This documentation aims to cover an analysis and methods to decide which options can be profitable. For options data, we will be pulling from Polygon.io (https://polygon.io/docs/rest/options/overview).

## Getting Started
So far, we have a uv/hatch managed `stonks` package. First, the repository should be cloned and then we can get started.

1. In the directory that contains the repository, run the command `hatch shell env create stonks-dev`. This will create a venv called `stonks-dev` with all the required packages. 

2. Each user must have their own API key for Polygon. The `data_preprocessing.py` script has been set up so that we can retrieve options data from the `Options Starter` plan and the 
    * This plan allows us to analyze the Greeks, historical options pricing, and various other "snapshots" of the stock.
    * The API KEY should also allow us to get access to the `Stocks Basics` plan.


