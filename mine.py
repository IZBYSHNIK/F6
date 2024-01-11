# Copyright 2024 Degtyarev Ivan

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import datetime
import json
import os


from StudentsManager import ManagerStudents, Student
from UserManager import UserManager, User


class Commands:
    def __init__(self, manager_students, manager_user):
        self.today = datetime.datetime.today()
        self.manager = manager_students
        self.manager_user = manager_user
        self.commands = {
            'Добавление студентов': self.add_student,
            'Удоление студентов': self.remove_student,
            'Просмотреть список студентов': self.get_students,
            'Вывод Ф6': self.save_f6,
            'Изменить период': self.set_period,
            'None2': None,
            'Заполнение текущего рабочего дня': self.add_work_day,
            'Заполнение пропущенного рабочего дня': self.add_last_day,
            'Показать статистику по студенту': self.get_statistic,
            'Создание нового пользователя': self.register_user,
            'Завершение работы': lambda: 'end',
            'Удалить пользователя': self.del_user,
        }

    def set_period(self):
        self.manager.set_period(int(input('M')), int(input('Y')))

    def add_student(self):
        try:
            student = Student(input("Введите ФИО студента: "))
            self.manager.add_student(student)
        except Exception as exc:
            print('Произошла ошибка, повторите попытку!', exc)
        else:
            print(f'Студент {student.fio}, успешно добавлен!')
            return student

    def del_user(self):
        answer = input('Вы точно хотите удалить аккаунт? (Y\\n): ')
        if answer == 'Y':
            self.manager_user.del_user()
        return answer == 'Y'

    def remove_student(self):
        print('Введите номер студента из списка')
        students = self.get_students()

        try:
            id_s = int(input())
            student = students[id_s-1]
            self.manager.remove_student_obj(student)
        except BaseException:
            print('Удаление завершилось с ошибкой')
        else:
            print(f'Студент {student.fio}, успешно удален!')

    def get_students(self):
        print(f'Список студентов:')
        students = self.manager.students
        for i in range(len(students)):
            print(i+1, students[i].fio)
        return students

    def get_statistic(self):
        print(self.manager.students[int(input('Введите номер студента из списка:')) - 1].get_statistic_for_student())

    def add_work_day(self):
        students = self.get_students()

        if students:
            print('Сегодня', self.today)
            id_s = [int(i)-1 for i in input('Введите номера студентов у которых прогул (через пробел без запятых): ').split()]
            for i in id_s:
                print(f'\t*Студент {students[i].fio}')

                students[i].add_absence_day(self.today.day, int(input('Введите общее время прогулов')))

            id_s = [int(i) - 1 for i in
                    input('Введите номера студентов которые на больничном (через пробел без запятых): ').split()]
            for i in id_s:
                print(f'\t*Студент {students[i].fio}')
                students[i].add_sick_day(self.today.day, int(input('Введите общее время прогулов')))
        else:
            print('Список студентов пуст')

    def add_last_day(self):
        students = self.get_students()

        if students:
            day = int(input("Введите номер дня: "))
            hours = int(input('Введите число часов за этот день: '))
            self.manager.add_hours_by_day(day, hours)
            id_a = [int(i) - 1 for i in
                    input('Введите номера студентов у которых прогул (через пробел без запятых): ').split()]
            for i in id_a:
                print(f'\t*Студент {students[i].fio}')
                self.manager.add_day(students[i], day, int(input('Введите время прогулов: ')), type_day='A')

            id_s = [int(i) - 1 for i in
                    input('Введите номера студентов которые на больничном (через пробел без запятых): ').split()]
            for i in id_s:
                print(f'\t*Студент {students[i].fio}')
                self.manager.add_day(students[i], day, int(input('Введите время прогулов: ')), type_day='S')
        else:
            print('Список студентов пуст')

    def save_f6(self):
        name_file = input('Введите названия сохроняемого файла')
        if not name_file.endswith('.xlsx'):
            name_file += '.xlsx'
        self.manager.save_f6(file_name=os.path.join(PACH_SAVE_F6, name_file))


    @staticmethod
    def register_user(path):
        print('Регистрация')
        user = User(input("Введите имя: "), input('Введите пароль:'))
        user_manager = UserManager(path)
        user_manager.link_user_by_obj(user)
        student_manager = ManagerStudents(input('Введите специальность:'), input('Введите группу:'),  tuple(map(int, input('Введите месяц и год').split())), user)

        user_manager.save_users()
        user.save_user()
        student_manager.save_students()

        return user_manager, student_manager



VERSION = '1.0.6'




is_work = True
is_new_user = False
dirname, filename = os.path.split(os.path.abspath(__file__))


BASE_PATH = dirname
DOCUMENTS_PATH = os.path.expanduser("~/F6")
PACH_SAVE_F6 = DOCUMENTS_PATH
BD_PATH = os.path.join(DOCUMENTS_PATH, 'BD')
if not os.path.exists(os.path.join(DOCUMENTS_PATH, 'BD')):
    os.makedirs(os.path.join(DOCUMENTS_PATH, "BD"))

IS_REGISTER = False
IS_AUTH = False
IS_USER_DELITE = False

print('Добро пожаловать в F6!')
while is_work:
    if os.path.exists(BD_PATH):
        user_manager = UserManager(BD_PATH)

        if len(user_manager.users_id) >= 1 or IS_REGISTER:
            for i, _id in enumerate(user_manager.users_id):
                print(i, user_manager.users_id[_id])
            while True:
                answer = input('Выберите номер пользователя(или зарегестрируйтесь, для этого укажите символ Y): ')
                if answer.isnumeric():
                    if len(user_manager.users_id) > int(answer) >= 0:
                        user_manager.link_user_by_pk(int(answer))
                        break
                elif answer.lower() == 'y':
                    new_user = True
                    um, sm = Commands.register_user(BD_PATH)
                    user_manager = um
                    manager = sm
                    break
                else:
                    print('Введен не корректный ответ, повторите попытку')
        else:
            new_user = True
            um, sm = Commands.register_user(BD_PATH)
            user_manager = um
            manager = sm
        IS_AUTH = True
        user = user_manager.user

        if not is_new_user:
            with open(os.path.join(user.path, 'students.json'), 'r') as s:
                manager = ManagerStudents.load_manager_students(user)


        if not is_new_user:
            print(f'С возвращением, {user.username}!')
            print('Что на этот раз будем делать?')
        else:
            print(f'С чего хотите начать работу?')

        comms = Commands(manager, user_manager)

        while is_work:
            commands_lst = list(comms.commands.keys())
            print('-'*10)
            for i in range(len(commands_lst)):
                print(str(i), commands_lst[i])
            print('-'*10)

            number = input()
            if number.isnumeric() and 0 <= int(number) <= len(commands_lst):
                number = int(number)
            else:
                continue

            result = comms.commands[commands_lst[number]]

            if number == 9:
                IS_REGISTER = True
            elif number == 11:
                IS_USER_DELITE = True
            else:
                result = result()

            if result == 'end':
                user_manager.save_users()
                manager.save_students()
                user.save_user()
                is_work = False

            elif IS_USER_DELITE:
                if comms.del_user():
                    print('Пользователь успешно удален!')
                    break

            elif IS_REGISTER or not IS_AUTH:
                user_manager.save_users()
                manager.save_students()
                user.save_user()
                break
            else:
                input('Нажмите Enter для продолжения')

    else:
        Commands.register_user(BD_PATH)

print('Удачного дня!', 'Завершение работы.', sep='\n')