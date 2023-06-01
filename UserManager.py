# Copyright 2022 Degtyarev Ivan

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from string import ascii_lowercase
import random
import bcrypt
import os
import json
import shutil


class User:
    LOWER_CASE = ascii_lowercase
    UPPER_CASE = ascii_lowercase.upper()
    NUMBERS = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
    HAPPY_DAYS = {
        '10': [4, ],
        '1': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, ],
        '12': [30, 31, ],
        '2': [23, ],
        '3': [8, ],
        '5': [1, 9, ],



    }

    @staticmethod
    def create_shorts_fio(fio: str) -> str:
        '''Создает сокращенную форму ФИО: ФФФФФФФ И. О., возвращает строку'''
        last_name, first_name, middle_name = fio.title().split()
        return f'{last_name} {first_name[0]}. {middle_name[0]}.'

    def __init__(self, username: str, password: str, parametrs=None, ):
        if parametrs is None:
            parametrs = {}
        self.path = None
        self.username = self.check_username(username)
        self.parametrs = parametrs
        if self.parametrs.get('happy_days'):
            self.happy_days = self.parametrs.get('happy_days')
        else:
            self.happy_days = self.HAPPY_DAYS


        self.user_id = self.generate_user_id() + '_' + username
        self.__password = self.check_password(password)

    @classmethod
    def check_fio(cls, fio: str) -> str:
        """Проверяет правильность ФИО, если все правильно возвращает его, иначе ошибка ValueError"""
        if not fio is None:
            if cls.is_valid_fio(fio):
                return fio
            raise ValueError('ФИО должно состоять только из букв и быть из 3 частей, каждая из которых не менее 2 символов')

    @staticmethod
    def is_valid_fio(fio: str) -> bool:
        return isinstance(fio.replace(' ', ''), str) and sum(
            [item.isalpha() and len(item) >= 2 for item in fio.split()]) == 3

    @property
    def password(self) -> str:
        return self.__password

    @password.setter
    def password(self, new: str) -> None:
        self.check_password(new)
        self.__password = new

    @classmethod
    def check_password(cls, password) -> str:
        """Проверяет пароль на правильность, если все верно, то возвращает его иначе ошибка ValueError"""
        if cls.is_valid_password(password):
            return password
        raise ValueError('Пароль должен быть строкой из 4-30 символов')

    @staticmethod
    def is_valid_password(password: str) -> bool:
        return isinstance(password, str) and 30 >= len(password) >= 4

    @classmethod
    def check_username(cls, username: str) -> str:
        '''Проверяет правильность имени пользователя, если все верно, то возвращает ее, иначе ошибка ValueError'''
        if cls.is_valid_username(username):
            return username
        raise ValueError('Имя пользователя должено быть строкой из 3-20 букв или числовых символов')

    @staticmethod
    def is_valid_username(username: str) -> bool:
        return isinstance(username, str) and 20 >= len(username) >= 3 and username.isalnum()

    @classmethod
    def generate_user_id(cls, len_id: int=8) -> str:
        """Генерирует уникальный идентификатор для пользователя"""
        result = '#'
        for i in range(len_id):
            result += str(random.choice(list(cls.LOWER_CASE+cls.UPPER_CASE)+list(cls.NUMBERS)))
        return result

    def save_user(self, file_name='user.json') -> None:
        self.parametrs['happy_days'] = self.happy_days
        date = {
            "username": self.username,
            "user_id": self.user_id,
            "parametrs": self.parametrs,
            "password": bcrypt.hashpw(self.__password.encode(), bcrypt.gensalt()).decode()
        }
        user_path = os.path.join(self.path, file_name)
        if not os.path.isdir(self.path):
            os.mkdir(self.path)
        with open(user_path, 'w') as f:
            json.dump(date, f)


    @staticmethod
    def load_user(data: dict, password: str):
        '''Создает новый экземпляр класса'''
        new_obj = User(data['username'], password, data['parametrs'])
        new_obj.user_id = data['user_id']
        return new_obj

    def add_achievement(self, coord: tuple) -> None:
        '''
        Добавляет новый кортеж достижений
        (x, y)
        '''
        if not self.parametrs.get('achievements'):
            self.parametrs['achievements'] = []
        self.parametrs['achievements'].append(coord)
        self.save_user()

    def restart_happy_day(self):
        self.happy_days = self.HAPPY_DAYS






class UserManager:
    USER_CLASS = User

    def __init__(self, path: str, parametrs: dict=None):
        self.base_file = 'USERS.json'
        self.path = path
        self.user = None
        self.parametrs = {} if not parametrs else parametrs
        self.users_id = self.load_user_manager(self.base_file)



    def link_user_by_obj(self, obj: User) -> None:
        if isinstance(obj, type(self).USER_CLASS):
            self.user = obj
        user_directory = os.path.join(self.path, f'user_{self.user.user_id}')
        self.user.path = user_directory
        if self.user.user_id not in self.users_id:
            self.users_id[self.user.user_id] = self.user.username

        self.user.save_user()
        self.save_users()

    def link_user_by_pk(self, pk: int) -> None:
        user_id = list(self.users_id)[pk]
        user_directory = os.path.join(self.path, f'user_{user_id}')

        with open(os.path.join(user_directory, 'user.json'), 'r') as u:
            data = json.load(u)
            password = data['password'].encode()
            while True:
                ps_valid = input('Введите пароль: ')
                if bcrypt.checkpw(ps_valid.encode(), password):
                    break

        self.user = type(self).USER_CLASS('None', '12345678').load_user(data, ps_valid)
        self.user.path = user_directory
        if self.user.user_id not in self.users_id:
            self.users_id[self.user.user_id] = self.user.username

    def link_user_by_username(self, username: str, ps: str) -> None:
        user_id = None
        for k, v in self.users_id.items():
            if v == username:
                user_id = k
                break

        if user_id is None:
            raise ValueError(f'Пользователя с именем {username} нет')

        user_directory = os.path.join(self.path, f'user_{user_id}')

        with open(os.path.join(user_directory, 'user.json'), 'r') as u:
            data = json.load(u)
            password = data['password'].encode()

        if bcrypt.checkpw(ps.encode(), password):
            self.user = type(self).USER_CLASS('None', '12345678').load_user(data, ps)
            self.user.path = user_directory
            self.parametrs['LastUser'] = self.user.user_id
            if self.user.user_id not in self.users_id:
                self.users_id[self.user.user_id] = self.user.username
            self.save_users()
        else:
            raise ValueError('Неверный пароль')

    def del_user(self) -> None:
        '''Удаляет папку с файлами пользователя'''
        shutil.rmtree(self.user.path)
        del self.users_id[self.user.user_id]
        self.user = None

    def del_user_by_pk(self, pk: int) -> None:
        del self.users_id[pk]

    def save_users(self, file_name: str='USERS.json') -> None:
        '''Сохраняет файл конфигурации всех пользователей'''
        data = {
            'Users': self.users_id,
            'Parametrs': self.parametrs,
        }
        file_name = os.path.join(self.path, file_name)
        if not os.path.isdir(self.path):
            os.mkdir(self.path)
        with open(file_name, 'w', encoding='UTF-16') as f:
            json.dump(data, f)

    def load_user_manager(self, file_name: str='USERS.json') -> dict:

        file_name = os.path.join(self.path, file_name)
        if os.path.exists(file_name):
            with open(file_name, 'r', encoding='UTF-16') as f:
                data = json.load(f)
        else:
            return {}

        new_list_id_users = list(map(lambda x: '_'.join(x.split('_')[1:]), [i for i in list(os.walk(self.path))[0][1] if i.startswith('user_#')]))
        if not(set(new_list_id_users) == set(data['Users'].keys())):

            for id_ in set(new_list_id_users) - set(data['Users'].keys()):
                user_directory = os.path.join(self.path, f'user_{id_}')
                with open(os.path.join(user_directory, 'user.json'), 'r') as u:
                    data1 = json.load(u)
                data['Users'][id_] = data1['username']



        result = {}
        for _id in data['Users']:
            if os.path.isdir(os.path.join(self.path, f'user_{_id}')):
                result[_id] = data['Users'][_id]
        self.parametrs = data['Parametrs']

        return result

    def update_user_id(self) -> None:
        self.users_id = self.load_user_manager(self.base_file)



