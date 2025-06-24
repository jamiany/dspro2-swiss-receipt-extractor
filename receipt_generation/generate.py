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

    for _ in range(count):
        map[str(uuid4())] = generate_receipt_data()

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

    # Save the result
    if not os.path.exists(f'out/{name}'):
        os.mkdir(f'out/{name}')

    cv2.imwrite(f'out/{name}/input.jpg', image_result)
    if preprocessed is not None:
        cv2.imwrite(f'out/{name}/preprocessed.jpg', preprocessed)

    with open(f'out/{name}/label.json', 'w') as f:
        f.write(json.dumps(generate_label(data), ensure_ascii=False))

