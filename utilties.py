from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys
import json
import os


def save_to_companies_json(name, address, telephone, contact, open_hour, close_hour):
    new_company = {"address": address, "telephone": telephone, "contact": contact,
                   "Opening hours": open_hour + "-" + close_hour}

    data = json.load(open('database/companies.json'))

    data[name] = new_company

    with open('database/companies.json', 'w') as json_file:
        json.dump(data, json_file)


def load_companies_json():
    data = json.load(open('database/companies.json'))
    result = set()
    for entry in data:
        result.add(entry)

    return result


def save_new_product_to_json(brand, product_id, company_name, accesory_list):
    new_product = {"company": company_name, "accesories": accesory_list}
    new_dict = dict()
    new_dict[product_id] = new_product
    data = json.load(open('database/products.json'))
    if brand in data:
        if product_id in data[brand]:
            data[brand][product_id].update(new_product)
        else:
            data[brand].update(new_dict)
    else:
        data[brand] = new_dict

    with open('database/products.json', 'w') as json_file:
        json.dump(data, json_file)