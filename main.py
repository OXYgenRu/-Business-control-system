import csv
import sys

import random

from PyQt5.QtCore import QDate, QRect, QSize, QTimer
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import (QWidget, QApplication, QPushButton, QLineEdit, QLabel, QLCDNumber,
                             QCheckBox, QRadioButton,
                             QMainWindow, QButtonGroup, QGridLayout, QTextEdit, QStatusBar, QTextBrowser,
                             QTableWidgetItem, QTableWidget, QInputDialog, QLayout, QSizePolicy, QHBoxLayout,
                             QVBoxLayout, QComboBox, QAction)

from PyQt5 import QtCore, QtGui, QtWidgets

from graphicclass import BusinessControlSystemGraphic


class BusinessControlSystem(QMainWindow, BusinessControlSystemGraphic):
    def __init__(self):
        super().__init__()
        self.business_name = ""
        self.business_about = ""
        self.user_type = ""
        self.setWindowTitle("Buisness Controll System")
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.setGeometry(100, 100, 1000, 600)

        self.create_actions_admin()
        self.connect_defs_admin_actions()
        self.create_admin_menubar()
        self.create_admin_toolbar()

        self.create_actions_user()
        self.connect_defs_user_actions()
        self.create_user_menubar()

        self.init_ui_admin()
        self.init_ui_user()
        self.init_ui_buiness_information()

        self.stacked_widget.addWidget(self.admin_widget)
        self.stacked_widget.addWidget(self.user_widget)
        self.stacked_widget.addWidget(self.buiness_information_widget)
        self.user_type_selection()

        self.save_infromation_button.clicked.connect(self.save_business_information)

        self.setCentralWidget(self.stacked_widget)
        # self.setCentralWidget(self.buiness_information_widget)

    def connect_defs_admin_actions(self):
        self.action_change_type_of_user_admin.triggered.connect(self.admin_change_typed_user_interface)
        self.action_exit_admin.triggered.connect(self.exit_app)
        self.action_buisness_information.triggered.connect(self.change_buisness_interface)
        self.action_open_main_page.triggered.connect(self.user_change_typed_user_interface)

    def connect_defs_user_actions(self):
        self.action_change_type_of_user_user.triggered.connect(self.user_change_typed_user_interface)
        self.action_exit_user.triggered.connect(self.exit_app)

    def user_type_selection(self):
        input_dialog = QInputDialog(self)
        items = ["Администратор - управление и доступ к информации",
                 "Клиент - взмаимодействие с бизнесом (потребитель)"]
        ok_pressed = False
        text = ""
        while ok_pressed is not True:
            text, ok_pressed = input_dialog.getItem(self, 'Выбор типа пользователя', 'Выберите тип пользователя:',
                                                    items,
                                                    editable=False)

        if text == "Клиент - взмаимодействие с бизнесом (потребитель)":
            self.admin_change_typed_user_interface()
        else:
            self.user_change_typed_user_interface()

    def admin_change_typed_user_interface(self):
        self.user_business_information_name.setPlainText(self.business_name)
        self.user_business_information_about.setPlainText(self.business_about)
        self.stacked_widget.setCurrentWidget(self.user_widget)
        self.user_type = "default_user"

    def user_change_typed_user_interface(self):
        self.stacked_widget.setCurrentWidget(self.admin_widget)
        self.user_type = "admin"

    def change_buisness_interface(self):
        self.stacked_widget.setCurrentWidget(self.buiness_information_widget)

    def exit_app(self):
        app.quit()

    def save_business_information(self):
        self.statusBar().showMessage("Информация сохранена")
        self.status_bar.setStyleSheet("background-color: green; color: white;")
        self.business_name = self.business_name_edit.toPlainText()
        self.business_about = self.business_about_edit.toPlainText()
        print(self.business_name, self.business_about)
        QTimer.singleShot(2000, self.restore_default_color)
        # self.status_bar.setStyleSheet("background-color: white; color: black;")

    def restore_default_color(self):
        self.status_bar.setStyleSheet("")
        self.status_bar.showMessage("")


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BusinessControlSystem()
    window.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
