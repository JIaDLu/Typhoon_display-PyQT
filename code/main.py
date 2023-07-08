from log_in import Ui_MainWindow
from register import Example as register_ui
import sys
from Face_Sorce_APP import MyWindow
from PyQt5 import QtWidgets,QtCore
from PyMysql import *
from PyQt5.Qt import *
from function_option import Function_Option_MainWindow
from MakupGUI import BP_Ui_MainWindow
from Public_Notice import PN_Ui_MainWindow
import warnings
warnings.filterwarnings('ignore')

# 主窗口
class MainWindow(QtWidgets.QMainWindow,Ui_MainWindow):
    switch_window1 = QtCore.pyqtSignal() # 跳转信号
    switch_window2 = QtCore.pyqtSignal()  # 跳转信号
    switch_window3 = QtCore.pyqtSignal()
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.pushButton_register.clicked.connect(self.goPic)
        self.pushButtonOK.clicked.connect(self.goapp)
        self.pushButtonCancel.clicked.connect(self.cancel_Log)
    def goPic(self):
        self.switch_window1.emit()
    def goapp(self):
        self.switch_window2.emit()
    def cancel_Log(self):
        self.switch_window3.emit()

# 注册窗口
class PicWindow(QtWidgets.QMainWindow, register_ui):
    switch_window5 = QtCore.pyqtSignal()  # 跳转信号
    def __init__(self):
        super(PicWindow, self).__init__()
        self.setui(self)
        self.pushButton_exit.clicked.connect(self.goPic_main)

    def goPic_main(self):
        self.switch_window5.emit()


# 颜值打分窗口
class FS_AppWindow(QtWidgets.QMainWindow, MyWindow):
    switch_window_1 = QtCore.pyqtSignal()  # 跳转信号
    def __init__(self):
        super(FS_AppWindow, self).__init__()
        self.commandLinkButton_2.clicked.connect(self.goback)
    def goback(self):
        self.switch_window_1.emit()


class BP_AppWindow(QtWidgets.QMainWindow, BP_Ui_MainWindow):
    switch_window_1 = QtCore.pyqtSignal()  # 跳转信号
    def __init__(self):
        super(BP_AppWindow, self).__init__()
        self.commandLinkButton.clicked.connect(self.goback)

    def goback(self):
        self.switch_window_1.emit()


class Public_notice_Window(QtWidgets.QMainWindow, PN_Ui_MainWindow):
    def __init__(self):
        super(Public_notice_Window, self).__init__()
        self.setupUi(self)

# 功能选择窗口
class Function_Option_Window(QtWidgets.QMainWindow, Function_Option_MainWindow):
    switch_window_FS = QtCore.pyqtSignal() # 跳转信号
    switch_window_BP = QtCore.pyqtSignal()  # 跳转信号
    close_fo_window = QtCore.pyqtSignal()  # 跳转信号
    def __init__(self):
        super(Function_Option_Window, self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.goFaceSorce)
        self.pushButton_2.clicked.connect(self.goBeautifyPhoto)
        self.pushButton_3.clicked.connect(self.close_window)
        self.mysql = MSSQL()
        self.notice_len = None
        self.mark = None
        self.PN = Public_notice_Window()

    def close_window(self):
        self.close_fo_window.emit()

    def aaa(self):
        self.notice_len = len(self.mysql.get_notice_data())
        n = (str(self.notice_len))
        self.mysql.insert_mark_data(n)

    def bbb(self):
        self.notice_len = int(len(self.mysql.get_notice_data()))
        print(self.notice_len)
        self.mark = int(self.mysql.get_mark_data()[0][1])
        print(self.mark)
        if self.notice_len != self.mark:
            QMessageBox.information(self, '消息', '您有一则新公告，请注意查收')

    def goFaceSorce(self):
        self.switch_window_FS.emit()

    def goBeautifyPhoto(self):
        self.switch_window_BP.emit()

# 利用一个控制器来控制页面的跳转
class Controller1(QWidget):
    def __init__(self):
        super().__init__()
        self.reg = PicWindow()
        self.main = MainWindow()
        self.fs_app = FS_AppWindow()
        self.bp_app = BP_AppWindow()
        self.funtion_o = Function_Option_Window()
        self.reg.hide()
        self.main.hide()
        self.fs_app.hide()
        self.bp_app.hide()
        self.funtion_o.hide()
        self.first_length = None
        self.last_length = None

    # 跳转到 main 窗口
    def show_main(self):
        self.main.show()
        self.main.switch_window1.connect(self.show_reg)
        self.main.switch_window2.connect(self.show_app)
        self.main.switch_window3.connect(self.cancel_Log)

    # 跳转到 pic窗口
    def show_reg(self):
        self.main.close()
        self.reg.show()
        self.reg.switch_window5.connect(self.return_log)

    def return_log(self):
        self.main.show()
        self.reg.hide()

    def cancel_Log(self):
        self.main.close()

    def show_Func_Op(self):
        self.funtion_o.show()
        self.main.close()
        # self.funtion_o.bbb()
        # self.funtion_o.aaa()
        # self.length = len(self.funtion_o.aaa())
        self.funtion_o.switch_window_FS.connect(self.show_Face_Sorce_Windows)
        self.funtion_o.switch_window_BP.connect(self.show_Beautify_Photo_Windows)
        self.funtion_o.close_fo_window.connect(self.close_function_option_windows)

    def close_function_option_windows(self):
        self.funtion_o.close()

    def show_Face_Sorce_Windows(self):
        self.fs_app.show()
        self.fs_app.show_year()
        self.funtion_o.close()
        # self.funtion_o.aaa()
        self.fs_app.switch_window_1.connect(self.goBack_1_from_fs)

    def goBack_1_from_fs(self):
        # self.fs_app.comboBox.setCurrentIndex(0)
        # if self.fs_app.year_mark == 1:
        #     self.fs_app.comboBox_3.clear()
        #     self.fs_app.comboBox_3.addItems(["请选择台风"])
        # self.fs_app.label_2.setPixmap(QPixmap("IBTrACS.png"))
        # self.fs_app.label_2.setScaledContents(True)
        self.fs_app.close()
        self.funtion_o.show()


    def show_Beautify_Photo_Windows(self):
        self.bp_app.show()
        self.funtion_o.close()
        # self.funtion_o.aaa()
        self.bp_app.switch_window_1.connect(self.goBack_2_from_bp)

    def goBack_2_from_bp(self):
        self.bp_app.close()
        self.funtion_o.show()

    # 跳转到 pic窗口
    def show_app(self):
        usr_name = self.main.sr_zh.text()
        usr_pwd = self.main.sr_mm.text()
        #2 查询数据库，判定是否有匹配
        ms = MSSQL()
        mark = [1]
        table_name = 'client_info'
        args = ('acount', 'password')
        result = ms.query_super(table_name, args,usr_name,usr_pwd)
        if(result > 0):
            print("密码正确")
            QMessageBox.information(self, '消息', '登录成功')
            self.fs_app.usr_name = usr_name
            self.show_Func_Op()
        else:
            print("密码错误")
            QMessageBox.warning(self,
                                "警告",
                                "用户名或密码错误！",
                                QMessageBox.Yes)
            self.main.sr_zh.setFocus()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    controller1 = Controller1()
    controller1.show_main()
    sys.exit(app.exec_())