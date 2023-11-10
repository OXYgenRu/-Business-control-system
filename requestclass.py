import sys

from PyQt5.QtCore import QDate, QRect, QSize, Qt
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import (QWidget, QApplication, QPushButton, QLineEdit, QLabel, QLCDNumber,
                             QCheckBox, QRadioButton,
                             QMainWindow, QButtonGroup, QGridLayout, QTextEdit, QStatusBar, QTextBrowser,
                             QTableWidgetItem, QTableWidget, QInputDialog, QLayout, QSizePolicy, QHBoxLayout,
                             QVBoxLayout, QComboBox, QAction, QMenuBar, QStackedWidget, QFrame, QFormLayout, QToolBar,
                             QListWidget, QScrollArea)

from PyQt5 import QtCore, QtGui, QtWidgets


class Request(QMainWindow):
    def __init__(self, id='', name='', secondname='', surname='', request='', type=''):
        super().__init__()
        self.id = QLineEdit(id, self)
        self.name = QLineEdit(name, self)
        self.secondname = QLineEdit(secondname, self)
        self.surname = QLineEdit(surname, self)
        self.message = QTextEdit(request, self)
        self.type = QLineEdit(type, self)

        self.id.setReadOnly(True)
        self.name.setReadOnly(True)
        self.secondname.setReadOnly(True)
        self.surname.setReadOnly(True)
        self.message.setReadOnly(True)
        self.type.setReadOnly(True)

        first_layout = QHBoxLayout()
        first_frame = QFrame(self)
        first_frame.setFrameShape(QFrame.StyledPanel)
        first_frame.setLayout(first_layout)

        second_layout = QFormLayout()
        second_layout.addRow(QLabel("Пользователь"))
        second_layout.addRow(QLabel("Id"), self.id)
        second_layout.addRow(QLabel("Имя"), self.name)
        second_layout.addRow(QLabel("Фамилия"), self.secondname)
        second_layout.addRow(QLabel("Отчество"), self.surname)
        second_layout.addRow(QLabel("Типы пользователя"), self.type)

        third_layout = QFormLayout()
        third_layout.addRow(QLabel("Сообщение"))
        third_layout.addRow(self.message)

        first_layout.addLayout(second_layout)
        first_layout.addLayout(third_layout)

        main_layout = QVBoxLayout()
        main_layout.addWidget(first_frame)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)

        self.setCentralWidget(central_widget)


class Type(QMainWindow):
    def __init__(self, type=''):
        super().__init__()
        self.type = type
        self.checkbox = QCheckBox(self.type, self)
        self.setCentralWidget(self.checkbox)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Request()
    window.show()
    sys.exit(app.exec())
