from multiprocessing import Pool
from uuid import uuid4

import numpy.random as rng

from base.receipt import generate_receipt_data
from generate_html import generate_html_receipt
from render_html import render_html


def generate(count):
    rng.seed(42)

    map = {}

    for i in range(count):
        map[str(uuid4())] = generate_receipt_data()

    with Pool() as pool:
        pool.map(process, map.items())


def process(input):
    name, data = input

    generate_html_receipt(name, data)

    render_html(name)

