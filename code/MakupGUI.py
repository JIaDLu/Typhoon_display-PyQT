import sys
import os
import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from PyQt5 import QtCore, QtGui, QtWidgets
from Beautiful_Photo import Ui_MainWindow
from PyQt5 import QtWidgets
from PyMysql import MSSQL
from longest_track import Ui_Dialog_track
from intensity import Ui_Dialog_intensity
from coexist import Ui_Dialog_coexist
from generation import Ui_Dialog_generation
from all_track import Ui_Dialog_all_track
from get_work_data import get_Data_Ui_MainWindow
import pandas as pd

class BP_Ui_MainWindow(QtWidgets.QWidget,Ui_MainWindow):
    def __init__(self):
        super(BP_Ui_MainWindow, self).__init__()
        self.setupUi(self)
        self.webEngineView.load(QtCore.QUrl("D://Pycharm//Lab//台风预报系统//demo.html"))
        self.ms = MSSQL()
        self.slot_init()
        self.year = None
        self.typhoon = None
        self.year_mark = 0
        self.typhoon_mark = 0
        self.label_3.setPixmap(QPixmap("typhoon-I.jpg"))  # 我的图片格式为png.与代码在同一目录下
        self.label_3.setScaledContents(True)

        self.lt = longest_track_Window()
        self.i = intensity_Window()
        self.co = coexist_Window()
        self.generation = generation_Window()

        self.all_track = all_track_Window()

        self.detail_typhoon = detail_info_Window()


    def slot_init(self):
        year_list = []
        Year = 'YEAR'
        table_Name = 'typhoon'
        year_info = self.ms.select_typhoon_year(Year,table_Name)
        for ech in year_info:
            year_list.append(ech[0])
        self.comboBox.addItems(year_list)
        self.pushButton.clicked.connect(self.show_typhoon_track)
        self.comboBox.currentIndexChanged.connect(self.set_typhoon_name)
        self.comboBox_3.currentIndexChanged.connect(self.change_typhoon_mark)
        self.pushButton_2.clicked.connect(self.show_long_track)
        self.pushButton_3.clicked.connect(self.show_intensity)
        self.pushButton_4.clicked.connect(self.show_coexist)
        self.pushButton_5.clicked.connect(self.show_all_track)
        self.pushButton_6.clicked.connect(self.show_generation)
        self.pushButton_7.clicked.connect(self.show_detail)

    def show_long_track(self):
        self.lt.show()

    def show_intensity(self):
        self.i.show()

    def show_coexist(self):
        self.co.show()

    def show_generation(self):
        self.generation.show()

    def show_all_track(self):
        self.all_track.show()

    def change_typhoon_mark(self):
        self.typhoon_mark = 1
        self.typhoon = self.comboBox_3.currentText()
        if self.year_mark == 1 and self.typhoon_mark == 1:
            self.pushButton.setStyleSheet("\n"
                                                        "background-color: rgb(245, 205, 121);")
            self.pushButton.setText('请开始查询')
            self.pushButton_7.setStyleSheet("\n"
                                                      "background-color: rgb(245, 205, 221);")
            self.pushButton_7.setText('台风详细信息')

    def show_detail(self):
        if self.year_mark == 1 and self.typhoon_mark == 1:
            self.detail_typhoon.show()
            table_name = 'typhoon'
            Year = 'YEAR'
            Name = 'NAME'
            result = self.ms.select_typhoon_detail(table_name, Year, self.year, Name, self.typhoon)
            #print(result[0])
            dict = {}
            for number,i in enumerate(result):
                dict[number] = i
            self.df = pd.DataFrame(dict)
            self.df = self.df.T
            self.df.loc[0]=['TID','YEAR','MONTH','DAY','HOUR','Intensify','LAT','LON','WND','PRES','NAME','NUM','CN_NAME']
            print(self.df)
            model = PdTable(self.df)
            view = self.detail_typhoon.tableView
            view.setModel(model)

            self.detail_typhoon.D_switch_window1.connect(self.setBrowerPath)
            self.detail_typhoon.D_switch_window2.connect(self.savefile)
        else:
            QMessageBox.information(self, '消息', '请选择具体希望查询的台风')

    def setBrowerPath(self):  # 选择文件夹进行存储
        download_path = QtWidgets.QFileDialog.getExistingDirectory(None, "浏览", "/home")
        self.detail_typhoon.lineEdit.setText(download_path)

    def savefile(self):
        if len(self.detail_typhoon.lineEdit_2.text()) < 1:
            QMessageBox.information(self.detail_typhoon.pushButton, ' ', '文件名不可为空', QMessageBox.Ok)
        else:
            try:
                self.df.to_csv(self.detail_typhoon.lineEdit.text() + '/' + self.detail_typhoon.lineEdit_2.text() + '.csv')
                QMessageBox.information(self, '消息', '已保存到指定路径')
                self.detail_typhoon.close()
            except:
                QMessageBox.information(self.detail_typhoon.pushButton, ' ', '所选目录错误！', QMessageBox.Ok)


    # 用于获取返回值的回调函数
    # def js_callback(self, result):
    #     print(result)

    def show_typhoon_track(self):
        if self.year_mark == 1 and self.typhoon_mark == 1:
            Lat = 'LAT'
            Lon = 'LON'
            table_name = 'typhoon'
            Year = 'YEAR'
            Name = 'NAME'
            info = self.ms.select_typhoon_track(Lat, Lon, table_name, Year, self.year, Name, self.typhoon)
            print(len(info))
            for track_poit in info:
                print(track_poit[0],track_poit[1])
                self.webEngineView.page().runJavaScript('re_first_last_name("' + track_poit[1] + track_poit[0] + '")')
            self.webEngineView.page().runJavaScript('pri_track_in_map()')
            print('finish')
        else:
            QMessageBox.information(self, '消息', '请选择具体年份的台风进行查询')

    # 根据第一个下拉框中的年份信息 获取第二个下拉框的内容
    def set_typhoon_name(self):
        self.year = self.comboBox.currentText()
        if self.year_mark == 0:
            table_name = 'typhoon'
            Year = 'YEAR'
            Name = 'NAME'
            info = self.ms.select_typhoon_name(Name, table_name,Year,self.year)
            for i in info:
                self.comboBox_3.addItem(i[0])
            self.year_mark = 1
        else:
            self.comboBox_3.clear()  #这个就是为了防止 正常选择了一次年份后， 后面在年份那选择了“请选择年份”，所以如果再选择了“请选择年份”，我们上一次查询的台风名称需要clear
            self.comboBox_3.addItems(["请选择台风"])
            self.year_mark = 0
            try:
                int(self.year)
                table_name = 'typhoon'
                Year = 'YEAR'
                Name = 'NAME'
                info = self.ms.select_typhoon_name(Name, table_name,Year,self.year)
                for i in info:
                    self.comboBox_3.addItem(i[0])
            except:
                QMessageBox.information(self, '消息', '请选择正确的年份')




class longest_track_Window(QtWidgets.QMainWindow, Ui_Dialog_track):
    def __init__(self):
        super(longest_track_Window, self).__init__()
        self.setupUi(self)
        self.label.setPixmap(QPixmap("longest_track.png"))  # 我的图片格式为png.与代码在同一目录下
        self.label.setScaledContents(True)



class intensity_Window(QtWidgets.QMainWindow, Ui_Dialog_intensity):
    def __init__(self):
        super(intensity_Window, self).__init__()
        self.setupUi(self)
        self.label.setPixmap(QPixmap("intensity.png"))  # 我的图片格式为png.与代码在同一目录下
        self.label.setScaledContents(True)


class coexist_Window(QtWidgets.QMainWindow, Ui_Dialog_coexist):
    def __init__(self):
        super(coexist_Window, self).__init__()
        self.setupUi(self)
        self.label.setPixmap(QPixmap("coexist.png"))  # 我的图片格式为png.与代码在同一目录下
        self.label.setScaledContents(True)


class generation_Window(QtWidgets.QMainWindow, Ui_Dialog_generation):
    def __init__(self):
        super(generation_Window, self).__init__()
        self.setupUi(self)
        self.label.setPixmap(QPixmap("generation_later.png"))  # 我的图片格式为png.与代码在同一目录下
        self.label.setScaledContents(True)
        self.label_3.setPixmap(QPixmap("generation_early.png"))  # 我的图片格式为png.与代码在同一目录下
        self.label_3.setScaledContents(True)

class all_track_Window(QtWidgets.QMainWindow, Ui_Dialog_all_track):
    def __init__(self):
        super(all_track_Window, self).__init__()
        self.setupUi(self)
        self.label.setPixmap(QPixmap("all_track.png"))  # 我的图片格式为png.与代码在同一目录下
        self.label.setScaledContents(True)


class detail_info_Window(QtWidgets.QMainWindow, get_Data_Ui_MainWindow):
    D_switch_window1 = QtCore.pyqtSignal()
    D_switch_window2 = QtCore.pyqtSignal()
    def __init__(self,parent=None):
        super(detail_info_Window, self).__init__(parent)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.Send_Signal_1)
        self.pushButton_2.clicked.connect(self.Send_Signal_2)

    def Send_Signal_1(self):
        self.D_switch_window1.emit()

    def Send_Signal_2(self):
        self.D_switch_window2.emit()



class PdTable(QAbstractTableModel):
    def __init__(self, data):
        QAbstractTableModel.__init__(self)
        self._data = data

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parent=None):
        return self._data.shape[1]

    # 显示数据
    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
        return None

    # 显示行和列头
    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[col]
        elif orientation == Qt.Vertical and role == Qt.DisplayRole:
            return self._data.axes[0][col]
        return None

