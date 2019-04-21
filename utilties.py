from PyQt5 import QtGui
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from uuid import uuid4
import csv
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
            data[brand][product_id] = new_product
        else:
            data[brand].update(new_dict)
    else:
        data[brand] = new_dict

    with open('database/products.json', 'w') as json_file:
        json.dump(data, json_file)


def load_brands_json():
    data = json.load(open('database/products.json'))
    result = []
    for entry in data:
        result.append(entry)

    return result


def brand_exists(brand):
    data = json.load(open('database/products.json'))
    if brand in data:
        return True
    return False


def generate_uuid():
    uuid = str(uuid4())[:8]
    data = json.load(open('database/uuid.json'))
    while uuid in data:
        uuid = str(uuid4())
    return uuid.upper()


def save_uuid(uuid):
    data = json.load(open('database/uuid.json'))
    data[uuid] = ""
    with open('database/uuid.json', 'w') as json_file:
        json.dump(data, json_file)


def show_products_from(brand):
    data = json.load(open('database/products.json'))
    result = []
    for entry in data[brand]:
        result.append(entry)

    return result


def show_accesories_from(product, brand):
    data = json.load(open('database/products.json'))
    result = []
    for acc in data[brand][product]["accesories"]:
        list_widget = QListWidgetItem(acc)
        list_widget.setCheckState(Qt.Unchecked)
        result.append(list_widget)

    return result


def save_product_to_csv(brand, product, problem, description, sn, missing_acc, uuid):
    data = json.load(open('database/products.json'))
    company_name = data[brand][product]["company"]
    if not os.path.isdir('database/archive'):
        os.mkdir('database/archive')
        os.mkdir('database/archive/active')
    if not os.path.isfile('database/archive/active/' + company_name + '.csv'):
        file = open('database/archive/active/' + company_name + '.csv', "w+")
        file.write("UUID,Brand,Product,Problem,Description,Serial Number,Missing Accesories\n")
        file.close()
    with open('database/archive/active/' + company_name + '.csv', 'a') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([uuid, brand, product, problem, description, sn, missing_acc])

    save_uuid(uuid)


def valid_status(company):
    result = []
    if os.path.isfile('database/archive/active/' + company + '.csv'):
        result.append("Active")
    if os.path.isfile('database/archive/sent/' + company + '.csv'):
        result.append("Sent")
    if os.path.isfile('database/archive/returned/' + company + '.csv'):
        result.append("Returned")

    return result


def read_csv_file(status, company):
    model = QtGui.QStandardItemModel()
    with open('database/archive/' + status.lower() + '/' + company + '.csv', "r") as csv_file:
        reader = csv.reader(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        model.setHorizontalHeaderLabels(next(reader))
        for row in reader:
            items = [QtGui.QStandardItem(field) for field in row]
            model.appendRow(items)
    return model
