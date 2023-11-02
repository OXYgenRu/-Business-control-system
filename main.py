import csv
import sys

import random

from PyQt5.QtCore import QDate, QRect, QSize, QTimer
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import (QWidget, QApplication, QPushButton, QLineEdit, QLabel, QLCDNumber,
                             QCheckBox, QRadioButton,
                             QMainWindow, QButtonGroup, QGridLayout, QTextEdit, QStatusBar, QTextBrowser,
                             QTableWidgetItem, QTableWidget, QInputDialog, QLayout, QSizePolicy, QHBoxLayout,
                             QVBoxLayout, QComboBox, QAction, QFileDialog)

from PyQt5 import QtCore, QtGui, QtWidgets

from graphicclass import BusinessControlSystemGraphic


class BusinessControlSystem(QMainWindow, BusinessControlSystemGraphic):
    def __init__(self):
        super().__init__()
        self.config_data = []
        self.business_name = ""
        self.business_description = ""
        self.user_type = ""
        self.setWindowTitle("business Controll System")
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.setGeometry(100, 100, 1000, 600)

        self.open_config_file()

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
        self.open_information_file.clicked.connect(self.open_new_information_file)

        self.setCentralWidget(self.stacked_widget)
        # self.setCentralWidget(self.buiness_information_widget)

    def connect_defs_admin_actions(self):
        self.action_change_type_of_user_admin.triggered.connect(self.admin_change_typed_user_interface)
        self.action_exit_admin.triggered.connect(self.exit_app)
        self.action_business_information.triggered.connect(self.change_business_interface)
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
        try:
            path = self.config_data[0].strip()
            with open(path, "r", encoding="utf-8") as file:
                file_input = file.read()
                len_name = int(file_input[:file_input.index('\n')])
                business_name = file_input[file_input.index('\n') + 1: file_input.index('\n') + len_name]
                business_description = file_input[file_input.index('\n') + len_name + 1:len(file_input) - 1]
                self.user_business_information_name.setPlainText(business_name)
                self.user_business_information_description.setPlainText(business_description)
        except IOError:
            self.user_business_information_name.setPlainText("Файл информации не настроен")
            self.user_business_information_description.setPlainText("Файл информации не настроен")
            self.statusBar().showMessage(f"Файл информации не настроен")
            self.status_bar.setStyleSheet("background-color: red; color: white;")
            QTimer.singleShot(10000, self.restore_default_color)
        except Exception as error:
            self.statusBar().showMessage(f"Ошибка чтения файла:  {str(error)}")
            self.status_bar.setStyleSheet("background-color: red; color: white;")
            QTimer.singleShot(10000, self.restore_default_color)
        self.stacked_widget.setCurrentWidget(self.user_widget)
        self.user_type = "default_user"

    def user_change_typed_user_interface(self):
        self.stacked_widget.setCurrentWidget(self.admin_widget)
        self.user_type = "admin"

    def change_business_interface(self):
        path = self.config_data[0].strip()
        self.current_file.setText(path)
        print(path)
        try:
            with open(path, "r", encoding="utf-8") as file:
                data = file.read()
                len_name = int(data[:data.index('\n')])
                business_name = data[data.index('\n') + 1: data.index('\n') + len_name]
                business_description = data[data.index('\n') + len_name + 1:len(data) - 1]
                self.business_name_edit.setText(business_name)
                self.business_description_edit.setText(business_description)
        except Exception as error:
            self.statusBar().showMessage("Ошибка загрузки файла, некоректный файл или файл не существует")
            self.status_bar.setStyleSheet("background-color: red; color: white;")
            self.business_description_edit.setText("")
            self.business_name_edit.setText("")
            QTimer.singleShot(5000, self.restore_default_color)
            print(error)
            pass
        self.stacked_widget.setCurrentWidget(self.buiness_information_widget)

    def save_business_information(self):
        self.config_data[0] = self.current_file.text()
        self.restore_default_color()
        self.statusBar().showMessage("Изменения сохранены")
        self.status_bar.setStyleSheet("background-color: green; color: white;")
        QTimer.singleShot(5000, self.restore_default_color)

    def open_config_file(self):
        try:
            with open('config.txt', 'r+') as config:
                self.config_data = config.readlines()
        except IOError:
            with open('config.txt', 'w+') as config:
                self.config_data = ['']
                pass
        if len(self.config_data) == 0:
            self.config_data = ['']

    def open_new_information_file(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(None, "Выберите файл", "", "Текстовые файлы (*.txt);;Все файлы (*)")
        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    data = file.read()
                    len_name = int(data[:data.index('\n')])
                    business_name = data[data.index('\n') + 1: data.index('\n') + len_name]
                    business_description = data[data.index('\n') + len_name + 1:len(data) - 1]
                    self.business_name_edit.setText(business_name)
                    self.business_description_edit.setText(business_description)
                    self.current_file.setText(file_path)
                    self.statusBar().showMessage("Файл успешно загружен")
                    self.status_bar.setStyleSheet("background-color: green; color: white;")
                    QTimer.singleShot(3000, self.save_warning)

            except Exception as error:
                self.statusBar().showMessage(
                    "Ошибка загрузки файла, некоректный файл или файл не существует. Изменения не сохранены")
                self.status_bar.setStyleSheet("background-color: red; color: white;")
                QTimer.singleShot(5000, self.restore_default_color)

    def save_warning(self):
        self.restore_default_color()
        self.statusBar().showMessage("Изменения не сохранены, сохраните изменения!")
        self.status_bar.setStyleSheet("background-color: orange; color: black;")

    def restore_default_color(self):
        self.status_bar.setStyleSheet("")
        self.status_bar.showMessage("")

    def exit_app(self):
        print(self.config_data)
        with open("config.txt", "w", encoding="utf-8") as file:
            file.writelines(self.config_data)
            app.quit()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BusinessControlSystem()
    app.aboutToQuit.connect(window.exit_app)
    window.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
