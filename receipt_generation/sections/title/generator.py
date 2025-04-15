from jinja2 import Template


def generate_title(data):
    shop = data['shop']

    with open('sections/title/template_title.html') as f:
        template = Template(f.read())

        result = template.render({
            'title': shop['chain']
        })

        return result
