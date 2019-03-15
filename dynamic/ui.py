# -*- coding: utf-8 -*-

import matplotlib
import os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import QFileDialog, QSizePolicy
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from dynamic.RealtimePlotter import RealtimePlotter

matplotlib.use('Qt5Agg')


class UiMainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(UiMainWindow, self).__init__()

        # define the object variable
        self.vertical_top_layout, self.vertical_main_layout = None, None
        self.horizontal_setting_layout, self.form_mode_layout = None, None
        self.vertical_control_layout, self.form_file_layout, self.vertical_text_layout = None, None, None

        self.central_widget, self.plotter, self.widget_canvas = None, None, None
        self.mode_label, self.mode_combobox = None, None
        self.data_class_label, self.data_class_combobox = None, None
        self.antenna_tx_label, self.antenna_tx_combobox = None, None
        self.shown_speed_label, self.shown_speed_combobox = None, None
        self.subcarrier_label, self.subcarrier_combobox = None, None
        self.antenna_rx_label, self.antenna_rx_combobox = None, None

        self.data_select_button, self.file_name = None, None
        self.start_button, self.pause_button, self.quit_button = None, None, None
        self.main_splitter, self.sub_splitter = None, None

        self.msg_text = None
        self.shown_speed = 1
        self.setup_ui(self)
        self.retranslate_ui(self)

    def setup_ui(self, main_window):
        main_window.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.central_widget = QtWidgets.QWidget(main_window)
        font_12 = QtGui.QFont()
        font_12.setPointSize(12)
        font_13 = QtGui.QFont()
        font_13.setPointSize(13)
        font_14 = QtGui.QFont()
        font_14.setPointSize(13.5)
        font_15 = QtGui.QFont()
        font_15.setPointSize(15)

        # define layout
        self.vertical_top_layout = QtWidgets.QVBoxLayout(self.central_widget)
        self.vertical_top_layout.setContentsMargins(10, 10, 10, 10)

        self.vertical_main_layout = QtWidgets.QVBoxLayout()
        self.vertical_top_layout.addLayout(self.vertical_main_layout)
        self.vertical_main_layout.setContentsMargins(10, 10, 10, 10)

        self.horizontal_setting_layout = QtWidgets.QHBoxLayout()
        self.vertical_top_layout.addLayout(self.horizontal_setting_layout)
        self.horizontal_setting_layout.setContentsMargins(10, 10, 0, 10)

        self.form_mode_layout = QtWidgets.QFormLayout()
        self.horizontal_setting_layout.addLayout(self.form_mode_layout)
        self.form_mode_layout.setContentsMargins(10, 10, 0, 10)

        self.vertical_control_layout = QtWidgets.QVBoxLayout()
        self.horizontal_setting_layout.addLayout(self.vertical_control_layout)
        self.vertical_control_layout.setContentsMargins(10, 10, 0, 0)

        self.form_file_layout = QtWidgets.QFormLayout()
        self.vertical_control_layout.addLayout(self.form_file_layout)
        self.form_file_layout.setContentsMargins(10, 0, 10, 10)

        self.vertical_text_layout = QtWidgets.QVBoxLayout()
        self.vertical_control_layout.addLayout(self.vertical_text_layout)
        self.vertical_text_layout.setContentsMargins(10, 5, 10, 10)

        # add widget into layouts
        self.plotter = RealtimePlotter(self)
        self.widget_canvas = FigureCanvas(self.plotter.fig)
        self.vertical_main_layout.addWidget(self.widget_canvas)

        self.mode_label = QtWidgets.QLabel()
        self.mode_label.setFont(font_12)
        self.form_mode_layout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.mode_label)
        self.mode_combobox = QtWidgets.QComboBox()
        self.mode_combobox.setFont(font_12)
        self.mode_combobox.addItem("")
        self.mode_combobox.addItem("")
        self.mode_combobox.addItem("")
        self.mode_combobox.addItem("")
        self.form_mode_layout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.mode_combobox)

        self.data_class_label = QtWidgets.QLabel()
        self.data_class_label.setFont(font_12)
        self.form_mode_layout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.data_class_label)
        self.data_class_combobox = QtWidgets.QComboBox()
        self.data_class_combobox.setFont(font_12)
        self.data_class_combobox.addItem("")
        self.data_class_combobox.addItem("")
        self.form_mode_layout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.data_class_combobox)

        self.antenna_tx_label = QtWidgets.QLabel()
        self.antenna_tx_label.setFont(font_12)
        self.form_mode_layout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.antenna_tx_label)
        self.antenna_tx_combobox = QtWidgets.QComboBox()
        self.antenna_tx_combobox.setFont(font_12)
        self.antenna_tx_combobox.addItem("")
        self.antenna_tx_combobox.addItem("")
        self.antenna_tx_combobox.addItem("")
        self.form_mode_layout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.antenna_tx_combobox)

        self.antenna_rx_label = QtWidgets.QLabel()
        self.antenna_rx_label.setFont(font_12)
        self.form_mode_layout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.antenna_rx_label)
        self.antenna_rx_combobox = QtWidgets.QComboBox()
        self.antenna_rx_combobox.setFont(font_12)
        self.antenna_rx_combobox.addItem("")
        self.antenna_rx_combobox.addItem("")
        self.antenna_rx_combobox.addItem("")
        self.form_mode_layout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.antenna_rx_combobox)

        self.subcarrier_label = QtWidgets.QLabel()
        self.subcarrier_label.setFont(font_12)
        self.form_mode_layout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.subcarrier_label)
        self.subcarrier_combobox = QtWidgets.QComboBox()
        self.subcarrier_combobox.setFont(font_12)
        for i in range(30):
            self.subcarrier_combobox.addItem("")
        self.form_mode_layout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.subcarrier_combobox)

        self.shown_speed_label = QtWidgets.QLabel()
        self.shown_speed_label.setFont(font_12)
        self.form_mode_layout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.shown_speed_label)
        self.shown_speed_combobox = QtWidgets.QComboBox()
        self.shown_speed_combobox.setFont(font_12)
        self.shown_speed_combobox.addItem("")
        self.shown_speed_combobox.addItem("")
        self.shown_speed_combobox.addItem("")
        self.shown_speed_combobox.addItem("")
        self.shown_speed_combobox.addItem("")
        self.form_mode_layout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.shown_speed_combobox)

        self.data_select_button = QtWidgets.QPushButton()
        self.data_select_button.setFont(font_14)
        self.form_file_layout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.data_select_button)
        self.file_name = QtWidgets.QLineEdit()
        self.file_name.setFont(font_12)
        self.file_name.setInputMethodHints(QtCore.Qt.ImhHiddenText)
        self.form_file_layout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.file_name)

        self.start_button = QtWidgets.QPushButton()
        self.start_button.setFont(font_15)

        self.pause_button = QtWidgets.QPushButton()
        self.pause_button.setFont(font_15)

        self.quit_button = QtWidgets.QPushButton()
        self.quit_button.setFont(font_15)

        self.msg_text = QtWidgets.QTextBrowser()
        self.msg_text.setFont(font_12)
        self.msg_text.textChanged.connect(self.auto_scroll)
        self.msg_text.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.msg_text.setObjectName("message")
        self.msg_text.append("<font color = 'black'>-> Set the right transmit antennas number!")
        self.msg_text.append("<font color = 'black'>-> Press the save-path button to select the filepath"
                             " and click the start button to show figture!")

        self.main_splitter = QtWidgets.QSplitter(Qt.Horizontal)
        self.sub_splitter = QtWidgets.QSplitter(Qt.Vertical)
        self.sub_splitter.addWidget(self.start_button)
        self.sub_splitter.addWidget(self.pause_button)
        self.sub_splitter.addWidget(self.quit_button)
        self.sub_splitter.setHandleWidth(8)
        self.main_splitter.addWidget(self.sub_splitter)
        self.main_splitter.addWidget(self.msg_text)
        self.main_splitter.setStretchFactor(0, 1)
        self.main_splitter.setStretchFactor(1, 100)
        self.vertical_text_layout.addWidget(self.main_splitter)

        main_window.setCentralWidget(self.central_widget)
        self.retranslate_ui(main_window)

    def retranslate_ui(self, main_window):
        _translate = QtCore.QCoreApplication.translate
        main_window.setWindowTitle("CSI Viewer")
        self.mode_label.setText("mode：")
        self.mode_combobox.setItemText(0, "rssi")
        self.mode_combobox.setItemText(1, "subcarrier")
        self.mode_combobox.setItemText(2, "antenna pair")
        self.mode_combobox.setItemText(3, "all csi")

        self.data_class_label.setText("type：")
        self.data_class_combobox.setItemText(0, "amplitude")
        self.data_class_combobox.setItemText(1, "phase")

        self.antenna_tx_label.setText("TX：")
        self.antenna_tx_combobox.setItemText(0, "A")
        self.antenna_tx_combobox.setItemText(1, "B")
        self.antenna_tx_combobox.setItemText(2, "C")

        self.antenna_rx_label.setText("RX：")
        self.antenna_rx_combobox.setItemText(0, "A")
        self.antenna_rx_combobox.setItemText(1, "B")
        self.antenna_rx_combobox.setItemText(2, "C")

        self.subcarrier_label.setText("NO：")
        for i in range(30):
            self.subcarrier_combobox.setItemText(i, str(i + 1))

        self.shown_speed_label.setText("rate:")
        self.shown_speed_combobox.setItemText(0, "1")
        self.shown_speed_combobox.setItemText(1, "10")
        self.shown_speed_combobox.setItemText(2, "100")
        self.shown_speed_combobox.setItemText(3, "1000")
        self.shown_speed_combobox.setItemText(4, "10000")

        self.data_select_button.setText("save-path")
        self.data_select_button.clicked.connect(self.open_file)
        self.file_name.setText("/home/luxiang/linux-80211n-csitool-supplementary/data/1.dat")
        self.start_button.setText("start")
        self.start_button.clicked.connect(self.start)
        self.pause_button.setText("pause")
        self.pause_button.clicked.connect(self.pause)
        self.quit_button.setText("quit")
        self.quit_button.clicked.connect(self.quit)

    def open_file(self):
        directory = QFileDialog.getExistingDirectory(self, "selcet the data file path", "/home/")
        self.file_name.setText(directory + '/')

    def speed_val(self):
        print(self.speed_bar.value())

    def start(self):
        if self.plotter.start_flag is True:
            return
        self.setting()
        self.plotter.start_flag = True
        self.plotter.start()
        self.msg_text.append("<font color = 'black'>-> Showing...")

    def setting(self):
        self.vertical_main_layout.removeWidget(self.widget_canvas)
        self.plotter = RealtimePlotter(self)
        self.widget_canvas = FigureCanvas(self.plotter.fig)
        self.vertical_main_layout.addWidget(self.widget_canvas)
        self.plotter.mode = self.mode_combobox.currentText()
        self.plotter.data = self.data_class_combobox.currentText()
        self.plotter.tx = ord(self.antenna_tx_combobox.currentText()) - ord('A')
        self.plotter.rx = ord(self.antenna_rx_combobox.currentText()) - ord('A')
        self.plotter.subcarrier_no = int(self.subcarrier_combobox.currentText()) - 1
        self.plotter.interval_msec = int(self.shown_speed_combobox.currentText())
        self.plotter.filename = self.file_name.text()

        if self.plotter.mode == "subcarrier":
            if self.plotter.data == "phase":
                self.plotter.axes.set_ylabel("Phase")
                self.plotter.axes.set_ylim(-3.14, 3.14)
                self.plotter.axes.yaxis.set_ticks([-3.14, 0, +3.14])
            elif self.plotter.data == "amplitude":
                self.plotter.axes.set_ylabel("Amplitude")
                self.plotter.axes.set_ylim(0, 70)
                self.plotter.axes.yaxis.set_ticks([0, 35, 70])

        elif self.plotter.mode == "antenna pair":
            self.plotter.axes.set_ylabel("Subcarriers")
            self.plotter.axes.set_ylim(0, 29.5)
            self.plotter.axes.yaxis.grid(False)
            self.plotter.axes.yaxis.set_ticks([0, 5, 10, 15, 20, 25])
        elif self.plotter.mode == "all csi":
            self.plotter.axes.set_ylabel("Subcarriers")
            self.plotter.axes.yaxis.grid(False)
            if self.plotter.tx == 0:
                self.plotter.axes.set_ylim(0, 89.5)
                self.plotter.axes.yaxis.set_ticks([0, 20, 40, 60])
            elif self.plotter.tx == 1:
                self.plotter.axes.set_ylim(0, 179.5)
                self.plotter.axes.yaxis.set_ticks([0, 30, 60, 90, 120, 150])
            elif self.plotter.tx == 2:
                self.plotter.axes.set_ylim(0, 269.5)
                self.plotter.axes.yaxis.set_ticks([0, 30, 60, 90, 120, 150, 180, 210, 240])
        elif self.plotter.mode == "rssi":
            self.plotter.axes.set_ylabel("RSSI")
            self.plotter.axes.set_ylim(-90, 0)
            self.plotter.axes.yaxis.set_ticks([-90, -60, -30, 0])

    def pause(self):
        if self.plotter.start_flag is False:
            return
        os.system("sudo kill -s 9 `ps -ef|grep '../netlink/log_to_file'|grep -v sudo|grep -v grep|awk '{print $2}'`")
        self.msg_text.append('-> Stop showing!')
        self.plotter.pause()
        self.plotter.start_flag = False

    def add_msg(self, msg):
        self.msg_text.append(msg)

    def auto_scroll(self):
        self.msg_text.moveCursor(QTextCursor.End)

    @staticmethod
    def quit():
        os.system("sudo kill -s 9 `ps -ef|grep '../netlink/log_to_file'|grep -v sudo|grep -v grep|awk '{print $2}'`")
        sys.exit(0)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = UiMainWindow()
    ui.setup_ui(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
