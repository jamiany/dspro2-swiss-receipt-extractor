import json
import os
from multiprocessing import Pool
from uuid import uuid4

import numpy.random as rng

from base.receipt import generate_receipt_data, generate_label
from generate_html import generate_html_receipt
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

    render_html(name)

    with open(f'temp/{name}.json', 'w') as f:
        f.write(json.dumps(generate_label(data), ensure_ascii=False))

    write_output(name)


def write_output(name):
    os.mkdir(f'out/{name}')
    os.rename(f'temp/{name}.png', f'out/{name}/input.png')
    os.rename(f'temp/{name}.json', f'out/{name}/label.json')

