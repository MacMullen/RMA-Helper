from PyQt5 import QtGui
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from uuid import uuid4
from reportlab.lib.units import cm, inch
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import *
from reportlab.lib.styles import getSampleStyleSheet
import csv
import json
import os
import datetime


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


def save_product_to_csv(brand, product, problem, sn, missing_acc, uuid):
    data = json.load(open('database/products.json'))
    company_name = data[brand][product]["company"]
    if not os.path.isdir('database/archive'):
        os.mkdir('database/archive')
        os.mkdir('database/archive/active')
    if not os.path.isfile('database/archive/active/' + company_name + '.csv'):
        file = open('database/archive/active/' + company_name + '.csv', "w+")
        file.write("UUID,Brand,Product,Problem,Missing Accesories,Serial Number\n")
        file.close()
    with open('database/archive/active/' + company_name + '.csv', 'a', newline='') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([uuid, brand, product, problem, missing_acc, sn])

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


def generate_pdf(company, status):
    # Source: https://stackoverflow.com/questions/48863462/writing-full-csv-table-to-pdf-in-python
    with open('database/archive/active/ServiTech.csv', "r") as csvfile:
        data = []
        for row in csv.reader(csvfile):
            row_data = []
            for index, column in enumerate(row):
                if index != 0:
                    row_data.append(column)
            data.append(row_data)

    elements = []

    # PDF Text
    # PDF Text - Styles
    styles = getSampleStyleSheet()
    styleNormal = styles['Normal']

    # PDF Text - Content
    line1 = '<font size=10><b>BM WEB SA</b></font>'
    line2 = '<b>Fecha: {}</b>'.format(datetime.datetime.now().strftime("%d-%m-%y"))
    line3 = 'REMITO INGRESO DE EQUIPOS PARA RMA - <b>{}</b>'.format(company)

    elements.append(Paragraph(line1, styleNormal))
    elements.append(Paragraph(line2, styleNormal))
    elements.append(Paragraph(line3, styleNormal))
    elements.append(Spacer(inch, .25 * inch))

    # PDF Table
    # PDF Table - Styles
    # [(start_column, start_row), (end_column, end_row)]
    all_cells = [(0, 0), (-1, -1)]
    header = [(0, 0), (-1, 0)]
    column0 = [(0, 0), (0, -1)]
    column1 = [(1, 0), (1, -1)]
    column2 = [(2, 0), (2, -1)]
    column3 = [(3, 0), (3, -1)]
    column4 = [(4, 0), (4, -1)]
    table_style = TableStyle([
        ('VALIGN', all_cells[0], all_cells[1], 'TOP'),
        ('LINEBELOW', header[0], header[1], 1, colors.black),
        ('ALIGN', column0[0], column0[1], 'LEFT'),
        ('ALIGN', column1[0], column1[1], 'LEFT'),
        ('ALIGN', column2[0], column2[1], 'LEFT'),
        ('ALIGN', column3[0], column3[1], 'LEFT'),
        ('ALIGN', column4[0], column4[1], 'LEFT'),
        ('GRID', (0, 1), (-1, -1), 0.25, colors.black)
    ])

    # PDF Table - Column Widths
    colWidths = [
        3 * cm,  # Column 0
        3 * cm,  # Column 1
        5.5 * cm,  # Column 2
        4 * cm,  # Column 4
        3 * cm,  # Column 5
    ]

    # PDF Table - Strip '[]() and add word wrap to column 5
    count = 0
    for index, row in enumerate(data):
        count += 1
        for col, val in enumerate(row):
            data[index][col] = Paragraph(val, styles['Normal'])

    # Add table to elements
    t = Table(data, colWidths=colWidths)
    t.setStyle(table_style)
    elements.append(t)

    # Botton part of the file.
    colWidths = [9.5 * cm, 9.5 * cm]
    rowHeights = [1 * cm, 3 * cm, 1.5 * cm, 1.5 * cm]
    deliver_header_line = Paragraph("""<font size=15><b>RECIBE</b></font>""", styles['Normal'])
    pick_header_line = Paragraph("""<font size=15><b>ENTREGA</b></font>""", styles['Normal'])
    signature_line = Paragraph("""<b>FIRMA:</b>""", styles['Normal'])
    text_line = Paragraph("""<b>ACLARACION:</b>""", styles['Normal'])
    document_line = Paragraph("""<b>DNI:</b>""", styles['Normal'])
    sign_table = [[pick_header_line, deliver_header_line], [signature_line, signature_line], [text_line, text_line],
                  [document_line, document_line]]
    bottom_table = Table(sign_table, colWidths=colWidths, rowHeights=rowHeights)
    bottom_table.setStyle((TableStyle([('ALIGN', (0, 1), (0, 1), 'RIGHT'),
                                       ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                                       ('GRID', (0, 1), (-1, -1), 0.25, colors.black)])))
    line4 = """<font size=12><b>Total: {}</b></font>""".format(count)

    elements.append(Spacer(inch, .30 * inch))
    elements.append(Paragraph(line4, styleNormal))
    elements.append(Spacer(inch, .30 * inch))
    elements.append(bottom_table)

    # Generate PDF
    archivo_pdf = SimpleDocTemplate(
        '{}_{}_invoice.pdf'.format(company, datetime.datetime.now().strftime("%d-%m-%y")),
        pagesize=A4,
        rightMargin=20,
        leftMargin=20,
        topMargin=40,
        bottomMargin=28)
    archivo_pdf.build(elements)
    os.startfile('{}_{}_invoice.pdf'.format(company, datetime.datetime.now().strftime("%d-%m-%y")))
