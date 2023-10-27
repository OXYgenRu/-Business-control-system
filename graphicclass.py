import csv
import sys

import random

from PyQt5.QtCore import QDate, QRect, QSize
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import (QWidget, QApplication, QPushButton, QLineEdit, QLabel, QLCDNumber,
                             QCheckBox, QRadioButton,
                             QMainWindow, QButtonGroup, QGridLayout, QTextEdit, QStatusBar, QTextBrowser,
                             QTableWidgetItem, QTableWidget, QInputDialog, QLayout, QSizePolicy, QHBoxLayout,
                             QVBoxLayout, QComboBox, QAction, QMenuBar, QStackedWidget)

from PyQt5 import QtCore, QtGui, QtWidgets


class BusinessControlSystemGraphic:
    def __init__(self):
        self.stacked_widget = QStackedWidget()

    def init_ui_admin(self):
        self.admin_widget = QMainWindow()
        self.admin_widget.setMenuBar(self.menuBarAdmin)
        self.push_batton = QPushButton("cool", self.admin_widget)
        self.push_batton.move(40, 40)

    def init_ui_user(self):
        self.user_widget = QMainWindow()
        self.user_widget.setMenuBar(self.menuBarUser)

    def create_actions_user(self):
        self.action_change_type_of_user_user = QAction(QIcon("icons/user-icon.svg"), "Change user", self)
        self.action_change_type_of_user_user.setShortcut("Ctrl+D")
        self.action_exit_user = QAction(QIcon("icons/exit-icon.svg"), "Exit", self)
        # self.action_exit_user.setShortcut("Alt+F4")

    def create_actions_admin(self):
        self.action_change_type_of_user_admin = QAction(QIcon("icons/user-icon.svg"), "Change user", self)
        self.action_change_type_of_user_admin.setShortcut("Ctrl+D")
        self.action_exit_admin = QAction(QIcon("icons/exit-icon.svg"), "Exit", self)
        # self.action_exit_admin.setShortcut("Alt+F4")

    def create_admin_menubar(self):
        self.menuBarAdmin = QMenuBar()
        self.settingsMenu = self.menuBarAdmin.addMenu("Настройки")
        self.settingsMenu.addAction(self.action_change_type_of_user_admin)
        self.settingsMenu.addAction(self.action_exit_admin)

    def create_user_menubar(self):
        self.menuBarUser = QMenuBar()
        self.settingsMenu = self.menuBarUser.addMenu("Настройки")
        self.settingsMenu.addAction(self.action_change_type_of_user_user)
        self.settingsMenu.addAction(self.action_exit_user)
        # self.action_change_type_of_user.triggered.connect(self.change_typed_user_interface)
