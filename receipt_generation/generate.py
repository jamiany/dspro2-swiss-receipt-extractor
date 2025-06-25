import json
import os
import shutil
from multiprocessing import Pool
from uuid import uuid4

import cv2
import numpy.random as rng

from base.receipt import generate_receipt_data, generate_label
from generate_html import generate_html_receipt
from preprocessing.extraction.extract_receipt import extract_receipt
from render_html import render_html


def generate_split(train, valid):
    if os.path.exists('out'):
        shutil.rmtree('out')
    os.mkdir('out')
    os.mkdir('out/train')
    os.mkdir('out/valid')

    rng.seed(42)

    generate('out/train', train)
    generate('out/valid', valid)


def generate(out_dir, count):
    key_map = {}

    for i in range(count):
        key_map[i] = generate_receipt_data()

    inputs = [(out_dir, count, name, data) for name, data in key_map.items()]

    with Pool() as pool:
        pool.map(process, inputs)


def process(input):
    out_dir, count, name, data = input

    # generate data
    generate_html_receipt(name, data)

    image_result = render_html(name)

    preprocessed = None
    try:
        preprocessed = extract_receipt(image_result)
    except Exception:
        pass

    # save the result
    number_places = len(str(count))
    if int(str(count)[0]) == 1:
        number_places -= 1
    filename = str(name).zfill(number_places) + '.jpg'

    if preprocessed is not None:
        cv2.imwrite(f'{out_dir}/{filename}', preprocessed)

    with open(f'{out_dir}/metadata.jsonl', 'a', encoding='utf8') as f:
        json.dump({"text": generate_label(data), "file_name": filename}, f, ensure_ascii=False)
        f.write('\n')

