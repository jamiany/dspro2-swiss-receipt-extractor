# DSPRO2 - HSLU AI/ML Swiss Receipt Extractor

## Project Members

- Jamian Rajakone
- Tamino Walter
- Diego Gonzalez

## Short Project Description

We aim to analyze the semantics of receipts and use computer vision to extract the details of the purchased items and their prices, the shop name / address, and the date into a structured output. This output could be used by accounting software or other money related applications.
We don’t only try to reliably extract the data from receipts but we also want to find out if it is feasible to rely on synthetically generated data for model training.

## Data Description

Our goal is to train the model exclusively on synthetically created data. We generate this data with inspiration of real receipts and make them as realistic as possible to achieve good results in the training. This generated data will be labelled automatically.
We will also use real receipts, which we will manually label as validation and testing data. For cloud service integration, we want to use Google Cloud.
## Kanban Tool

We will use GitHub Projects as our Kanban tool.

## Experiment Tracking Tool

We will use Weights & Biases as our experiment tracking tool.

## Code Base

### Generate Data

open receipts_generation/generate.ipynb.

set train and test data splits and run it.

this will generate train and test data and save the pre-processed images with the labels

### Pre-processing

to preprocess an image call `extract_receipt(img)` from the file preprocessing/extraction/extract_receipt.py
