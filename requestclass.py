import sys

from PyQt5.QtCore import QDate, QRect, QSize, Qt, QTimer
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import (QWidget, QApplication, QPushButton, QLineEdit, QLabel, QLCDNumber,
                             QCheckBox, QRadioButton,
                             QMainWindow, QButtonGroup, QGridLayout, QTextEdit, QStatusBar, QTextBrowser,
                             QTableWidgetItem, QTableWidget, QInputDialog, QLayout, QSizePolicy, QHBoxLayout,
                             QVBoxLayout, QComboBox, QAction, QMenuBar, QStackedWidget, QFrame, QFormLayout, QToolBar,
                             QListWidget, QScrollArea)

from PyQt5 import QtCore, QtGui, QtWidgets


class Request(QMainWindow):
    def __init__(self, id='', name='', secondname='', surname='', request='', type='', num='0', sql_id=0, answer='',
                 conn=None, curs=None, main_widget=None):
        super().__init__()
        self.id = QLineEdit(id, self)
        self.name = QLineEdit(name, self)
        self.secondname = QLineEdit(secondname, self)
        self.surname = QLineEdit(surname, self)
        self.message = QTextEdit(request, self)
        self.type = QLineEdit(type, self)
        if answer is None:
            self.answer = QTextEdit("Ответа нет", self)
        else:
            self.answer = QTextEdit(answer, self)
        self.save_answer_button = QPushButton("Сохранить ответ", self)
        self.sql_id = sql_id
        self.conn = conn
        self.curs = curs
        self.save_answer_button.clicked.connect(self.save_answer)
        self.main_window = main_widget
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
        second_layout.addRow(QLabel("Тип пользователя"), self.type)

        third_layout = QFormLayout()
        third_layout.addRow(QLabel("Сообщение"))
        third_layout.addRow(self.message)

        fourth_layout = QFormLayout()
        fourth_layout.addRow(QLabel("Ответ"))
        fourth_layout.addRow(self.answer)
        fourth_layout.addRow(self.save_answer_button)

        first_layout.addWidget(QLabel(f"Номер запроса: {num}"))
        first_layout.addLayout(second_layout)
        first_layout.addLayout(third_layout)
        first_layout.addLayout(fourth_layout)

        main_layout = QVBoxLayout()
        main_layout.addWidget(first_frame)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)

        self.setCentralWidget(central_widget)

    def save_answer(self):
        try:
            query = f"""UPDATE requests
            SET answer = '{self.answer.toPlainText()}'
            WHERE id = {self.sql_id}"""
            self.curs.execute(query)
            self.conn.commit()
            self.main_window.statusBar().showMessage("Изменение сохранены")
            self.main_window.statusBar().setStyleSheet("background-color: green; color: white;")
            QTimer.singleShot(5000, self.main_window.restore_default_color)
        except Exception as error:
            self.statusBar().showMessage(
                f"Ошибка при записи сообщения {error}")
            self.main_window.status_bar.setStyleSheet("background-color: red; color: white;")
            QTimer.singleShot(5000, self.main_window.restore_default_color)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Request()
    window.show()
    sys.exit(app.exec())
