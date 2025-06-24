from faker import Faker
from receipt_generation.base.location_generator import FakeLocationProvider
from receipt_generation.base.grocery_generator import FakeGroceryProvider
from datetime import datetime, timedelta

Faker.seed(42)

fake = Faker('de_DE')
fake.add_provider(FakeLocationProvider)
fake.add_provider(FakeGroceryProvider)


def generate_receipt_data():
    products = []

    overall_total_baseline = 0
    overall_discount_baseline = 0

    for _ in range(fake.random_int(1, 7)):
        # prices between 0.45 - 50.00
        price_baseline = random_price()

        # approximately 7% probability to use decimal amount
        if fake.random_int(0, 14) >= 14:
            amount = '%.3f' % (float(fake.random_int(10, 2999)) / 1000)
        else:
            amount = random_amount()

        # 5% probability to add a discount
        discount_baseline = 0
        if fake.random_int(0, 19) >= 19:
            discount_baseline = fake.random_int(1, int(price_baseline / 2))
            overall_discount_baseline += discount_baseline

        discounted_price_baseline = price_baseline - discount_baseline
        total_baseline = discounted_price_baseline
        if isinstance(amount, int):
            total_baseline *= amount
        overall_total_baseline += total_baseline

        products.append({
            'name': fake.grocery(),
            'amount': amount,
            'tax_id': 0,
            'discounted_price': 0.0,
            'discount': 0.0,
            'price': price_from_baseline(price_baseline),
            'total': price_from_baseline(total_baseline),
        })

    chain = fake.chain()

    return {
        'shop': {
            'chain': chain,
            'branch': fake.branch(),

            'address': fake.address(),
            'postcode': fake.postal_code(),
            'city': fake.city(),

            'telephone': fake.phone_number(),
            'email': fake.email(),
            'website': fake.website(chain),

            'tax': fake.tax_number(),

            'staff': fake.first_name(),
        },
        'meta': {
            'img_seed': fake.random_number(20),
            'gen_seed': fake.random_number(20),
            'date': fake.date_time_between_dates(datetime_start=datetime(2023, 1, 1), datetime_end=datetime(2025, 3, 30)),
            'time': fake.time_object(),
        },
        'purchase': {
            'payment_method': 'Mastercard',  # TODO
            'products': products,
            'total_price': price_from_baseline(overall_total_baseline),
            'total_discount': price_from_baseline(overall_discount_baseline),
        }
    }


def generate_label(data):
    products = []

    for product in data['purchase']['products']:
        # discounted_price = None
        # if not product['discounted_price'] == product['price']:
        #     discounted_price = float(product['discounted_price'])

        products.append({
            'name': product['name'],
            'amount': str(product['amount']),
            'price': str(float(product['total'])),
        })

    return {
        'shop_name': data['shop']['chain'],
        'date': f'{data['meta']['date'].strftime("%d.%m.%Y")}',
        'products': products,
        'total': str(float(data['purchase']['total_price']))
    }


def random_price():
    price_baseline = fake.random_int(9, 200)

    i = 0
    while i < 5 and fake.random_int(0, 1) == 0:
        price_baseline += fake.random_int(1, 200)
        i += 1

    return price_baseline


def random_amount():
    amount = 1

    while fake.random_int(0, 1) == 0:
        amount += 1

    return amount


def price_from_baseline(baseline):
    return '%.2f' % (float(baseline) * 0.05)
