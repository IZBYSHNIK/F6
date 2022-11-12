import datetime
import json
import os
import sys

from PyQt6.QtGui import QIcon
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import (
    QApplication, QWidget, QTableWidget,
    QTableWidgetItem, QVBoxLayout, QHeaderView
)
from StudentsManager import ManagerStudents, Student
from UserManager import UserManager, User


VERSION = '1.0.7'




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


class Regist(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QtGui.QIcon('media\\logo.ico'))
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
        self.message_regist.setGeometry(40, 550+30, 351, 41)
        self.message_regist.setStyleSheet('border: none; color: red; font: 14px; background-color: rgba(249, 248, 244, 0);')

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

        self.obj_auth = None


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
        self.password_lable_2.setText(_translate("Regist", "*Повториет пароль"))
        self.teamleader_lable.setText(_translate("Regist", "ФИО Кл.руководителя"))
        self.office_name_lable.setText(_translate("Regist", "Свое ФИО"))
        self.email_lable.setText(_translate("Regist", "Почтовый адрес для востановления"))

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

        return self.login_edit.text(), self.password_edit.text(), {'offical_name': None if not self.office_name_edit.text() else self.office_name_edit.text(),
                                                                   'teamleader': None if not self.teamleader_edit.text() else self.teamleader_edit.text()}

    def click_create_push(self):
        self.message_regist.setText('')
        try:
            username, password, kwargs = self.check_lables()
            USER_MANAGER.link_user_by_obj(USER_MANAGER.USER_CLASS(username, password, kwargs))
            USER_MANAGER.save_users()
            self.obj_auth.spin_box.addItem(QIcon('0'),  username)
            self.click_cancel_push()
        except BaseException as message:
            self.message_regist.setText('*'+str(message))

    def click_cancel_push(self):
        self.close()
        self.obj_auth.show()


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        # self.setStyleSheet('QPushButton#game_over_push:hover {filter: invert(42%) sepia(93%) saturate(1352%) hue-rotate(87deg) brightness(119%) contrast(119%);}')
        self.setWindowIcon(QtGui.QIcon('media\\logo.ico'))
        self.init_students_manager()
        self.setObjectName("MainWindow")
        self.resize(1002, 787)
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
        self.is_sick_rb.setChecked(True)
        self.horizontalLayout_4.addWidget(self.is_sick_rb)
        self.radioButton_2 = QtWidgets.QRadioButton(self.frame)
        self.radioButton_2.setObjectName("radioButton_2")
        self.horizontalLayout_4.addWidget(self.radioButton_2)

        self.horizontalLayout_2.addLayout(self.horizontalLayout_4)
        self.game_over_push = QtWidgets.QPushButton(self.frame)
        self.game_over_push.setObjectName("game_over_push")
        self.game_over_push.setIcon(QIcon('media\\game_over.svg'))
        self.game_over_push.setIconSize(QtCore.QSize(40, 40))
        self.game_over_push.setStyleSheet('#game_over_push {border: none;} #game_over_push:hover {background: rgb(0,0,0); margin: 31px; border-radius: 2px;}')
        self.game_over_push.setMinimumSize(40, 40)
        self.game_over_push.setToolTip('Завершить текущий месяц')
        self.horizontalLayout_2.addWidget(self.game_over_push)


        self.save_to_exel_push = QtWidgets.QPushButton(self.frame)
        self.save_to_exel_push.setObjectName("save_to_exel_push")
        self.save_to_exel_push.setIcon(QIcon('media\\save_exel.svg'))
        self.save_to_exel_push.setIconSize(QtCore.QSize(35, 35))
        self.save_to_exel_push.setToolTip('Сохронить в EXEL')
        self.save_to_exel_push.setMinimumSize(35, 35)

        self.horizontalLayout_2.addWidget(self.save_to_exel_push)
        self.horizontalLayout_3.addLayout(self.horizontalLayout_2)
        self.verticalLayout_3.addWidget(self.frame)
        self.verticalLayout.addLayout(self.verticalLayout_3)


        self.tableWidget = self.generate_table()

        self.tableWidget.setObjectName("tableView")
        self.verticalLayout.addWidget(self.tableWidget)
        self.tableWidget.cellChanged.connect(lambda: self.check_value(self.tableWidget))




        self.group.addTab(self.F6, "")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.group.addTab(self.tab, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")

        self.group.addTab(self.tab_3, "")
        self.verticalLayout_2.addWidget(self.group)
        self.setCentralWidget(self.centralwidget)
        self.action_2 = QtGui.QAction(self)
        self.action_2.setObjectName("action_2")

        self.retranslateUi()
        self.group.setCurrentIndex(2)
        QtCore.QMetaObject.connectSlotsByName(self)

        self.save_to_exel_push.clicked.connect(self.save_to_exel)



    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_2.setText(_translate("MainWindow", f"Добро пожаловать, {USER_MANAGER.user.username}!"))
        self.is_sick_rb.setText(_translate("MainWindow", "ПОУВ"))
        self.radioButton_2.setText(_translate("MainWindow", "НЕУВ"))
        # self.game_over_push.setText(_translate("MainWindow", "game_over_push"))
        # self.save_to_exel_push.setText(_translate("MainWindow", "Сохронить в EXEL"))
        self.group.setTabText(self.group.indexOf(self.F6), _translate("MainWindow", "Ф6"))
        self.group.setTabText(self.group.indexOf(self.tab), _translate("MainWindow", "Page"))
        self.group.setTabText(self.group.indexOf(self.tab_3), _translate("MainWindow", "Page"))
        self.action_2.setText(_translate("MainWindow", "ншнге"))

    def save_to_exel(self):
        self.manager_students.save_f6('beta.xlsx')

    def init_students_manager(self):
        try:
            self.manager_students = ManagerStudents.load_manager_students(USER_MANAGER.user)
        except BaseException as message:
            self.manager_students = ManagerStudents('', '', (datetime.date.today().month, datetime.date.today().year), USER_MANAGER.user)
            self.manager_students.save_students()

    def generate_table(self):
        table = QtWidgets.QTableWidget()

        table.setStyleSheet("""QTableWidget {border: none;}""")

        table.setColumnCount(36)
        table.setRowCount(2 + len(self.manager_students.students)+2)
        table.setColumnWidth(0, 5)
        table.setColumnWidth(33, 50)
        table.setColumnWidth(1, 200)

        table.horizontalHeader().setVisible(False)
        table.verticalHeader().setVisible(False)
        table.setSpan(0, 0, 1, 36)
        table.setSpan(1, 1, 2, 1)
        table.setSpan(34, 2, 1, 1)

        table.setItem(0, 0, QTableWidgetItem("ВЕДОМОСТЬ УЧЁТА ЧАСОВ, ПРОПУЩЕННЫХ СТУДЕНТАМИ"))
        title = table.item(0, 0)
        title.setBackground(QtGui.QColor(153, 153, 153))
        # table.item(0, 0).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        title.setFont(QtGui.QFont('Calibri', 20))
        title.setFlags(QtCore.Qt.ItemFlag.ItemIsEnabled)


        table.setItem(1, 1, QTableWidgetItem("ФИО"))
        fio = table.item(1, 1)
        fio.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        fio.setFlags(QtCore.Qt.ItemFlag.ItemIsEnabled)
        table.setItem(1, 33, QTableWidgetItem("Итог"))
        result_up = table.item(1, 33)
        result_up.setFlags(QtCore.Qt.ItemFlag.ItemIsEnabled)

        for i in range(2, 32 + 1):
            if i-1 in self.manager_students.days:
                table.setItem(1, i, QTableWidgetItem(str(self.manager_students.days[i-1])))
            else:
                table.setItem(1, i, QTableWidgetItem(str('✖')))
                table.item(1, i).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                table.item(1, i).setBackground(QtGui.QColor(220, 220, 220))
                table.item(1, i).setFlags(QtCore.Qt.ItemFlag.ItemIsEnabled)
                try:
                    for j in range(2, table.rowCount()-1):
                        table.setItem(j, i, QTableWidgetItem(""))
                        table.item(j, i).setBackground(QtGui.QColor(220, 220, 220))
                        table.item(j, i).setFlags(QtCore.Qt.ItemFlag.ItemIsEnabled)

                except BaseException as f:
                    print(f)
            table.setItem(2, i, QTableWidgetItem(str(i - 1)))
            table.item(2, i).setFlags(QtCore.Qt.ItemFlag.ItemIsEnabled)
            if not i-1 in self.manager_students.days:
                table.item(2, i).setBackground(QtGui.QColor(220, 220, 220))
            table.setColumnWidth(i, 10)

        for i, student in enumerate(self.manager_students.students):
            i += 3
            table.setItem(i, 1, QTableWidgetItem(student.create_shorts_fio(student.fio)))
            table.item(i, 1).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            table.item(i, 1).setFlags(QtCore.Qt.ItemFlag.ItemIsEnabled)
            table.item(i, 1).setToolTip(f"""
            ФИО: {student.fio};
            Прогулы по неув. причине: {str(i)};
            Прогулы по ув. причине: {'1'}
            """)
            table.setItem(i, 0, QTableWidgetItem(str(i-2)))
            table.setRowHeight(i, 5)

            for s_d in student.sick_days:
                table.setItem(i, s_d+1, QTableWidgetItem(str(student.sick_days.get(s_d))))
                table.item(i, s_d+1).setBackground(QtGui.QColor(51, 204, 0))
                table.item(i, s_d + 1).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

            for a_d in student.absence_days:
                table.setItem(i, a_d+1, QTableWidgetItem(str(student.absence_days.get(a_d))))
                table.item(i, a_d+1).setBackground(QtGui.QColor(255, 102, 51))
                table.item(i, a_d+1).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        return table

    def check_value(self, table):
        item = table.currentItem()
        if not item is None:
            try:
                if item.row() == 1 and 2 <= item.column() <= 32:
                    if item.text().isnumeric() and 0 <= int(item.text()) <= 8:
                        self.manager_students.add_hours_by_day(item.column()-1, int(item.text()))
                    else:
                        item.setText(str(self.manager_students.days.get(item.column()-1, '')))

                elif 32 >= item.column() >= 2 and len(self.manager_students.students)+2 >= item.row() >= 2:
                    if item.text() == '' or item.text() == ' ':
                        if item.column() - 1 in self.manager_students.students[item.row() - 3].absence_days:
                            del self.manager_students.students[item.row() - 3].absence_days[item.column() - 1]
                        if item.column() - 1 in self.manager_students.students[item.row() - 3].sick_days:
                            del self.manager_students.students[item.row() - 3].sick_days[item.column() - 1]
                        item.setBackground(QtGui.QColor(255, 255, 255))

                    elif item.text().isnumeric() and 0 < int(item.text()) <= 8:
                        if self.is_sick_rb.isChecked():
                            if item.column() - 1 in self.manager_students.students[item.row()-3].absence_days:
                                del self.manager_students.students[item.row()-3].absence_days[item.column() - 1]
                            self.manager_students.add_day(
                                self.manager_students.students[item.row()-3],
                                item.column() - 1,
                                int(item.text()),
                                type_day='S',
                            )
                            self.tableWidget.item(item.row(), item.column()).setBackground(QtGui.QColor(51, 204, 0))
                        else:
                            if item.column() - 1 in self.manager_students.students[item.row()-3].sick_days:
                                del self.manager_students.students[item.row()-3].sick_days[item.column() - 1]
                            self.manager_students.add_day(
                                self.manager_students.students[item.row() - 3],
                                item.column() - 1,
                                int(item.text()),
                                type_day='A',
                            )
                            self.tableWidget.item(item.row(), item.column()).setBackground(QtGui.QColor(255, 51, 51))

                    else:
                        if self.manager_students.students[item.row()-3].sick_days.get(item.column() - 1, ''):
                            item.setText(str(self.manager_students.students[item.row()-3].sick_days.get(item.column() - 1, '')))
                        elif self.manager_students.students[item.row()-3].absence_days.get(item.column() - 1, ''):
                            item.setText(str(self.manager_students.students[item.row() - 3].absence_days.get(item.column() - 1, '')))
                        else:
                            item.setText('')

                elif item.column() == 1:
                    if item.row() == len(self.manager_students.students)+3:
                        try:
                            self.manager_students.CLASS_STUDENT.chech_fio(item.text())
                        except BaseException:
                            item.setText('')
                        else:
                            try:
                                self.manager_students.add_student(self.manager_students.CLASS_STUDENT(item.text()))
                                self.tableWidget.setRowCount(self.tableWidget.rowCount()+1)
                                for i in range(2, 32 + 1):
                                    if not i - 1 in self.manager_students.days:
                                        self.tableWidget.setItem(self.tableWidget.rowCount()-2, i, QTableWidgetItem(""))
                                        self.tableWidget.item(self.tableWidget.rowCount()-2, i).setBackground(QtGui.QColor(220, 220, 220))
                                        self.tableWidget.item(self.tableWidget.rowCount()-2, i).setFlags(QtCore.Qt.ItemFlag.ItemIsEnabled)

                            except BaseException as f:
                                print(f)

            except BaseException as f:
                print(f)

class Auth(QtWidgets.QWidget):
    CLASS_REGIST = Regist
    CLASS_WINDOW = MainWindow

    def __init__(self):
        super(Auth, self).__init__()
        self.setFixedSize(442, 580)
        self.setWindowIcon(QtGui.QIcon('media\\logo.ico'))
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

        self.message_auth.setStyleSheet('border: none; color: red; font: 14px; background-color: rgba(249, 248, 244, 0);')

        self.spin_box = QtWidgets.QComboBox(self)
        self.spin_box.setGeometry(QtCore.QRect(60, 180, 351, 41))
        self.spin_box.setStyleSheet("""QComboBox {color:white;font: 16px;background: black;}\n""")

        for i in USER_MANAGER.users_id:
            self.spin_box.addItem(QIcon('0'),  USER_MANAGER.users_id[i])

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)


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

    def checking_log_password(self):
        USER_MANAGER.USER_CLASS.check_username(self.spin_box.currentText())
        USER_MANAGER.USER_CLASS.check_password(self.password_edit.text())
        return self.spin_box.currentText(), self.password_edit.text()

    def click_auth_push(self):
        try:
            username, password = self.checking_log_password()
        except BaseException as message:
            # self.message = QtWidgets.QMessageBox().critical(self, "Ошибка", str(message), QtWidgets.QMessageBox.StandardButton.Ok)
            self.message_auth.setText('*'+str(message))


        else:
            try:
                USER_MANAGER.link_user_by_username(username, password)
            except BaseException as message:
                self.message_auth.setText('*' + str(message))
            else:
                self.obj_window = self.CLASS_WINDOW()
                self.obj_window.obj_auth = self
                self.close()
                self.obj_window.show()

    def click_regis_push(self):
        self.obj_regist = self.CLASS_REGIST()
        self.obj_regist.obj_auth = self
        self.close()
        self.obj_regist.show()


app = QtWidgets.QApplication(sys.argv)

auth = Auth()
auth.show()

status = app.exec()

try:
    auth.obj_window.manager_students.save_students()
    USER_MANAGER.save_users()
except BaseException as f:
    pass
else:
    pass
print()
sys.exit(status)