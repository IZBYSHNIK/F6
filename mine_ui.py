import datetime
import json
import os
import sys
import random
import time

from PyQt6.QtGui import QIcon, QScreen
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import (
    QApplication, QWidget, QTableWidget,
    QTableWidgetItem, QVBoxLayout, QHeaderView

)
from StudentsManager import ManagerStudents, Student
from UserManager import UserManager, User


VERSION = '1.0.9beta'


class SplashScreen(QtWidgets.QSplashScreen):
    def __init__(self):
        super().__init__()
        self.setObjectName("splash_screen")
        self.setFixedSize(379, 443)
        self.move((app.primaryScreen().size().width()-self.size().width())//2, (app.primaryScreen().size().height()-self.size().height())//2-40)
        self.logo = QtWidgets.QLabel(self)
        self.logo.setMinimumWidth(379)
        logo = QtGui.QPixmap(os.path.join('media', 'logo.svg'))
        self.logo.setPixmap(logo)
        self.logo.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        font = QtGui.QFont()
        font.setPointSize(36)
        self.logo.setFont(font)
        self.logo.setText("")
        self.logo.setObjectName("logo")
        self.progressBar = QtWidgets.QProgressBar(self)
        self.progressBar.setGeometry(QtCore.QRect(0, 400, 381, 51))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setTextVisible(False)
        self.progressBar.setObjectName("progressBar")
        self.version = QtWidgets.QLabel(self)
        self.version.setGeometry(QtCore.QRect(340, 400, 61, 41))
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
        font.setWeight(50)
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
        self.teamleader_lable.setGeometry(QtCore.QRect(230, 380, 311, 51))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.teamleader_lable.setFont(font)
        self.teamleader_lable.setObjectName("teamleader_lable")
        self.teamleader_edit = QtWidgets.QLineEdit(self)
        self.teamleader_edit.setGeometry(QtCore.QRect(240, 430, 160, 40))
        self.teamleader_edit.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)
        self.teamleader_edit.setObjectName("teamleader_edit")
        self.office_name_edit = QtWidgets.QLineEdit(self)
        self.office_name_edit.setGeometry(QtCore.QRect(40, 430, 161, 40))
        self.office_name_edit.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)
        self.office_name_edit.setObjectName("office_name_edit")
        self.office_name_lable = QtWidgets.QLabel(self)
        self.office_name_lable.setGeometry(QtCore.QRect(70, 380, 91, 51))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.office_name_lable.setFont(font)
        self.office_name_lable.setObjectName("office_name_lable")
        self.email_edit = QtWidgets.QLineEdit(self)
        self.email_edit.setGeometry(QtCore.QRect(40, 520, 360, 40))
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.email_edit.setFont(font)
        self.email_edit.setObjectName("email_edit")
        self.email_lable = QtWidgets.QLabel(self)
        self.email_lable.setGeometry(QtCore.QRect(30, 470, 311, 51))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.email_lable.setFont(font)
        self.email_lable.setObjectName("email_lable")

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
        self.email_lable.setText(_translate("Regist", "Почтовый адрес для восстановления"))

    def check_lables(self):
        USER_MANAGER.USER_CLASS.check_username(self.login_edit.text())
        if self.login_edit.text() in USER_MANAGER.users_id.values():
            raise ValueError('Имя пользователя занято')
        USER_MANAGER.USER_CLASS.check_password(self.password_edit.text())
        if not self.password_edit.text() == self.password_edit_2.text():
            raise ValueError('Не совподают пароли')
        if self.office_name_edit.text() != '':
            USER_MANAGER.USER_CLASS.check_fio(self.office_name_edit.text())
        if self.teamleader_edit.text() != '':
            USER_MANAGER.USER_CLASS.check_fio(self.teamleader_edit.text())

        return self.login_edit.text(), self.password_edit.text(), {
            'offical_name': None if not self.office_name_edit.text() else self.office_name_edit.text(),
            'teamleader': None if not self.teamleader_edit.text() else self.teamleader_edit.text()}

    def click_create_push(self):
        self.message_regist.setText('')
        try:
            username, password, kwargs = self.check_lables()
            USER_MANAGER.link_user_by_obj(USER_MANAGER.USER_CLASS(username, password, kwargs))
            USER_MANAGER.save_users()


        except BaseException as message:
            self.message_regist.setText('*' + str(message))
        else:
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

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Auth", "Авторизация"))
        self.auth.setText(_translate("Auth", "<p>АВТОРИЗАЦИЯ </p>"))
        self.in_push.setText(_translate("Auth", "Вход"))
        self.regist_push.setText(_translate("Auth", "Регистрация"))
        self.login_lable.setText(_translate("Auth", "Логин"))
        self.password_lable.setText(_translate("Auth", "Пароль"))

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
                self.status = 1
                self.close()

    def click_regis_push(self):
        self.status = 3
        self.close()


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        self.status = 0
        super().__init__()
        self.setStyleSheet(
            """
            #game_over_push, #save_to_exel_push, #save_table_push {border: none;} #game_over_push:hover {background: rgb(0,0,0); margin-right: 5px; margin-left: 5px; margin-top: 5px; margin-bottom: 5px; border-radius: 2px;}
            #tableView {margin-left: auto; margin-right: auto;}
            #profile QPushButton {background-color: rgba(249, 248, 244, 0);}

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
        self.F6 = QtWidgets.QWidget()
        self.F6.setObjectName("F6")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.F6)
        self.verticalLayout.setObjectName("verticalLayout")

        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.frame = QtWidgets.QFrame(self.F6)
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

        self.horizontalLayout_2.addLayout(self.horizontalLayout_4)

        self.save_table_push = Push(self.frame, 40, 40, 5)
        self.save_table_push.setObjectName("save_table_push")
        self.horizontalLayout_2.addWidget(self.save_table_push)

        self.game_over_push = QtWidgets.QPushButton(self.frame)
        self.game_over_push.setObjectName("game_over_push")
        self.horizontalLayout_2.addWidget(self.game_over_push)

        self.save_to_exel_push = Push(self.frame, 55, 55, 5)
        self.save_to_exel_push.setObjectName("save_to_exel_push")
        self.horizontalLayout_2.addWidget(self.save_to_exel_push)
        self.horizontalLayout_3.addLayout(self.horizontalLayout_2)
        self.verticalLayout_3.addWidget(self.frame)
        self.verticalLayout.addLayout(self.verticalLayout_3)

        self.tableWidget = QtWidgets.QTableWidget()

        self.tableWidget.setStyleSheet("""QTableWidget {border: none;}""")

        self.tableWidget.setObjectName("tableView")
        self.verticalLayout.addWidget(self.tableWidget)

        self.group.addTab(self.F6, "")

        self.students = QtWidgets.QWidget()
        self.students.setObjectName("students")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.students)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setContentsMargins(-1, -1, 0, -1)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.label = QtWidgets.QLabel(self.students)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.verticalLayout_6.addWidget(self.label)
        self.listWidget = QtWidgets.QListWidget(self.students)
        self.listWidget.setObjectName("listWidget")

        self.listWidget.setStyleSheet('''#listWidget {margin: auto; border: none;} ''')

        self.verticalLayout_6.addWidget(self.listWidget)
        self.horizontalLayout_6.addLayout(self.verticalLayout_6)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.fio_label = QtWidgets.QLabel(self.students)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.fio_label.setFont(font)
        self.fio_label.setObjectName("fio_label")
        self.verticalLayout_5.addWidget(self.fio_label)
        self.fio_edit = QtWidgets.QLineEdit(self.students)
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
        self.del_push = QtWidgets.QPushButton(self.students)
        self.del_push.setObjectName("del_push")
        self.horizontalLayout_5.addWidget(self.del_push)
        self.save_push = QtWidgets.QPushButton(self.students)
        self.save_push.setObjectName("save_push")
        self.horizontalLayout_5.addWidget(self.save_push)
        self.verticalLayout_5.addLayout(self.horizontalLayout_5)
        self.verticalLayout_4.addLayout(self.verticalLayout_5)
        self.horizontalLayout_6.addLayout(self.verticalLayout_4)
        self.group.addTab(self.students, "")


        self.profile = QtWidgets.QWidget()
        self.profile.setObjectName("profile")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout(self.profile)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout()
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.accaunt_label = QtWidgets.QLabel(self.profile)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.accaunt_label.setFont(font)
        self.accaunt_label.setObjectName("accaunt_label")
        self.verticalLayout_8.addWidget(self.accaunt_label)
        self.username_label = QtWidgets.QLabel(self.profile)

        font = QtGui.QFont()
        font.setPointSize(15)
        self.username_label.setFont(font)
        self.username_label.setObjectName("username_label")
        self.verticalLayout_8.addWidget(self.username_label)
        self.username_edit = QtWidgets.QLineEdit(self.profile)

        self.username_edit.setMinimumSize(QtCore.QSize(0, 30))
        self.username_edit.setMaximumSize(QtCore.QSize(400, 16777215))
        self.username_edit.setObjectName("username_edit")
        self.verticalLayout_8.addWidget(self.username_edit)
        self.fio_user_label = QtWidgets.QLabel(self.profile)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.fio_user_label.setFont(font)
        self.fio_user_label.setObjectName("fio_user_label")
        self.verticalLayout_8.addWidget(self.fio_user_label)
        self.fio_user_edit = QtWidgets.QLineEdit(self.profile)
        self.fio_user_edit.setMinimumSize(QtCore.QSize(0, 30))
        self.fio_user_edit.setMaximumSize(QtCore.QSize(400, 16777215))
        self.fio_user_edit.setObjectName("fio_user_edit")
        self.verticalLayout_8.addWidget(self.fio_user_edit)
        self.teamleader_label = QtWidgets.QLabel(self.profile)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.teamleader_label.setFont(font)
        self.teamleader_label.setObjectName("teamleader_label")
        self.verticalLayout_8.addWidget(self.teamleader_label)
        self.fio_teamleader_edit = QtWidgets.QLineEdit(self.profile)
        self.fio_teamleader_edit.setMinimumSize(QtCore.QSize(0, 30))
        self.fio_teamleader_edit.setMaximumSize(QtCore.QSize(400, 16777215))
        self.fio_teamleader_edit.setObjectName("fio_teamleader_edit")
        self.verticalLayout_8.addWidget(self.fio_teamleader_edit)
        self.email_label = QtWidgets.QLabel(self.profile)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.email_label.setFont(font)
        self.email_label.setObjectName("email_label")
        self.verticalLayout_8.addWidget(self.email_label)
        self.email_edit = QtWidgets.QLineEdit(self.profile)
        self.email_edit.setMinimumSize(QtCore.QSize(0, 30))
        self.email_edit.setMaximumSize(QtCore.QSize(400, 16777215))
        self.email_edit.setObjectName("email_edit")
        self.verticalLayout_8.addWidget(self.email_edit)

        self.group_label = QtWidgets.QLabel(self.profile)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.group_label.setFont(font)
        self.group_label.setObjectName("group_label")
        self.verticalLayout_8.addWidget(self.group_label)
        self.group_edit = QtWidgets.QLineEdit(self.profile)
        self.group_edit.setMinimumSize(QtCore.QSize(0, 30))
        self.group_edit.setMaximumSize(QtCore.QSize(400, 16777215))
        self.group_edit.setObjectName("group_edit")
        self.verticalLayout_8.addWidget(self.group_edit)

        self.specialization_label = QtWidgets.QLabel(self.profile)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.specialization_label.setFont(font)
        self.specialization_label.setObjectName("specialization_label")
        self.verticalLayout_8.addWidget(self.specialization_label)
        self.specialization_edit = QtWidgets.QLineEdit(self.profile)
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
        self.save_user_push = Push(self.profile, 35, 35, 5, )
        self.save_user_push.setObjectName("save_user_push")
        self.horizontalLayout_7.addWidget(self.save_user_push)
        self.set_password_push = Push(self.profile, 35, 35, 5)
        self.set_password_push.setObjectName("set_password_push")
        self.horizontalLayout_7.addWidget(self.set_password_push)
        self.del_user_push = Push(self.profile, 35, 35, 5)
        self.del_user_push.setObjectName("del_user_push")
        self.horizontalLayout_7.addWidget(self.del_user_push)
        self.verticalLayout_8.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_8.addLayout(self.verticalLayout_8)
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.verticalLayout_12 = QtWidgets.QVBoxLayout()
        self.verticalLayout_12.setObjectName("verticalLayout_12")

        self.photo = QtWidgets.QLabel(self.profile)
        photo = QtGui.QPixmap(os.path.join('media', 'profile', f'{str(random.randint(1, 9))}.svg'))
        photo = photo.scaled(200, 200)
        self.photo.setPixmap(photo)
        self.photo.setObjectName("photo")
        self.photo.setStyleSheet('#photo{margin: auto;}')
        self.verticalLayout_12.addWidget(self.photo, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_7.addLayout(self.verticalLayout_12)
        self.verticalLayout_7.addItem(
            QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding))
        self.verticalLayout_13 = QtWidgets.QVBoxLayout()
        self.verticalLayout_13.setObjectName("verticalLayout_13")

        for i in range(5):
            self.verticalLayout_14 = QtWidgets.QHBoxLayout()
            for j in range(6):
                qlable = QtWidgets.QLabel()
                qlable.setFixedSize(50, 60)
                qlable.setStyleSheet('background: red;')
                self.verticalLayout_14.addWidget(qlable)

            self.verticalLayout_13.addLayout(self.verticalLayout_14)
        self.verticalLayout_7.addLayout(self.verticalLayout_13)
        self.horizontalLayout_8.addLayout(self.verticalLayout_7)
        self.group.addTab(self.profile, "")

        self.profile.setObjectName("profile")
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

        self.save_to_exel_push.clicked.connect(self.save_to_exel)
        self.listWidget.itemClicked.connect(lambda: self.click_list(self.listWidget))
        self.tableWidget.cellChanged.connect(lambda: self.check_value(self.tableWidget))
        self.save_push.clicked.connect(self.save_student)
        self.del_push.clicked.connect(self.del_student)
        self.save_user_push.clicked.connect(self.save_user)
        self.save_table_push.clicked.connect(self.save_table)
        self.del_user_push.clicked.connect(self.del_user)

        self.save_user_push.setIcon(QIcon(os.path.join('media', 'buttons', 'save.svg')))
        self.save_user_push.setToolTip('Сохронить изменения')
        self.save_table_push.setIcon(QIcon(os.path.join('media', 'buttons', 'save.svg')))
        self.save_table_push.setToolTip('Сохронить изменения')
        self.del_user_push.setIcon(QIcon(os.path.join('media', 'buttons', 'del_user.svg')))
        self.del_user_push.setToolTip('Удалить пользователя')
        self.set_password_push.setIcon(QIcon(os.path.join('media', 'buttons', 'set_password.svg')))
        self.set_password_push.setToolTip('Изменить пароль')

        self.save_to_exel_push.setIcon(QIcon('media\\save_exel.svg'))
        self.save_to_exel_push.setToolTip('Сохронить в EXEL')

        self.game_over_push.setIcon(QIcon('media\\game_over.svg'))
        self.game_over_push.setIconSize(QtCore.QSize(40, 40))
        self.game_over_push.setMinimumSize(40, 40)
        self.game_over_push.setToolTip('Завершить текущий месяц')

        # self.init_students_manager()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_2.setText(_translate("MainWindow", f"Добро пожаловать, Nouname!"))
        self.is_sick_rb.setText(_translate("MainWindow", "ПОУВ"))
        self.radioButton_2.setText(_translate("MainWindow", "НЕУВ"))
        self.group.setTabText(self.group.indexOf(self.F6), _translate("MainWindow", "Ф6"))
        self.fio_label.setText(_translate("MainWindow", "ФИО"))
        self.del_push.setText(_translate("MainWindow", "Удалить"))
        self.save_push.setText(_translate("MainWindow", "Сохранить"))
        self.group.setTabText(self.group.indexOf(self.students), _translate("MainWindow", "Студенты"))
        self.label.setText(_translate("MainWindow", "Список студентов"))
        # self.group.setTabText(self.group.indexOf(self.settings), _translate("MainWindow", "Настройки"))
        self.accaunt_label.setText(_translate("MainWindow", "Аккаунт"))
        self.username_label.setText(_translate("MainWindow", "Имя пользователя"))
        self.fio_user_label.setText(_translate("MainWindow", "ФИО Своё"))
        self.teamleader_label.setText(_translate("MainWindow", "ФИО Кл.руководителя"))
        self.email_label.setText(_translate("MainWindow", "Почта"))
        self.group_label.setText(_translate('MainWindow', "Группа"))
        self.specialization_label.setText(_translate('MainWindow', "Специализация"))
        self.group.setTabText(self.group.indexOf(self.profile), _translate("MainWindow", "Профиль"))
        self.action_2.setText(_translate("MainWindow", "ншнге"))

    def update_user_info(self):
        self.username_edit.setText(USER_MANAGER.user.username)
        self.fio_teamleader_edit.setText(USER_MANAGER.user.parametrs.get('teamleader', ''))
        self.fio_user_edit.setText(USER_MANAGER.user.parametrs.get('offical_name', ''))
        self.email_edit.setText(USER_MANAGER.user.parametrs.get('email', ''))
        self.group_edit.setText(USER_MANAGER.user.parametrs.get('group', ''))
        self.specialization_edit.setText(USER_MANAGER.user.parametrs.get('specialization', ''))

    def update_statistics(self):
        statistics = self.manager_students.get_statistics()
        if statistics.get('man_hours') > 0:
            self.statustic1.setText(f'Чел.час = {str(statistics.get("man_hours"))} \t\t Посещ.Кач. = {str(round(statistics.get("quality_attendance"), 2)*100)}%')
            self.statustic2.setText(f'Посещ.Общ. = {str(round(statistics.get("total_attendance", 2)*100))}% \t Прогул 1 студ. = {str(round(statistics.get("absences_by_student", 1)))}')
        else:
            self.statustic1.clear()
            self.statustic2.clear()

    def update_list_students(self):
        self.listWidget.clear()
        for indx, student in enumerate(self.manager_students.students):
            self.listWidget.addItem(QtWidgets.QListWidgetItem(f'{str(indx + 1)}. {student.fio}'))

    def update_table_students(self):
        self.tableWidget.clear()
        self.generate_table()

    def update_hours_day(self):
        self.tableWidget.item(2, 33).setText(str(sum(self.manager_students.days.values())))

    def update_statistics_student(self, row):
        statistics = self.manager_students.students[row - 3].get_statistic_for_student()
        self.tableWidget.item(row, 34).setText(
            str(statistics['Sick_days'][1] if statistics['Sick_days'][1] > 0 else ''))
        self.tableWidget.item(row, 35).setText(
            str(statistics['Absence_days'][1] if statistics['Absence_days'][1] > 0 else ''))
        self.tableWidget.item(row, 1).setToolTip(f"""
    ФИО: {statistics['FIO']};
    Прогулы по неув. причине: {str(statistics["Absence_days"][1])};
    Прогулы по ув. причине: {str(statistics["Sick_days"][1])}
                        """)

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
            USER_MANAGER.user.parametrs['email'] = self.email_edit.text()
            USER_MANAGER.user.parametrs['group'] = self.group_edit.text()
            USER_MANAGER.user.parametrs['specialization'] = self.specialization_edit.text()


        except BaseException as f:
            self.message_profile.setText(str(f))
        else:
            self.message_profile.setText('')
            USER_MANAGER.user.save_user()

    def save_to_exel(self):
        self.manager_students.save_f6('beta.xlsx')

    def save_table(self):
        self.manager_students.save_students()

    def init_students_manager(self):
        try:
            self.manager_students = ManagerStudents.load_manager_students(USER_MANAGER.user)
        except BaseException as message:
            self.manager_students = ManagerStudents((datetime.date.today().month, datetime.date.today().year),
                                                    USER_MANAGER.user)
            self.manager_students.save_students()
        if len(self.manager_students.students) == 0:
            self.students.setEnabled(False)
        self.label_2.setText(f"Добро пожаловать, {USER_MANAGER.user.username}!")

        self.update_list_students()
        self.update_table_students()
        self.update_user_info()
        self.update_statistics()

    def add_hours_in_table(self, row, column, hours, type_day='s'):
        self.tableWidget.item(row, column).setText(str(hours))
        if type_day.lower() == 's':
            self.tableWidget.item(row, column).setBackground(QtGui.QColor(51, 204, 0))
        else:
            self.tableWidget.item(row, column).setBackground(QtGui.QColor(255, 102, 51))

        self.tableWidget.item(row, column).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

    def generate_table(self):
        self.tableWidget.setColumnCount(36)
        self.tableWidget.setRowCount(2 + len(self.manager_students.students) + 2)
        self.tableWidget.setColumnWidth(0, 5)
        self.tableWidget.setColumnWidth(33, 60)
        self.tableWidget.setColumnWidth(1, 210)
        self.tableWidget.setColumnWidth(34, 60)
        self.tableWidget.setColumnWidth(35, 60)

        self.tableWidget.horizontalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.setSpan(0, 0, 1, 36)
        self.tableWidget.setSpan(1, 1, 2, 1)
        self.tableWidget.setSpan(1, 34, 1, 2)
        self.tableWidget.setSpan(1, 0, 2, 1)

        self.tableWidget.setItem(0, 0, QTableWidgetItem(
            f"ВЕДОМОСТЬ УЧЁТА ЧАСОВ ПРОГУЛОВ за {str(self.manager_students.MONTHS[self.manager_students.period[0] - 1]) + ' ' + str(self.manager_students.period[1])}"))
        title = self.tableWidget.item(0, 0)
        title.setBackground(QtGui.QColor(153, 153, 153))
        # table.item(0, 0).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        title.setFont(QtGui.QFont('Calibri', 20))
        title.setFlags(QtCore.Qt.ItemFlag.ItemIsEnabled)

        self.tableWidget.setItem(1, 34, QTableWidgetItem("Из них"))
        self.tableWidget.item(1, 34).setFlags(QtCore.Qt.ItemFlag.ItemIsEnabled)
        self.tableWidget.item(1, 34).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.tableWidget.setItem(2, 34, QTableWidgetItem("УВ"))
        self.tableWidget.item(2, 34).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tableWidget.item(2, 34).setFlags(QtCore.Qt.ItemFlag.ItemIsEnabled)
        self.tableWidget.setItem(2, 35, QTableWidgetItem("НЕУВ"))
        self.tableWidget.item(2, 35).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tableWidget.item(2, 35).setFlags(QtCore.Qt.ItemFlag.ItemIsEnabled)

        self.tableWidget.setItem(2, 33, QTableWidgetItem(str(self.manager_students.get_statistics()['all_hours'])))

        self.tableWidget.setItem(1, 1, QTableWidgetItem("ФИО"))
        fio = self.tableWidget.item(1, 1)
        fio.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        fio.setFlags(QtCore.Qt.ItemFlag.ItemIsEnabled)
        self.tableWidget.setItem(1, 33, QTableWidgetItem("Итог"))
        result_up = self.tableWidget.item(1, 33)
        result_up.setFlags(QtCore.Qt.ItemFlag.ItemIsEnabled)

        for i in range(2, 32 + 1):
            if i - 1 in self.manager_students.days:
                self.tableWidget.setItem(1, i, QTableWidgetItem(
                    str(self.manager_students.days[i - 1] if self.manager_students.days[i - 1] else '')))
            else:
                self.tableWidget.setItem(1, i, QTableWidgetItem(str('✖')))
                self.tableWidget.item(1, i).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.tableWidget.item(1, i).setBackground(QtGui.QColor(220, 220, 220))
                self.tableWidget.item(1, i).setFlags(QtCore.Qt.ItemFlag.ItemIsEnabled)
                try:
                    for j in range(2, self.tableWidget.rowCount()):
                        self.tableWidget.setItem(j, i, QTableWidgetItem(""))
                        self.tableWidget.item(j, i).setBackground(QtGui.QColor(220, 220, 220))
                        self.tableWidget.item(j, i).setFlags(QtCore.Qt.ItemFlag.ItemIsEnabled)

                except BaseException as f:
                    print(f)
            self.tableWidget.setItem(2, i, QTableWidgetItem(str(i - 1)))
            self.tableWidget.item(2, i).setFlags(QtCore.Qt.ItemFlag.ItemIsEnabled)
            if not i - 1 in self.manager_students.days:
                self.tableWidget.item(2, i).setBackground(QtGui.QColor(220, 220, 220))
            self.tableWidget.setColumnWidth(i, 10)

        for i, student in enumerate(self.manager_students.students):
            i += 3

            self.tableWidget.setItem(i, 1, QTableWidgetItem(student.create_shorts_fio(student.fio)))
            self.tableWidget.item(i, 1).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            self.tableWidget.item(i, 1).setFlags(QtCore.Qt.ItemFlag.ItemIsEnabled)
            self.tableWidget.setItem(i, 0, QTableWidgetItem(str(i - 2)))
            self.tableWidget.setItem(i, 34, QTableWidgetItem(str(i - 2)))
            self.tableWidget.setItem(i, 35, QTableWidgetItem(str(i - 2)))
            self.tableWidget.setRowHeight(i, 5)
            for s_d in student.sick_days:
                self.tableWidget.setItem(i, s_d + 1, QTableWidgetItem(''))
                self.add_hours_in_table(i, s_d + 1, str(student.sick_days.get(s_d)), type_day='s')

            for a_d in student.absence_days:
                self.tableWidget.setItem(i, a_d + 1, QTableWidgetItem(''))
                self.add_hours_in_table(i, a_d + 1, str(student.absence_days.get(a_d)), type_day='a')
            self.update_statistics_student(i)

    def click_list(self, listwidget):
        self.fio_edit.setText(' '.join(listwidget.currentItem().text().split()[1:]))

    def save_student(self):
        self.message_students.setText('')
        try:
            self.manager_students.CLASS_STUDENT.chech_fio(self.fio_edit.text())
        except BaseException as f:
            self.message_students.setText(str(f))
        else:

            self.manager_students.students[
                self.listWidget.row(self.listWidget.currentItem())].fio = self.fio_edit.text()
            self.update_list_students()
            self.update_table_students()

    def del_student(self):
        if self.listWidget.currentItem():
            message_main = QtWidgets.QMessageBox().question(self, "Удаление студента",
                                                            str(f'Вы точно хотите навсегда удалить студента {" ".join(self.listWidget.currentItem().text().split()[1:])}?'),
                                                            QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
            if message_main == message_main.Yes:
                self.manager_students.remove_student_id(self.listWidget.row(self.listWidget.currentItem()))
                self.listWidget.removeItemWidget(self.listWidget.currentItem())
                self.update_list_students()
                self.update_table_students()

        if len(self.manager_students.students) == 0:
            self.students.setEnabled(False)
            self.save_to_exel_push.setEnabled(False)
        self.update_statistics()

    def del_user(self):
        message = QtWidgets.QMessageBox.question(self, 'Удаление пользователя', "Вы точно хотите удалить свой аккаунт?",
                                                 QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
        if message == message.Yes:
            USER_MANAGER.del_user()
            self.status = 2
            self.close()

    def check_value(self, tablewidget):

        if len(self.manager_students.students) != 0:
            self.students.setEnabled(True)
            self.save_to_exel_push.setEnabled(True)

        item = tablewidget.currentItem()
        if not item is None:
            try:
                if item.row() == 1 and 2 <= item.column() <= 32:
                    if item.text() == '' or item.text() == ' ':
                        if self.manager_students.days.get(item.column() - 1):
                            self.manager_students.days[item.column() - 1] = 0
                        item.setText('')
                    elif item.text().isnumeric() and 0 <= int(item.text()) <= 8:
                        self.manager_students.add_hours_by_day(item.column() - 1, int(item.text()))
                    else:
                        item.setText(str(self.manager_students.days.get(item.column() - 1, '')))
                    self.update_hours_day()

                elif 32 >= item.column() >= 2 and len(self.manager_students.students) + 2 >= item.row() >= 2:
                    if item.text() == '' or item.text() == ' ':
                        if item.column() - 1 in self.manager_students.students[item.row() - 3].absence_days:
                            del self.manager_students.students[item.row() - 3].absence_days[item.column() - 1]
                        if item.column() - 1 in self.manager_students.students[item.row() - 3].sick_days:
                            del self.manager_students.students[item.row() - 3].sick_days[item.column() - 1]
                        item.setBackground(QtGui.QColor(255, 255, 255))

                    elif item.text().isnumeric() and 0 < int(item.text()) <= 8:
                        if self.is_sick_rb.isChecked():
                            if item.column() - 1 in self.manager_students.students[item.row() - 3].absence_days:
                                del self.manager_students.students[item.row() - 3].absence_days[item.column() - 1]
                            self.manager_students.add_day(
                                self.manager_students.students[item.row() - 3],
                                item.column() - 1,
                                int(item.text()),
                                type_day='S',
                            )
                            self.add_hours_in_table(item.row(), item.column(), item.text(), type_day='s')
                        else:
                            if item.column() - 1 in self.manager_students.students[item.row() - 3].sick_days:
                                del self.manager_students.students[item.row() - 3].sick_days[item.column() - 1]
                            self.manager_students.add_day(
                                self.manager_students.students[item.row() - 3],
                                item.column() - 1,
                                int(item.text()),
                                type_day='A',
                            )

                            self.add_hours_in_table(item.row(), item.column(), item.text(), type_day='a')

                    else:
                        if self.manager_students.students[item.row() - 3].sick_days.get(item.column() - 1, ''):
                            item.setText(str(
                                self.manager_students.students[item.row() - 3].sick_days.get(item.column() - 1, '')))
                        elif self.manager_students.students[item.row() - 3].absence_days.get(item.column() - 1, ''):
                            item.setText(str(
                                self.manager_students.students[item.row() - 3].absence_days.get(item.column() - 1, '')))
                        else:
                            item.setText('')
                    self.update_statistics_student(item.row())

                elif item.column() == 1:
                    if item.row() == len(self.manager_students.students) + 3:
                        try:
                            self.manager_students.CLASS_STUDENT.chech_fio(item.text())
                        except BaseException:
                            item.setText('')
                        else:
                            try:
                                self.manager_students.add_student(self.manager_students.CLASS_STUDENT(item.text()))
                                self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
                                for i in range(2, 32 + 1):
                                    if not i - 1 in self.manager_students.days:
                                        self.tableWidget.setItem(self.tableWidget.rowCount() - 2, i,
                                                                 QTableWidgetItem(""))
                                        self.tableWidget.item(self.tableWidget.rowCount() - 2, i).setBackground(
                                            QtGui.QColor(220, 220, 220))
                                        self.tableWidget.item(self.tableWidget.rowCount() - 2, i).setFlags(
                                            QtCore.Qt.ItemFlag.ItemIsEnabled)

                            except BaseException as f:
                                print(f)
                            else:
                                self.update_table_students()
                                self.update_list_students()

            except BaseException as f:
                print(f)
            self.update_statistics()


class Push(QtWidgets.QPushButton):
    def __init__(self, parent, base_weight, base_height, growth):
        super().__init__()
        self.base_height = base_height
        self.base_weight = base_weight
        self.growth = growth
        self.setIconSize(QtCore.QSize(self.base_weight, self.base_height))


    def enterEvent(self, e):
        self.setIconSize(QtCore.QSize(self.base_weight + self.growth, self.base_height + self.growth))

    def leaveEvent(self, e):
        self.setIconSize(QtCore.QSize(self.base_weight, self.base_height))


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
            self.main.init_students_manager()
            self.main.show()
        elif self.auth.status == 3:
            self.regist.show()
        else:

            self.auth.close()
        self.auth.status = 0

    def close_event_by_main(self, e):
        if self.main.status == 2:
            self.auth.update_users()
            self.auth.show()
        elif self.auth.status == 3:
            self.regist.show()
        else:
            self.main.close()
            message = QtWidgets.QMessageBox.question(windows.main, 'Сохранение изменений', "Сохронить изменения?",
                                                     QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
            if message == message.Yes:
                windows.main.save_table()

        self.main.status = 0

    def close_event_by_regist(self, e):
        if self.regist.status == 1:
            self.main.init_students_manager()
            self.main.show()
        elif self.regist.status == 2:
            self.auth.update_users()
            self.auth.show()
        else:
            self.regist.close()
        self.regist.status = 0

    def show(self):

        if USER_MANAGER.users_id:
            self.auth.show()
        else:
            self.regist.show()


is_work = True
is_new_user = False
dirname, filename = os.path.split(os.path.abspath(__file__))


BASE_PATH = dirname
DOCUMENTS_PATH = os.path.expanduser("~/F6")
PACH_SAVE_F6 = DOCUMENTS_PATH
BD_PATH = os.path.join(DOCUMENTS_PATH, 'BD')
if not os.path.exists(os.path.join(DOCUMENTS_PATH, 'BD')):
    os.makedirs(os.path.join(DOCUMENTS_PATH, "BD"))

USER_MANAGER = UserManager(BD_PATH)


app = QtWidgets.QApplication(sys.argv)


windows = ControlerWindows(SplashScreen, Auth, Regist, MainWindow)
windows.show()

status = app.exec()


print(status, '-')
sys.exit(status)