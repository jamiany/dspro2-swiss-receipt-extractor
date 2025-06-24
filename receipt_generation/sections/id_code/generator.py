import numpy as np
import numpy.random as rng
from jinja2 import Template


def generate_id_code(data):

    templates = [
        'template_1',
        'template_2',
    ]

    name = templates[rng.randint(len(templates))]

    with open(f'sections/id_code/{name}.html', encoding='utf-8') as f:
        template = Template(f.read())

        digit6 = rng.randint(0, 1_000_000)
        digit14_1 = rng.randint(0, np.int64(100_000_000_000_000), dtype=np.int64)
        digit14_2 = rng.randint(0, np.int64(100_000_000_000_000), dtype=np.int64)

        result = template.render({
            'digit28': str(digit14_1).zfill(14) + str(digit14_2).zfill(14),
            'digit33': str(digit14_1).zfill(14) + str(digit14_2).zfill(14) + str(digit6).zfill(6),
        })

        return result
