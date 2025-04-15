from jinja2 import Template

from receipt_generation.sections.address.generator import generate_address
from receipt_generation.sections.payment.generator import generate_payment
from receipt_generation.sections.product_table.generator import generate_product_table
from receipt_generation.sections.tax.generator import generate_tax
from receipt_generation.sections.technical_details.generator import generate_technical_details
from receipt_generation.sections.title.generator import generate_title
from receipt_generation.sections.total.generator import generate_total


def generate_html_receipt(name, data):
    title = generate_title(data)
    address = generate_address(data)
    product_table = generate_product_table(data)
    total = generate_total(data)
    payment = generate_payment(data)
    tax = generate_tax(data)
    technical_details = generate_technical_details(data)

    with open('base/base.html', 'r') as f:
        template = Template(f.read())

        result = template.render({
            'title': title,
            'sections': [
                address,
                product_table,
                total,
                payment,
                tax,
                technical_details
            ]
        })

    with open(f'temp/{name}.html', 'w') as f:
        f.write(result)
