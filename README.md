# dspro2-swiss-receipt-extractor
Extract structured informationfrom swiss receipts - DSPRO2 HSLU project

## generate data

open receipts_generation/generate.ipynb.

set train and test data splits and run it.

this will generate train and test data and save the pre-processed images with the labels

## pre-processing

to preprocess an image call `extract_receipt(img)` from the file preprocessing/extraction/extract_receipt.py
