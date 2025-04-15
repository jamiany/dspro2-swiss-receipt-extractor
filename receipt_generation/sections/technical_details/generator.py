from jinja2 import Template


def generate_technical_details(data):
    meta = data['meta']

    with open('sections/technical_details/template_1.html') as f:
        template = Template(f.read())

        result = template.render({
            'date': meta['date'].strftime("%d.%m.%y"),
            'time': meta['time'].strftime("%H:%M"),
        })

        return result
