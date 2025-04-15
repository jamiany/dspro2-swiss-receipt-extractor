from jinja2 import Template


def generate_product_table(data):
    purchase = data['purchase']

    with open('sections/product_table/template_napat.html') as f:
        template = Template(f.read())

        result = template.render({
            'products': purchase['products'],
        })

        return result
