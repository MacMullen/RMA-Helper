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
