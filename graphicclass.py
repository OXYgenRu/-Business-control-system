import csv
import sys

import random

from PyQt5.QtCore import QDate, QRect, QSize, Qt
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import (QWidget, QApplication, QPushButton, QLineEdit, QLabel, QLCDNumber,
                             QCheckBox, QRadioButton,
                             QMainWindow, QButtonGroup, QGridLayout, QTextEdit, QStatusBar, QTextBrowser,
                             QTableWidgetItem, QTableWidget, QInputDialog, QLayout, QSizePolicy, QHBoxLayout,
                             QVBoxLayout, QComboBox, QAction, QMenuBar, QStackedWidget, QFrame, QFormLayout, QToolBar)

from PyQt5 import QtCore, QtGui, QtWidgets


class BusinessControlSystemGraphic:
    def __init__(self):
        self.stacked_widget = QStackedWidget()

    def init_ui_admin(self):
        self.admin_widget = QMainWindow()
        self.admin_widget.setMenuBar(self.menuBarAdmin)
        self.admin_widget.addToolBar(Qt.LeftToolBarArea, self.main_tool_bar)
        # self.label = QLabel("admin", self.admin_widget)
        # self.label.move(30, 30)

    def init_ui_user(self):
        self.user_widget = QMainWindow()
        self.user_widget.setMenuBar(self.menuBarUser)
        self.user_business_information_name = QTextEdit(self.user_widget)
        self.user_business_information_description = QTextEdit(self.user_widget)
        self.user_business_information_name.setReadOnly(True)
        self.user_business_information_description.setReadOnly(True)
        first_layout = QFormLayout()
        first_layout.addRow(self.user_business_information_name)
        first_layout.addRow(self.user_business_information_description)
        form_layout = QVBoxLayout()
        form_layout.addLayout(first_layout)

        central_widget = QWidget()
        central_widget.setLayout(form_layout)

        self.user_widget.setCentralWidget(central_widget)
        # self.label1 = QLabel("user", self.user_widget)
        # self.label1.move(30, 30)

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

        self.business_name_edit = QTextEdit(first_frame)
        self.business_description_edit = QTextEdit(first_frame)
        self.save_infromation_button = QPushButton("Сохранить изменения в файл конфигурации",
                                                   self.buiness_information_widget)
        self.current_file = QLineEdit(third_frame)
        self.current_file.setReadOnly(True)
        self.business_name_edit.setReadOnly(True)
        self.business_description_edit.setReadOnly(True)
        self.open_information_file = QPushButton("Загрузить файл с информацией", self.buiness_information_widget)
        # first_frame.setStyleSheet("border: 1px solid black;")
        # second_frame.setStyleSheet("border: 1px solid black;")

        first_layout = QFormLayout()
        second_layout = QFormLayout()
        third_layout = QFormLayout()

        first_layout.addRow(QLabel("Информация о бизнесе"))
        first_layout.addRow(QLabel("Настройте информацию о бизнесе, которую будут видеть пользователи."))

        second_layout.addRow(QLabel("Просмотр текущего файла"))
        second_layout.addRow(self.business_name_edit, QLabel("Название"))
        second_layout.addRow(self.business_description_edit, QLabel("Описание"))

        third_layout.addRow(QLabel("Загружать информацию из файла:"), self.current_file)
        third_layout.addRow(QLabel("Выбрать новый файл с информацией"), self.open_information_file)

        main_layout = QVBoxLayout()

        first_frame.setLayout(first_layout)
        second_frame.setLayout(second_layout)
        third_frame.setLayout(third_layout)

        main_layout.addWidget(first_frame, stretch=1)
        main_layout.addWidget(third_frame, stretch=1)
        main_layout.addWidget(second_frame, stretch=2)
        main_layout.addStretch(5)
        main_layout.addWidget(self.save_infromation_button, stretch=2)
        # form_layout.addWidget(first_frame)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)

        self.buiness_information_widget.setCentralWidget(central_widget)

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
        # self.action_open_main_page.setStyleSheet("color: red; background-color: yellow;")

    def create_admin_menubar(self):
        self.menuBarAdmin = QMenuBar()
        self.user_now_admin = self.menuBarAdmin.addMenu("Администратор")
        # self.user_now_admin.setStyleSheet("background-color: #FF0000;")
        self.settingsMenu = self.menuBarAdmin.addMenu("Настройки")
        self.businessInformationMenu = self.menuBarAdmin.addMenu("Информация о бизнесе")

        self.settingsMenu.addAction(self.action_change_type_of_user_admin)
        self.settingsMenu.addAction(self.action_exit_admin)

        self.businessInformationMenu.addAction(self.action_business_information)

        self.menuBarBuinessInformation = QMenuBar()
        self.menuBarBuinessInformation.addMenu(self.user_now_admin)
        self.menuBarBuinessInformation.addMenu(self.settingsMenu)
        self.menuBarBuinessInformation.addMenu(self.businessInformationMenu)

    def create_user_menubar(self):
        self.menuBarUser = QMenuBar()
        self.user_now_user = self.menuBarUser.addMenu("Клиент")
        self.settingsMenu = self.menuBarUser.addMenu("Настройки")
        self.settingsMenu.addAction(self.action_change_type_of_user_user)
        self.settingsMenu.addAction(self.action_exit_user)
        # self.action_change_type_of_user.triggered.connect(self.change_typed_user_interface)

    def create_admin_toolbar(self):
        self.main_tool_bar = QToolBar()
        self.main_tool_bar.setContextMenuPolicy(Qt.PreventContextMenu)
        self.main_tool_bar.setMovable(False)
        self.main_tool_bar.setOrientation(Qt.Vertical)
        self.main_tool_bar.addAction(self.action_open_main_page)
        self.main_tool_bar.addAction(self.action_business_information)

        self.buiness_information_tool_bar = QToolBar()
        self.buiness_information_tool_bar.setContextMenuPolicy(Qt.PreventContextMenu)
        self.buiness_information_tool_bar.setMovable(False)
        self.buiness_information_tool_bar.setOrientation(Qt.Vertical)
        self.buiness_information_tool_bar.addAction(self.action_open_main_page)
        self.buiness_information_tool_bar.addAction(self.action_business_information)
