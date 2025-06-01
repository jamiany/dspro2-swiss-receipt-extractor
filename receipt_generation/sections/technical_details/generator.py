from jinja2 import Template
import numpy.random as rng


def generate_technical_details(data):
    meta = data['meta']

    with open('sections/technical_details/template_1.html') as f:
        template = Template(f.read())

        date_formats = (
            "%d.%m.%Y",
            "%d.%m.%y",
            "%d-%b-%Y",
            "%d-%b-%y",
        )
        date_format = date_formats[rng.randint(0, len(date_formats))]

        time_formats = (
            "%H:%M",
            "%H:%M:%S",
        )
        time_format = time_formats[rng.randint(0, len(time_formats))]

        result = template.render({
            'date': meta['date'].strftime(date_format),
            'time': meta['time'].strftime(time_format),
        })

        return result
