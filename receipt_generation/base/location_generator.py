from faker.providers import BaseProvider


class FakeLocationProvider(BaseProvider):
    chains = (
        "Migros",
        "Coop",
    )

    branches = (
        "Luzern Bahnhof",
        "Luzern Löwencenter",
    )

    cities = (
        "Zürich",
        "Luzern",
        "Rotkreuz",
        "Bern",
    )

    streets = (
        "Bahnhofstrasse",
        "Mattweg",
    )

    def chain(self) -> str:
        return self.random_element(self.chains)

    def branch(self) -> str:
        return self.random_element(self.branches)

    def city(self) -> str:
        return self.random_element(self.cities)

    def postal_code(self) -> str:
        return str(self.random_int(1000, 9999))

    def address(self) -> str:
        house_number = str(self.random_int(1, 500))

        add_letter = self.random_int(0, 20)
        if add_letter == 0:
            house_number += self.random_uppercase_letter()
        elif add_letter == 1:
            house_number += self.random_lowercase_letter()

        return self.random_element(self.streets) + ' ' + house_number

    def tax_number(self) -> str:
        part1 = self.random_int(100, 999)
        part2 = self.random_int(100, 999)
        part3 = self.random_int(100, 999)

        return f"CHE-{part1}.{part2}.{part3}"

    def phone_number(self) -> str:
        prefix = self.random_element((
            '+41 ',
            '0',
        ))

        part1 = self.random_int(10, 99)
        part2 = str(self.random_int(0, 999)).zfill(3)
        part3 = str(self.random_int(0, 99)).zfill(2)
        part4 = str(self.random_int(0, 99)).zfill(2)

        return f'{prefix}{part1} {part2} {part3} {part4}'

    def website(self, company_name: str) -> str:
        top_level = self.random_element((
            'ch',
            'com',
            'swiss',
            'org',
        ))

        separator = self.random_element((
            '',
            '-',
            '_',
        ))

        name = company_name.lower().replace(' ', separator)

        return f'www.{name}.{top_level}'
