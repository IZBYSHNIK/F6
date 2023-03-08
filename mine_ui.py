import datetime
import os
import random
import sys

from PySide6 import QtCore, QtGui, QtWidgets, QtSvg
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QTableWidgetItem
from PySide6 import QtSvgWidgets
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar


from StudentsManager import ManagerStudents
from UserManager import UserManager


VERSION = '1.1.4'

is_work = True
is_new_user = False
dirname, filename = os.path.split(os.path.abspath(__file__))


DEBAG = True
BASE_PATH = dirname
DOCUMENTS_PATH = os.path.expanduser("~/F6")
PACH_SAVE_F6 = DOCUMENTS_PATH
BD_PATH = os.path.join(DOCUMENTS_PATH, 'BD')
if not os.path.exists(os.path.join(DOCUMENTS_PATH, 'BD')):
    os.makedirs(os.path.join(DOCUMENTS_PATH, "BD"))

USER_MANAGER = UserManager(BD_PATH)
MANAGER_STUDENTS = None

is_click_license = 0

class SplashScreen(QtWidgets.QSplashScreen):
    def __init__(self):
        super().__init__()
        self.setObjectName("splash_screen")
        self.setFixedSize(379, 443)
        self.move((app.primaryScreen().size().width() - self.size().width()) // 2,
                  (app.primaryScreen().size().height() - self.size().height()) // 2 - 40)

        self.logo = QtSvgWidgets.QSvgWidget(os.path.join(BASE_PATH, 'media', 'logo.svg'), parent=self)
        self.logo.move(65,25)
        self.logo.setFixedSize(256, 256)
        self.logo.setObjectName("logo")

        self.progressBar = QtWidgets.QProgressBar(self)
        self.progressBar.setGeometry(QtCore.QRect(0, 400, 381, 51))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setTextVisible(False)
        self.progressBar.setObjectName("progressBar")
        self.version = QtWidgets.QLabel(self)
        self.version.setGeometry(QtCore.QRect(330, 400, 61, 41))
        font = QtGui.QFont()
        font.setItalic(True)
        self.version.setFont(font)
        self.version.setLayoutDirection(QtCore.Qt.LayoutDirection.RightToLeft)
        self.version.setObjectName("version")
        self.message = QtWidgets.QLabel(self)
        self.message.setGeometry(QtCore.QRect(10, 360, 351, 20))
        self.message.setObjectName("message")
        self.progressBar.raise_()
        self.logo.raise_()
        self.version.raise_()
        self.message.raise_()

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Form", "Form"))
        self.version.setText(_translate("Form", VERSION))
        self.message.setText(_translate("Form", "Идет загрузка программы, ожидайте ..."))


class LicenseWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(LicenseWindow, self).__init__(parent=parent)
        self.setObjectName("Form")
        self.resize(600, 700)
        self.setWindowIcon(QtGui.QIcon('media\\logo.svg'))
        self.setFixedSize(QtCore.QSize(600, 700))
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.logo = QtSvgWidgets.QSvgWidget(os.path.join(BASE_PATH, 'media', 'logo.svg'))
        self.logo.setFixedSize(QtCore.QSize(50, 50))

        self.logo.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.logo, QtCore.Qt.AlignmentFlag.AlignVCenter,QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.label = QtWidgets.QLabel(self)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.textBrowser = QtWidgets.QTextBrowser(self)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.textBrowser.setFont(font)
        self.textBrowser.setObjectName("textBrowser")
        self.verticalLayout_2.addWidget(self.textBrowser)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, 8, -1, -1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton = QtWidgets.QPushButton(self)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

        self.pushButton.clicked.connect(self.click_OK)
        self.init_license(os.path.join(BASE_PATH, 'license.txt'))


    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Form", "Лицензия"))
        self.label.setText(_translate("Form", "Лицензионное соглашение"))
        self.textBrowser.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">ппппппппппппппп</span></p></body></html>"))
        self.pushButton.setText(_translate("Form", "ОК"))

    def click_OK(self):
        global is_click_license
        is_click_license = 1
        self.close()

    def init_license(self, file_puth=None):
        with open(file_puth, 'r', encoding='Windows-1251') as f:
            self.textBrowser.setText(''.join(f.readlines()))


class Regist(QtWidgets.QWidget):
    def __init__(self):
        self.status = 0
        super().__init__()
        self.setWindowIcon(QtGui.QIcon('media\\logo.svg'))
        self.setObjectName("Regist")
        self.setFixedSize(442, 700)
        self.setStyleSheet("QPushButton{\n"
                           "font-size: 20px;\n"
                           "color: white;\n"
                           "}\n"
                           "\n"
                           "QPushButton:hover {\n"
                           "    border: 6px solid green;\n"
                           "    font: 21px;\n"
                           "\n"
                           "}\n"
                           "\n"
                           "Form {\n"
                           "background: #f9f8f4;\n"
                           "}\n"
                           "\n"
                           "QLabel#regist_lable{\n"
                           "    font-size: 45px;\n"
                           "font-family: Myriad Pro;\n"
                           "text-align: center;\n"
                           "background: #bcbbb7;\n"
                           "}\n"
                           "\n"
                           "QLineEdit {\n"
                           "border: none;\n"
                           "color:white;\n"
                           "padding-left: 15px;\n"
                           "padding-right: 15px;\n"
                           "font: 16px;\n"
                           "background: black;\n"
                           "}\n"
                           "")
        self.regist_lable = QtWidgets.QLabel(self)
        self.regist_lable.setEnabled(True)
        self.regist_lable.setGeometry(QtCore.QRect(0, -10, 442, 100))
        self.regist_lable.setMinimumSize(QtCore.QSize(442, 100))
        self.regist_lable.setMaximumSize(QtCore.QSize(442, 70))
        self.regist_lable.setStyleSheet("")
        self.regist_lable.setTextFormat(QtCore.Qt.TextFormat.RichText)
        self.regist_lable.setScaledContents(False)
        self.regist_lable.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.regist_lable.setObjectName("regist_lable")
        self.login_edit = QtWidgets.QLineEdit(self)
        self.login_edit.setGeometry(QtCore.QRect(41, 150, 360, 40))
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(False)
        font.setItalic(False)
        # font.setWeight(50)
        self.login_edit.setFont(font)
        self.login_edit.setObjectName("login_edit")
        self.create_push = QtWidgets.QPushButton(self)
        self.create_push.setGeometry(QtCore.QRect(60, 630, 151, 61))
        self.create_push.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.ArrowCursor))
        self.create_push.setAutoFillBackground(False)
        self.create_push.setStyleSheet("background: #2ac11a;\n"
                                       "border: none;\n"
                                       "\n"
                                       "\n"
                                       "\n"
                                       "\n"
                                       "")
        self.create_push.setCheckable(False)
        self.create_push.setAutoRepeat(False)
        self.create_push.setDefault(False)
        self.create_push.setObjectName("create_push")
        self.cancel_push = QtWidgets.QPushButton(self)
        self.cancel_push.setGeometry(QtCore.QRect(220, 630, 151, 61))
        self.cancel_push.setStyleSheet("background: #2ac11a;\n"
                                       "border: none;")
        self.cancel_push.setObjectName("cancel_push")
        self.password_edit = QtWidgets.QLineEdit(self)
        self.password_edit.setGeometry(QtCore.QRect(41, 240, 360, 40))
        self.password_edit.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)
        self.password_edit.setObjectName("password_edit")
        self.login_lable = QtWidgets.QLabel(self)
        self.login_lable.setGeometry(QtCore.QRect(20, 100, 311, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.login_lable.setFont(font)
        self.login_lable.setObjectName("login_lable")
        self.password_lable = QtWidgets.QLabel(self)
        self.password_lable.setGeometry(QtCore.QRect(20, 190, 141, 51))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.password_lable.setFont(font)
        self.password_lable.setObjectName("password_lable")
        self.password_edit_2 = QtWidgets.QLineEdit(self)
        self.password_edit_2.setGeometry(QtCore.QRect(40, 330, 360, 40))
        self.password_edit_2.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)
        self.password_edit_2.setObjectName("password_edit_2")
        self.password_lable_2 = QtWidgets.QLabel(self)
        self.password_lable_2.setGeometry(QtCore.QRect(30, 280, 311, 51))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.password_lable_2.setFont(font)
        self.password_lable_2.setObjectName("password_lable_2")
        self.teamleader_lable = QtWidgets.QLabel(self)
        self.teamleader_lable.setGeometry(QtCore.QRect(240, 380, 311, 51))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.teamleader_lable.setFont(font)
        self.teamleader_lable.setObjectName("teamleader_lable")
        self.teamleader_edit = QtWidgets.QLineEdit(self)
        self.teamleader_edit.setGeometry(QtCore.QRect(240, 430, 160, 40))
        self.teamleader_edit.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)
        self.teamleader_edit.setObjectName("teamleader_edit")
        self.office_name_edit = QtWidgets.QLineEdit(self)
        self.office_name_edit.setGeometry(QtCore.QRect(40, 430, 160, 40))
        self.office_name_edit.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)
        self.office_name_edit.setObjectName("office_name_edit")
        self.office_name_lable = QtWidgets.QLabel(self)
        self.office_name_lable.setGeometry(QtCore.QRect(40, 380, 91, 51))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.office_name_lable.setFont(font)
        self.office_name_lable.setObjectName("office_name_lable")
        self.group_edit = QtWidgets.QLineEdit(self)
        self.group_edit.setGeometry(QtCore.QRect(40, 520, 160, 40))
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(QtGui.QFont.Weight(50))
        self.group_edit.setFont(font)
        self.group_edit.setObjectName("group_edit")

        self.specialization_edit = QtWidgets.QLineEdit(self)
        self.specialization_edit.setGeometry(QtCore.QRect(240, 520, 160, 40))
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(QtGui.QFont.Weight(50))
        self.specialization_edit.setFont(font)
        self.specialization_edit.setObjectName("specialization_edit")

        self.group_lable = QtWidgets.QLabel(self)
        self.group_lable.setGeometry(QtCore.QRect(40, 470, 311, 51))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.group_lable.setFont(font)
        self.group_lable.setObjectName("group_lable")

        self.specialization_lable = QtWidgets.QLabel(self)
        self.specialization_lable.setGeometry(QtCore.QRect(240, 470, 311, 51))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.specialization_lable.setFont(font)
        self.specialization_lable.setObjectName("specialization_lable")

        self.message_regist = QtWidgets.QTextBrowser(self)
        self.message_regist.setGeometry(40, 550 + 30, 351, 41)
        self.message_regist.setStyleSheet(
            'border: none; color: red; font: 14px; background-color: rgba(249, 248, 244, 0);')

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

        self.create_push.clicked.connect(self.click_create_push)
        self.cancel_push.clicked.connect(self.click_cancel_push)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Regist", "Регистрация"))
        self.regist_lable.setText(_translate("Regist", "<html><head/><body><p>РЕГИСТРАЦИЯ</p></body></html>"))
        self.create_push.setText(_translate("Regist", "Создать"))
        self.cancel_push.setText(_translate("Regist", "Отмена"))
        self.login_lable.setText(_translate("Regist", "*Имя пользователя"))
        self.password_lable.setText(_translate("Regist", "*Пароль"))
        self.password_lable_2.setText(_translate("Regist", "*Повторите пароль"))
        self.teamleader_lable.setText(_translate("Regist", "ФИО Кл.руководителя"))
        self.office_name_lable.setText(_translate("Regist", "Своё ФИО"))
        self.group_lable.setText(_translate("Regist", "Группа"))
        self.specialization_lable.setText('Специализация')

    def check_lables(self):
        kwargs = {}
        USER_MANAGER.USER_CLASS.check_username(self.login_edit.text())
        USER_MANAGER.USER_CLASS.check_password(self.password_edit.text())
        if self.login_edit.text() in USER_MANAGER.users_id.values():
            raise ValueError('Имя пользователя занято')
        if not self.password_edit.text() == self.password_edit_2.text():
            raise ValueError('Не совподают пароли')
        if self.office_name_edit.text():
            kwargs['offical_name'] = USER_MANAGER.USER_CLASS.check_fio(self.office_name_edit.text())
        if self.teamleader_edit.text():
            kwargs['teamleader'] = USER_MANAGER.USER_CLASS.check_fio(self.teamleader_edit.text())
        if self.group_edit.text():
            kwargs['group'] = self.group_edit.text()
        if self.specialization_edit.text():
            kwargs['specialization'] = self.specialization_edit.text()
        return self.login_edit.text(), self.password_edit.text(), kwargs

    def click_create_push(self):
        self.message_regist.setText('')
        try:
            username, password, kwargs = self.check_lables()
            user = USER_MANAGER.USER_CLASS(username, password, kwargs)
            USER_MANAGER.link_user_by_obj(user)
            USER_MANAGER.save_users()


        except BaseException as message:
            self.message_regist.setText('*' + str(message))
        else:
            self.password_edit.clear()
            self.password_edit_2.clear()
            self.group_edit.clear()
            self.specialization_edit.clear()
            self.login_edit.clear()
            self.teamleader_edit.clear()
            self.office_name_edit.clear()
            self.status = 1
            self.close()

    def click_cancel_push(self):
        self.status = 2
        self.close()


class Auth(QtWidgets.QWidget):

    def __init__(self):
        self.status = 0
        super(Auth, self).__init__()
        self.setWindowIcon(QtGui.QIcon('media\\logo.svg'))
        self.setFixedSize(442, 580)
        self.setStyleSheet("QPushButton{font: 18px; border: none; color: white; padding: 0px; margin: 0px}\n"
                           "QPushButton:hover {font-size: 21px;}\n"
                           "Form {background: #f9f8f4;}\n"
                           "QLabel#auth{font-size: 45px;font-family: Myriad Pro;text-align: center;background: #bcbbb7;}\n"
                           "QLabel#login_lable{font-size: 35px;text-align: center;}\n"
                           "QLabel#password_lable{font-size: 35px;text-align: center;}\n"
                           "QLabel{font-size: 14px;text-align: center;}\n"
                           "QLineEdit {border: 2px solid black;color:white;padding-left: 15px;font: 16px;background: black;}\n")
        self.auth = QtWidgets.QLabel(self)
        self.auth.setEnabled(True)
        self.auth.setGeometry(QtCore.QRect(0, -10, 442, 100))
        self.auth.setMinimumSize(QtCore.QSize(442, 100))
        self.auth.setMaximumSize(QtCore.QSize(442, 70))
        self.auth.setStyleSheet("")
        self.auth.setTextFormat(QtCore.Qt.TextFormat.RichText)
        self.auth.setScaledContents(False)
        self.auth.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.auth.setObjectName("auth")
        self.in_push = QtWidgets.QPushButton(self)
        self.in_push.setGeometry(QtCore.QRect(70, 480, 151, 61))
        self.in_push.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.ArrowCursor))
        self.in_push.setAutoFillBackground(False)
        self.in_push.setStyleSheet("background: #2ac11a;\n")
        self.in_push.setCheckable(False)
        self.in_push.setAutoRepeat(False)
        self.in_push.setDefault(False)
        self.in_push.setObjectName("in_push")
        self.regist_push = QtWidgets.QPushButton(self)
        self.regist_push.setGeometry(QtCore.QRect(230, 480, 151, 61))
        self.regist_push.setStyleSheet("background: #2ac11a;\n")
        self.regist_push.setObjectName("regist_push")
        self.password_edit = QtWidgets.QLineEdit(self)
        self.password_edit.setGeometry(QtCore.QRect(60, 300, 351, 41))
        self.password_edit.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)
        self.password_edit.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.password_edit.setObjectName("password_edit")
        self.login_lable = QtWidgets.QLabel(self)
        self.login_lable.setGeometry(QtCore.QRect(70, 120, 131, 41))
        self.login_lable.setObjectName("login_lable")
        self.password_lable = QtWidgets.QLabel(self)
        self.password_lable.setGeometry(QtCore.QRect(70, 235, 141, 51))
        self.password_lable.setObjectName("password_lable")
        self.message_auth = QtWidgets.QTextBrowser(self)
        self.message_auth.setGeometry(60, 351 + 20, 351, 41)

        self.licensewindow = LicenseWindow()

        self.license_link = QtWidgets.QCommandLinkButton(self)
        self.license_link.setText('©2022DegtyarevIvan')
        self.license_link.setIcon(QtGui.QIcon(''))
        self.license_link.setGeometry(QtCore.QRect(125, 540, 442, 100))



        self.message_auth.setStyleSheet(
            'border: none; color: red; font: 14px; background-color: rgba(249, 248, 244, 0);')

        self.spin_box = QtWidgets.QComboBox(self)
        self.spin_box.setGeometry(QtCore.QRect(60, 180, 351, 41))
        self.spin_box.setStyleSheet("""QComboBox {color:white;font: 16px;background: black;}\n""")

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

        self.update_users()

        self.in_push.clicked.connect(self.click_auth_push)
        self.regist_push.clicked.connect(self.click_regis_push)
        self.license_link.clicked.connect(self.click_license)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Auth", "Авторизация"))
        self.auth.setText(_translate("Auth", "<p>АВТОРИЗАЦИЯ </p>"))
        self.in_push.setText(_translate("Auth", "Вход"))
        self.regist_push.setText(_translate("Auth", "Регистрация"))
        self.login_lable.setText(_translate("Auth", "Логин"))
        self.password_lable.setText(_translate("Auth", "Пароль"))

    def keyPressEvent(self, e):
        k = e.key()
        super().keyPressEvent(e)
        if k == 16777220:
            self.click_auth_push()

    def update_users(self):
        self.spin_box.clear()
        for i in USER_MANAGER.users_id:
            self.spin_box.addItem(QIcon('0'), USER_MANAGER.users_id[i])

    def checking_log_password(self):
        USER_MANAGER.USER_CLASS.check_username(self.spin_box.currentText())
        USER_MANAGER.USER_CLASS.check_password(self.password_edit.text())
        return self.spin_box.currentText(), self.password_edit.text()

    def click_auth_push(self):
        try:
            username, password = self.checking_log_password()
        except BaseException as message:
            # self.message = QtWidgets.QMessageBox().critical(self, "Ошибка", str(message), QtWidgets.QMessageBox.StandardButton.Ok)
            self.message_auth.setText('*' + str(message))
        else:
            try:
                USER_MANAGER.link_user_by_username(username, password)
            except BaseException as message:
                self.message_auth.setText('*' + str(message))
            else:
                self.password_edit.clear()
                self.status = 1
                self.close()

    def click_regis_push(self):
        self.status = 3
        self.close()

    def click_license(self):
        self.licensewindow.show()


class AbsenceTab(QtWidgets.QWidget):
    def __init__(self, parent):
        super(AbsenceTab, self).__init__(parent=parent)
        self.parent = parent
        self.setObjectName("F6")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")

        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.frame = QtWidgets.QFrame(self)
        self.frame.setMinimumSize(QtCore.QSize(0, 80))
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetMinimumSize)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setMinimumSize(QtCore.QSize(250, 0))
        self.label_2.setObjectName("label_2")
        self.label_2.setFont(QtGui.QFont('Calibri', 15))
        self.horizontalLayout.addWidget(self.label_2)
        self.horizontalLayout_3.addLayout(self.horizontalLayout)
        self.wLayout = QtWidgets.QVBoxLayout()
        self.statustic1 = QtWidgets.QLabel(self.frame)
        self.statustic2 = QtWidgets.QLabel(self.frame)

        self.wLayout.addWidget(self.statustic1)
        self.wLayout.addWidget(self.statustic2)
        self.horizontalLayout_3.addLayout(self.wLayout)

        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding,
                                           QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(7, -1, -1, -1)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout_4 = QtWidgets.QVBoxLayout()
        self.horizontalLayout_4.setContentsMargins(7, -1, -1, -1)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.is_sick_rb = QtWidgets.QRadioButton(self.frame)
        self.is_sick_rb.setObjectName("is_sick_rb")
        self.horizontalLayout_4.addWidget(self.is_sick_rb)
        self.radioButton_2 = QtWidgets.QRadioButton(self.frame)
        self.radioButton_2.setObjectName("radioButton_2")
        self.radioButton_2.setChecked(True)
        self.horizontalLayout_4.addWidget(self.radioButton_2)

        # ________________________________________
        self.set_size_posetiv_font_push = Push(self.frame, 40, 40, 5, tool_tip='Увеличить размер текста',
                                               icon_path=os.path.join('media', 'posetive.svg'))
        self.horizontalLayout_2.addWidget(self.set_size_posetiv_font_push)

        self.set_size_negativ_font_push = Push(self.frame, 40, 40, 5, tool_tip='Уменьшить размер текста',
                                               icon_path=os.path.join('media', 'negative.svg'))
        self.horizontalLayout_2.addWidget(self.set_size_negativ_font_push)

        # _________________________________________

        self.horizontalLayout_2.addLayout(self.horizontalLayout_4)

        self.save_table_push = Push(self.frame, 40, 40, 5, tool_tip='Сохронить изменения',
                                    icon_path=os.path.join('media', 'buttons', 'save.svg'))
        self.save_table_push.setObjectName("save_table_push")
        self.horizontalLayout_2.addWidget(self.save_table_push)
        self.game_over_push = Push(self.frame, 40, 40, 5, tool_tip='Завершить текущий месяц',
                                   icon_path=os.path.join('media', 'game_over.svg'))
        self.game_over_push.setObjectName("game_over_push")
        self.horizontalLayout_2.addWidget(self.game_over_push)
        self.save_to_exel_push = Push(self.frame, 55, 55, 5, tool_tip='Сохронить в EXEL',
                                      icon_path=os.path.join('media', 'save_exel.svg'))
        self.save_to_exel_push.setObjectName("save_to_exel_push")
        self.horizontalLayout_2.addWidget(self.save_to_exel_push)
        self.horizontalLayout_3.addLayout(self.horizontalLayout_2)
        self.verticalLayout_3.addWidget(self.frame)
        self.verticalLayout.addLayout(self.verticalLayout_3)

        self.retranslateUi()
        self.add_function()


        self.is_click_end_period = 0
    def add_function(self):
        self.save_to_exel_push.clicked.connect(self.save_to_exel)
        self.save_table_push.clicked.connect(self.save_table)
        self.game_over_push.clicked.connect(self.click_end_period)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.label_2.setText(_translate("MainWindow", f"Добро пожаловать, Nouname!"))
        self.is_sick_rb.setText(_translate("MainWindow", "ПОУВ"))
        self.radioButton_2.setText(_translate("MainWindow", "НЕУВ"))

    def update_statistics(self):
        statistics = MANAGER_STUDENTS.get_statistics()
        if statistics.get('man_hours') > 0:
            self.statustic1.setText(
                f'Чел.час = {str(statistics.get("man_hours"))} \t\t Посещ.Кач. = {str(round(statistics.get("quality_attendance") * 100, 2))}%')
            self.statustic2.setText(
                f'Посещ.Общ. = {str(round(statistics.get("total_attendance") * 100, 2))}% \t Прогул 1 студ. = {str(round(statistics.get("absences_by_student", 1)))}')
        else:
            self.statustic1.clear()
            self.statustic2.clear()

    def save_to_exel(self):
        try:
            path = MANAGER_STUDENTS.save_f6(os.path.join(DOCUMENTS_PATH,
                                                         f'{"_".join(["П", str(MANAGER_STUDENTS.MONTHS[MANAGER_STUDENTS.period[0] - 1]), str(MANAGER_STUDENTS.period[1]), str(USER_MANAGER.user.username)])}.xlsx'))
        except BaseException as f:
            QtWidgets.QMessageBox.critical(self, 'Ошибка сохранения', 'Файл не был сохранен. Повторите попытку')
        else:
            QtWidgets.QMessageBox.information(self, 'Успешное сохранение',
                                              f'Файл успешно сохранен в дириктории: {path}')

    def save_table(self):
        MANAGER_STUDENTS.save_students()

    def set_size_font(self, table, is_posetiv=True):
        if is_posetiv and table.mod_size < 25:
            table.update_table_students(size=table.mod_size + 2)
        elif is_posetiv and table.mod_size > 25:
            self.parent.profile.cod = [1, 4]
        elif table.mod_size < -7:
            self.parent.profile.cod = [1, 3]
        elif table.mod_size > -8:
            table.update_table_students(size=table.mod_size - 2)

    def check_value(self, tablewidget):
        if self.parent.group.indexOf(self.parent.students) == -1 and len(MANAGER_STUDENTS.students) != 0:
            self.parent.group.insertTab(2, self.parent.students, 'Cтуденты')

        item = tablewidget.currentItem()
        if not item is None:
            try:
                if item.row() == 1 and 2 <= item.column() <= 32:
                    if item.text() == '' or item.text() == ' ':
                        if MANAGER_STUDENTS.days.get(item.column() - 1):
                            MANAGER_STUDENTS.days[item.column() - 1] = 0
                        item.setText('')
                    elif item.text().isnumeric() and  0 <= int(item.text()) <= 10 :
                        MANAGER_STUDENTS.add_hours_by_day(item.column() - 1, int(item.text()))
                    else:
                        item.setText(str(MANAGER_STUDENTS.days.get(item.column() - 1, '')))
                    item.setFont(QtGui.QFont('Calibri', 14 + tablewidget.mod_size))
                    tablewidget.update_hours_day()

                elif 32 >= item.column() >= 2 and len(MANAGER_STUDENTS.students) + 2 >= item.row() >= 2:
                    if item.text() == '' or item.text() == ' ':
                        if item.column() - 1 in MANAGER_STUDENTS.students[item.row() - 3].absence_days:
                            del MANAGER_STUDENTS.students[item.row() - 3].absence_days[item.column() - 1]
                        if item.column() - 1 in MANAGER_STUDENTS.students[item.row() - 3].sick_days:
                            del MANAGER_STUDENTS.students[item.row() - 3].sick_days[item.column() - 1]
                        item.setBackground(QtGui.QColor(255, 255, 255))

                    elif item.text().isnumeric() and 0 <= int(item.text()) <= 10:
                        if self.is_sick_rb.isChecked():
                            tablewidget.add_hours_in_table(item.row(), item.column(), int(item.text()), type_day='s')
                        else:
                            tablewidget.add_hours_in_table(item.row(), item.column(), int(item.text()), type_day='a')


                    else:
                        if MANAGER_STUDENTS.students[item.row() - 3].sick_days.get(item.column() - 1, ''):
                            item.setText(str(
                                MANAGER_STUDENTS.students[item.row() - 3].sick_days.get(item.column() - 1, '')))
                        elif MANAGER_STUDENTS.students[item.row() - 3].absence_days.get(item.column() - 1, ''):
                            item.setText(str(
                                MANAGER_STUDENTS.students[item.row() - 3].absence_days.get(item.column() - 1, '')))
                        else:
                            item.setText('')
                    tablewidget.update_statistics_student(item.row())

                elif item.column() == 1:
                    if item.row() == len(MANAGER_STUDENTS.students) + 3:
                        try:
                            MANAGER_STUDENTS.CLASS_STUDENT.chech_fio(item.text())
                        except BaseException:
                            item.setBackground(QtGui.QColor(255, 0, 0))
                        else:
                            self.parent.profile.cod = [0, 1]
                            if item.text().lower() == 'чайковский пётр ильич':
                                self.parent.profile.cod = [2, 2]
                            if len(MANAGER_STUDENTS.students) < 30:
                                MANAGER_STUDENTS.add_student(MANAGER_STUDENTS.CLASS_STUDENT(item.text()))
                                for i in range(2, 32 + 1):
                                    if not i - 1 in MANAGER_STUDENTS.days:
                                        tablewidget.setItem(tablewidget.rowCount() - 2, i,
                                                            QTableWidgetItem(""))
                                        tablewidget.item(tablewidget.rowCount() - 2, i).setBackground(
                                            QtGui.QColor(220, 220, 220))
                                        tablewidget.item(tablewidget.rowCount() - 2, i).setFlags(
                                            QtCore.Qt.ItemFlag.ItemIsEnabled)
                            tablewidget.update_table_students()
                            if hasattr(self.parent, 'marks'):
                                self.parent.marks.tableWidget_3.update_table_students()
                            if hasattr(self.parent, 'students'):
                                self.parent.students.update_list_students()

            except BaseException as f:
                print(f)
            self.update_statistics()

    def click_end_period(self):
        self.is_click_end_period = 1
        self.parent.profile.cod = [0, 2]

        message = QtWidgets.QMessageBox.question(self, 'Завершение',
                                                 'Вы точно хотите завершить этот месяц? \n После этого форма шесть будет сохранена, перенесена и находится в архиве.',
                                                 QtWidgets.QMessageBox.StandardButton.No | QtWidgets.QMessageBox.StandardButton.Yes)
        if message.Yes == message:
            MANAGER_STUDENTS.save_students()
            try:
                MANAGER_STUDENTS.push_archive()
            except BaseException as f:
                print(f, 3743)
            else:

                MANAGER_STUDENTS.create_new_table()
                self.update_statistics()
                self.parent.marks.update_statistics_2()
                self.tableWidget.update_table_students()
                self.parent.marks.tableWidget_3.update_table_students()
                self.parent.archive.init_archive()
                self.parent.profile.cod = [3, 2]

    def init_table_absence(self, only_show=False):
        if hasattr(self, 'tableWidget'):
            self.verticalLayout.removeWidget(self.tableWidget)

        self.tableWidget = TableAbsence()
        self.tableWidget.setStyleSheet("""QTableWidget {border: none;}""")
        self.tableWidget.setObjectName("tableView")

        self.verticalLayout.addWidget(self.tableWidget)
        self.verticalLayout.addItem(
            QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum))

        self.set_size_negativ_font_push.clicked.connect(lambda: self.set_size_font(self.tableWidget, False))
        self.set_size_posetiv_font_push.clicked.connect(lambda: self.set_size_font(self.tableWidget))
        self.tableWidget.update_table_students()
        self.update_statistics()
        self.tableWidget.cellPressed.connect(self.cellPressed)

        if not only_show:
            self.tableWidget.cellChanged.connect(lambda: self.check_value(self.tableWidget))
    def cellPressed(self, row, column):
        if self.tableWidget.hasFocus():
            if 32 >= column >= 2 and len(
                    MANAGER_STUDENTS.students) + 2 >= row >= 3 and column - 1 in MANAGER_STUDENTS.days:
                try:
                    if hasattr(self.tableWidget, 'old_item1'):
                        self.tableWidget.item(self.tableWidget.old_item1[0], 0).setBackground(
                            QtGui.QColor(255, 255, 255))
                        self.tableWidget.item(2, self.tableWidget.old_item1[1]).setBackground(
                            QtGui.QColor(255, 255, 255))
                        self.tableWidget.old_item1 = (row, column)
                        self.tableWidget.item(self.tableWidget.old_item1[0], 0)
                    else:
                        self.tableWidget.old_item1 = (row, column)
                    self.tableWidget.item(row, 0).setBackground(QtGui.QColor(102, 102, 102))
                    self.tableWidget.item(2, column).setBackground(QtGui.QColor(102, 102, 102))

                except BaseException as f:
                    print(repr(f))


class MarksTab(QtWidgets.QWidget):
    def __init__(self, parent):
        super(MarksTab, self).__init__(parent=parent)
        self.parent = parent
        self.setObjectName("marks")
        self.verticalLayout_25 = QtWidgets.QVBoxLayout(self)
        self.verticalLayout_25.setObjectName("verticalLayout_25")
        self.verticalLayout_24 = QtWidgets.QVBoxLayout()
        self.verticalLayout_24.setObjectName("verticalLayout_24")
        self.frame_3 = QtWidgets.QFrame(self)
        self.frame_3.setMinimumSize(QtCore.QSize(0, 80))
        self.frame_3.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_3.setObjectName("frame_3")
        self.horizontalLayout_17 = QtWidgets.QHBoxLayout(self.frame_3)
        self.horizontalLayout_17.setObjectName("horizontalLayout_17")

        self.wLayout2 = QtWidgets.QVBoxLayout()
        self.statustic3 = QtWidgets.QLabel(self.frame_3)
        self.statustic4 = QtWidgets.QLabel(self.frame_3)
        self.wLayout2.addWidget(self.statustic3)
        self.wLayout2.addWidget(self.statustic4)

        self.horizontalLayout_17.addLayout(self.wLayout2)

        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding,
                                            QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_17.addItem(spacerItem1)
        self.horizontalLayout_19 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_19.setContentsMargins(7, -1, -1, -1)
        self.horizontalLayout_19.setObjectName("horizontalLayout_19")
        self.pushButton_9 = Push(self.frame_3, 40, 40, 5, tool_tip='Сохронить изменения',
                                 icon_path=os.path.join('media', 'buttons', 'save.svg'))
        self.pushButton_9.setObjectName("pushButton_9")

        # ___________________________________________________________________
        self.set_size_posetiv_font_push2 = Push(self.frame_3, 40, 40, 5, tool_tip='Увеличить размер текста',
                                                icon_path=os.path.join('media', 'posetive.svg'))
        self.horizontalLayout_19.addWidget(self.set_size_posetiv_font_push2)

        self.set_size_negativ_font_push2 = Push(self.frame_3, 40, 40, 5, tool_tip='Уменьшить размер текста',
                                                icon_path=os.path.join('media', 'negative.svg'))
        self.horizontalLayout_19.addWidget(self.set_size_negativ_font_push2)

        # ___________________________________________________________________
        self.horizontalLayout_19.addWidget(self.pushButton_9)
        self.save_to_exel_marks_push = Push(self.frame_3, 55, 55, 5, tool_tip='Сохронить в EXEL',
                                            icon_path=os.path.join('media', 'save_exel.svg'))
        self.save_to_exel_marks_push.setObjectName("pushButton_10")
        self.horizontalLayout_19.addWidget(self.save_to_exel_marks_push)
        self.horizontalLayout_17.addLayout(self.horizontalLayout_19)
        self.verticalLayout_24.addWidget(self.frame_3)
        self.verticalLayout_25.addLayout(self.verticalLayout_24)

        self.add_function()

    def add_function(self):
        self.pushButton_9.clicked.connect(self.save_table)
        self.save_to_exel_marks_push.clicked.connect(self.save_to_exel_marks)

    def update_statistics_2(self):
        statistics = MANAGER_STUDENTS.get_statistics_marks()
        if statistics.get('is_ready') == 1:
            self.statustic3.setText(
                f'Кол-во студ. им-х 2 = {statistics.get("heaving_2")!r} | Кол-во студ. им-х одну 3 = {statistics.get("heaving_one_3")!r} \t| Успеваемость общая = {str(round(statistics.get("total_academic_performance", 0) * 100, 2))}%')
            self.statustic4.setText(
                f'Кол-во студ. им-х 5 = {statistics.get("heaving_5")!r} | Кол-во студ. им-х 4 и 5 = {statistics.get("heaving_4_and_5")!r}\t| Успеваемость качественная = {round(statistics.get("quality_academic_performance", 0) * 100, 2)!r}%')
        else:
            self.statustic3.clear()
            self.statustic4.clear()

    def save_table(self):
        MANAGER_STUDENTS.save_students()

    def init_table_marks(self, only_show=False):
        if hasattr(self, 'tableWidget_3'):
            self.verticalLayout_25.removeWidget(self.tableWidget_3)

        self.tableWidget_3 = TableMarks(only_show=only_show)
        self.tableWidget_3.setObjectName("tableWidget_3")
        self.verticalLayout_25.addWidget(self.tableWidget_3)
        self.verticalLayout_25.addItem(
            QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum))

        self.set_size_negativ_font_push2.clicked.connect(lambda: self.set_size_font(self.tableWidget_3, False))
        self.set_size_posetiv_font_push2.clicked.connect(lambda: self.set_size_font(self.tableWidget_3))
        self.tableWidget_3.update_table_students()

        if not only_show:
            self.tableWidget_3.cellPressed.connect(self.cellPressed)
            self.tableWidget_3.cellChanged.connect(lambda: self.clicked_table_marks(self.tableWidget_3))

    def clicked_table_marks(self, table_widget):
        item = table_widget.currentItem()
        if not item is None:
            if item.column() == 1:
                if item.row() == len(MANAGER_STUDENTS.students) + 3:
                    try:
                        MANAGER_STUDENTS.CLASS_STUDENT.chech_fio(item.text())
                    except BaseException:
                        print('ошибка')
                    else:
                        try:
                            MANAGER_STUDENTS.add_student(MANAGER_STUDENTS.CLASS_STUDENT(item.text()))
                        except BaseException as f:
                            print(f)
                        else:
                            table_widget.update_table_students()
                            if hasattr(self.parent, 'F6'):
                                self.parent.F6.tableWidget.update_table_students()
                            if hasattr(self.parent, 'students'):
                                self.parent.students.update_list_students()
            elif 32 >= item.column() >= 2 and len(MANAGER_STUDENTS.students) + 2 >= item.row() >= 3:
                if item.text().isnumeric() and 5 >= int(item.text()) >= 2:
                    table_widget.add_mark_table(item.row(), item.column(), item.text())
                else:
                    item.setText('')
                    table_widget.del_mark_table(item.row(), item.column())

            elif item.row() == 1 and item.column() >= 2:
                self.tableWidget_3.add_couples(item.column() - 1, couple=item.text())
            elif item.row() == 2 and item.column() >= 2:
                self.tableWidget_3.add_couples(item.column() - 1, fio=item.text())
        self.update_statistics_2()


    def set_size_font(self, table, is_posetiv=True):
        if is_posetiv and table.mod_size < 25:
            table.update_table_students(size=table.mod_size + 2)
        elif table.mod_size > -8:
            table.update_table_students(size=table.mod_size - 2)

    def save_to_exel_marks(self):
        try:
            path = MANAGER_STUDENTS.save_f6_marks(os.path.join(DOCUMENTS_PATH,
                                                               f'{"_".join(["О", str(MANAGER_STUDENTS.MONTHS[MANAGER_STUDENTS.period[0] - 1]), str(MANAGER_STUDENTS.period[1]), str(USER_MANAGER.user.username)])}.xlsx'))
        except BaseException as f:
            QtWidgets.QMessageBox.critical(self.parent, 'Ошибка сохранения', 'Файл не был сохранен. Повторите попытку')
        else:
            QtWidgets.QMessageBox.information(self.parent, 'Успешное сохранение',
                                              f'Файл успешно сохранен в дириктории: {path}')

    def cellPressed(self, row, column):
        if self.tableWidget_3.hasFocus():
            if 32 >= column >= 2 and row >= 3:
                try:
                    if hasattr(self.tableWidget_3, 'old_item1'):
                        self.tableWidget_3.item(self.tableWidget_3.old_item1[0], 0).setBackground(
                            QtGui.QColor(255, 255, 255))
                        self.tableWidget_3.item(2, self.tableWidget_3.old_item1[1]).setBackground(
                            QtGui.QColor(255, 255, 255))
                        self.tableWidget_3.old_item1 = (row, column)
                        self.tableWidget_3.item(self.tableWidget_3.old_item1[0], 0)
                    else:
                        self.tableWidget_3.old_item1 = (row, column)
                    self.tableWidget_3.item(row, 0).setBackground(QtGui.QColor(102, 102, 102))
                    self.tableWidget_3.item(2, column).setBackground(QtGui.QColor(102, 102, 102))

                except BaseException as f:
                    print(repr(f))


class StudentsTab(QtWidgets.QWidget):
    def __init__(self, parent):
        super(StudentsTab, self).__init__(parent=parent)
        self.parent = parent
        self.setStyleSheet("""
                        #del_push {
                           font-size: 16px;
                           color: black;
                           background-color: red;
                           border: none;
                           padding: 5px;
                           color: white;
                           }
                        #del_push:hover {
                           font: 18px;
                           border: 2px solid #990000;
                           }
                        #save_push {
                           font-size: 16px;
                           color: black;
                           background-color: green;
                           border: none;
                           padding: 5px;
                           color: white;
                           }
                    
                        #save_push:hover {
                           font: 18px;
                           border: 2px solid #009900;
                           }

                        QLineEdit {
                           border: none;
                           color:white;
                           padding-left: 15px;
                           padding-right: 15px;
                           font: 16px;
                           background: black;
                           }
                           """)
        self.setObjectName("students")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setContentsMargins(-1, -1, 0, -1)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.label = QtWidgets.QLabel(self)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.verticalLayout_6.addWidget(self.label)
        self.listWidget = QtWidgets.QListWidget(self)
        self.listWidget.setObjectName("listWidget")
        self.listWidget.setStyleSheet('''#listWidget {margin: auto; border: none;} ''')
        self.verticalLayout_6.addWidget(self.listWidget)
        self.horizontalLayout_6.addLayout(self.verticalLayout_6)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.fio_label = QtWidgets.QLabel(self)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.fio_label.setFont(font)
        self.fio_label.setObjectName("fio_label")
        self.verticalLayout_5.addWidget(self.fio_label)
        self.fio_edit = QtWidgets.QLineEdit(self)
        self.fio_edit.setMinimumSize(QtCore.QSize(0, 30))
        self.fio_edit.setMaximumSize(QtCore.QSize(468, 16777215))
        self.fio_edit.setObjectName("fio_edit")
        self.verticalLayout_5.addWidget(self.fio_edit)
        self.message_students = QtWidgets.QTextBrowser(self)
        self.message_students.setFixedSize(400, 400)
        self.message_students.setStyleSheet(
            'border: none; color: red; font: 14px; background-color: rgba(249, 248, 244, 0);')
        self.verticalLayout_5.addWidget(self.message_students)

        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum,
                                            QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout_5.addItem(spacerItem1)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.del_push = QtWidgets.QPushButton(self)
        self.del_push.setObjectName("del_push")
        self.horizontalLayout_5.addWidget(self.del_push)
        self.save_push = QtWidgets.QPushButton(self)
        self.save_push.setObjectName("save_push")
        self.horizontalLayout_5.addWidget(self.save_push)
        self.verticalLayout_5.addLayout(self.horizontalLayout_5)
        self.verticalLayout_4.addLayout(self.verticalLayout_5)
        self.horizontalLayout_6.addLayout(self.verticalLayout_4)

        self.add_function()
        self.retranslateUi()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.fio_label.setText(_translate("MainWindow", "ФИО"))
        self.del_push.setText(_translate("MainWindow", "Удалить"))
        self.save_push.setText(_translate("MainWindow", "Сохранить"))
        self.label.setText(_translate("MainWindow", "Список студентов"))

    def add_function(self):
        self.save_push.clicked.connect(self.save_student)
        self.del_push.clicked.connect(self.del_student)

        self.listWidget.itemClicked.connect(lambda: self.click_list(self.listWidget))

    def update_list_students(self):
        self.listWidget.clear()
        for indx, student in enumerate(MANAGER_STUDENTS.students):
            self.listWidget.addItem(QtWidgets.QListWidgetItem(f'{str(indx + 1)}. {student.fio}'))

    def save_student(self):
        self.message_students.setText('')
        if self.listWidget.currentItem():
            try:
                MANAGER_STUDENTS.CLASS_STUDENT.chech_fio(self.fio_edit.text())
            except BaseException as f:
                self.message_students.setText(str(f))
            else:
                MANAGER_STUDENTS.students[
                    self.listWidget.row(self.listWidget.currentItem())].fio = self.fio_edit.text()
                self.update_list_students()
                if hasattr(self.parent, 'marks'):
                    self.parent.marks.tableWidget_3.update_table_students()
                if hasattr(self.parent, 'F6'):
                    self.parent.F6.tableWidget.update_table_students()

    def del_student(self):
        if self.listWidget.currentItem():
            message_main = QtWidgets.QMessageBox().question(self, "Удаление студента",
                                                            str(f'Вы точно хотите навсегда удалить студента {" ".join(self.listWidget.currentItem().text().split()[1:])}?'),
                                                            QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
            if message_main == message_main.Yes:
                MANAGER_STUDENTS.remove_student_id(self.listWidget.row(self.listWidget.currentItem()))
                if hasattr(self.parent, 'marks'):
                    self.parent.marks.tableWidget_3.update_table_students()
                if hasattr(self.parent, 'F6'):
                    self.parent.F6.tableWidget.update_table_students()
                self.listWidget.removeItemWidget(self.listWidget.currentItem())
                self.update_list_students()
                USER_MANAGER.save_users()

        if len(MANAGER_STUDENTS.students) == 0:
            self.parent.group.removeTab(self.parent.group.indexOf(self))
            self.update_list_students()

    def click_list(self, listwidget):
        self.fio_edit.setText(' '.join(listwidget.currentItem().text().split()[1:]))


class ArchiveTab(QtWidgets.QWidget):
    def __init__(self, parent):
        super(ArchiveTab, self).__init__(parent=parent)
        self.parent = parent
        self.setObjectName("archive")
        self.setStyleSheet("""
                                #del_file_push {
                                   font-size: 16px;
                                   color: black;
                                   background-color: red;
                                   border: none;
                                   padding: 5px;
                                   color: white;
                                   }
                                #del_file_push:hover {
                                   font: 18px;
                                   border: 2px solid #990000;
                                   }
                                #load_file_push {
                                   font-size: 16px;
                                   color: black;
                                   background-color: green;
                                   border: none;
                                   padding: 5px;
                                   color: white;
                                   }

                                #load_file_push:hover {
                                   font: 18px;
                                   border: 2px solid #009900;
                                   }
                                   """)
        self.verticalLayout_11 = QtWidgets.QVBoxLayout(self)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.label_4 = QtWidgets.QLabel(self)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_11.addWidget(self.label_4)
        self.list_archive = QtWidgets.QListWidget(self)
        self.list_archive.setObjectName("list_archive")
        self.verticalLayout_11.addWidget(self.list_archive)
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setContentsMargins(-1, 10, 0, -1)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        # spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding,
        #                                     QtWidgets.QSizePolicy.Policy.Minimum)
        # self.horizontalLayout_9.addItem(spacerItem3)
        self.del_file_push = QtWidgets.QPushButton(self)
        self.del_file_push.setObjectName("del_file_push")
        self.horizontalLayout_9.addWidget(self.del_file_push)
        self.load_file_push = QtWidgets.QPushButton(self)
        self.load_file_push.setObjectName("load_file_push")
        self.horizontalLayout_9.addWidget(self.load_file_push)
        self.verticalLayout_11.addLayout(self.horizontalLayout_9)
        self.logout_archive_push = Push(self.parent.F6.frame, 40, 40, 5, tool_tip='Выйти из архива',
                                        icon_path=os.path.join('media', 'undo.svg'))
        self.logout_archive_push.hide()
        self.logout_archive_push.setObjectName("logout_archive_push")

        self.parent.F6.horizontalLayout_2.addWidget(self.logout_archive_push)
        self.add_function()
        self.retranslateUi()

        self.is_comebake = 0
        self.is_delite_file = 0

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.label_4.setText(_translate("MainWindow", "Доступные файлы"))
        self.del_file_push.setText(_translate("MainWindow", "Удалить"))
        self.load_file_push.setText(_translate("MainWindow", "Активировать"))

    def add_function(self):
        self.del_file_push.clicked.connect(self.clicked_del_file_push)
        self.load_file_push.clicked.connect(self.clicked_load_file_push)

        self.logout_archive_push.clicked.connect(self.logout_archive)

    def init_archive(self):
        path, files = MANAGER_STUDENTS.init_archive()
        self.list_archive.clear()
        for i in files:
            self.list_archive.addItem(QtWidgets.QListWidgetItem(i))
        self.path_archive = path
        self.files_archive = files

    def clicked_load_file_push(self):
        item = self.list_archive.currentItem()
        if item:
            try:
                self.parent.init_students_manager(path=os.path.join('archive', item.text()), only_show=True)
            except BaseException as f:
                QtWidgets.QMessageBox.critical(self, 'Просмотр архивного файла',
                                               f'При попытки  загрузки файла {item.text()} произошла ошибка. Попробуйте загрузить его заного. Если проблема не исчезнет, то скорее всего файл поврежден или удален.',
                                               QtWidgets.QMessageBox.StandardButton.Ok)

            else:
                self.logout_archive_push.show()

                self.parent.F6.save_table_push.hide()
                self.parent.F6.game_over_push.hide()
                self.parent.F6.radioButton_2.hide()
                self.parent.marks.pushButton_9.hide()
                self.parent.F6.is_sick_rb.hide()

                self.parent.group.removeTab(self.parent.group.indexOf(self.parent.students))
                self.parent.group.removeTab(self.parent.group.indexOf(self.parent.settings))

                QtWidgets.QMessageBox.information(self, 'Просмотр архивного файла',
                                                  'Файла успешно загружен. Вы можете перейти к просмотру.',
                                                  QtWidgets.QMessageBox.StandardButton.Ok)

    def clicked_del_file_push(self):
        item = self.list_archive.currentItem()
        if item:
            self.del_file_archive(item.text())
            self.is_delite_file = 1
            self.parent.profile.cod = [2, 4]

    def del_file_archive(self, file_name):
        if file_name in self.files_archive:
            message = QtWidgets.QMessageBox.question(self.parent, 'Удаление архивного файла',
                                                     f'Вы точно хотите удалить файл: {file_name}? \n После этого он будет удален навсегда',
                                                     QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
            if message == message.Yes:
                try:
                    os.remove(os.path.join(self.path_archive, file_name))
                except BaseException:
                    pass
                finally:
                    self.init_archive()

    def logout_archive(self):
        self.is_comebake = 1
        self.parent.profile.cod = [3, 1]
        self.parent.init_students_manager(path='students.json')
        self.logout_archive_push.hide()

        self.parent.F6.save_table_push.show()
        self.parent.F6.game_over_push.show()
        self.parent.marks.pushButton_9.show()
        self.parent.F6.radioButton_2.show()
        self.parent.F6.is_sick_rb.show()

        self.parent.group.insertTab(2, self.parent.students, 'Cтуденты')
        self.parent.group.insertTab(4, self.parent.settings, 'Настройки')


class SettingsTab(QtWidgets.QWidget):
    def __init__(self, parent):
        super(SettingsTab, self).__init__(parent=parent)
        self.parent = parent
        QtWidgets.QWidget()
        self.setObjectName("settings")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(self)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.scrollArea = QtWidgets.QScrollArea(self)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 950, 712))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_9.setObjectName("verticalLayout_9")

        self.setings1_label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(QtGui.QFont.Weight(50))
        self.setings1_label.setFont(font)
        self.setings1_label.setObjectName("setings1_label")
        self.verticalLayout_9.addWidget(self.setings1_label)
        self.add_work_day_link_button = QtWidgets.QCommandLinkButton(self.scrollAreaWidgetContents)
        self.add_work_day_link_button.setTabletTracking(True)
        self.add_work_day_link_button.setObjectName("add_work_day_link_button")
        self.verticalLayout_9.addWidget(self.add_work_day_link_button)
        self.del_work_day_link_button = QtWidgets.QCommandLinkButton(self.scrollAreaWidgetContents)
        self.del_work_day_link_button.setCheckable(False)
        self.del_work_day_link_button.setObjectName("del_work_day_link_button")
        self.verticalLayout_9.addWidget(self.del_work_day_link_button)

        line = QtWidgets.QFrame(self.scrollAreaWidgetContents)
        line.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        line.setObjectName("line")
        self.verticalLayout_9.addWidget(line)
        # self.line_2 = QtWidgets.QFrame(self.scrollAreaWidgetContents)
        # self.line_2.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        # self.line_2.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        # self.line_2.setObjectName("line_2")
        # self.verticalLayout_9.addWidget(self.line_2)
        #
        # self.table_label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        # font = QtGui.QFont()
        # font.setPointSize(14)
        # font.setBold(False)
        # font.setItalic(False)
        # font.setUnderline(False)
        # font.setWeight(QtGui.QFont.Weight(50))
        # self.table_label.setFont(font)
        # self.table_label.setObjectName("setings2_label")
        # self.verticalLayout_9.addWidget(self.table_label)
        # self.create_table_marks_link_button = QtWidgets.QCommandLinkButton(self.scrollAreaWidgetContents)
        # self.create_table_marks_link_button.setTabletTracking(True)
        # self.create_table_marks_link_button.setObjectName("create_table_marks_link_button")
        # self.verticalLayout_9.addWidget(self.create_table_marks_link_button)
        # self.del_table_marks_link_button = QtWidgets.QCommandLinkButton(self.scrollAreaWidgetContents)
        # self.del_table_marks_link_button.setCheckable(False)
        # self.del_table_marks_link_button.setObjectName("del_table_marks_link_button")
        # self.verticalLayout_9.addWidget(self.del_table_marks_link_button)
        #
        # self.setings2_label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        # font = QtGui.QFont()
        # font.setPointSize(14)
        # font.setBold(False)
        # font.setItalic(False)
        # font.setUnderline(False)
        # font.setWeight(QtGui.QFont.Weight(50))
        # self.setings2_label.setFont(font)
        # self.setings2_label.setObjectName("setings2_label")
        # self.verticalLayout_9.addWidget(self.setings2_label)
        # self.set_path_save_bd_link_button = QtWidgets.QCommandLinkButton(self.scrollAreaWidgetContents)
        # self.set_path_save_bd_link_button.setTabletTracking(True)
        # self.set_path_save_bd_link_button.setObjectName("set_path_save_bd_link_button")
        # self.verticalLayout_9.addWidget(self.set_path_save_bd_link_button)
        # self.set_path_save_exel_link_button = QtWidgets.QCommandLinkButton(self.scrollAreaWidgetContents)
        # self.set_path_save_exel_link_button.setCheckable(False)
        # self.set_path_save_exel_link_button.setObjectName("set_path_save_exel_link_button")
        # self.verticalLayout_9.addWidget(self.set_path_save_exel_link_button)

        self.on_off_table_marks_label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(QtGui.QFont.Weight(50))
        self.on_off_table_marks_label.setFont(font)
        self.on_off_table_marks_label.setObjectName("on_off_table_marks_label")
        self.verticalLayout_9.addWidget(self.on_off_table_marks_label)
        self.on_off_table_marks_link_button = QtWidgets.QCommandLinkButton(self.scrollAreaWidgetContents)
        self.on_off_table_marks_link_button.setTabletTracking(True)
        self.on_off_table_marks_link_button.setObjectName("on_off_table_marks_link_button")
        self.verticalLayout_9.addWidget(self.on_off_table_marks_link_button)




        line = QtWidgets.QFrame(self.scrollAreaWidgetContents)
        line.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        line.setObjectName("line")
        self.verticalLayout_9.addWidget(line)
        self.clear_table_label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(QtGui.QFont.Weight(50))
        self.clear_table_label.setFont(font)
        self.clear_table_label.setObjectName("clear_table_label")
        self.verticalLayout_9.addWidget(self.clear_table_label)
        self.clear_table_abcense_link_button = QtWidgets.QCommandLinkButton(self.scrollAreaWidgetContents)
        self.clear_table_abcense_link_button.setCheckable(False)
        self.clear_table_abcense_link_button.setObjectName("clear_table_abcense_link_button")
        self.verticalLayout_9.addWidget(self.clear_table_abcense_link_button)
        self.clear_table_marks_link_button = QtWidgets.QCommandLinkButton(self.scrollAreaWidgetContents)
        self.clear_table_marks_link_button.setTabletTracking(True)
        self.clear_table_marks_link_button.setObjectName("clear_table_marks_link_button")
        self.verticalLayout_9.addWidget(self.clear_table_marks_link_button)


        line = QtWidgets.QFrame(self.scrollAreaWidgetContents)
        line.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        line.setObjectName("line")
        self.verticalLayout_9.addWidget(line)


        self.set_data_table_link_button = QtWidgets.QCommandLinkButton(self.scrollAreaWidgetContents)
        self.set_data_table_link_button.setCheckable(False)
        self.set_data_table_link_button.setObjectName("set_data_table_link_button")
        self.verticalLayout_9.addWidget(self.set_data_table_link_button)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum,
                                            QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout_9.addItem(spacerItem2)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout_10.addWidget(self.scrollArea)

        self.add_function()
        self.retranslateUi()

        self.is_add_work_day = 0
        self.is_del_work_day = 0

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setings1_label.setText(_translate("MainWindow", "Рабочие/нерабочие дни"))
        self.add_work_day_link_button.setText(_translate("MainWindow", "Добавить рабочий день"))
        self.set_data_table_link_button.setText(_translate("MainWindow", "Изменить месяц и год"))
        self.del_work_day_link_button.setText(_translate("MainWindow", "Удалить рабочий день"))
        # self.setings2_label.setText(_translate("MainWindow", "Пути сохранения"))
        # self.set_path_save_bd_link_button.setText(_translate("MainWindow", "Изменить путь сохранения базы данных"))
        # self.set_path_save_exel_link_button.setText(
            # _translate("MainWindow", "Изменить путь сохранения файлов exel"))
        # self.table_label.setText(_translate("MainWindow", "Таблицы"))
        # self.create_table_marks_link_button.setText(_translate("MainWindow", "Создать таблицу для оценок"))
        # self.del_table_marks_link_button.setText(_translate("MainWindow", "Удалить таблицу для оценок"))

        self.clear_table_label.setText('Отчистка таблицы')
        self.clear_table_marks_link_button.setText('Отчистить таблицу оценок')
        self.clear_table_abcense_link_button.setText('Отчистить таблицу прогулов')
        self.on_off_table_marks_label.setText('Таблицу оценок')
        self.on_off_table_marks_link_button.setText('Включить/выключить таблицу оценок')

    def add_function(self):
        self.add_work_day_link_button.clicked.connect(self.add_work_day)
        self.del_work_day_link_button.clicked.connect(self.del_work_day)
        self.set_data_table_link_button.clicked.connect(self.set_data_table)
        # self.create_table_marks_link_button.clicked.connect(self.create_table_marks)

        self.clear_table_marks_link_button.clicked.connect(self.clear_table_marks)
        self.clear_table_abcense_link_button.clicked.connect(self.clear_table_abcense)
        self.on_off_table_marks_link_button.clicked.connect(self.on_off_table)

    def add_work_day(self):
        deal = SettingsWindows(self)
        deal.show()
        deal.exec()
        if not (deal.result is None):
            MANAGER_STUDENTS.on_day(deal.result)
            self.parent.F6.tableWidget.update_table_students()
            self.parent.F6.update_statistics()
            self.is_add_work_day = 1
        self.parent.profile.cod = [1, 0]

    def del_work_day(self):
        deal = SettingsWindows(self)
        deal.show()
        deal.exec()
        if not (deal.result is None):
            MANAGER_STUDENTS.off_day(deal.result)
            self.parent.F6.tableWidget.update_table_students()
            self.parent.F6.update_statistics()
            self.is_del_work_day = 1
        self.parent.profile.cod = [1, 1]

    def set_data_table(self):
        try:
            s = SettingsData(self)
            s.show()
            s.exec()
        except BaseException as f:
            print(repr(f))
        else:
            self.parent.init_students_manager(period=tuple(map(lambda x: int(x), s.dateEdit.text().split('.'))))


    def del_table_marks(self):
        MANAGER_STUDENTS.clear_marks()

    def clear_table_marks(self):
        message = QtWidgets.QMessageBox.question(self, 'Отчиста таблицы оценок', 'Вы точно хотите отчистить таблицу оценок?', QtWidgets.QMessageBox.StandardButton.Yes, QtWidgets.QMessageBox.StandardButton.No)
        if message == QtWidgets.QMessageBox.StandardButton.Yes:
            MANAGER_STUDENTS.clear_marks()
            MANAGER_STUDENTS.save_students()
            if hasattr(self.parent, 'marks'):
                self.parent.marks.tableWidget_3.update_table_students()


    def clear_table_abcense(self):
        message = QtWidgets.QMessageBox.question(self, 'Отчиста таблицы прогулов',
                                                 'Вы точно хотите отчистить таблицу прогулов?',
                                                 QtWidgets.QMessageBox.StandardButton.Yes,
                                                 QtWidgets.QMessageBox.StandardButton.No)
        if message == QtWidgets.QMessageBox.StandardButton.Yes:
            MANAGER_STUDENTS.clear_absences()
            MANAGER_STUDENTS.save_students()
            if hasattr(self.parent, 'F6'):
                self.parent.F6.tableWidget.update_table_students()


    def on_off_table(self):
        if self.parent.group.indexOf(self.parent.marks) != -1:
            self.parent.group.removeTab(self.parent.group.indexOf(self.parent.marks))
            USER_MANAGER.user.parametrs['table_marks'] = False
        else:
            self.parent.group.insertTab(1, self.parent.marks, 'Оценки')
            USER_MANAGER.user.parametrs['table_marks'] = True
        USER_MANAGER.user.save_user()



class ProfileTab(QtWidgets.QWidget):
    ACHIEVEMENT = {
        (0, 0): ('Поехали!', os.path.join('media', 'achievements', '10.svg')),
        (0, 1): ('Fullstack', os.path.join('media', 'achievements', '1.svg')),
        (0, 2): ('Игра окончена', os.path.join('media', 'achievements', '2.svg')),
        (0, 3): ('Шерлок?', os.path.join('media', 'achievements', '4.svg')),
        (0, 4): ('Исследователь', os.path.join('media', 'achievements', '5.svg')),
        (1, 0): ('Делу время....', os.path.join('media', 'achievements', '7.svg')),
        (1, 1): ('..потехе час', os.path.join('media', 'achievements', '8.svg')),
        (1, 2): ('Частичка истории', os.path.join('media', 'achievements', '14.svg')),
        (1, 3): ('Это что? Микробы!', os.path.join('media', 'achievements', '12.svg')),
        (1, 4): ('Я видел темную сторону Луны', os.path.join('media', 'achievements', '13.svg')),
        (2, 0): ('Моя прелесть', os.path.join('media', 'achievements', '16.svg')),
        (2, 1): ('Сова', os.path.join('media', 'achievements', '17.svg')),
        (2, 2): ('Классику сер?', os.path.join('media', 'achievements', '15.svg')),
        (2, 3): ('Трансформация', os.path.join('media', 'achievements', '3.svg')),
        (2, 4): ('Быть или не быть', os.path.join('media', 'achievements', '9.svg')),
        (3, 0): ('Ушел по-английски', os.path.join('media', 'achievements', '11.svg')),
        (3, 1): ('Назад в будущее', os.path.join('media', 'achievements', '18.svg')),
        (3, 2): ('Коллекционер', os.path.join('media', 'achievements', '6.svg')),
        (3, 3): ('С НГ!', os.path.join('media', 'achievements', '19.svg')),
        (3, 4): ('Звезда', os.path.join('media', 'achievements', '20.svg')),
    }


    def __init__(self, parent):
        super(ProfileTab, self).__init__(parent=parent)
        self.setStyleSheet("""
                                QLineEdit, #username_edit{
                                   border: none;
                                   color:white;
                                   font: 16px;
                                   padding-left: 15px;
                                   background: black;
                                  
                                   }
                                   """)
        self.parent = parent
        self.setObjectName("profile")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout(self)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout()
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.accaunt_label = QtWidgets.QLabel(self)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.accaunt_label.setFont(font)
        self.accaunt_label.setObjectName("accaunt_label")
        self.verticalLayout_8.addWidget(self.accaunt_label)
        self.username_label = QtWidgets.QLabel(self)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.username_label.setFont(font)
        self.username_label.setObjectName("username_label")
        self.verticalLayout_8.addWidget(self.username_label)
        self.username_edit = QtWidgets.QLabel(self)
        self.username_edit.setFont(font)
        self.username_edit.setMinimumSize(QtCore.QSize(0, 30))
        self.username_edit.setMaximumSize(QtCore.QSize(400, 16777215))
        self.username_edit.setObjectName("username_edit")
        self.verticalLayout_8.addWidget(self.username_edit)
        self.fio_user_label = QtWidgets.QLabel(self)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.fio_user_label.setFont(font)
        self.fio_user_label.setObjectName("fio_user_label")
        self.verticalLayout_8.addWidget(self.fio_user_label)
        self.fio_user_edit = QtWidgets.QLineEdit(self)
        self.fio_user_edit.setMinimumSize(QtCore.QSize(0, 30))
        self.fio_user_edit.setMaximumSize(QtCore.QSize(400, 16777215))
        self.fio_user_edit.setObjectName("fio_user_edit")
        self.verticalLayout_8.addWidget(self.fio_user_edit)
        self.teamleader_label = QtWidgets.QLabel(self)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.teamleader_label.setFont(font)
        self.teamleader_label.setObjectName("teamleader_label")
        self.verticalLayout_8.addWidget(self.teamleader_label)
        self.fio_teamleader_edit = QtWidgets.QLineEdit(self)
        self.fio_teamleader_edit.setMinimumSize(QtCore.QSize(0, 30))
        self.fio_teamleader_edit.setMaximumSize(QtCore.QSize(400, 16777215))
        self.fio_teamleader_edit.setObjectName("fio_teamleader_edit")
        self.verticalLayout_8.addWidget(self.fio_teamleader_edit)
        self.group_label = QtWidgets.QLabel(self)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.group_label.setFont(font)
        self.group_label.setObjectName("group_label")
        self.verticalLayout_8.addWidget(self.group_label)
        self.group_edit = QtWidgets.QLineEdit(self)
        self.group_edit.setMinimumSize(QtCore.QSize(0, 30))
        self.group_edit.setMaximumSize(QtCore.QSize(400, 16777215))
        self.group_edit.setObjectName("group_edit")
        self.verticalLayout_8.addWidget(self.group_edit)
        self.specialization_label = QtWidgets.QLabel(self)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.specialization_label.setFont(font)
        self.specialization_label.setObjectName("specialization_label")
        self.verticalLayout_8.addWidget(self.specialization_label)
        self.specialization_edit = QtWidgets.QLineEdit(self)
        self.specialization_edit.setMinimumSize(QtCore.QSize(0, 30))
        self.specialization_edit.setMaximumSize(QtCore.QSize(400, 16777215))
        self.specialization_edit.setObjectName("specialization_edit")
        self.verticalLayout_8.addWidget(self.specialization_edit)
        self.message_profile = QtWidgets.QTextBrowser(self)
        self.message_profile.setFixedSize(400, 400)
        self.message_profile.setStyleSheet(
            'border: none; color: red; font: 14px; background-color: rgba(249, 248, 244, 0);')
        self.verticalLayout_8.addWidget(self.message_profile)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum,
                                            QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout_8.addItem(spacerItem2)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.save_user_push = Push(self, 35, 35, 5, tool_tip='Сохронить изменения',
                                   icon_path=os.path.join('media', 'buttons', 'save.svg'))
        self.save_user_push.setObjectName("save_user_push")
        self.horizontalLayout_7.addWidget(self.save_user_push)
        self.set_password_push = Push(self, 35, 35, 5, tool_tip='Изменить пароль',
                                      icon_path=os.path.join('media', 'buttons', 'set_password.svg'))
        self.set_password_push.setObjectName("set_password_push")
        self.horizontalLayout_7.addWidget(self.set_password_push)
        self.del_user_push = Push(self, 35, 35, 5, tool_tip='Удалить пользователя',
                                  icon_path=os.path.join('media', 'buttons', 'del_user.svg'))
        self.del_user_push.setObjectName("del_user_push")
        self.horizontalLayout_7.addWidget(self.del_user_push)
        self.logout_push = Push(self, 35, 35, 5, tool_tip='Выйти из аккаунта',
                                icon_path=os.path.join('media', 'buttons', 'logout.svg'))
        self.logout_push.setObjectName("logout_push")
        self.horizontalLayout_7.addWidget(self.logout_push)
        self.verticalLayout_8.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_8.addLayout(self.verticalLayout_8)
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.verticalLayout_12 = QtWidgets.QVBoxLayout()
        self.verticalLayout_12.setObjectName("verticalLayout_12")
        self.photo = QtSvgWidgets.QSvgWidget(os.path.join('media', 'profile', f'{str(random.randint(1, 15))}.svg'))
        self.photo.setFixedSize(QtCore.QSize(250, 250))
        self.photo.setObjectName("photo")


        self.verticalLayout_12.addItem(
                    QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding))
        self.verticalLayout_12.addWidget(self.photo, QtCore.Qt.AlignmentFlag.AlignVCenter, QtCore.Qt.AlignmentFlag.AlignHCenter)

        self.verticalLayout_12.addItem(
            QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding))
        self.verticalLayout_7.addLayout(self.verticalLayout_12)

        self.verticalLayout_13 = QtWidgets.QVBoxLayout()
        self.verticalLayout_13.setObjectName("verticalLayout_13")

        self.verticalLayout_7.addLayout(self.verticalLayout_13)
        self.horizontalLayout_8.addLayout(self.verticalLayout_7)

        self.setObjectName("profile")

        self.add_function()
        self.retranslateUi()

        self.is_exit = 0
        self.is_clicked = 0


    def add_function(self):
        self.save_user_push.clicked.connect(self.save_user)
        self.set_password_push.clicked.connect(self.set_password)
        self.del_user_push.clicked.connect(self.del_user)
        self.logout_push.clicked.connect(self.logout)
        self.photo.mousePressEvent = self.click_profile

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.accaunt_label.setText(_translate("MainWindow", "Аккаунт"))
        self.username_label.setText(_translate("MainWindow", "Имя пользователя"))
        self.fio_user_label.setText(_translate("MainWindow", "ФИО Своё"))
        self.teamleader_label.setText(_translate("MainWindow", "ФИО Кл.руководителя"))
        self.group_label.setText(_translate('MainWindow', "Группа"))
        self.specialization_label.setText(_translate('MainWindow', "Специальность"))

    def click_profile(self, *args, **kwargs):
        photo = QtSvgWidgets.QSvgWidget(os.path.join('media', 'profile', f'{str(random.randint(1, 15))}.svg'))
        photo.setFixedSize(QtCore.QSize(250, 250))
        self.verticalLayout_12.replaceWidget(self.photo, photo)
        self.photo.deleteLater()
        self.photo = photo
        self.photo.mousePressEvent = self.click_profile
        if not self.is_clicked:
            self.cod = [2, 3]
            self.is_clicked = 1


    def init_atchivments(self):
        if hasattr(self, 'atchivmenys_layout'):
            self.verticalLayout_13 = QtWidgets.QHBoxLayout()
        if not USER_MANAGER.user.parametrs.get('achievements'):
            achievements = []
        else:
            achievements = USER_MANAGER.user.parametrs.get('achievements')

        for i in range(4):

            self.atchivmenys_layout = QtWidgets.QHBoxLayout()
            for j in range(5):
                if [i, j] in achievements:
                    qlable = QtSvgWidgets.QSvgWidget(self.ACHIEVEMENT[(i, j)][1])
                    qlable.setToolTip(str(self.ACHIEVEMENT[(i, j)][0]))
                    qlable.setFixedSize(QtCore.QSize(80, 80))
                else:
                    qlable = QtSvgWidgets.QSvgWidget(os.path.join('media', 'achievements', '0.svg'))
                    # qlable.setToolTip(str(self.ACHIEVEMENT[(i, j)][0]))
                    qlable.setFixedSize(QtCore.QSize(80, 80))
                self.atchivmenys_layout.addWidget(qlable)
            self.verticalLayout_13.addLayout(self.atchivmenys_layout)

    def __setattr__(self, key, value):
        if key == 'cod':
            if self.checking_condition(tuple(value)):
                user_atch = USER_MANAGER.user.parametrs.get('achievements')

                if user_atch:
                    USER_MANAGER.user.parametrs['achievements'].append(list(value))
                else:
                    USER_MANAGER.user.parametrs['achievements'] = [list(value)]

                USER_MANAGER.user.save_user()

        else:
            super().__setattr__(key, value)

    def save_user(self):
        try:
            if self.fio_user_edit.text():
                USER_MANAGER.user.parametrs['offical_name'] = USER_MANAGER.USER_CLASS.check_fio(
                    self.fio_user_edit.text()).title()
                self.fio_user_edit.setText(USER_MANAGER.user.parametrs.get('offical_name'))
            if self.fio_teamleader_edit.text():
                USER_MANAGER.user.parametrs['teamleader'] = USER_MANAGER.USER_CLASS.check_fio(
                    self.fio_teamleader_edit.text()).title()
                self.fio_teamleader_edit.setText(USER_MANAGER.user.parametrs.get('teamleader'))
            USER_MANAGER.user.parametrs['group'] = self.group_edit.text()
            USER_MANAGER.user.parametrs['specialization'] = self.specialization_edit.text()
            if USER_MANAGER.user.parametrs['specialization'].lower() == 'великий сыщик':
                self.cod = [0, 3]



        except BaseException as f:
            self.message_profile.setText(str(f))
        else:
            self.message_profile.setText('')
            USER_MANAGER.user.save_user()

    def del_user(self):
        message = QtWidgets.QMessageBox.question(self.parent, 'Удаление пользователя',
                                                 "Вы точно хотите удалить свой аккаунт?",
                                                 QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
        if message == message.Yes:
            USER_MANAGER.del_user()
            self.parent.status = 2
            self.parent.close()

    def logout(self):
        self.is_exit = 1
        self.cod = [3, 0]
        USER_MANAGER.user = None
        self.parent.status = 4
        self.parent.close()

    def set_password(self):
        window_password = WindowSetPassword(self.parent)
        window_password.show()

    def update_user_info(self):
        if not USER_MANAGER.user is None:
            self.username_edit.setText(USER_MANAGER.user.username)
            self.fio_teamleader_edit.setText(USER_MANAGER.user.parametrs.get('teamleader', ''))
            self.fio_user_edit.setText(USER_MANAGER.user.parametrs.get('offical_name', ''))
            self.group_edit.setText(USER_MANAGER.user.parametrs.get('group', ''))
            self.specialization_edit.setText(USER_MANAGER.user.parametrs.get('specialization', ''))

    def checking_condition(self, key):
        CONDITION = {
            (0, 0): 'True',
            (0, 1): 'len(MANAGER_STUDENTS.students) >= 25',
            (0, 2): 'self.parent.F6.is_click_end_period',
            (3, 2): 'len(self.parent.archive.files_archive) >= 12',
            (1, 0): 'self.parent.settings.is_add_work_day',
            (1, 1): 'self.parent.settings.is_del_work_day',
            (3, 0): 'self.is_exit',
            (1, 2): 'MANAGER_STUDENTS.period[1] == 1961',
            (1, 3): 'True',
            (1, 4): 'True',
            (3, 3): 'MANAGER_STUDENTS.period[0] == 12',
            (3, 1): 'self.parent.archive.is_comebake',
            (2, 1): 'datetime.datetime.today().time().hour >= 21',
            (2, 2): 'True',
            (2, 0): 'is_click_license',
            (2, 3): 'True',
            (2, 4): 'self.parent.archive.is_delite_file',
            (0, 4): 'len(self.parent.tab_set) >= 5',
            (0, 3): 'True',
            (3, 4): 'len(USER_MANAGER.user.parametrs.get("achievements")) >= 19',



        }
        if CONDITION.get(tuple(key)):
            if USER_MANAGER.user.parametrs:
                if not list(key) in USER_MANAGER.user.parametrs.get('achievements'):
                    return eval(CONDITION[tuple(key)])


class StatisticTab(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(StatisticTab, self).__init__(parent=parent)
        self.parent = parent
        self.setObjectName(u"tab_2")
        self.verticalLayout_14 = QtWidgets.QVBoxLayout(self)
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")

        self.button_before = QtWidgets.QPushButton()
        self.button_before.setText('Создать статистику')
        self.button_before.clicked.connect(self.clicked_before)
        self.verticalLayout_14.addWidget(self.button_before)





    def init_statistic(self):
        self.scrollArea_2 = QtWidgets.QScrollArea(self)
        self.scrollArea_2.setObjectName(u"scrollArea_2")
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setObjectName(u"scrollAreaWidgetContents_2")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout(self.scrollAreaWidgetContents_2)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")

        self.verticalLayout_16 = QtWidgets.QVBoxLayout()
        self.verticalLayout_16.setObjectName(u"verticalLayout_16")
        self.grafic_group = Grafics(self.scrollAreaWidgetContents_2)
        self.verticalLayout_16.addWidget(self.grafic_group)

        self.horizontalLayout_10.addLayout(self.verticalLayout_16)
        self.verticalLayout_17 = QtWidgets.QVBoxLayout()
        self.verticalLayout_17.setObjectName(u"verticalLayout_17")
        self.grafic_period = Grafics(self.scrollAreaWidgetContents_2)
        self.verticalLayout_17.addWidget(self.grafic_period)

        self.horizontalLayout_10.addLayout(self.verticalLayout_17)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum,
                                            QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout_17.addItem(spacerItem2)
        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_2)
        self.verticalLayout_14.addWidget(self.scrollArea_2)
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.horizontalLayout_11.setContentsMargins(-1, 4, -1, -1)
        self.update_statistic_push_button = QtWidgets.QPushButton(self)
        self.update_statistic_push_button.setObjectName(u"update_statistic_push_button")
        self.horizontalLayout_11.addWidget(self.update_statistic_push_button)
        self.pushButton_7 = QtWidgets.QPushButton(self)
        self.pushButton_7.setObjectName(u"pushButton_7")
        self.horizontalLayout_11.addWidget(self.pushButton_7)
        self.pushButton_6 = QtWidgets.QPushButton(self)
        self.pushButton_6.setObjectName(u"pushButton_6")
        self.horizontalLayout_11.addWidget(self.pushButton_6)
        self.pushButton_5 = QtWidgets.QPushButton(self)
        self.pushButton_5.setObjectName(u"pushButton_5")
        self.horizontalLayout_11.addWidget(self.pushButton_5)
        self.verticalLayout_14.addLayout(self.horizontalLayout_11)
        self.add_function()

        self.retranslateUi()

    def retranslateUi(self):
        self.update_statistic_push_button.setText('Обновить статистику')


    def add_function(self):
        self.update_statistic_push_button.clicked.connect(self.update_statistic)

    def clicked_before(self):
        self.init_statistic()
        self.update_statistic()
        self.button_before.hide()



    def update_statistic(self):
        self.draw_circle_graph()
        self.draw_graph()

    def draw_circle_graph(self):
        self.__add_legend(*self.grafic_group.draw_circle_graph())

    def draw_graph(self):
        self.__add_legend2(*self.grafic_period.draw_graph())

    def __add_legend(self, *args):
        if hasattr(self, 'table_layout'):
            self.verticalLayout_16.removeWidget(self.table_layout)
            self.table_layout.hide()

        self.table_layout = QtWidgets.QTableWidget()


        self.table_layout.setRowCount(len(args[0]))
        self.table_layout.setColumnCount(2)
        fios, fractions = map(lambda x: list(x), args)

        for row in range(len(args[0])):
            self.table_layout.setItem(row, 0, QTableWidgetItem(fios[row]))
            self.table_layout.setItem(row, 1, QTableWidgetItem(str(round(fractions[row]*100, 2))+'%'))

        self.table_layout.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.verticalLayout_16.addWidget(self.table_layout)

    def __add_legend2(self, *args):
        if hasattr(self, 'table_layout2'):
            self.verticalLayout_17.removeWidget(self.table_layout2)
            self.table_layout2.hide()

        self.table_layout2 = QtWidgets.QTableWidget()


        self.table_layout2.setRowCount(len(args[0]))
        self.table_layout2.setColumnCount(4)
        month, sike_days, abcense_days, all_days = map(lambda x: list(x), args)
        for row in range(len(args[0])):
            self.table_layout2.setItem(row, 0, QTableWidgetItem(str(month[row])))
            self.table_layout2.setItem(row, 1, QTableWidgetItem(str(sike_days[row])))
            self.table_layout2.setItem(row, 2, QTableWidgetItem(str(abcense_days[row])))
            self.table_layout2.setItem(row, 3, QTableWidgetItem(str(all_days[row])))


        self.table_layout2.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.verticalLayout_17.addWidget(self.table_layout2)



class Grafics(QtWidgets.QWidget):
    STYLE = ['Solarize_Light2', '_classic_test_patch', '_mpl-gallery', '_mpl-gallery-nogrid', 'bmh', 'classic',
             'dark_background', 'fast', 'fivethirtyeight', 'ggplot', 'grayscale', 'seaborn-v0_8', 'seaborn-v0_8-bright',
             'seaborn-v0_8-colorblind', 'seaborn-v0_8-dark', 'seaborn-v0_8-dark-palette', 'seaborn-v0_8-darkgrid',
             'seaborn-v0_8-deep', 'seaborn-v0_8-muted', 'seaborn-v0_8-notebook', 'seaborn-v0_8-paper',
             'seaborn-v0_8-pastel', 'seaborn-v0_8-poster', 'seaborn-v0_8-talk', 'seaborn-v0_8-ticks',
             'seaborn-v0_8-white', 'seaborn-v0_8-whitegrid', 'tableau-colorblind10']
    def __init__(self, parent=None):
        super(Grafics, self).__init__(parent=parent)
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        plt.style.use('seaborn-v0_8-whitegrid')
        # self.toolbar = NavigationToolbar(self.canvas, self)

        self.layout = QtWidgets.QVBoxLayout()
        # self.layout.addWidget(self.toolbar)
        # self.setMinimumSize(300, 300)
        # self.setMaximumSize(900, 600)

        self.layout.addWidget(self.canvas)
        self.setLayout(self.layout)

    def draw_graph(self):
        statistic = MANAGER_STUDENTS.get_total_statistic_period()


        labels = statistic.keys()
        labels = list(map(lambda x: f'{x[0]!r} {ManagerStudents.MONTHS[x[1]]}', labels))

        data = list(map(lambda x: x[0], statistic.values()))
        data1 = list(map(lambda x: x[1], statistic.values()))
        data2 = list(map(lambda x: x[2], statistic.values()))

        self.figure.clear()
        ax = self.figure.add_subplot()
        ax.plot(list(map(str, range(1, len(labels)+1))), data, label ='ПОУВ')
        ax.plot(data1, label='НЕУВ')
        ax.plot(data2, label='Всего')



        ax.scatter(list(map(str, range(1, len(labels)+1))), data, s=5)
        ax.scatter(list(map(str, range(1, len(labels) + 1))), data1, s=5)
        ax.scatter(list(map(str, range(1, len(labels) + 1))), data2, s=5)


        ax.legend(loc='upper left')
        ax.set_title('Тенденция прогулов по месяцам')
        self.canvas.draw()
        return labels, data, data1, data2




    def draw_circle_graph(self):
        try:
            labels = MANAGER_STUDENTS.get_statistics_for_graph().keys()
            all_abcense = sum(MANAGER_STUDENTS.get_statistics_for_graph().values())
            values = list(map(lambda x: x/all_abcense,MANAGER_STUDENTS.get_statistics_for_graph().values()))
        except ZeroDivisionError:
            print('Ltktybt yf yjkm')
        else:
            self.figure.clear()
            ax = self.figure.add_subplot()
            ax.pie(values, labels=list(range(1, len(labels)+1)))
            ax.set_title('Доля прогулов на студента за месяц')
            self.canvas.draw()
            return labels, values



class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        self.status = 0
        super().__init__()
        self.setStyleSheet(
            """
            #game_over_push, #save_to_exel_push, #save_table_push {border: none;}
            #QButton {margin: auto;}
            QTableWidget {margin-left: auto; margin-right: auto;}
            QListWidget {margin-left: auto; margin-top: 20%; margin-right: auto; border: none;}
            #profile QPushButton {background-color: rgba(249, 248, 244, 0);}
            QScrollArea {border: none}

            """)
        self.setWindowIcon(QtGui.QIcon('media\\logo.svg'))
        self.setObjectName("MainWindow")
        self.resize(1024, 768)
        self.setMinimumSize(800, 450)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.group = QtWidgets.QTabWidget(self.centralwidget)
        self.group.setTabPosition(QtWidgets.QTabWidget.TabPosition.North)
        self.group.setTabShape(QtWidgets.QTabWidget.TabShape.Rounded)
        self.group.setDocumentMode(False)
        self.group.setTabsClosable(False)
        self.group.setMovable(False)
        self.group.setTabBarAutoHide(False)
        self.group.setObjectName("group")


        self.F6 = AbsenceTab(self)
        self.group.addTab(self.F6, "")


        self.marks = MarksTab(self)
        self.group.addTab(self.marks, "")


        self.students = StudentsTab(self)
        self.group.addTab(self.students, "")

        self.archive = ArchiveTab(self)
        self.group.addTab(self.archive, "")

        self.settings = SettingsTab(self)
        self.group.addTab(self.settings, "")
        if DEBAG:
            self.statistics = StatisticTab(self)
            self.group.addTab(self.statistics, "")

        self.profile = ProfileTab(self)
        self.group.addTab(self.profile, "")




        self.verticalLayout_2.addWidget(self.group)
        self.setCentralWidget(self.centralwidget)
        self.action_2 = QtGui.QAction(self)
        self.action_2.setObjectName("action_2")
        self.verticalLayout_2.addWidget(self.group)
        self.setCentralWidget(self.centralwidget)
        self.action_2 = QtGui.QAction(self)
        self.action_2.setObjectName("action_2")
        self.retranslateUi()
        self.group.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(self)

        self.tab_set = set()
        self.add_function()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        if hasattr(self, 'marks'):
            self.group.setTabText(self.group.indexOf(self.marks), _translate("MainWindow", "Оценки"))
        self.setWindowTitle(_translate("MainWindow", "F6"))
        self.group.setTabText(self.group.indexOf(self.F6), _translate("MainWindow", "Прогулы"))
        self.group.setTabText(self.group.indexOf(self.students), _translate("MainWindow", "Студенты"))
        self.group.setTabText(self.group.indexOf(self.settings), _translate("MainWindow", "Настройки"))
        self.group.setTabText(self.group.indexOf(self.profile), _translate("MainWindow", "Профиль"))
        self.action_2.setText(_translate("MainWindow", "ншнге"))
        self.group.setTabText(self.group.indexOf(self.archive), _translate("MainWindow", "Архив"))
        if DEBAG:
            self.group.setTabText(self.group.indexOf(self.statistics), _translate("MainWindow", "Статистика"))


    def click_tab(self):
        if self.group.currentIndex() not in self.tab_set:
            self.tab_set.add(self.group.currentIndex())

        self.profile.cod = [0, 4]


    def add_function(self):
        pass


    def init_students_manager(self, path=None, only_show=False, period=None):
        self.profile.cod = [3, 4]
        self.profile.cod = [2, 0]



        global MANAGER_STUDENTS
        if not [0, 0] in USER_MANAGER.user.parametrs.get('achievements', []):
            USER_MANAGER.user.add_achievement([0, 0])
        if not period:
            try:
                MANAGER_STUDENTS = ManagerStudents.load_manager_students(USER_MANAGER.user, file_name=path)
            except BaseException as message:
                if 'archive' in path:
                    raise FileNotFoundError
                print(120, message)
                MANAGER_STUDENTS = ManagerStudents((datetime.date.today().month, datetime.date.today().year),
                                                   USER_MANAGER.user)
        else:
            students = []
            if not MANAGER_STUDENTS is None:
                students = MANAGER_STUDENTS.students
                for i in range(len(students)):
                    students[i].sick_days.clear()
                    students[i].absence_days.clear()
                    students[i].marks.clear()
            MANAGER_STUDENTS = ManagerStudents(period,
                                               USER_MANAGER.user, students=students)
        if len(MANAGER_STUDENTS.students) == 0:
            self.group.removeTab(self.group.indexOf(self.students))
        try:
            self.F6.init_table_absence(only_show)
            if hasattr(self, 'marks'):
                self.marks.init_table_marks(only_show)
        except:
            print(144)

        self.students.update_list_students()
        self.F6.label_2.setText(f"Добро пожаловать, {USER_MANAGER.user.username}!")
        self.profile.update_user_info()
        self.archive.init_archive()
        self.profile.init_atchivments()
        if [0, 4] not in (USER_MANAGER.user.parametrs.get('achievements') or []):
            self.group.tabBarClicked.connect(self.click_tab)

        if USER_MANAGER.user.parametrs.get('table_marks') == False:
            self.group.removeTab(self.group.indexOf(self.marks))



        self.profile.cod = [1, 2]
        self.profile.cod = [3, 3]
        self.profile.cod = [2, 1]
        self.profile.cod = [3, 4]
        self.group.currentIndex()



class BaseTable():
    pass


class TableAbsence(QtWidgets.QTableWidget):
    """Модуль TableAbsence отвечает за создание и обновление таблицы прогулов принимает на вход режим отображения:
    атрибут only_show, который может быть логическим(True/False)"""

    def __init__(self, only_show=False):
        super(TableAbsence, self).__init__()
        self.setStyleSheet("""QTableWidget {border:red;}""")
        self.setObjectName("tableView")
        self.only_show = only_show

    def generate_table(self, size=0):
        self.mod_size = size
        self.setColumnCount(36)

        if not self.only_show and len(MANAGER_STUDENTS.students) < 30:
            self.setRowCount(2 + len(MANAGER_STUDENTS.students) + 2)
        else:
            self.setRowCount(2 + len(MANAGER_STUDENTS.students) + 1)

        self.horizontalHeader().setVisible(False)
        self.verticalHeader().setVisible(False)
        self.setSpan(0, 0, 1, 36)
        self.setSpan(1, 1, 2, 1)
        self.setSpan(1, 34, 1, 2)
        self.setSpan(1, 0, 2, 1)

        self.setItem(0, 0, QTableWidgetItem(
            f"ВЕДОМОСТЬ УЧЁТА ЧАСОВ ПРОГУЛОВ за {str(ManagerStudents.MONTHS[MANAGER_STUDENTS.period[0] - 1]) + ' ' + str(MANAGER_STUDENTS.period[1])}"))
        title = self.item(0, 0)
        title.setBackground(QtGui.QColor(153, 153, 153))
        title.setFont(QtGui.QFont('Calibri', 26 + size))
        title.setFlags(QtCore.Qt.ItemFlag.ItemIsEnabled)

        self.setItem(1, 34, QTableWidgetItem("Из них"))
        self.item(1, 34).setFont(QtGui.QFont('Calibri', 14 + size))
        self.item(1, 34).setFlags(QtCore.Qt.ItemFlag.ItemIsEnabled)
        self.item(1, 34).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.setItem(2, 34, QTableWidgetItem("УВ"))
        self.item(2, 34).setFont(QtGui.QFont('Calibri', 14 + size))
        self.item(2, 34).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.item(2, 34).setFlags(QtCore.Qt.ItemFlag.ItemIsEnabled)

        self.setItem(2, 35, QTableWidgetItem("НЕУВ"))
        self.item(2, 35).setFont(QtGui.QFont('Calibri', 14 + size))
        self.item(2, 35).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.item(2, 35).setFlags(QtCore.Qt.ItemFlag.ItemIsEnabled)

        self.setItem(2, 33, QTableWidgetItem(str(sum(MANAGER_STUDENTS.days.values()))))

        self.setItem(1, 1, QTableWidgetItem("ФИО"))
        fio = self.item(1, 1)
        fio.setFont(QtGui.QFont('Calibri', 14 + size))
        fio.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        fio.setFlags(QtCore.Qt.ItemFlag.ItemIsEnabled)
        self.setItem(1, 33, QTableWidgetItem("Итог"))
        result_up = self.item(1, 33)
        result_up.setFont(QtGui.QFont('Calibri', 14 + size))
        result_up.setFlags(QtCore.Qt.ItemFlag.ItemIsEnabled)

        for i in range(2, 32 + 1):
            if i - 1 in MANAGER_STUDENTS.days:
                self.setItem(1, i, QTableWidgetItem(
                    str(MANAGER_STUDENTS.days[i - 1] if MANAGER_STUDENTS.days[i - 1] else '')))
                self.item(1, i).setFont(QtGui.QFont('Calibri', 14 + size))
            else:
                self.setItem(1, i, QTableWidgetItem(str('✖')))
                self.item(1, i).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.item(1, i).setFont(QtGui.QFont('Calibri', 14 + size))
                self.item(1, i).setBackground(QtGui.QColor(220, 220, 220))
                self.item(1, i).setFlags(QtCore.Qt.ItemFlag.ItemIsEnabled)

                try:
                    for j in range(2, self.rowCount()):
                        self.setItem(j, i, QTableWidgetItem(""))
                        self.item(j, i).setBackground(QtGui.QColor(220, 220, 220))

                        self.item(j, i).setFlags(QtCore.Qt.ItemFlag.ItemIsEnabled)

                except BaseException as f:
                    print(f)
            self.setItem(2, i, QTableWidgetItem(str(i - 1)))
            self.item(2, i).setFlags(QtCore.Qt.ItemFlag.ItemIsEnabled)
            self.item(2, i).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            self.item(2, i).setFont(QtGui.QFont('Calibri', 14 + size))
            if not i - 1 in MANAGER_STUDENTS.days:
                self.item(2, i).setBackground(QtGui.QColor(220, 220, 220))
            self.setColumnWidth(i, 10)

        for i, student in enumerate(MANAGER_STUDENTS.students):
            i += 3

            self.setItem(i, 1, QTableWidgetItem(student.create_shorts_fio(student.fio)))
            self.item(i, 1).setFont(QtGui.QFont('Calibri', 14 + size))
            self.item(i, 1).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            self.item(i, 1).setFlags(QtCore.Qt.ItemFlag.ItemIsEnabled)
            self.setItem(i, 0, QTableWidgetItem(str(i - 2)))
            self.item(i, 0).setFont(QtGui.QFont('Calibri', 14 + size))

            self.setItem(i, 34, QTableWidgetItem(str(i - 2)))
            self.setItem(i, 35, QTableWidgetItem(str(i - 2)))

            for s_d in student.sick_days:
                self.setItem(i, s_d + 1, QTableWidgetItem(''))
                self.item(i, s_d + 1).setFont(QtGui.QFont('Calibri', 14 + size))
                self.add_hours_in_table(i, s_d + 1, student.sick_days.get(s_d), type_day='s')

            for a_d in student.absence_days:
                self.setItem(i, a_d + 1, QTableWidgetItem(''))
                self.item(i, a_d + 1).setFont(QtGui.QFont('Calibri', 14 + size))
                self.add_hours_in_table(i, a_d + 1, student.absence_days.get(a_d), type_day='a')
            self.update_statistics_student(i)
            self.update_hours_day()
            self.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
            self.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
            self.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
            self.horizontalHeader().setSectionResizeMode(33, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
            self.horizontalHeader().setSectionResizeMode(34, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
            self.horizontalHeader().setSectionResizeMode(35, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
            self.verticalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)

    def add_hours_in_table(self, row: int, column: int, hours: int, type_day: str = 's'):
        """Функция принимает координаты ячейки и число прогулов(часы) и
        тип дня(бывает a – прогулы по неуважительной причине и s – прогулы по болезни).
        Функция добавляет прогулы к объекту студент и в таблицу для отображения в приложении"""

        if type_day.lower() == 's':
            if column - 1 in MANAGER_STUDENTS.students[row - 3].absence_days:
                del MANAGER_STUDENTS.students[row - 3].absence_days[column - 1]
        elif type_day.lower() == 'a':
            if column - 1 in MANAGER_STUDENTS.students[row - 3].sick_days:
                del MANAGER_STUDENTS.students[row - 3].sick_days[column - 1]
        MANAGER_STUDENTS.add_day(
            MANAGER_STUDENTS.students[row - 3],
            column - 1,
            int(hours),
            type_day=type_day,
        )
        self.item(row, column).setText(str(hours))
        if type_day.lower() == 's':
            self.item(row, column).setBackground(QtGui.QColor(51, 204, 0))
        else:
            self.item(row, column).setBackground(QtGui.QColor(255, 102, 51))

        self.item(row, column).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.item(row, column).setFont(QtGui.QFont('Calibri', 14 + self.mod_size))

    def update_hours_day(self):
        """Обновляет значения часов для всех рабочих дней"""
        self.item(2, 33).setText(str(sum(MANAGER_STUDENTS.days.values())))
        self.item(2, 33).setFont(QtGui.QFont('Calibri', 14 + self.mod_size))

    def update_statistics_student(self, row):
        """Обновляет значения прогулов для всех студентов"""
        statistics = MANAGER_STUDENTS.students[row - 3].get_statistic_for_student()
        self.item(row, 34).setText(
            str(statistics['Sick_days'][1] if statistics['Sick_days'][1] > 0 else ''))
        self.item(row, 35).setText(
            str(statistics['Absence_days'][1] if statistics['Absence_days'][1] > 0 else ''))
        self.item(row, 1).setToolTip(f"""
    ФИО: {statistics['FIO']};
    Прогулы по неув. причине: {str(statistics["Absence_days"][1])};
    Прогулы по ув. причине: {str(statistics["Sick_days"][1])}
                        """)
        self.item(row, 34).setFont(QtGui.QFont('Calibri', 14 + self.mod_size))
        self.item(row, 35).setFont(QtGui.QFont('Calibri', 14 + self.mod_size))

    def update_table_students(self, *args, **kwargs):
        """Отчищает полностью таблицу и создает ее заново"""
        self.clear()
        self.generate_table(*args, **kwargs)
        if len(MANAGER_STUDENTS.students) >= 25:
            if not [0, 1] in USER_MANAGER.user.parametrs.get('achievements', []):
                USER_MANAGER.user.add_achievement([0, 1])


class TableMarks(QtWidgets.QTableWidget):
    """Модуль TableMarks отвечает за создание и обновление таблицы оценок, принимает на вход режим отображения:
        атрибут only_show, который может быть логическим(True/False)"""

    def __init__(self, only_show):
        super().__init__()
        self.setStyleSheet("""QTableWidget {border: none;}""")
        self.only_show = only_show

    def generate_table(self, size=0):
        self.mod_size = size

        self.setColumnCount(13)
        if not self.only_show and len(MANAGER_STUDENTS.students) < 30:
            self.setRowCount(2 + len(MANAGER_STUDENTS.students) + 2)
        else:
            self.setRowCount(2 + len(MANAGER_STUDENTS.students) + 1)
        self.horizontalHeader().setVisible(False)
        self.verticalHeader().setVisible(False)
        self.setSpan(0, 0, 1, 36)
        self.setSpan(1, 1, 2, 1)
        self.setSpan(1, 34, 1, 2)
        self.setSpan(1, 0, 2, 1)

        self.setItem(0, 0, QTableWidgetItem(
            f"ВЕДОМОСТЬ УЧЁТА УСПЕВАЕМОСТИ за {str(ManagerStudents.MONTHS[MANAGER_STUDENTS.period[0] - 1]) + ' ' + str(MANAGER_STUDENTS.period[1])}"))
        title = self.item(0, 0)
        title.setBackground(QtGui.QColor(153, 153, 153))
        title.setFont(QtGui.QFont('Calibri', 26 + size))
        title.setFlags(QtCore.Qt.ItemFlag.ItemIsEnabled)

        self.setItem(1, 1, QTableWidgetItem("ФИО"))
        fio = self.item(1, 1)
        fio.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        fio.setFlags(QtCore.Qt.ItemFlag.ItemIsEnabled)
        fio.setFont(QtGui.QFont('Calibri', 14 + size))
        for i in range(2, 13):
            self.setItem(1, i, QTableWidgetItem(MANAGER_STUDENTS.couples.get(str(i - 1), '  ')[0]))
            self.setItem(2, i, QTableWidgetItem(MANAGER_STUDENTS.couples.get(str(i - 1), '  ')[1]))
            self.item(1, i).setFont(QtGui.QFont('Calibri', 14 + size))
            self.item(2, i).setFont(QtGui.QFont('Calibri', 14 + size))

        for i, student in enumerate(MANAGER_STUDENTS.students):
            i += 3
            self.setItem(i, 0, QTableWidgetItem(str(i - 2)))
            self.item(i, 0).setFont(QtGui.QFont('Calibri', 14 + size))
            self.setItem(i, 1, QTableWidgetItem(student.create_shorts_fio(student.fio)))
            self.item(i, 1).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            self.item(i, 1).setFlags(QtCore.Qt.ItemFlag.ItemIsEnabled)
            self.item(i, 1).setFont(QtGui.QFont('Calibri', 14 + size))
            self.update_statistics_student(i)
            for j in MANAGER_STUDENTS.students[i - 3].marks:
                self.setItem(i, j + 1, QTableWidgetItem(''))
                self.add_mark_table(i, j + 1, MANAGER_STUDENTS.students[i - 3].marks[j], size=size)
        # self.resizeColumnsToContents()
        self.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self.verticalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)

    def add_mark_table(self, row, column, mark, size=0):
        mark = int(mark)
        MANAGER_STUDENTS.students[row - 3].marks[column - 1] = mark
        self.item(row, column).setText(str(mark))
        self.item(row, column).setFont(QtGui.QFont('Calibri', 14 + size))
        self.item(row, column).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        if mark == 5:
            self.item(row, column).setBackground(QtGui.QColor('#f1c30f'))
        elif mark == 4:
            self.item(row, column).setBackground(QtGui.QColor('#f39c11'))
        elif mark == 3:
            self.item(row, column).setBackground(QtGui.QColor('#d15400'))
        else:
            self.item(row, column).setBackground(QtGui.QColor('#c2392c'))



    def del_mark_table(self, row, column):
        if MANAGER_STUDENTS.students[row - 3].marks.get(column - 1):
            del MANAGER_STUDENTS.students[row - 3].marks[column - 1]
            self.item(row, column).setBackground(QtGui.QColor('#fff'))

    def update_hours_day(self):
        self.item(2, 33).setText(str(sum(MANAGER_STUDENTS.days.values())))

    def update_statistics_student(self, row):
        statistics = MANAGER_STUDENTS.students[row - 3].get_statistic_for_student()
        self.item(row, 1).setToolTip(f"""
    ФИО: {statistics['FIO']};
                        """)

    def update_table_students(self, *args, **kwargs):
        self.clear()
        self.generate_table(*args, **kwargs)
        if len(MANAGER_STUDENTS.students) >= 25:
            if not [0, 1] in USER_MANAGER.user.parametrs.get('achievements', []):
                USER_MANAGER.user.add_achievement([0, 1])

    def add_couples(self, number, couple=None, fio=None):
        if fio:
            fio = USER_MANAGER.user.check_fio(fio)
        #_______________________________________________________ ______________________

        if MANAGER_STUDENTS.couples.get(str(number)):
            row = MANAGER_STUDENTS.couples[str(number)]
            if couple:
                row[0] = couple if couple else ''
            if fio:
                row[1] = fio if fio else ''

            MANAGER_STUDENTS.couples[str(number)] = row
        else:
            MANAGER_STUDENTS.couples[str(number)] = [couple if couple else '', fio if fio else '']


class SettingsWindows(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(SettingsWindows, self).__init__(parent)
        self.setObjectName("SettingsWindows")
        self.setFixedSize(400, 200)
        self.setModal(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.scrollArea = QtWidgets.QScrollArea(self)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 376, 120))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.title_messages = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.title_messages.setObjectName("label")
        self.verticalLayout_2.addWidget(self.title_messages)
        self.lineEdit = QtWidgets.QSpinBox(self.scrollAreaWidgetContents)
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout_2.addWidget(self.lineEdit)
        self.messages_error = QtWidgets.QTextBrowser(self.scrollAreaWidgetContents)
        self.messages_error.setStyleSheet("color: red; background: none; border: none;")
        self.messages_error.setFixedHeight(50)
        self.verticalLayout_2.addWidget(self.messages_error)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum,
                                           QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, 20, -1, -1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding,
                                            QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.save_button = QtWidgets.QPushButton(self)
        self.save_button.setObjectName("save_button")
        self.horizontalLayout.addWidget(self.save_button)
        self.cancel_button = QtWidgets.QPushButton(self)
        self.cancel_button.setObjectName("cancel_button")
        self.horizontalLayout.addWidget(self.cancel_button)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.result = None

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

        self.cancel_button.clicked.connect(self.clicked_cancel)
        self.save_button.clicked.connect(self.clicked_save)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Form", "Form"))
        self.title_messages.setText(_translate("Form", "TextLabel"))
        self.cancel_button.setText(_translate("Form", "Отмена"))
        self.save_button.setText(_translate("Form", "Сохранить"))

    def clicked_cancel(self):
        self.close()

    def check_value(self):
        if self.lineEdit.text().isnumeric() and 31 >= int(self.lineEdit.text()) > 0:
            return int(self.lineEdit.text())
        raise ValueError('Введен недопустимый номер дня')

    def clicked_save(self):
        try:
            res = self.check_value()
        except ValueError as f:
            self.messages_error.setText(str(f))
        else:
            self.result = res
            self.close()


class SettingsData(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(SettingsData, self).__init__(parent)
        self.setObjectName("SettingsData")
        self.resize(431, 160)
        self.setFixedSize(QtCore.QSize(430, 160))
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.dateEdit = QtWidgets.QDateEdit(self)
        self.dateEdit.setDateTime(QtCore.QDateTime(QtCore.QDate(2022, 1, 1), QtCore.QTime(0, 0, 0)))
        self.dateEdit.setObjectName("dateEdit")
        self.dateEdit.setDisplayFormat("MM.yyyy")
        self.verticalLayout.addWidget(self.dateEdit)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum,
                                           QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.create_new_table_pushButton = QtWidgets.QPushButton(self)
        self.create_new_table_pushButton.setObjectName("create_new_table_pushButton")
        self.horizontalLayout.addWidget(self.create_new_table_pushButton)
        self.cancel_pushButton = QtWidgets.QPushButton(self)
        self.cancel_pushButton.setMinimumSize(QtCore.QSize(0, 0))
        self.cancel_pushButton.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.cancel_pushButton.setObjectName("cancel_pushButton")
        self.horizontalLayout.addWidget(self.cancel_pushButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

        self.create_new_table_pushButton.clicked.connect(self.clicked_create_table)
        self.cancel_pushButton.clicked.connect(self.clicked_cancel)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("self", "self"))
        self.create_new_table_pushButton.setText(_translate("self", "Изменить"))
        self.cancel_pushButton.setText(_translate("self", "Отмена"))

    def clicked_create_table(self):
        self.close()

    def clicked_cancel(self):
        self.close()


class Push(QtWidgets.QPushButton):
    def __init__(self, parent, base_weight, base_height, growth, tool_tip=None, icon_path=None):
        super().__init__()
        self.setStyleSheet('border: none;')
        self.base_height = base_height
        self.base_weight = base_weight
        self.growth = growth
        self.setIconSize(QtCore.QSize(self.base_weight, self.base_height))
        if tool_tip:
            self.setToolTip(tool_tip)
        if icon_path:
            self.setIcon(QIcon(icon_path))

    def enterEvent(self, e):
        self.setIconSize(QtCore.QSize(self.base_weight + self.growth, self.base_height + self.growth))

    def leaveEvent(self, e):
        self.setIconSize(QtCore.QSize(self.base_weight, self.base_height))


class WindowSetPassword(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("Form")
        self.resize(500, 300)
        self.setMaximumSize(QtCore.QSize(500, 300))
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.old_password_edit = QtWidgets.QLineEdit(self)
        self.old_password_edit.setEnabled(True)
        self.old_password_edit.setObjectName("old_password_edit")
        self.verticalLayout.addWidget(self.old_password_edit)
        self.label_2 = QtWidgets.QLabel(self)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.new_password_edit1 = QtWidgets.QLineEdit(self)
        self.new_password_edit1.setObjectName("new_password_edit1")
        self.verticalLayout.addWidget(self.new_password_edit1)
        self.label_3 = QtWidgets.QLabel(self)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.new_password_edit2 = QtWidgets.QLineEdit(self)
        self.new_password_edit2.setObjectName("new_password_edit2")
        self.verticalLayout.addWidget(self.new_password_edit2)
        self.fielderrors = QtWidgets.QTextBrowser(self)
        self.fielderrors.setObjectName("fielderrors")
        self.verticalLayout.addWidget(self.fielderrors)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum,
                                           QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.save_password_pushbutton = QtWidgets.QPushButton(self)
        self.save_password_pushbutton.setObjectName("save_password_pushbutton")
        self.horizontalLayout.addWidget(self.save_password_pushbutton)
        self.line = QtWidgets.QFrame(self)
        self.line.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout.addWidget(self.line)
        self.cancel_pushbutton = QtWidgets.QPushButton(self)
        self.cancel_pushbutton.setObjectName("cancel_pushbutton")
        self.horizontalLayout.addWidget(self.cancel_pushbutton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.retranslateUi()

        self.add_function()

    def retranslateUi(self, ):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "Старый пароль"))
        self.label_2.setText(_translate("Form", "Новый пороль"))
        self.label_3.setText(_translate("Form", "Повторите новый пароль"))
        self.save_password_pushbutton.setText(_translate("Form", "Сохронить"))
        self.cancel_pushbutton.setText(_translate("Form", "Отмена"))

    def add_function(self):
        self.cancel_pushbutton.clicked.connect(self.click_cancel)
        self.save_password_pushbutton.clicked.connect(self.click_save)

    def click_cancel(self):
        self.close()

    def checking_parametrs(self):
        if not self.old_password_edit.text() == USER_MANAGER.user.password:
            raise ValueError('Введен неверный текущий пароль')
        if not self.new_password_edit2.text() == self.new_password_edit1.text():
            raise ValueError('Пароли не соответствуют')

    def click_save(self):
        self.fielderrors.clear()
        try:
            self.checking_parametrs()
        except ValueError as m:
            self.fielderrors.setText(str(m))

        else:
            try:
                USER_MANAGER.user.password = self.new_password_edit1.text()
            except ValueError as m:
                self.fielderrors.setText(str(m))
            else:
                USER_MANAGER.user.save_user()
                MANAGER_STUDENTS.user = USER_MANAGER.user

                MANAGER_STUDENTS.save_students()
                self.close()


class ControlerWindows:
    def __init__(self, splash_screen, auth, regist, main):
        self.splash_screen = splash_screen()
        self.splash_screen.show()
        self.auth = auth()
        self.load_splash_screen(0, 31)
        self.regist = regist()
        self.load_splash_screen(31, 61)
        self.main = main()
        self.load_splash_screen(61, 101)

        self.auth.closeEvent = self.close_event_by_auth
        self.main.closeEvent = self.close_event_by_main
        self.regist.closeEvent = self.close_event_by_regist
        self.splash_screen.close()

    def load_splash_screen(self, starts=0, end=0):
        for i in range(starts, end):
            self.splash_screen.progressBar.setValue(i)
            QtCore.QThread.msleep(4)

    def close_event_by_auth(self, e):
        if self.auth.status == 1:
            self.main.init_students_manager('students.json')
            self.main.show()
        elif self.auth.status == 3:
            self.regist.show()
        else:
            self.auth.close()
        self.auth.status = 0
        self.auth.closeEvent = self.close_event_by_auth

    def close_event_by_main(self, e):
        if self.main.status == 2:
            self.auth.update_users()
            self.auth.show()
        elif self.main.status == 3:
            self.regist.show()
        elif self.main.status == 4:
            self.main = type(self.main)()
            self.auth.show()
        else:
            self.main.close()
            message = QtWidgets.QMessageBox.question(windows.main, 'Сохранение изменений', "Сохронить изменения?",
                                                     QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
            if message == message.Yes:
                windows.main.save_table()

        self.main.status = 0
        self.main.closeEvent = self.close_event_by_main

    def close_event_by_regist(self, e):
        if self.regist.status == 1:
            self.auth.update_users()
            self.main.init_students_manager('students.json')
            self.main.show()
        elif self.regist.status == 2:
            self.auth.show()
        else:
            self.regist.close()
        self.regist.status = 0

    def show(self):
        if USER_MANAGER.users_id:
            self.auth.show()
        else:
            self.regist.show()


app = QtWidgets.QApplication(sys.argv)

windows = ControlerWindows(SplashScreen, Auth, Regist, MainWindow)
windows.show()

status = app.exec()

print(status, '-')
sys.exit(status)
