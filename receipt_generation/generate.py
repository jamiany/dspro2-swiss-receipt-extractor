import json
import os
from multiprocessing import Pool
from uuid import uuid4

import cv2
import numpy.random as rng

from base.receipt import generate_receipt_data, generate_label
from generate_html import generate_html_receipt
from preprocessing.extraction.extract_receipt import extract_receipt
from render_html import render_html

def generate(count):
    rng.seed(42)

    map = {}

    for i in range(count):
        map[i] = generate_receipt_data()

    with Pool() as pool:
        pool.map(process, map.items())

def process(input):
    name, data = input

    generate_html_receipt(name, data)

    image_result = render_html(name)

    preprocessed = None
    try:
        preprocessed = extract_receipt(image_result)
    except Exception:
        pass

    filename = f'{name:03d}.jpg'
    cv2.imwrite(f'out/{filename}', preprocessed)

    with open(f'out/metadata.jsonl', 'a', encoding='utf8') as outfile:
        json.dump({"text":generate_label(data),"file_name":filename}, outfile, ensure_ascii=False)
        outfile.write('\n')