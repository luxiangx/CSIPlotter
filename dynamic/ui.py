# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

import matplotlib
import os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFileDialog, QSizePolicy
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from dynamic.plot import Plotter

matplotlib.use('Qt5Agg')


class UiMainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(UiMainWindow, self).__init__()
        self.central_widget = None
        self.vertical_top_layout = None
        self.vertical_second_layout = None
        self.horizontal_second_layout = None
        self.form_third_layout = None
        self.vertical_third_layout = None
        self.form_forth_layout = None
        self.vertical_forth_layout = None
        self.plotter = None
        self.widget_canvas = None
        self.mode_label = None
        self.mode_combobox = None
        self.data_class_label = None
        self.antenna_tx_label = None
        self.data_class_combobox = None
        self.antenna_tx_combobox = None
        self.subcarrier_label = None
        self.antenna_rx_label = None
        self.antenna_rx_combobox = None
        self.subcarrier_combobox = None
        self.data_select_button = None
        self.file_name = None
        self.start_button = None
        self.pause_button = None
        self.quit_button = None
        self.main_splitter = None
        self.sub_splitter = None
        self.msg_text = None
        self.setup_ui(self)
        self.retranslate_ui(self)

    def setup_ui(self, main_window):
        main_window.setObjectName("CSI Viewer")
        main_window.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.central_widget = QtWidgets.QWidget(main_window)
        self.central_widget.setObjectName("central_widget")
        font = QtGui.QFont()
        font.setPointSize(12)

        # define layout
        self.vertical_top_layout = QtWidgets.QVBoxLayout(self.central_widget)
        self.vertical_top_layout.setObjectName("top_layout")
        self.vertical_top_layout.setContentsMargins(10, 10, 10, 10)

        self.vertical_second_layout = QtWidgets.QVBoxLayout()
        self.vertical_top_layout.addLayout(self.vertical_second_layout)
        self.vertical_second_layout.setObjectName("horizontal_second_layout")
        self.vertical_second_layout.setContentsMargins(10, 10, 10, 10)

        self.horizontal_second_layout = QtWidgets.QHBoxLayout()
        self.vertical_top_layout.addLayout(self.horizontal_second_layout)
        self.horizontal_second_layout.setObjectName("horizontal_second_layout")
        self.horizontal_second_layout.setContentsMargins(10, 10, 0, 10)

        self.form_third_layout = QtWidgets.QFormLayout()
        self.horizontal_second_layout.addLayout(self.form_third_layout)
        self.form_third_layout.setObjectName("form_third_layout")
        self.form_third_layout.setContentsMargins(10, 10, 0, 10)

        self.vertical_third_layout = QtWidgets.QVBoxLayout()
        self.horizontal_second_layout.addLayout(self.vertical_third_layout)
        self.vertical_third_layout.setObjectName("vertical_third_layout")
        self.vertical_third_layout.setContentsMargins(10, 10, 0, 0)

        self.form_forth_layout = QtWidgets.QFormLayout()
        self.vertical_third_layout.addLayout(self.form_forth_layout)
        self.form_forth_layout.setObjectName("form_forth_layout")
        self.form_forth_layout.setContentsMargins(10, 0, 10, 10)

        self.vertical_forth_layout = QtWidgets.QVBoxLayout()
        self.vertical_third_layout.addLayout(self.vertical_forth_layout)
        self.vertical_forth_layout.setObjectName("vertical_forth_layout")
        self.vertical_forth_layout.setContentsMargins(10, 5, 10, 10)

        self.plotter = Plotter()
        self.widget_canvas = FigureCanvas(self.plotter.fig)
        self.widget_canvas.setSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                         QtWidgets.QSizePolicy.Expanding)
        self.widget_canvas.updateGeometry()
        self.vertical_second_layout.addWidget(self.widget_canvas)

        self.mode_label = QtWidgets.QLabel()
        self.mode_label.setFont(font)
        self.mode_label.setObjectName("mode_label")
        self.form_third_layout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.mode_label)
        self.mode_combobox = QtWidgets.QComboBox()
        self.mode_combobox.setFont(font)
        self.mode_combobox.setEditable(False)
        self.mode_combobox.setObjectName("mode_combobox")
        self.mode_combobox.addItem("")
        self.mode_combobox.addItem("")
        self.mode_combobox.addItem("")
        self.form_third_layout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.mode_combobox)

        self.data_class_label = QtWidgets.QLabel()
        self.data_class_label.setFont(font)
        self.data_class_label.setObjectName("data_class_label")
        self.form_third_layout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.data_class_label)
        self.data_class_combobox = QtWidgets.QComboBox()
        self.data_class_combobox.setFont(font)
        self.data_class_combobox.setObjectName("data_class_combobox")
        self.data_class_combobox.addItem("")
        self.data_class_combobox.addItem("")
        self.form_third_layout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.data_class_combobox)

        self.antenna_tx_label = QtWidgets.QLabel()
        self.antenna_tx_label.setFont(font)
        self.antenna_tx_label.setObjectName("antenna_tx_label")
        self.form_third_layout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.antenna_tx_label)
        self.antenna_tx_combobox = QtWidgets.QComboBox()
        self.antenna_tx_combobox.setFont(font)
        self.antenna_tx_combobox.setObjectName("antenna_tx_combobox")
        self.antenna_tx_combobox.addItem("")
        self.antenna_tx_combobox.addItem("")
        self.antenna_tx_combobox.addItem("")
        self.form_third_layout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.antenna_tx_combobox)

        self.antenna_rx_label = QtWidgets.QLabel()
        self.antenna_rx_label.setFont(font)
        self.antenna_rx_label.setObjectName("antenna_rx_label")
        self.form_third_layout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.antenna_rx_label)
        self.antenna_rx_combobox = QtWidgets.QComboBox()
        self.antenna_rx_combobox.setFont(font)
        self.antenna_rx_combobox.setObjectName("antenna_rx_comboBox")
        self.antenna_rx_combobox.addItem("")
        self.antenna_rx_combobox.addItem("")
        self.antenna_rx_combobox.addItem("")
        self.form_third_layout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.antenna_rx_combobox)

        self.subcarrier_label = QtWidgets.QLabel()
        self.subcarrier_label.setFont(font)
        self.subcarrier_label.setObjectName("subcarrier_label")
        self.form_third_layout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.subcarrier_label)
        self.subcarrier_combobox = QtWidgets.QComboBox()
        self.subcarrier_combobox.setFont(font)
        self.subcarrier_combobox.setObjectName("subcarrier_combobox")
        for i in range(30):
            self.subcarrier_combobox.addItem("")
        self.form_third_layout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.subcarrier_combobox)

        self.data_select_button = QtWidgets.QPushButton()
        self.data_select_button.setFont(font)
        self.data_select_button.setObjectName("data_select_button")
        self.form_forth_layout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.data_select_button)
        self.file_name = QtWidgets.QLineEdit()
        self.file_name.setFont(font)
        self.file_name.setInputMethodHints(QtCore.Qt.ImhHiddenText)
        self.file_name.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.file_name.setObjectName("file_name")
        self.form_forth_layout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.file_name)

        self.start_button = QtWidgets.QPushButton()
        self.start_button.setFont(font)
        self.start_button.setObjectName("start_button")

        self.pause_button = QtWidgets.QPushButton()
        self.pause_button.setFont(font)
        self.pause_button.setObjectName("pause_button")

        self.quit_button = QtWidgets.QPushButton()
        self.quit_button.setFont(font)
        self.quit_button.setObjectName("quit_button")

        self.msg_text = QtWidgets.QTextBrowser()
        self.msg_text.setFont(font)
        self.msg_text.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.msg_text.setObjectName("message")
        self.msg_text.append("-> <font color='red'>注意选择发送天线不要超过最大发送天线编号！</font>")
        self.msg_text.append("-> <font color='red'>选择数据存放地址，点击开始按钮画图。</font>")

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

        self.vertical_forth_layout.addWidget(self.main_splitter)

        main_window.setCentralWidget(self.central_widget)
        self.retranslate_ui(main_window)

    def retranslate_ui(self, main_window):
        _translate = QtCore.QCoreApplication.translate
        main_window.setWindowTitle("CSI Viewer")
        self.mode_label.setText("模式：")
        self.mode_combobox.setItemText(0, "子载波显示")
        self.mode_combobox.setItemText(1, "天线对显示")
        self.mode_combobox.setItemText(2, "全数据显示")

        self.data_class_label.setText("数据：")
        self.data_class_combobox.setItemText(0, "幅值")
        self.data_class_combobox.setItemText(1, "相位")

        self.antenna_tx_label.setText("发送天线：")
        self.antenna_tx_combobox.setItemText(0, "A")
        self.antenna_tx_combobox.setItemText(1, "B")
        self.antenna_tx_combobox.setItemText(2, "C")

        self.antenna_rx_label.setText("接收天线：")
        self.antenna_rx_combobox.setItemText(0, "A")
        self.antenna_rx_combobox.setItemText(1, "B")
        self.antenna_rx_combobox.setItemText(2, "C")

        self.subcarrier_label.setText("子载波编号：")
        for i in range(30):
            self.subcarrier_combobox.setItemText(i, str(i + 1))

        self.data_select_button.setText("数据选择")
        self.data_select_button.clicked.connect(self.open_file)
        self.file_name.setText("/home/luxiang/linux-80211n-csitool-supplementary/data/1.dat")
        self.start_button.setText("开始")
        self.start_button.clicked.connect(self.start)
        self.pause_button.setText("暂停")
        self.pause_button.clicked.connect(self.pause)
        self.quit_button.setText("退出")
        self.quit_button.clicked.connect(self.quit)

    def open_file(self):
        open_file_name = QFileDialog.getOpenFileName(self.central_widget,
                                                     "open file", "/home/luxiang/",
                                                     "Dat files(*.dat)")

        self.file_name.setText(open_file_name[0])

    def start(self):
        self.setting()
        self.plotter.filename = self.file_name.text()
        self.plotter.pause_flag = False
        self.plotter.start()
        self.msg_text.append('-> 画图中...')

    def setting(self):
        self.plotter.mode = self.mode_combobox.currentText()
        self.plotter.data = self.data_class_combobox.currentText()
        if self.plotter.data == "相位":
            self.plotter.axes.set_ylabel("Phase")
            self.plotter.axes.set_ylim(-3.14, 3.14)
            self.plotter.axes.yaxis.set_ticks([-3.14, 0, +3.14])
        else:
            self.plotter.axes.set_ylabel("Amplitude")
            self.plotter.axes.set_ylim(0, 70)
            self.plotter.axes.yaxis.set_ticks([0, 35, 70])
        self.plotter.tx = self.antenna_tx_combobox.currentText()
        self.plotter.rx = self.antenna_rx_combobox.currentText()
        self.plotter.subcarrier_no = self.subcarrier_combobox.currentText()

    def pause(self):
        os.system("sudo kill -s 9 `ps -ef|grep '../netlink/log_to_file_1'|grep -v sudo|grep -v grep|awk '{print $2}'`")
        self.msg_text.append('-> 暂停画图！')
        self.plotter.pause_flag = True
        self.plotter.puase()

    @staticmethod
    def quit():
        sys.exit(0)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = UiMainWindow()
    ui.setup_ui(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
