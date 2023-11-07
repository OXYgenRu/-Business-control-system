import csv
import sys
import os

from functools import partial

from PyQt5.QtCore import QDate, QRect, QSize, Qt, QTimer
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import (QWidget, QApplication, QPushButton, QLineEdit, QLabel, QLCDNumber,
                             QCheckBox, QRadioButton,
                             QMainWindow, QButtonGroup, QGridLayout, QTextEdit, QStatusBar, QTextBrowser,
                             QTableWidgetItem, QTableWidget, QInputDialog, QLayout, QSizePolicy, QHBoxLayout,
                             QVBoxLayout, QComboBox, QAction, QMenuBar, QStackedWidget, QFrame, QFormLayout, QToolBar,
                             QFileDialog, QMessageBox)

from PyQt5 import QtCore, QtGui, QtWidgets


class FileEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.status_bar = QStatusBar()
        self.initUI()

        self.file_path_choise.clicked.connect(self.choice_file_path)
        self.create_file_button.clicked.connect(self.create_file)

    def initUI(self):
        self.setGeometry(150, 150, 600, 400)
        self.setWindowTitle('Создать файл')
        self.main_layout = QVBoxLayout()
        self.file_name_edit = QLineEdit(self)
        self.file_path_choise = QPushButton("Выбор пути файла")
        self.file_path_edit = QLineEdit(self)
        self.name = QTextEdit(self)
        self.description = QTextEdit(self)
        self.create_file_button = QPushButton("Создать файл", self)

        first_frame = QFrame(self)
        first_frame.setFrameShape(QFrame.StyledPanel)
        second_frame = QFrame(self)
        second_frame.setFrameShape(QFrame.StyledPanel)

        first_layout = QFormLayout()
        first_layout.addRow(QLabel("Выберете название нового файла(с .txt):"), self.file_name_edit)
        first_layout.addRow(QLabel("Выберете папку расположения нового файла:"), self.file_path_choise)
        first_layout.addRow(QLabel("Файл будет распологаться в:"))
        first_layout.addRow(self.file_path_edit)

        second_layout = QFormLayout()
        second_layout.addRow(self.name, QLabel("Название"))
        second_layout.addRow(self.description, QLabel("Описание"))

        first_frame.setLayout(first_layout)
        second_frame.setLayout(second_layout)

        self.main_layout.addWidget(first_frame)
        self.main_layout.addWidget(second_frame)
        self.main_layout.addWidget(self.create_file_button)

        self.central_widget = QWidget()
        self.central_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.central_widget)

    def choice_file_path(self):
        file_dialog = QFileDialog()
        file_path = QFileDialog.getExistingDirectory(self, "Выберите папку для нового файла", "")
        print(file_path)
        if file_path:
            self.file_path_edit.setText(file_path)

    def create_file(self):
        flag = False
        path = f"{self.file_path_edit.text()}/{self.file_name_edit.text()}"
        if os.path.exists(path):
            flag = True
            reply = QMessageBox.question(self, "Предупреждение", "Данный файл уже существует, хоите перезаписать его?",
                                         QMessageBox.Ok | QMessageBox.Cancel, QMessageBox.Cancel)
            if reply == QMessageBox.Ok:
                flag = False
        if not flag:
            try:
                with open(path, "w", encoding="utf-8") as file:
                    file.write(f"{len(self.name.toPlainText()) + 1}\n")
                    file.write(self.name.toPlainText())
                    file.write(self.description.toPlainText())
                self.statusBar().showMessage("Файл успешно записан")
                self.statusBar().setStyleSheet("background-color: green; color: white;")
                QTimer.singleShot(5000, self.restore_default_color)

            except Exception as error:
                self.statusBar().showMessage(f"Ошибка записи файла: {error}")
                self.statusBar().setStyleSheet("background-color: red; color: black;")
                QTimer.singleShot(5000, self.restore_default_color)

    def restore_default_color(self):
        self.statusBar().setStyleSheet("")
        self.statusBar().showMessage("")
