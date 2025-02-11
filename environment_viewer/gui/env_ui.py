
import sys
import os
from pathlib import PurePath

try:
    from PyQt5 import QtWidgets, QtGui, QtCore
except:
    ## PySide2 is for Nuke
    from PySide2 import QtWidgets, QtGui, QtCore

abspath = PurePath(os.path.abspath(__file__))
CSS_PATH = os.path.join(abspath.parents[1],"stylesheet", 'gui_stylesheet.css')


class EnvironmentViewer(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(EnvironmentViewer, self).__init__(parent=parent)

        self.setWindowTitle("Environment Viewer")
        self.resize(800,700)
        self.setWindowFlag(QtCore.Qt.WindowType.WindowStaysOnTopHint)

        # Create the main layout for the window
        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.setContentsMargins(2,2,2,2)
        self.main_layout.setSpacing(1)


        # FitlerPanel
        filter_layout = QtWidgets.QVBoxLayout()
        filter_layout.setContentsMargins(0,0,0,0)
        self.filter_bar = QtWidgets.QLineEdit()
        self.filter_bar.textChanged.connect(lambda: self.filter_environments())
        self.filter_bar.setPlaceholderText("Filter Environment Variables...")
        filter_layout.addWidget(self.filter_bar)

        # Table Widget
        self.environ_table = QtWidgets.QTableWidget()
        self.environ_table.horizontalHeader().setStretchLastSection(True)
        self.environ_table.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.environ_table.verticalHeader().setVisible(False)
        self.environ_table.verticalHeader().setFixedWidth(600)
        self.environ_table.setWordWrap(True)




        for index, envs in enumerate(os.environ):
            self.environ_table.setRowCount(index+1)
            self.environ_table.setColumnCount(2)

            environ_name = QtWidgets.QTableWidgetItem(envs)
            environ_name.setToolTip(envs)
            environ_name.setFlags(environ_name.flags() & QtCore.Qt.ItemIsSelectable)


            environ_value = QtWidgets.QTableWidgetItem(os.environ[envs])
            environ_value.setToolTip(os.environ[envs])

            self.environ_table.setItem(index, 0, environ_name)
            self.environ_table.setItem(index, 1, environ_value)
        self.environ_table.setColumnWidth(0, 250)
        self.environ_table.setHorizontalHeaderLabels(['Key',"Value"])


        # Create New Environment Button
        button_layout = QtWidgets.QHBoxLayout()
        new_environ_btn = QtWidgets.QPushButton()
        new_environ_btn.setText("Create New Environment Variable")
        new_environ_btn.clicked.connect(lambda: self.create_new_environ())
        button_layout.setContentsMargins(0,0,0,0)
        button_layout.addWidget(new_environ_btn)


        self.main_layout.addLayout(filter_layout)
        self.main_layout.addWidget(self.environ_table)
        self.main_layout.addLayout(button_layout)

        self.apple_stylesheet()
        self.setLayout(self.main_layout)


    def apple_stylesheet(self):
        """Applys a CSS stylesheet to the app"""
        with open(CSS_PATH, "r") as R:
            style_sheet = R.read()
            self.setStyleSheet(style_sheet)

    def update_environment(self):
        """Sets the New Environments to the System"""
        for row in range(self.environ_table.rowCount()):
            key = self.environ_table.item(row,0)
            value = self.environ_table.item(row,1)

            new_key = None
            new_value = None
            if key and value:
                new_key = key.text()
                new_value = value.text()

            try:
                os.environ[new_key] = new_value
            except TypeError:
                pass

    def create_new_environ(self):
        """Creates a Empty Table Widget for adding a new Variable"""
        row_count = self.environ_table.rowCount()
        self.environ_table.setRowCount(row_count+1)
        new_env = QtWidgets.QTableWidgetItem()
        self.environ_table.setItem(row_count+1, 0, new_env)

    def filter_environments(self):
        filter_name = self.filter_bar.text().upper()
        for index in range(self.environ_table.rowCount()):
            items = self.environ_table.item(index, 0)
            value = self.environ_table.item(index, 1)
            item_name = items.text()

            if filter_name == item_name:
                items.setSelected(True)
                value.setSelected(True)
            else:
                items.setSelected(False)
                value.setSelected(False)

    def closeEvent(self, event):
        """Task happens upon closing the app

        Args:
            event (_type_): _description_
        """
        self.update_environment()


def run_env():
    global window
    app = QtWidgets.QApplication.instance()
    if not app:
        app = QtWidgets.QApplication(sys.argv)

    window = EnvironmentViewer()
    window.show()