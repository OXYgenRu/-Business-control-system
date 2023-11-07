import csv
import sys
import sqlite3
import random

from PyQt5.QtCore import QDate, QRect, QSize, Qt
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import (QWidget, QApplication, QPushButton, QLineEdit, QLabel, QLCDNumber,
                             QCheckBox, QRadioButton,
                             QMainWindow, QButtonGroup, QGridLayout, QTextEdit, QStatusBar, QTextBrowser,
                             QTableWidgetItem, QTableWidget, QInputDialog, QLayout, QSizePolicy, QHBoxLayout,
                             QVBoxLayout, QComboBox, QAction, QMenuBar, QStackedWidget, QFrame, QFormLayout, QToolBar,
                             QListWidget)

from PyQt5 import QtCore, QtGui, QtWidgets


class BusinessControlSystemGraphic:
    def __init__(self):
        self.stacked_widget = QStackedWidget()
        self.check_box_dict = {}

    def init_ui_admin(self):
        self.admin_widget = QMainWindow()
        self.admin_widget.setMenuBar(self.menuBarAdmin)
        self.admin_widget.addToolBar(Qt.LeftToolBarArea, self.main_tool_bar)

    def init_ui_user(self):
        self.user_widget = QMainWindow()
        self.user_widget.setMenuBar(self.menuBarUser)

        first_frame = QFrame(self.user_widget)
        first_frame.setFrameShape(QFrame.StyledPanel)
        second_frame = QFrame(self.user_widget)
        second_frame.setFrameShape(QFrame.StyledPanel)

        self.user_business_information_name = QTextEdit(self.user_widget)
        self.user_business_information_description = QTextEdit(self.user_widget)
        self.user_business_information_name.setReadOnly(True)
        self.user_business_information_description.setReadOnly(True)
        self.client_types_list = QComboBox(self.user_widget)
        self.client_name = QLineEdit(self.user_widget)
        self.client_secondname = QLineEdit(self.user_widget)
        self.client_surname = QLineEdit(self.user_widget)
        # self.client_telephone = QLineEdit(self.user_widget)
        self.client_massage = QTextEdit(self.user_widget)
        self.client_send_massage_button = QPushButton("Отправить", self.user_widget)

        first_layout = QFormLayout()
        second_layout = QFormLayout()
        first_frame.setLayout(first_layout)
        second_frame.setLayout(second_layout)

        first_layout.addRow(QLabel("Добро пожаловать в систему взаимодействия клиента и бизнеса!"))
        first_layout.addRow(QLabel("Наша компания:"), self.user_business_information_name)
        first_layout.addRow(QLabel("О нас:"), self.user_business_information_description)

        second_layout.addRow(QLabel("Напишите сообщение или заказ и отправьте нам!"))
        second_layout.addRow(QLabel("Выберете цель сообщения:"), self.client_types_list)
        second_layout.addRow(QLabel("Фамилия"), self.client_secondname)
        second_layout.addRow(QLabel("Имя"), self.client_name)
        second_layout.addRow(QLabel("Отчество"), self.client_surname)
        # second_layout.addRow(QLabel("Телефон(Для одного клиента вводить всегда в одном виде)"), self.client_telephone)
        second_layout.addRow(QLabel("Введите сообщение"), self.client_massage)

        main_layout = QVBoxLayout()
        main_layout.addWidget(first_frame, stretch=1)
        main_layout.addWidget(second_frame, stretch=2)
        main_layout.addWidget(self.client_send_massage_button)
        main_layout.addStretch(50)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)

        self.user_widget.setCentralWidget(central_widget)

    def init_ui_buiness_information(self):
        # self.business_infromatiom_menubar = self.menuBarAdmin
        self.buiness_information_widget = QMainWindow()
        self.buiness_information_widget.setMenuBar(self.menuBarBuinessInformation)
        self.buiness_information_widget.addToolBar(Qt.LeftToolBarArea, self.buiness_information_tool_bar)

        first_frame = QFrame(self.buiness_information_widget)
        first_frame.setFrameShape(QFrame.StyledPanel)
        second_frame = QFrame(self.buiness_information_widget)
        second_frame.setFrameShape(QFrame.StyledPanel)
        third_frame = QFrame(self.buiness_information_widget)
        third_frame.setFrameShape(QFrame.StyledPanel)
        forth_frame = QFrame(self.buiness_information_widget)
        forth_frame.setFrameShape(QFrame.StyledPanel)

        self.business_name_edit = QTextEdit(first_frame)
        self.business_description_edit = QTextEdit(first_frame)
        self.save_infromation_button = QPushButton("Сохранить изменения в файл конфигурации",
                                                   self.buiness_information_widget)
        self.update_current_file_button = QPushButton("Сохранить изменения текущего файла")
        self.update_current_file_button.setDisabled(True)
        self.create_file_button = QPushButton("Создать файл", self.buiness_information_widget)
        self.current_file = QLineEdit(third_frame)
        self.current_file.setReadOnly(True)
        self.business_name_edit.setReadOnly(True)
        self.business_description_edit.setReadOnly(True)
        self.open_information_file_button = QPushButton("Загрузить файл с информацией", self.buiness_information_widget)
        self.ready_edit_file_button = QCheckBox("Хочу редактировать файл")

        first_layout = QFormLayout()
        second_layout = QFormLayout()
        third_layout = QFormLayout()
        forth_layout = QFormLayout()

        first_layout.addRow(QLabel("Информация о бизнесе"))
        first_layout.addRow(QLabel("Настройте информацию о бизнесе, которую будут видеть пользователи."))

        second_layout.addRow(QLabel("Просмотр текущего файла"))
        second_layout.addRow(self.business_name_edit, QLabel("Название"))
        second_layout.addRow(self.business_description_edit, QLabel("Описание"))
        second_layout.addRow(self.ready_edit_file_button, self.update_current_file_button)

        third_layout.addRow(QLabel("Загружать информацию из файла:"))
        third_layout.addRow(self.current_file)
        third_layout.addRow(QLabel("Выбрать новый файл с информацией"), self.open_information_file_button)

        forth_layout.addRow(QLabel("Создать новый файл информации"), self.create_file_button)

        main_layout = QVBoxLayout()

        first_frame.setLayout(first_layout)
        second_frame.setLayout(second_layout)
        third_frame.setLayout(third_layout)
        forth_frame.setLayout(forth_layout)

        main_layout.addWidget(first_frame, stretch=1)
        main_layout.addWidget(third_frame, stretch=1)
        main_layout.addWidget(second_frame, stretch=2)
        main_layout.addWidget(forth_frame, stretch=1)
        main_layout.addStretch(5)
        main_layout.addWidget(self.save_infromation_button, stretch=2)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)

        self.buiness_information_widget.setCentralWidget(central_widget)

    def init_ui_types_clients(self):
        self.types_clients_widget = QMainWindow()
        self.types_clients_widget.setMenuBar(self.menuBarTypesClients)
        self.types_clients_widget.addToolBar(Qt.LeftToolBarArea, self.types_clients_tool_bar)
        self.check_box_1 = QCheckBox("Задать вопрос", self.types_clients_widget)
        self.check_box_2 = QCheckBox("Покупатель", self.types_clients_widget)
        self.check_box_3 = QCheckBox("Другое", self.types_clients_widget)
        self.type_list = QListWidget(self.types_clients_widget)
        self.new_type_edit = QLineEdit(self.types_clients_widget)
        self.add_new_type_button = QPushButton("Добавить новый тип", self.types_clients_widget)
        self.delete_current_element_button = QPushButton("Удалить выбранный элемент", self.types_clients_widget)
        self.current_element_edit = QLineEdit(self.types_clients_widget)
        self.save_types_clients_button = QPushButton("Сохранить изменения", self.types_clients_widget)

        self.check_box_dict[self.check_box_1.text()] = self.check_box_1
        self.check_box_dict[self.check_box_2.text()] = self.check_box_2
        self.check_box_dict[self.check_box_3.text()] = self.check_box_3

        self.current_element_edit.setReadOnly(True)

        first_frame = QFrame(self.types_clients_widget)
        first_frame.setFrameShape(QFrame.StyledPanel)
        second_frame = QFrame(self.types_clients_widget)
        second_frame.setFrameShape(QFrame.StyledPanel)
        third_frame = QFrame(self.types_clients_widget)
        third_frame.setFrameShape(QFrame.StyledPanel)

        first_layout = QFormLayout()
        second_layout = QFormLayout()
        third_layout = QFormLayout()

        first_layout.addRow(QLabel("Типы клиентов"))
        first_layout.addRow(QLabel("Настройте типы клиентов, под которыми пользователи будут отмечены в базе данных."))

        second_layout.addRow(QLabel("Выберете стандартные типы из списка:"))
        second_layout.addRow(self.check_box_1, self.check_box_2)
        second_layout.addRow(self.check_box_3)

        third_layout.addRow(QLabel("Типы пользователей:"), self.type_list)
        third_layout.addRow(self.add_new_type_button, self.new_type_edit)
        third_layout.addRow(self.delete_current_element_button, self.current_element_edit)

        first_frame.setLayout(first_layout)
        second_frame.setLayout(second_layout)
        third_frame.setLayout(third_layout)

        main_layout = QVBoxLayout()
        main_layout.addWidget(first_frame, stretch=1)
        main_layout.addWidget(second_frame, stretch=1)
        main_layout.addWidget(third_frame, stretch=1)
        main_layout.addWidget(self.save_types_clients_button)
        main_layout.addStretch(1)
        central_widget = QWidget()
        central_widget.setLayout(main_layout)

        self.types_clients_widget.setCentralWidget(central_widget)

    def init_ui_db_interface(self):
        self.db_widget = QMainWindow()
        self.db_widget.setMenuBar(self.menuBarDB)
        self.db_widget.addToolBar(Qt.LeftToolBarArea, self.db_tool_bar)

    def create_actions_user(self):
        self.action_change_type_of_user_user = QAction(QIcon("icons/user-icon.svg"), "Сменить тип пользователя на "
                                                                                     "администратор", self)
        self.action_change_type_of_user_user.setShortcut("Ctrl+D")
        self.action_exit_user = QAction(QIcon("icons/exit-icon.svg"), "Выход", self)
        self.action_exit_user.setShortcut("Alt+F4")

    def create_actions_admin(self):
        self.action_change_type_of_user_admin = QAction(QIcon("icons/user-icon.svg"), "Сменить тип пользователя на "
                                                                                      "клиент", self)
        self.action_change_type_of_user_admin.setShortcut("Ctrl+D")
        self.action_exit_admin = QAction(QIcon("icons/exit-icon.svg"), "Выход", self)
        self.action_exit_admin.setShortcut("Alt+F4")
        self.action_business_information = QAction(QIcon("icons/infromation-icon.svg"), "Открыть информацию о бизнесе",
                                                   self)
        self.action_open_main_page = QAction(QIcon("icons/mainpage-icon.svg"), "Главная страница")
        self.action_open_clients_types_page = QAction(QIcon("icons/types-users-icon.svg"),
                                                      "Открыть настройки типов клиентов")
        self.action_create_information_file = QAction(QIcon("icons/create-information-file-icon.svg"),
                                                      "Создать файл информации")
        self.action_open_db_page = QAction(QIcon("icons/db-icon.svg"), "Открыть базу данных")

    def create_admin_menubar(self):
        self.menuBarAdmin = QMenuBar()
        self.user_now_admin = self.menuBarAdmin.addMenu("Администратор")
        # self.user_now_admin.setStyleSheet("background-color: #FF0000;")
        self.settingsMenu = self.menuBarAdmin.addMenu("Настройки")
        self.businessInformationMenu = self.menuBarAdmin.addMenu("Информация о бизнесе")
        self.settingsMenu.addAction(self.action_change_type_of_user_admin)
        self.settingsMenu.addAction(self.action_exit_admin)
        self.businessInformationMenu.addAction(self.action_business_information)
        self.businessInformationMenu.addAction(self.action_create_information_file)
        self.typesClientsMenu = self.menuBarAdmin.addMenu("Типы клиентов")
        self.typesClientsMenu.addAction(self.action_open_clients_types_page)
        self.dbMenu = self.menuBarAdmin.addMenu("Открыть базу данных клиентов")
        self.dbMenu.addAction(self.action_open_db_page)

        self.menuBarBuinessInformation = QMenuBar()
        self.menuBarBuinessInformation.addMenu(self.user_now_admin)
        self.menuBarBuinessInformation.addMenu(self.settingsMenu)
        self.menuBarBuinessInformation.addMenu(self.businessInformationMenu)
        self.menuBarBuinessInformation.addMenu(self.typesClientsMenu)
        self.menuBarBuinessInformation.addMenu(self.dbMenu)

        self.menuBarTypesClients = QMenuBar()
        self.menuBarTypesClients.addMenu(self.user_now_admin)
        self.menuBarTypesClients.addMenu(self.settingsMenu)
        self.menuBarTypesClients.addMenu(self.businessInformationMenu)
        self.menuBarTypesClients.addMenu(self.typesClientsMenu)
        self.menuBarTypesClients.addMenu(self.dbMenu)

        self.menuBarDB = QMenuBar()
        self.menuBarDB.addMenu(self.user_now_admin)
        self.menuBarDB.addMenu(self.settingsMenu)
        self.menuBarDB.addMenu(self.businessInformationMenu)
        self.menuBarDB.addMenu(self.typesClientsMenu)
        self.menuBarDB.addMenu(self.dbMenu)

    def create_user_menubar(self):
        self.menuBarUser = QMenuBar()
        self.user_now_user = self.menuBarUser.addMenu("Клиент")
        self.settingsMenu = self.menuBarUser.addMenu("Настройки")
        self.settingsMenu.addAction(self.action_change_type_of_user_user)
        self.settingsMenu.addAction(self.action_exit_user)

    def create_admin_toolbar(self):
        self.main_tool_bar = QToolBar()
        self.main_tool_bar.setContextMenuPolicy(Qt.PreventContextMenu)
        self.main_tool_bar.setMovable(False)
        self.main_tool_bar.setOrientation(Qt.Vertical)
        self.main_tool_bar.addAction(self.action_open_main_page)
        self.main_tool_bar.addAction(self.action_business_information)
        self.main_tool_bar.addAction(self.action_open_clients_types_page)
        self.main_tool_bar.addAction(self.action_open_db_page)

        self.buiness_information_tool_bar = QToolBar()
        self.buiness_information_tool_bar.setContextMenuPolicy(Qt.PreventContextMenu)
        self.buiness_information_tool_bar.setMovable(False)
        self.buiness_information_tool_bar.setOrientation(Qt.Vertical)
        self.buiness_information_tool_bar.addAction(self.action_open_main_page)
        self.buiness_information_tool_bar.addAction(self.action_business_information)
        self.buiness_information_tool_bar.addAction(self.action_open_clients_types_page)
        self.buiness_information_tool_bar.addAction(self.action_open_db_page)

        self.types_clients_tool_bar = QToolBar()
        self.types_clients_tool_bar.setContextMenuPolicy(Qt.PreventContextMenu)
        self.types_clients_tool_bar.setMovable(False)
        self.types_clients_tool_bar.setOrientation(Qt.Vertical)
        self.types_clients_tool_bar.addAction(self.action_open_main_page)
        self.types_clients_tool_bar.addAction(self.action_business_information)
        self.types_clients_tool_bar.addAction(self.action_open_clients_types_page)
        self.types_clients_tool_bar.addAction(self.action_open_db_page)

        self.db_tool_bar = QToolBar()
        self.db_tool_bar.setContextMenuPolicy(Qt.PreventContextMenu)
        self.db_tool_bar.setMovable(False)
        self.db_tool_bar.setOrientation(Qt.Vertical)
        self.db_tool_bar.addAction(self.action_open_main_page)
        self.db_tool_bar.addAction(self.action_business_information)
        self.db_tool_bar.addAction(self.action_open_clients_types_page)
        self.db_tool_bar.addAction(self.action_open_db_page)
