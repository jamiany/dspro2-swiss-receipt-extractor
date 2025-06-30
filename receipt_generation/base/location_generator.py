from faker.providers import BaseProvider


class FakeLocationProvider(BaseProvider):
    chains = (
        "Aldi",
        "Billa",
        "Coop",
        "Edeka",
        "Globus",
        "Lidl",
        "Migros",
        "Netto",
        "Penny",
        "Real",
        "Rewe",
        "Spar",
    )

    shopping_centers = (
        "A1",
        "Avry Centre",
        "Balexert",
        "Birchi Center",
        "Birs Center",
        "Brunaupark",
        "Bahnhof",
        "Centre Bahnhof",
        "Centre Brügg",
        "Centre Manor Chavannes",
        "Centro Lugano Sud",
        "Emmen Center",
        "Foxtown",
        "Fribourg Centre",
        "Glattzentrum",
        "Heimberg Shopping",
        "Herblinger Markt",
        "Ladedorf",
        "Lago",
        "Länderpark",
        "Léman Centre",
        "LenzoPark",
        "Letzipark",
        "Löwencenter",
        "Lyssach Center",
        "Lyssbachpark",
        "Manor Centre Vevey",
        "Marin Centre",
        "Messepark",
        "Metalli",
        "Müli Märt",
        "Mythen Center Schwyz",
        "Neudorf Center",
        "Neumarkt Brugg",
        "Neumarkt Oerlikon",
        "Panorama Center",
        "Parkallee Bachenbülach",
        "Passage",
        "Pilatusmarkt",
        "Pizolpark",
        "Riet Center",
        "Rigimärt",
        "Rosenberg",
        "Sälipark",
        "Säntispark",
        "Seedamm Center",
        "Seemaxx Factory Outlet",
        "Seepark",
        "Seewen markt",
        "Shoppi Tivoli",
        "Shopping Arena",
        "Shopping-Center Schönbühl",
        "Shoppingcenter Gäupark",
        "Shoppyland",
        "Sihlcity",
        "Sonnenhof",
        "St.Jakob park",
        "Surseepark",
        "Telli",
        "Tellpark",
        "Mall of Switzerland",
        "Volkiland",
        "Wankdorf Center",
        "Westside Bern Brünnen",
        "Wydehof Einkaufs-Center",
        "Wynecenter",
        "Zänti Volketswil",
        "Zentrum Neuwiesen",
        "Zentrum Oberland",
        "Zentrum Regensdorf",
        "Zugerland"
    )

    cities = (
        "Aarau",
        "Adliswil",
        "Allschwil",
        "Amriswil",
        "Arbon",
        "Baar",
        "Baden",
        "Basel",
        "Bellinzona",
        "Bern",
        "Biel",
        "Binningen",
        "Bülach",
        "Bulle",
        "Burgdorf",
        "Carouge",
        "Cham",
        "Chur",
        "Dietikon",
        "Dübendorf",
        "Ebikon",
        "Einsiedeln",
        "Emmen",
        "Frauenfeld",
        "Freiburg",
        "Freienbach",
        "Genf",
        "Glarus",
        "Gossau",
        "Grenchen",
        "Herisau",
        "Horgen",
        "Horw",
        "Illnau-Effretikon",
        "Kloten",
        "Köniz",
        "Kreuzlingen",
        "Kriens",
        "Küsnacht",
        "Küssnacht SZ",
        "La Chaux-de-Fonds",
        "Lancy",
        "Langenthal",
        "Lausanne",
        "Liestal",
        "Locarno",
        "Lugano",
        "Luzern",
        "Lyss",
        "Martigny",
        "Meilen",
        "Mendrisio",
        "Meyrin",
        "Monthey",
        "Montreux",
        "Morges",
        "Muttenz",
        "Neuenburg",
        "Nyon",
        "Oftringen",
        "Olten",
        "Onex",
        "Opfikon",
        "Ostermundigen",
        "Pratteln",
        "Pully",
        "Rapperswil-Jona",
        "Regensdorf",
        "Reinach",
        "Renens",
        "Rheinfelden",
        "Richterswil",
        "Riehen",
        "Schaffhausen",
        "Schlieren",
        "Schwyz",
        "Siders",
        "Sitten",
        "Solothurn",
        "St. Gallen",
        "Stäfa",
        "Steffisburg",
        "Thalwil",
        "Thônex",
        "Thun",
        "Uster",
        "Val-de-Ruz",
        "Vernier",
        "Vevey",
        "Volketswil",
        "Wädenswil",
        "Wallisellen",
        "Wettingen",
        "Wetzikon",
        "Wil",
        "Winterthur",
        "Wohlen",
        "Yverdon-les-Bains",
        "Zug",
        "Zürich",
    )

    streets = (
            "Linden", "Haupt", "Schiller", "Goethe", "Garten", "Berg", "Wiesen",
            "Dorf", "Bahnhof", "Schloss", "Kirch", "Mühlen", "Sonnen", "Feld",
            "Wald", "Park", "Rosen", "Tal", "Amts", "Schul", "Markt", "Heide",
            "Tannen", "Eichen", "Weiden", "Hof", "Alten", "Brunnen", "Graben",
            "Hain", "Jäger", "Kapellen", "Kloster", "Königs", "Lehm", "Moor",
            "Neuen", "Ober", "Unter", "Ried", "Seiten", "Stein", "Teich", "Turm",
            "Ufer", "Ziegel", "Kastanien", "Birken", "Ahorn", "Fichten", "Matt", "Zürcher"
    )

    street_suffixes = (
        "gasse",
        "platz",
        "pl.",
        "strasse",
        "str.",
        "weg",
        "allee",
    )

    def chain(self) -> str:
        return self.random_element(self.chains)

    def branch(self) -> str:
        branch = self.random_element(self.shopping_centers)

        typ = self.random_int(0, 3)
        if typ == 0:
            city = self.random_element(self.cities)
            branch = f'{city} {branch}'

        return branch

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

        street = self.random_element(self.streets)
        street_suffix = self.random_element(self.street_suffixes)

        return f'{street}{street_suffix} {house_number}'

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

# https://www.kaggle.com/datasets/dhiaznaidi/receiptdatasetssd300v2
# https://www.kaggle.com/datasets/trainingdatapro/ocr-receipts-text-detection
# https://www.kaggle.com/datasets/mdhstama23/receipt-invoice-ml-ch2ps357
# https://www.kaggle.com/datasets/adondoumit/receipts
# https://huggingface.co/docs/transformers/en/model_doc/vision-encoder-decoder
# https://huggingface.co/docs/transformers/en/model_doc/donut
# https://huggingface.co/tasks/image-to-text
# https://mychen76.medium.com/finetune-llm-to-convert-a-receipt-image-to-json-or-xml-3f9a6237e991
# https://ai.google.dev/gemma/docs/paligemma
# https://huggingface.co/blog/smolvlm

# https://fonts.google.com/specimen/Libre+Barcode+39+Text?preview.text=test&query=barcode
