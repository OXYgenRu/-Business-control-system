import csv
import sys
import os
import sqlite3
from PyQt5.QtCore import QDate, QRect, QSize, QTimer
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import (QWidget, QApplication, QPushButton, QLineEdit, QLabel, QLCDNumber,
                             QCheckBox, QRadioButton,
                             QMainWindow, QButtonGroup, QGridLayout, QTextEdit, QStatusBar, QTextBrowser,
                             QTableWidgetItem, QTableWidget, QInputDialog, QLayout, QSizePolicy, QHBoxLayout,
                             QVBoxLayout, QComboBox, QAction, QFileDialog, QMessageBox, QScrollArea, QWidgetItem)

from PyQt5 import QtCore, QtGui, QtWidgets

from initclass import BusinessControlSystemGraphic
from fileeditor import FileEditor
from requestclass import Request
from myExeptions import WrongClientInf


class BusinessControlSystem(QMainWindow, BusinessControlSystemGraphic):
    def __init__(self):
        super().__init__()
        self.global_path = os.path.dirname(os.path.abspath(__file__))
        self.user_types_list = []
        self.config_data = []
        self.base_user_types_list = []
        self.client_types_checkbox = []
        self.business_name = ""
        self.business_description = ""
        self.user_type = ""
        self.setWindowTitle("business Controll System")
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.setGeometry(100, 100, 1000, 600)

        self.init_sql()

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
        self.init_ui_types_clients()

        self.init_ui_db_interface()
        self.init_db_ui_requets()

        self.stacked_widget.addWidget(self.admin_widget)
        self.stacked_widget.addWidget(self.user_widget)
        self.stacked_widget.addWidget(self.buiness_information_widget)
        self.stacked_widget.addWidget(self.types_clients_widget)
        self.stacked_widget.addWidget(self.db_widget)
        self.user_type_selection()

        self.save_infromation_button.clicked.connect(self.save_business_information)
        self.open_information_file_button.clicked.connect(self.open_new_information_file)
        self.ready_edit_file_button.clicked.connect(self.ready_to_edit_file)
        self.update_current_file_button.clicked.connect(self.save_to_information_file)
        self.create_file_button.clicked.connect(self.open_file_editor)
        self.check_box_1.clicked.connect(self.types_user_clicked)
        self.check_box_2.clicked.connect(self.types_user_clicked)
        self.check_box_3.clicked.connect(self.types_user_clicked)
        self.type_list.currentItemChanged.connect(self.display_current_element)
        self.delete_current_element_button.clicked.connect(self.delete_current_element)
        self.add_new_type_button.clicked.connect(self.add_current_element)
        self.save_types_clients_button.clicked.connect(self.save_types_clients)
        self.client_send_massage_button.clicked.connect(self.save_request)
        self.use_name_checkbox.clicked.connect(self.unlock_filters)
        self.use_surname_checkbox.clicked.connect(self.unlock_filters)
        self.use_secondname_checkbox.clicked.connect(self.unlock_filters)
        self.find_clients_button.clicked.connect(self.load_clients)
        self.db_view.clicked.connect(self.display_selected_client)
        self.save_changes_button.clicked.connect(self.change_client_inf)
        self.save_changes_button.clicked.connect(self.load_clients)
        self.base_user_types_list.append(self.check_box_1.text())
        self.base_user_types_list.append(self.check_box_2.text())
        self.base_user_types_list.append(self.check_box_3.text())
        self.type_db_combobox.currentTextChanged.connect(self.change_ui_client_db)
        self.type_db_combobox_requests.currentTextChanged.connect(self.change_ui_client_db)
        self.load_db_requests_button.clicked.connect(self.load_requests)
        self.client_id_checkbox.clicked.connect(self.unlock_client_id_edit)
        self.load_answers_button.clicked.connect(self.load_answers)

        self.setCentralWidget(self.stacked_widget)
        # self.setCentralWidget(self.buiness_information_widget)

    def connect_defs_admin_actions(self):
        self.action_change_type_of_user_admin.triggered.connect(self.admin_change_typed_user_interface)
        self.action_exit_admin.triggered.connect(self.exit_app)
        self.action_business_information.triggered.connect(self.change_business_interface)
        self.action_open_main_page.triggered.connect(self.user_change_typed_user_interface)
        self.action_open_clients_types_page.triggered.connect(self.clients_types_interface)
        self.action_create_information_file.triggered.connect(self.open_file_editor)
        self.action_open_db_page.triggered.connect(self.open_db)

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

    def clients_types_interface(self):
        self.user_types_list.clear()
        try:
            with open("clients-types.csv", 'r', newline='', encoding="utf8") as csvfile:
                reader = csv.reader(csvfile, delimiter=';', quotechar='"')
                for row in reader:
                    self.user_types_list.append(row[1])
                    if row[1] in self.check_box_dict:
                        self.check_box_dict[row[1]].setChecked(True)
                self.type_list.clear()
                self.type_list.addItems(self.user_types_list)

        except Exception as error:
            self.statusBar().showMessage(f"Ошибка чтения csv файла:  {str(error)}")
            self.status_bar.setStyleSheet("background-color: red; color: white;")
            QTimer.singleShot(10000, self.restore_default_color)

        self.stacked_widget.setCurrentWidget(self.types_clients_widget)

    def admin_change_typed_user_interface(self):
        try:
            path = self.config_data[0].strip()
            with open(path, "r", encoding="utf-8") as file:
                file_input = file.read()
                len_name = int(file_input[:file_input.index('\n')])
                business_name = file_input[file_input.index('\n') + 1: file_input.index('\n') + len_name]
                business_description = file_input[file_input.index('\n') + len_name:len(file_input)]
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

        try:
            with open("clients-types.csv", 'r', newline='', encoding="utf8") as csvfile:
                type_list = []
                reader = csv.reader(csvfile, delimiter=';', quotechar='"')
                self.client_types_list.clear()
                self.client_types_list.clear()
                for row in reader:
                    self.client_types_list.addItem(row[1])
        except Exception as error:
            self.statusBar().showMessage(f"Ошибка чтения csv файла:  {str(error)}")
            self.status_bar.setStyleSheet("background-color: red; color: white;")
            QTimer.singleShot(10000, self.restore_default_color)

        self.stacked_widget.setCurrentWidget(self.user_widget)
        self.user_type = "default_user"

    def user_change_typed_user_interface(self):
        result = self.cursor.execute("""SELECT * FROM  requests""").fetchall()
        self.request_cnt.setText(str(len(result)))
        result = self.cursor.execute("""SELECT * FROM  clients""").fetchall()
        self.client_cnt.setText(str(len(result)))
        self.stacked_widget.setCurrentWidget(self.admin_widget)
        self.stacked_widget.setCurrentWidget(self.admin_widget)
        self.user_type = "admin"

    def open_db(self):
        self.load_client_types()
        self.stacked_widget.setCurrentWidget(self.db_widget)

    def change_business_interface(self):
        path = self.config_data[0].strip()
        self.current_file.setText(path)
        try:
            with open(path, "r", encoding="utf-8") as file:
                self.load_buisness_information(file)
        except Exception as error:
            self.statusBar().showMessage("Ошибка загрузки файла, некоректный файл или файл не существует")
            self.status_bar.setStyleSheet("background-color: red; color: white;")
            self.business_description_edit.setText("")
            self.business_name_edit.setText("")
            QTimer.singleShot(5000, self.restore_default_color)
        self.stacked_widget.setCurrentWidget(self.buiness_information_widget)

    def save_business_information(self):
        self.config_data[0] = self.current_file.text()
        self.restore_default_color()
        self.statusBar().showMessage("Изменения сохранены")
        self.status_bar.setStyleSheet("background-color: green; color: white;")
        QTimer.singleShot(5000, self.restore_default_color)

    def open_config_file(self):
        try:
            with open("config.txt", 'r+') as config:
                self.config_data = config.readlines()
        except IOError:
            with open("config.txt", 'w+') as config:
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
                    self.load_buisness_information(file)
                    self.current_file.setText(file_path)
                    self.statusBar().showMessage("Файл успешно загружен")
                    self.status_bar.setStyleSheet("background-color: green; color: white;")
                    QTimer.singleShot(3000, self.save_warning)

            except Exception as error:
                self.statusBar().showMessage(
                    "Ошибка загрузки файла, некоректный файл или файл не существует. Изменения не сохранены")
                self.status_bar.setStyleSheet("background-color: red; color: white;")
                QTimer.singleShot(5000, self.restore_default_color)

    def load_buisness_information(self, file):
        data = file.read()
        len_name = int(data[:data.index('\n')])
        business_name = data[data.index('\n') + 1: data.index('\n') + len_name]
        business_description = data[data.index('\n') + len_name:len(data)]
        self.business_name_edit.setText(business_name)
        self.business_description_edit.setText(business_description)

    def save_to_information_file(self):
        file_path = self.current_file.text()
        try:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(f"{len(self.business_name_edit.toPlainText()) + 1}\n")
                file.write(self.business_name_edit.toPlainText())
                file.write(self.business_description_edit.toPlainText())
                self.statusBar().showMessage("Изменения сохранены")
                self.status_bar.setStyleSheet("background-color: green; color: white;")
                QTimer.singleShot(5000, self.restore_default_color)

        except Exception as error:
            self.statusBar().showMessage(
                "Ошибка загрузки файла, некоректный файл или файл не существует. Изменения не сохранены")
            self.status_bar.setStyleSheet("background-color: red; color: white;")
            QTimer.singleShot(5000, self.restore_default_color)

    def open_file_editor(self):
        self.file_editor = FileEditor()
        self.file_editor.show()

    def save_warning(self):
        self.restore_default_color()
        self.statusBar().showMessage("Изменения не сохранены, сохраните изменения!")
        self.status_bar.setStyleSheet("background-color: orange; color: black;")

    def restore_default_color(self):
        self.status_bar.setStyleSheet("")
        self.status_bar.showMessage("")

    def exit_app(self):
        self.conn.close()
        with open( "config.txt", "w", encoding="utf-8") as file:
            file.writelines(self.config_data)
            app.quit()

    def ready_to_edit_file(self):
        if self.ready_edit_file_button.isChecked():
            self.update_current_file_button.setEnabled(True)
            self.business_name_edit.setReadOnly(False)
            self.business_description_edit.setReadOnly(False)
        else:
            self.update_current_file_button.setDisabled(True)
            self.business_name_edit.setReadOnly(True)
            self.business_description_edit.setReadOnly(True)

    def types_user_clicked(self):
        if self.sender().isChecked():
            self.user_types_list.append(self.sender().text())
        else:
            if self.current_element_edit.text() == self.sender().text():
                self.current_element_edit.setText('')
            self.user_types_list.pop(self.user_types_list.index(self.sender().text()))
        self.type_list.clear()
        self.type_list.addItems(self.user_types_list)
        # self.type_list.addItem(self.sender().text())

    def display_current_element(self, current_item):

        if current_item is not None:
            self.current_element_edit.setText(f"{current_item.text()}")

    def delete_current_element(self):
        if self.current_element_edit.text() in self.base_user_types_list:
            self.check_box_dict[self.current_element_edit.text()].setChecked(False)
        self.user_types_list.pop(self.user_types_list.index(self.current_element_edit.text()))
        self.type_list.clear()
        self.type_list.addItems(self.user_types_list)
        self.current_element_edit.setText('')

    def add_current_element(self):
        if self.new_type_edit.text() != '':
            self.user_types_list.append(self.new_type_edit.text())
            self.type_list.clear()
            self.type_list.addItems(self.user_types_list)

    def save_types_clients(self):
        with open("clients-types.csv", 'w', newline='', encoding="utf8") as csvfile:
            writer = csv.writer(csvfile, delimiter=';', quotechar='"')
            for i in range(self.type_list.count()):
                item = self.type_list.item(i)
                writer.writerow([i, item.text()])
                result = self.cursor.execute("""SELECT type FROM requestType WHERE type =  ?""",
                                             (item.text(),)).fetchall()
                if len(result) == 0:
                    self.cursor.execute("""INSERT INTO requestType(type) VALUES (?)""", (item.text(),))
                    self.conn.commit()
                result = self.cursor.execute("""SELECT * FROM requestType """).fetchall()
            self.statusBar().showMessage("Изменения сохранены")
            self.status_bar.setStyleSheet("background-color: green; color: white;")
            QTimer.singleShot(5000, self.restore_default_color)

    def init_sql(self):
        print(self.global_path)
        if not os.path.exists("clientDB.sqlite"):
            QMessageBox.warning(self, "Предупреждение", f"База данных не найдена, проверьте базу данных")
        try:
            self.conn = sqlite3.connect("clientDB.sqlite")
            self.cursor = self.conn.cursor()
        except Exception as error:
            QMessageBox.warning(self, "Предупреждение", f"Ошибка загрузки базы данных {error}")

    def save_request(self):
        # try:
        name = self.client_name.text().lower()
        second_name = self.client_secondname.text().lower()
        surname = self.client_surname.text().lower()
        request_type = self.client_types_list.currentText()
        massage = self.client_massage.toPlainText()
        try:
            id_client = self.cursor.execute(
                """ 
                SELECT * FROM clients WHERE name = ? and secondname = ? and surname = ?""",
                (name, second_name, surname)).fetchone()
            if id_client is None:
                self.cursor.execute("""INSERT INTO clients(name,secondname,surname) VALUES (?,?,?)""",
                                    (name, second_name, surname))
                self.conn.commit()
            id_client = self.cursor.execute(
                """SELECT * FROM clients WHERE name = ? and secondname = ? and surname = ?""",
                (name, second_name, surname)).fetchone()[0]
            request_id = \
                self.cursor.execute("""SELECT id FROM requestType WHERE type = ?""", (request_type,)).fetchone()[0]
            self.cursor.execute("""INSERT INTO requests(client,type,request) VALUES (?,?,?)""",
                                (id_client, request_id, massage))
            self.conn.commit()
            self.statusBar().showMessage("Сообщение записано")
            self.status_bar.setStyleSheet("background-color: green; color: white;")
            QTimer.singleShot(5000, self.restore_default_color)
        except Exception as error:
            self.statusBar().showMessage(
                f"Ошибка при записи сообщения {error}")
            self.status_bar.setStyleSheet("background-color: red; color: white;")
            QTimer.singleShot(5000, self.restore_default_color)

    def load_clients(self):
        query = """SELECT * FROM clients"""
        cnt = 0
        if self.use_name_checkbox.isChecked():
            if self.substr_checkbox.isChecked():
                if cnt != 0:
                    query += f" and name like '%{self.use_name_edit.text()}%'"
                else:
                    query += f" WHERE name like '%{self.use_name_edit.text()}%'"
            else:
                if cnt != 0:
                    query += f" and name = '{self.use_name_edit.text()}'"
                else:
                    query += f" WHERE name = '{self.use_name_edit.text()}'"
            cnt += 1
        if self.use_surname_checkbox.isChecked():
            if self.substr_checkbox.isChecked():
                if cnt != 0:
                    query += f" and surname like '%{self.use_surname_edit.text()}%'"
                else:
                    query += f" WHERE surname like '%{self.use_surname_edit.text()}%'"
            else:
                if cnt != 0:
                    query += f" and surname = '{self.use_surname_edit.text()}'"
                else:
                    query += f" WHERE surname = '{self.use_surname_edit.text()}'"
            cnt += 1
        if self.use_secondname_checkbox.isChecked():
            if self.substr_checkbox.isChecked():
                if cnt != 0:
                    query += f" and secondname like '%{self.use_secondname_edit.text()}%'"
                else:
                    query += f" WHERE secondname like '%{self.use_secondname_edit.text()}%'"
            else:
                if cnt != 0:
                    query += f" and secondname = '{self.use_secondname_edit.text()}'"
                else:
                    query += f" WHERE secondname = '{self.use_secondname_edit.text()}'"
            cnt += 1
        result = self.cursor.execute(query).fetchall()
        data = []
        for row in result:
            data.append(row)
        self.found_strings.setText("Найдено строк: " + str(len(data)))
        if len(data) != 0:
            self.db_view.setColumnCount((len(data[0])))
            self.db_view.setRowCount(len(data))
            self.db_view.setHorizontalHeaderLabels(["Id", "Имя", "Фамилия", "Отчество"])
            for i, row in enumerate(data):
                for j, element in enumerate(row):
                    self.db_view.setItem(i, j, QTableWidgetItem(str(element)))
        else:
            self.db_view.setRowCount(0)

    def unlock_filters(self):
        if self.sender().text() == "Искать с таким именем" and self.sender().isChecked():
            self.use_name_edit.setEnabled(True)
        elif self.sender().text() == "Искать с такой Фамилией" and self.sender().isChecked():
            self.use_secondname_edit.setEnabled(True)
        elif self.sender().text() == "Искать с таким отчеством" and self.sender().isChecked():
            self.use_surname_edit.setEnabled(True)

        if self.sender().text() == "Искать с таким именем" and not self.sender().isChecked():
            self.use_name_edit.setDisabled(True)
        elif self.sender().text() == "Искать с такой Фамилией" and not self.sender().isChecked():
            self.use_secondname_edit.setDisabled(True)
        elif self.sender().text() == "Искать с таким отчеством" and not self.sender().isChecked():
            self.use_surname_edit.setDisabled(True)

    def display_selected_client(self):
        row0 = self.db_view.item(self.db_view.currentRow(), 0).text()
        row1 = self.db_view.item(self.db_view.currentRow(), 1).text()
        row2 = self.db_view.item(self.db_view.currentRow(), 2).text()
        row3 = self.db_view.item(self.db_view.currentRow(), 3).text()
        self.current_client_id.setText(row0)
        self.current_client_name.setText(row1)
        self.current_client_secondname.setText(row2)
        self.current_client_surname.setText(row3)

    def change_client_inf(self):
        try:
            if self.current_client_id.text() != '':
                if self.current_client_name.text() == '':
                    raise WrongClientInf("Имя клиента не может быть пустым")
                if self.current_client_secondname.text() == '':
                    raise WrongClientInf("Фамилия клиента не может быть пустым")
                if self.current_client_surname.text() == '':
                    raise WrongClientInf("Отчество клиента не может быть пустым")

                query = f"""UPDATE clients SET name = '{self.current_client_name.text().lower()}'  WHERE id = 
                '{self.current_client_id.text()}'"""
                self.cursor.execute(query)
                self.conn.commit()
                query = f"""UPDATE clients SET secondname = '{self.current_client_secondname.text().lower()}' 
                 WHERE id = 
                              '{self.current_client_id.text()}'"""
                self.cursor.execute(query)
                self.conn.commit()
                query = f"""UPDATE clients SET surname = '{self.current_client_surname.text().lower()}'  WHERE id = 
                              '{self.current_client_id.text()}'"""
                self.cursor.execute(query)
                self.conn.commit()
                self.statusBar().showMessage("Изменение сохранены")
                self.status_bar.setStyleSheet("background-color: green; color: white;")
                QTimer.singleShot(5000, self.restore_default_color)
        except Exception as error:
            self.statusBar().showMessage(
                f"Ошибка при записи сообщения {error}")
            self.status_bar.setStyleSheet("background-color: red; color: white;")
            QTimer.singleShot(5000, self.restore_default_color)

    def change_ui_client_db(self):
        if self.sender().currentText() == "База данных клиентов":
            self.local_stacked_widget.setCurrentIndex(0)
            self.type_db_combobox.setCurrentIndex(0)
        else:
            self.load_client_types()
            self.local_stacked_widget.setCurrentIndex(1)
            self.type_db_combobox_requests.setCurrentIndex(1)

    def load_requests(self):
        query = """SELECT * FROM requests LEFT JOIN clients ON clients.id = requests.client LEFT JOIN requestType 
        ON requests.type = requestType.id"""
        if self.client_id_checkbox.isChecked():
            query += f""" WHERE requests.client = {(self.client_id_edit.text())}"""
            if self.types_clients_checkbox.isChecked():
                local_query = " and ("

                cnt = 0
                for i in range(self.vbx_layout.count()):
                    if self.client_types_checkbox[i].isChecked():
                        if cnt == 0:
                            local_query += f"""  requestType.type = '{self.client_types_checkbox[i].text()}'"""
                        else:
                            local_query += f""" or requestType.type = '{self.client_types_checkbox[i].text()}'"""
                        cnt += 1
                local_query += ')'
                if cnt != 0:
                    query += local_query
        else:
            cnt = 0
            if self.types_clients_checkbox.isChecked():
                for i in range(self.vbx_layout.count()):
                    if self.client_types_checkbox[i].isChecked():

                        if cnt == 0:
                            query += f""" WHERE requestType.type = '{self.client_types_checkbox[i].text()}'"""
                        else:
                            query += f""" or requestType.type = '{self.client_types_checkbox[i].text()}'"""
                        cnt += 1
        try:
            result = self.cursor.execute(query).fetchall()
            data = []
            for row in result:
                data.append(row)
            self.loaded_rows.setText("Загружено строк: " + str(len(data)))
            while self.db_view_requests.count():
                item = self.db_view_requests.takeAt(0)
                widget = item.widget()
                if widget:
                    widget.deleteLater()
            to_view = []
            if len(data) != 0:
                cnt = len(data)
                for i, row in enumerate(data):
                    cnt -= 1
                    to_view.append(
                        Request(id=str(row[1]), name=row[6], secondname=row[7], surname=row[8], request=row[3],
                                type=row[-1],
                                num=cnt, sql_id=row[0], answer=row[4], conn=self.conn, curs=self.cursor,
                                main_widget=self))
                if self.time_checkbox.isChecked():
                    to_view.reverse()
                for i in range(len(data)):
                    self.db_view_requests.addWidget(to_view[i])
        except Exception as error:
            self.statusBar().showMessage(
                f"Ошибка при записи сообщения {error}")
            self.status_bar.setStyleSheet("background-color: red; color: white;")
            QTimer.singleShot(5000, self.restore_default_color)

    def unlock_client_id_edit(self):
        if self.client_id_checkbox.isChecked():
            self.client_id_edit.setEnabled(True)
        else:
            self.client_id_edit.setDisabled(True)

    def load_client_types(self):
        try:
            with open(f"clients-types.csv", 'r', newline='', encoding="utf8") as csvfile:
                reader = csv.reader(csvfile, delimiter=';', quotechar='"')
                self.client_types_checkbox.clear()
                while self.vbx_layout.count():
                    item = self.vbx_layout.takeAt(0)
                    widget = item.widget()
                    if widget:
                        widget.deleteLater()
                for row in reader:
                    tp = QCheckBox(row[1])
                    self.vbx_layout.addWidget(tp)
                    self.client_types_checkbox.append(tp)
        except Exception as error:
            self.statusBar().showMessage(f"Ошибка чтения csv файла:  {str(error)}")
            self.status_bar.setStyleSheet("background-color: red; color: white;")
            QTimer.singleShot(10000, self.restore_default_color)

    def load_answers(self):
        try:
            query = """SELECT * FROM requests LEFT JOIN clients ON clients.id = requests.client LEFT JOIN requestType 
            ON requests.type = requestType.id"""
            query += (f" WHERE name = '{self.client_name.text()}' and secondname = '{self.client_secondname.text()}' "
                      f"and surname = '{self.client_surname.text()}'")
            result = self.cursor.execute(query).fetchall()
            data = []
            to_view = []
            for row in result:
                data.append(row)
            while self.third_layout.count():
                item = self.third_layout.takeAt(0)
                widget = item.widget()
                if widget:
                    widget.deleteLater()
            self.loaded_strings.setText(f"Загружено строк: {len(data)}")
            if len(data) != 0:
                cnt = len(data)
                for i, row in enumerate(data):
                    cnt -= 1
                    new_request = Request(id=str(row[1]), name=row[6], secondname=row[7], surname=row[8],
                                          request=row[3],
                                          type=row[-1],
                                          num=cnt, sql_id=row[0], answer=row[4], conn=self.conn, curs=self.cursor,
                                          main_widget=self)
                    new_request.save_answer_button.setDisabled(True)
                    new_request.answer.setReadOnly(True)
                    to_view.append(new_request)
                for element in to_view:
                    self.third_layout.addWidget(element)

        except Exception as error:
            print(error)
            self.statusBar().showMessage(
                f"Ошибка при записи сообщения {error}")
            self.status_bar.setStyleSheet("background-color: red; color: white;")
            QTimer.singleShot(5000, self.restore_default_color)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BusinessControlSystem()
    app.aboutToQuit.connect(window.exit_app)
    window.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
