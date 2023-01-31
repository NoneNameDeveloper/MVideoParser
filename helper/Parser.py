import json
import requests

from helper import data
from helper import Links


class Parser:

    def __init__(self, category_id: int):
        self.products_ids = None
        self.category_id = category_id

        self.res_dict = {}

        self.get_product_ids()
        self.get_names()
        self.get_prices()


    def get_product_ids(self):
        """
        getting product ids
        """
        params = {
            "categoryId": self.category_id
        }

        response_json = requests.get(Links.listing, params=params, cookies=data.cookies, headers=data.headers).json()

        products_ids = response_json['body']['products']

        for u in products_ids:
            self.res_dict.setdefault(u, {})

        self.products_ids = products_ids

    def get_names(self):
        """
        getting product names by product_ids
        """
        json_data = {
            'productIds': self.products_ids,
            'mediaTypes': [
                'images',
            ],
            'category': True,
            'status': True,
            'brand': True,
            'propertyTypes': [
                'KEY',
            ],
            'propertiesConfig': {
                'propertiesPortionSize': 5,
            },
            'multioffer': True,
        }

        response_json = requests.post(Links.list, headers=data.headers, cookies=data.cookies, json=json_data).json()

        products_ = response_json['body']['products']
        for u in products_:
            p_id = u['productId']

            self.res_dict[p_id].update({"title": u['name']})

    def get_prices(self):
        """
        get items prices
        """
        params = {
            'productIds': ",".join(self.products_ids),
            'addBonusRubles': 'true',
            'isPromoApplied': 'true',
        }

        res_json = requests.get(Links.prices, params=params, cookies=data.cookies, headers=data.headers).json()

        prices_ = res_json['body']['materialPrices']

        for u in prices_:
            p_id = u['productId']

            self.res_dict[p_id].update({"price": u['price']['basePrice']})



