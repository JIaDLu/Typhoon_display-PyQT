import matplotlib.pyplot as plt
import numpy as np
from threading import Thread
from PyMysql import *
from PIL import Image
from face_sorce import Ui_MainWindow
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from PyQt5.QtWidgets import QFileDialog
from PyQt5 import QtWidgets,QtGui,QtCore
from PyQt5 import QtWebEngineWidgets
import sys
import time
from PyMysql import MSSQL
from PyQt5 import QtWidgets,QtCore
from PyQt5.QtGui import QImage, QPixmap
import warnings
warnings.filterwarnings('ignore')

class MyWindow(QtWidgets.QWidget,Ui_MainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setupUi(self)
        self.webEngineView.load(QtCore.QUrl("D://Pycharm//Lab//台风预报系统//ht.html"))
        self.mysql = MSSQL()
        self.slot_putton()
        self.label_2.setPixmap(QPixmap("IBTrACS.png"))
        self.label_2.setScaledContents(True)

        self.year_mark = 0
        self.typhoon_mark = 0

    def show_year(self):
        year_list = []
        Year = 'YEAR'
        table_Name = 'ibtracs'
        year_info = self.mysql.select_typhoon_year(Year, table_Name)
        for ech in year_info:
            year_list.append(ech[0])
        self.comboBox.addItems(year_list)

    def slot_putton(self):
        year_list = []
        Year = 'YEAR'
        table_Name = 'ibtracs'
        year_info = self.mysql.select_typhoon_year(Year, table_Name)
        for ech in year_info:
            year_list.append(ech[0])
        self.comboBox.addItems(year_list)
        self.comboBox.currentIndexChanged.connect(self.set_typhoon_name)
        self.comboBox_3.currentIndexChanged.connect(self.change_typhoon_mark)
        self.pushButton.clicked.connect(self.show_typhoon_track)


    def change_typhoon_mark(self):
        self.typhoon_mark = 1
        self.typhoon = self.comboBox_3.currentText()

    # 根据第一个下拉框中的年份信息 获取第二个下拉框的内容
    def set_typhoon_name(self):
        self.year = self.comboBox.currentText()
        if self.year_mark == 0:
            table_name = 'typhoon'
            Year = 'YEAR'
            Name = 'NAME'
            info = self.mysql.select_typhoon_name(Name, table_name, Year, self.year)
            for i in info:
                self.comboBox_3.addItem(i[0])
            self.year_mark = 1
        else:
            self.comboBox_3.clear()  # 这个就是为了防止 正常选择了一次年份后， 后面在年份那选择了“请选择年份”，所以如果再选择了“请选择年份”，我们上一次查询的台风名称需要clear
            self.comboBox_3.addItems(["请选择台风"])
            self.typhoon_mark = 0
            try:
                int(self.year)
                table_name = 'typhoon'
                Year = 'YEAR'
                Name = 'NAME'
                info = self.mysql.select_typhoon_name(Name, table_name, Year, self.year)
                for i in info:
                    self.comboBox_3.addItem(i[0])
            except:
                QMessageBox.information(self, '消息', '请选择正确的年份')


    def show_typhoon_track(self):
        if self.year_mark == 1 and self.typhoon_mark == 1:
            try:
                self.label_2.deleteLater()
                Lat = 'LAT'
                Lon = 'LON'
                table_name = 'typhoon'
                Year = 'YEAR'
                Name = 'NAME'
                info = self.mysql.select_typhoon_track(Lat, Lon, table_name, Year, self.year, Name, self.typhoon)
                print(len(info))
                for track_poit in info:
                    print(track_poit[0], track_poit[1])
                    self.webEngineView.page().runJavaScript(
                        're_first_last_name("' + track_poit[1] + track_poit[0] + '")')
                self.webEngineView.page().runJavaScript('pri_track_in_map()')
                print('finish')
            except:
                Lat = 'LAT'
                Lon = 'LON'
                table_name = 'typhoon'
                Year = 'YEAR'
                Name = 'NAME'
                info = self.mysql.select_typhoon_track(Lat, Lon, table_name, Year, self.year, Name, self.typhoon)
                print(len(info))
                for track_poit in info:
                    print(track_poit[0], track_poit[1])
                    self.webEngineView.page().runJavaScript('re_first_last_name("' + track_poit[1] + track_poit[0] + '")')
                self.webEngineView.page().runJavaScript('pri_track_in_map()')
                print('finish')
        else:
            QMessageBox.information(self, '消息', '请选择具体年份的台风进行查询')





    

        