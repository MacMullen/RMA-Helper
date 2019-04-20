from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys
from utilties import *
import os


def center(main_window: QMainWindow):
    qr = main_window.frameGeometry()
    cp = QDesktopWidget().availableGeometry().center()
    qr.moveCenter(cp)
    main_window.move(qr.topLeft())


class MainWindow(QMainWindow):
    def __init__(self):
        self.companies = load_companies_json()
        super(MainWindow, self).__init__()
        self.resize(1280, 720)
        self.setWindowTitle("PyBank")
        center(self)
        self.main_widget = QStackedWidget()
        self.setCentralWidget(self.main_widget)

        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('&File')
        fileMenu.addAction(self.add_product_action())
        fileMenu.addAction(self.new_product_action())
        fileMenu.addAction(self.new_company_action())
        fileMenu.addSeparator()
        fileMenu.addAction(self.exit_action())
        toolsMenu = mainMenu.addMenu('&Tools')
        toolsMenu.addAction(self.invoice_action())

        self.main_widget.addWidget(self.add_product_page())
        self.main_widget.addWidget(self.new_product_page())
        self.main_widget.addWidget(self.new_company_page())
        self.main_widget.addWidget(self.invoice_page())

        self.show()

    def add_product_page(self):
        base_widget = QWidget()

        base_layout = QVBoxLayout()

        brand_label = QLabel("Brand")
        self.add_prod_brand_combo_box = QComboBox()
        product_label = QLabel("Product")
        self.add_prod_product_combo_box = QComboBox()
        problem_label = QLabel("Problem")
        self.add_prod_problem_edit_box = QLineEdit()
        description_label = QLabel("Description")
        self.add_prod_description_text_box = QTextEdit()
        sn_label = QLabel("Serial Number")
        self.add_prod_sn_edit_box = QLineEdit()
        acc_label = QLabel("Accesories")
        self.add_prod_acc_text_box = QTextEdit()
        uuid_label = QLabel("UUID")
        self.add_prod_uuid_edit_box = QLineEdit()
        save_button = QPushButton("Save")

        base_layout.addWidget(brand_label)
        base_layout.addWidget(self.add_prod_brand_combo_box)
        base_layout.addWidget(product_label)
        base_layout.addWidget(self.add_prod_product_combo_box)
        base_layout.addWidget(problem_label)
        base_layout.addWidget(self.add_prod_problem_edit_box)
        base_layout.addWidget(description_label)
        base_layout.addWidget(self.add_prod_description_text_box)
        base_layout.addWidget(sn_label)
        base_layout.addWidget(self.add_prod_sn_edit_box)
        base_layout.addWidget(acc_label)
        base_layout.addWidget(self.add_prod_acc_text_box)
        base_layout.addWidget(uuid_label)
        base_layout.addWidget(self.add_prod_uuid_edit_box)
        base_layout.addWidget(save_button, alignment=Qt.AlignRight)

        base_widget.setLayout(base_layout)

        return base_widget

    def new_product_page(self):
        base_widget = QWidget()

        base_layout = QVBoxLayout()

        brand_label = QLabel("Brand")
        self.new_prod_brand_edit_box = QLineEdit()
        product_label = QLabel("Product ID")
        self.new_prod_product_edit_box = QLineEdit()
        company_label = QLabel("Company")
        self.new_prod_company_combo_box = QComboBox()
        accesories_label = QLabel("Accesories")
        self.new_prod_acc_edit_box = QLineEdit()
        add_button = QPushButton("Add")
        self.new_prod_accesories_list = QListWidget()
        save_button = QPushButton("Save")

        base_layout.addWidget(brand_label)
        base_layout.addWidget(self.new_prod_brand_edit_box)
        base_layout.addWidget(product_label)
        base_layout.addWidget(self.new_prod_product_edit_box)
        base_layout.addWidget(company_label)
        base_layout.addWidget(self.new_prod_company_combo_box)
        base_layout.addWidget(accesories_label)
        base_layout.addWidget(self.new_prod_acc_edit_box)
        base_layout.addWidget(add_button, alignment=Qt.AlignRight)
        base_layout.addWidget(self.new_prod_accesories_list)
        base_layout.addWidget(save_button, alignment=Qt.AlignRight)

        base_widget.setLayout(base_layout)

        return base_widget

    def new_company_page(self):
        base_widget = QWidget()

        base_layout = QVBoxLayout()

        name_label = QLabel("Name")
        self.new_company_name_edit_box = QLineEdit()
        address_label = QLabel("Address")
        self.new_company_address_edit_box = QLineEdit()
        telephone_label = QLabel("Telephone")
        self.new_company_telephone_edit_box = QLineEdit()
        contact_label = QLabel("Contact")
        self.new_company_contact_edit_box = QLineEdit()
        opening_hours_label = QLabel("Opening Hours")
        hours_layout = QHBoxLayout()
        self.open_hour = QTimeEdit()
        self.close_hour = QTimeEdit()
        hours_layout.addWidget(self.open_hour)
        hours_layout.addWidget(QLabel("--"))
        hours_layout.addWidget(self.close_hour)
        hours_layout.addStretch(1)
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_new_company)

        base_layout.addWidget(name_label)
        base_layout.addWidget(self.new_company_name_edit_box)
        base_layout.addWidget(address_label)
        base_layout.addWidget(self.new_company_address_edit_box)
        base_layout.addWidget(telephone_label)
        base_layout.addWidget(self.new_company_telephone_edit_box)
        base_layout.addWidget(contact_label)
        base_layout.addWidget(self.new_company_contact_edit_box)
        base_layout.addWidget(opening_hours_label)
        base_layout.addLayout(hours_layout)
        base_layout.addStretch(1)
        base_layout.addWidget(save_button, alignment=Qt.AlignRight)

        base_widget.setLayout(base_layout)

        return base_widget

    def invoice_page(self):
        base_widget = QWidget()

        base_layout = QVBoxLayout()

        company_label = QLabel("Company")
        self.invoice_company_edit_box = QComboBox()
        status_label = QLabel("Status")
        self.invoice_status_combo_box = QComboBox()
        self.invoice_table_view = QTableView()
        print_button = QPushButton("Print Invoice")
        change_status_label = QLabel("Change Status")
        self.invoice_change_status_combo_box = QComboBox()
        change_status_button = QPushButton("Change Status")

        base_layout.addWidget(company_label)
        base_layout.addWidget(self.invoice_company_edit_box)
        base_layout.addWidget(status_label)
        base_layout.addWidget(self.invoice_status_combo_box)
        base_layout.addWidget(self.invoice_table_view)
        base_layout.addWidget(print_button, alignment=Qt.AlignRight)
        base_layout.addWidget(change_status_label)
        base_layout.addWidget(self.invoice_change_status_combo_box)
        base_layout.addWidget(change_status_button, alignment=Qt.AlignRight)

        base_widget.setLayout(base_layout)

        return base_widget

    def add_product_action(self):
        addProductAction = QAction("&Add Product", self)
        addProductAction.setStatusTip('Add a new product')
        addProductAction.triggered.connect(lambda: self.main_widget.setCurrentIndex(0))
        return addProductAction

    def new_product_action(self):
        newProductAction = QAction("&New Product", self)
        newProductAction.setStatusTip('Register a new product in the database')
        newProductAction.triggered.connect(lambda: self.main_widget.setCurrentIndex(1))
        return newProductAction

    def new_company_action(self):
        newCompanyAction = QAction("&New Company", self)
        newCompanyAction.setStatusTip('Add a new product')
        newCompanyAction.triggered.connect(lambda: self.main_widget.setCurrentIndex(2))
        return newCompanyAction

    def exit_action(self):
        exitAction = QAction("&Exit", self)
        exitAction.triggered.connect(self.close)
        return exitAction

    def invoice_action(self):
        invoiceAction = QAction("&Print Invoice", self)
        invoiceAction.setStatusTip('Print an invoice from the database')
        invoiceAction.triggered.connect(lambda: self.main_widget.setCurrentIndex(3))
        return invoiceAction

    def save_new_company(self):
        if self.new_company_name_edit_box.text() == "":
            self.new_company_name_edit_box.setStyleSheet("background: rgba(255,0,0,0.2);")
            return

        save_to_companies_json(self.new_company_name_edit_box.text(),
                                        self.new_company_address_edit_box.text(),
                                        self.new_company_telephone_edit_box.text(),
                                        self.new_company_contact_edit_box.text(),
                                        self.open_hour.text(),
                                        self.close_hour.text())

        self.new_company_name_edit_box.setText("")
        self.new_company_name_edit_box.setStyleSheet("background: white;")
        self.new_company_address_edit_box.setText("")
        self.new_company_telephone_edit_box.setText("")
        self.new_company_contact_edit_box.setText("")
        self.open_hour.setTime(QTime(0, 0, 0, 0))
        self.close_hour.setTime(QTime(0, 0, 0, 0))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    GUI = MainWindow()
    app.exec_()