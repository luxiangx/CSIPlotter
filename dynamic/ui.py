# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!
import threading
from time import sleep, clock

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QSizePolicy
import matplotlib

matplotlib.use('Qt5Agg')
# matplotlib.rcParams['backend'] = 'Qt5Agg'
# matplotlib.rcParams['backend.qt5'] = 'PyQt5'
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
# from dynamic.MyMplCanvas import *
from dynamic.RealtimePlotter import RealtimePlotter
from dynamic.plot import Plotter
from dynamic.run import run


class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        self.setupUi(self)
        self.retranslateUi(self)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("CSI Viewer")
        MainWindow.resize(800, 600)
        MainWindow.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.central_widget = QtWidgets.QWidget(MainWindow)
        self.central_widget.setObjectName("central_widget")
        # self.central_widget.setLayout(self.vertical_top_layout)
        # MainWindow.setAutoFillBackground(True)
        font = QtGui.QFont()
        font.setPointSize(12)

        # define layout
        self.vertical_top_layout = QtWidgets.QVBoxLayout(self.central_widget)
        self.vertical_top_layout.setGeometry(QtCore.QRect(0, 0, 800, 600))
        self.vertical_top_layout.setObjectName("top_layout")
        self.vertical_top_layout.setContentsMargins(10, 10, 10, 10)

        self.vertical_second_layout = QtWidgets.QVBoxLayout()
        self.vertical_top_layout.addLayout(self.vertical_second_layout)
        # self.vertical_second_layout.setGeometry(QtCore.QRect(20, 20, 750, 500))
        self.vertical_second_layout.setObjectName("horizontal_second_layout")
        self.vertical_second_layout.setContentsMargins(10, 10, 10, 10)

        self.horizontal_second_layout = QtWidgets.QHBoxLayout()
        self.vertical_top_layout.addLayout(self.horizontal_second_layout)
        self.horizontal_second_layout.setObjectName("horizontal_second_layout")
        self.horizontal_second_layout.setContentsMargins(10, 10, 10, 10)

        self.form_third_layout = QtWidgets.QFormLayout()
        self.horizontal_second_layout.addLayout(self.form_third_layout)
        self.form_third_layout.setObjectName("form_third_layout")
        self.form_third_layout.setContentsMargins(10, 10, 10, 10)

        self.vertical_third_layout = QtWidgets.QVBoxLayout()
        self.horizontal_second_layout.addLayout(self.vertical_third_layout)
        self.vertical_third_layout.setObjectName("vertical_third_layout")
        self.vertical_third_layout.setContentsMargins(10, 10, 10, 10)

        self.form_forth_layout = QtWidgets.QFormLayout()
        self.vertical_third_layout.addLayout(self.form_forth_layout)
        self.form_forth_layout.setObjectName("form_forth_layout")
        self.form_forth_layout.setContentsMargins(10, 10, 10, 10)

        self.horizontal_forth_layout = QtWidgets.QHBoxLayout()
        self.vertical_third_layout.addLayout(self.horizontal_forth_layout)
        self.horizontal_forth_layout.setObjectName("horizontal_forth_layout")
        self.horizontal_forth_layout.setContentsMargins(10, 10, 10, 10)

        self.gird_fifth_layout = QtWidgets.QGridLayout()
        self.horizontal_forth_layout.addLayout(self.gird_fifth_layout)
        # self.gird_fifth_layout.setGeometry(QtCore.QRect(450, 470, 100, 130))
        self.gird_fifth_layout.setObjectName("gird_fifth_layout")
        self.gird_fifth_layout.setContentsMargins(10, 10, 10, 10)

        # add widgets into layout

        self.plotter = Plotter()
        self.widget_canvas = FigureCanvas(self.plotter.fig)
        self.widget_canvas.setSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                         QtWidgets.QSizePolicy.Expanding)
        self.widget_canvas.updateGeometry()
        self.vertical_second_layout.addWidget(self.widget_canvas)

        # self.fig = Plotter()
        # self.vertical_top_layout.addWidget(self.fig)
        # self.mode_label.setObjectName("figure")

        # self.frame = QtWidgets.QFrame()
        # self.frame.setGeometry(QtCore.QRect(0, 0, 800, 400))
        # self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        # self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        # self.frame.setObjectName("frame")
        # self.vertical_top_layout.addWidget(self.frame)
        # self.vertical_second_layout.addWidget(self.frame)

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
        self.file_name.setText('/home/luxiang/1.dat')
        self.file_name.setInputMethodHints(QtCore.Qt.ImhHiddenText)
        self.file_name.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.file_name.setObjectName("file_name")
        self.form_forth_layout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.file_name)

        self.start_button = QtWidgets.QPushButton()
        self.start_button.setFont(font)
        self.start_button.setObjectName("start_button")
        self.gird_fifth_layout.addWidget(self.start_button, 1, 1)

        self.pause_button = QtWidgets.QPushButton()
        self.pause_button.setFont(font)
        self.pause_button.setObjectName("pauseButton")
        self.gird_fifth_layout.addWidget(self.pause_button, 1, 2)

        self.export_data_button = QtWidgets.QPushButton()
        self.export_data_button.setFont(font)
        self.export_data_button.setObjectName("exportDataButton")
        self.gird_fifth_layout.addWidget(self.export_data_button, 2, 1)

        self.quit_button = QtWidgets.QPushButton()
        self.quit_button.setFont(font)
        self.quit_button.setObjectName("quitButton")
        self.gird_fifth_layout.addWidget(self.quit_button, 2, 2)

        self.msg_text = QtWidgets.QTextBrowser()
        self.msg_text.setFont(font)
        self.msg_text.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.msg_text.setObjectName("message")
        self.horizontal_forth_layout.addWidget(self.msg_text)

        MainWindow.setCentralWidget(self.central_widget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        # self.frame.triggered.connect(run)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "CSI Viewer"))
        self.flag = False
        self.mode_label.setText(_translate("MainWindow", "模式："))
        self.mode_combobox.setItemText(0, _translate("MainWindow", "子载波显示"))
        self.mode_combobox.setItemText(1, _translate("MainWindow", "天线对显示"))
        self.mode_combobox.setItemText(2, _translate("MainWindow", "全数据显示"))

        self.data_class_label.setText(_translate("MainWindow", "数据："))
        self.data_class_combobox.setItemText(0, _translate("MainWindow", "幅值"))
        self.data_class_combobox.setItemText(1, _translate("MainWindow", "相位"))

        self.antenna_tx_label.setText(_translate("MainWindow", "发送天线："))
        self.antenna_tx_combobox.setItemText(0, _translate("MainWindow", "A"))
        self.antenna_tx_combobox.setItemText(1, _translate("MainWindow", "B"))
        self.antenna_tx_combobox.setItemText(2, _translate("MainWindow", "C"))

        self.antenna_rx_label.setText(_translate("MainWindow", "接收天线："))
        self.antenna_rx_combobox.setItemText(0, _translate("MainWindow", "A"))
        self.antenna_rx_combobox.setItemText(1, _translate("MainWindow", "B"))
        self.antenna_rx_combobox.setItemText(2, _translate("MainWindow", "C"))

        self.subcarrier_label.setText(_translate("MainWindow", "子载波编号："))
        self.subcarrier_combobox.setItemText(0, _translate("MainWindow", "1"))
        self.subcarrier_combobox.setItemText(1, _translate("MainWindow", "2"))
        self.subcarrier_combobox.setItemText(2, _translate("MainWindow", "3"))
        self.subcarrier_combobox.setItemText(3, _translate("MainWindow", "4"))
        self.subcarrier_combobox.setItemText(4, _translate("MainWindow", "5"))
        self.subcarrier_combobox.setItemText(5, _translate("MainWindow", "6"))
        self.subcarrier_combobox.setItemText(6, _translate("MainWindow", "7"))
        self.subcarrier_combobox.setItemText(7, _translate("MainWindow", "8"))
        self.subcarrier_combobox.setItemText(8, _translate("MainWindow", "9"))
        self.subcarrier_combobox.setItemText(9, _translate("MainWindow", "10"))
        self.subcarrier_combobox.setItemText(10, _translate("MainWindow", "11"))
        self.subcarrier_combobox.setItemText(11, _translate("MainWindow", "12"))
        self.subcarrier_combobox.setItemText(12, _translate("MainWindow", "13"))
        self.subcarrier_combobox.setItemText(13, _translate("MainWindow", "14"))
        self.subcarrier_combobox.setItemText(14, _translate("MainWindow", "15"))
        self.subcarrier_combobox.setItemText(15, _translate("MainWindow", "16"))
        self.subcarrier_combobox.setItemText(16, _translate("MainWindow", "17"))
        self.subcarrier_combobox.setItemText(17, _translate("MainWindow", "18"))
        self.subcarrier_combobox.setItemText(18, _translate("MainWindow", "19"))
        self.subcarrier_combobox.setItemText(19, _translate("MainWindow", "20"))
        self.subcarrier_combobox.setItemText(20, _translate("MainWindow", "21"))
        self.subcarrier_combobox.setItemText(21, _translate("MainWindow", "22"))
        self.subcarrier_combobox.setItemText(22, _translate("MainWindow", "23"))
        self.subcarrier_combobox.setItemText(23, _translate("MainWindow", "24"))
        self.subcarrier_combobox.setItemText(24, _translate("MainWindow", "25"))
        self.subcarrier_combobox.setItemText(25, _translate("MainWindow", "26"))
        self.subcarrier_combobox.setItemText(26, _translate("MainWindow", "27"))
        self.subcarrier_combobox.setItemText(27, _translate("MainWindow", "28"))
        self.subcarrier_combobox.setItemText(28, _translate("MainWindow", "29"))
        self.subcarrier_combobox.setItemText(29, _translate("MainWindow", "30"))
        self.data_select_button.setText(_translate("MainWindow", "数据选择"))
        self.data_select_button.clicked.connect(self.openfile)
        self.file_name.setText(_translate("MainWindow", ""))
        self.start_button.setText(_translate("MainWindow", "开始"))
        self.start_button.clicked.connect(self.start)
        self.pause_button.setText(_translate("MainWindow", "暂停"))
        self.pause_button.clicked.connect(self.pause)
        self.export_data_button.setText(_translate("MainWindow", "导出数据"))
        self.export_data_button.clicked.connect(self.export_data)
        self.quit_button.setText(_translate("MainWindow", "退出"))
        self.quit_button.clicked.connect(self.quit)

    def openfile(self):
        _translate = QtCore.QCoreApplication.translate
        openfile_name = QFileDialog.getOpenFileName(self, 'open file',
                                                    '/home/luxiang/',
                                                    'Dat files(*.dat)')
        self.file_name.setText(_translate("MainWindow", openfile_name[0]))

    def start(self):
        self.plotter.flag = True
        self.widget_canvas.tx = self.antenna_tx_combobox.currentText()
        self.widget_canvas.rx = self.antenna_rx_combobox.currentText()
        self.widget_canvas.subcarrier_no = self.subcarrier_combobox.currentText()
        self.widget_canvas.mode = self.mode_combobox.currentText()
        self.widget_canvas.data = self.data_class_combobox.currentText()
        self.msg_text.append('start')
        self.plotter.start()
        self.msg_text.append('run')

    def pause(self):
        self.plotter.pause = True
        self.msg_text.append('pause')

    def export_data(self):
        pass

    def quit(self):
        sys.exit(0)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
