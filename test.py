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

import unittest

from  StudentsManager import Student, ManagerStudents



class TestStudent(unittest.TestCase):
    def setUp(self):
        self.student = Student('Конев Олег Филипович')

    def test_check_fio_p(self):
        TEST_MASSIV = {
            'алекСеев Максим МаКСиМОВИч': 'Алексеев Максим Максимович',
            'Фролов константин олегович': 'Фролов Константин Олегович',
            'АнДрОпОв ксенон    Анатольевич': 'Андропов Ксенон Анатольевич',
        }
        for key, value in TEST_MASSIV.items():
            self.assertEqual(Student.check_fio(key), value)

    def test_check_fio_n(self):
        TEST_MASSIV = {
            'Фролов константинолегович': ValueError,
            'Фролов константин олегович-робентроп': ValueError,
            'Фро*лов конс!тантин олег№ович': ValueError,
            '5ролов константин олегович': ValueError,
            'олов  олегович': ValueError,
            '5рололегович': ValueError,
            "@@@### $$$#@@ &&%&$^&*#": ValueError,
        }
        for key, value in TEST_MASSIV.items():
            with self.assertRaises(value):
                Student.check_fio(key)

    def test_is_valud_fio_p(self):
        TEST_MASSIV = [
            'алекСеев Максим МаКСиМОВИч',
            'Фролов константин олегович',
            'АнДрОпОв ксенон Анатольевич',
            'sdfhsd dfdf dfsdfs',
        ]
        for k in TEST_MASSIV:
            t1 = Student.is_valud_fio(k)
            self.assertTrue(Student.is_valud_fio(k))

    def test_is_valud_fio_n(self):
        TEST_MASSIV = [
            'Фролов константинолегович',
            'Фролов константин олегович-робентроп',
            'Фро*лов конс!тантин олег№ович',
            '5ролов константин олегович',
            'фролов костя   ',
            '666',
        ]
        for k in TEST_MASSIV:
            t1 = Student.is_valud_fio(k)
            self.assertFalse(Student.is_valud_fio(k))

    def test_check_day_p(self):
        TEST_MASSIV = {
            1: 1,
            20: 20,
            10: 10,
            31: 31,
            15: 15,

        }
        for k, v in TEST_MASSIV.items():
            self.assertEqual(k, v)

    def test_check_day_n(self):
        TEST_MASSIV = {
            0: ValueError,
            32: ValueError,
            33: ValueError,
            -1: ValueError,
            -20: ValueError,
            -45: ValueError,
            55: ValueError,
            -10: ValueError,
        }
        for k, v in TEST_MASSIV.items():
            with self.assertRaises(v):
                Student.check_day(k)

    def test_is_valud_day_p(self):
        TEST_MASSIV = [1, 31, 30, 15, 10,]
        for k  in TEST_MASSIV:
            self.assertTrue(Student.check_day(k))

    def test_is_valud_day_n(self):
        TEST_MASSIV = [
            0,
            32,
            33,
            -1,
            -20,
            -45,
            55,
            -10,
        ]
        for k in TEST_MASSIV:
            self.assertFalse(Student.is_valud_day(k))

    def test_create_shorts_fio_p(self):
        TEST_MASSIV = {
            "александро анатолий Фларинович": 'Александро А. Ф.',
            "семЕнЧюк ЮсУп анатольевич":  'Семенчюк Ю. А.',
            "Афанасьев Павел Иванович": "Афанасьев П. И.",
            "ФРОЛОВ антон РАХМАТУЛЛА": "Фролов А. Р.",

        }
        for k, v in TEST_MASSIV.items():
            self.assertEqual(Student.create_shorts_fio(k), v)

    def test_create_shorts_fio_n(self):
        TEST_MASSIV = {
            "александро анат5лий Фларинович": ValueError,
            "семЕнЧюк анатольевич":  ValueError,
            "Афанасьев! Павел! Иванович!": ValueError,
            "ФРОЛОВРАХМАТУЛЛА": ValueError,

        }
        for k, v in TEST_MASSIV.items():
            with self.assertRaises(v):
                Student.create_shorts_fio(k)

    def test_add_sick_day_p(self):
        TEST_MASSIV = {
            5: 6,
            1: 10,
            31: 2,
            3: 0,
            15: 1,

        }


        for k, v in TEST_MASSIV.items():
            self.student.add_sick_day(k, v)
        self.assertDictEqual(self.student.sick_days, {5: 6, 1: 10, 31: 2, 3: 0, 15: 1, })

    def test_add_sick_day_n(self):
        TEST_MASSIV = {
            5: 11,
            32: 2,
            -5: 1,

        }


        for k, v in TEST_MASSIV.items():
            with self.assertRaises(ValueError):
                self.student.add_sick_day(k, v)
        self.assertDictEqual(self.student.sick_days, {})

    def test_add_absence_day_p(self):
        TEST_MASSIV = {
            5: 6,
            1: 10,
            31: 2,
            15: 1,

        }


        for k, v in TEST_MASSIV.items():
            self.student.add_absence_day(k, v)
        self.assertDictEqual(self.student.absence_days, {5: 6, 1: 10, 31: 2, 15:1, })

    def test_add_absence_day_n(self):
        TEST_MASSIV = {
            5: 11,
            32: 2,
            -5: 1,

        }


        for k, v in TEST_MASSIV.items():
            with self.assertRaises(ValueError):
                self.student.add_absence_day(k, v)
        self.assertDictEqual(self.student.absence_days, {})

    def test_add_day_p(self):
        TEST_MASSIV = {
            (5, 6): 's',
            (1, 10): 'a',
            (31, 2): 'S',
            (15, 1): 'a',
            (6, 7): 's',
            (2, 10): 'a',
            (17, 4): 'S',
            (31, 3): 'a',

        }

        for k, v in TEST_MASSIV.items():
            self.student.add_day(k[0], k[1], v)
        self.assertDictEqual(self.student.sick_days, {5: 6, 31: 2, 6: 7, 17: 4,})
        self.assertDictEqual(self.student.absence_days, {1: 10,15: 1, 2: 10, 31:3,})

    def test_add_day_n(self):
        TEST_MASSIV = {
            (5, 11): 's',
            (1, 0): 'a',
            (32, 5): 'S',
            (0, 15): 'a',
            (40, 10): 's',
            (2, 20): 'a',
            (17, -2): 'S',
            (31, -3): 'a',

        }
        with self.assertRaises(ValueError):
            for k, v in TEST_MASSIV.items():
                self.student.add_day(k[0], k[1], v)

    def test_init_p(self):
        TEST_MASSIV = {
            'фролов генадий генадевич': [{1: 2, 10: 5, 21: 5, 31: 10}, {}],
            'кузьма филипп филиппович': [{1: 2, 10: 5, 21: 5, 31: 10}, {11: 6, 12: 8, 25: 5, 30: 10}],
            'фролов генадий генадевич': [{}, {1: 2, 10: 5, 21: 5, 31: 10}],
            'кузьма филипп филиппович': [{}, {}],
        }
        for k, v in TEST_MASSIV.items():
            s = Student(k, *v)
            self.assertListEqual([s.sick_days, s.absence_days], v)

    def test_init_n(self):
        TEST_MASSIV = {
            'фролов генадий генадевич': [{1: 20, 10: 5, 21: 5, 31: 10}, {}],
            'кузьма филипп филиппович': [{1: 2, 33: 5, 21: 5, 31: 10}, {11: 6, 12: 8, 25: 5, 30: 10}],
            'фролов генадий генадевич': [{'fgdgf'}, {1: 2, 10: 5, 21: 5, 31: 10}],
            'кузьма филипп филиппович': [{}, {'2': '8'}],
        }
        for k, v in TEST_MASSIV.items():
            with self.assertRaises(ValueError):
                s = Student(k, *v)


class TestManagerStudents(unittest.TestCase):
    def setUp(self):
        self.manager = ManagerStudents([1, 2020], user=None)

    def test_generate_work_days_p(self):
        TEST_MASSIV = {
            (1, 2017): {
                        11: 0,
                        12: 0,
                        13: 0,
                        16: 0,
                        17: 0,
                        18: 0,
                        19: 0,
                        20: 0,
                        23: 0,
                        24: 0,
                        25: 0,
                        26: 0,
                        27: 0,
                        30: 0,
                        31: 0,
            },
            (1, 2000): {
                11: 0,
                12: 0,
                13: 0,
                14: 0,
                17: 0,
                18: 0,
                19: 0,
                20: 0,
                21: 0,
                24: 0,
                25: 0,
                26: 0,
                27: 0,
                28: 0,
                31: 0,
            },
            (2, 2022): {
                1: 0,
                2: 0,
                3: 0,
                4: 0,
                7: 0,
                8: 0,
                9: 0,
                10: 0,
                11: 0,
                14: 0,
                15: 0,
                16: 0,
                17: 0,
                18: 0,
                21: 0,
                22: 0,
                24: 0,
                25: 0,
                28: 0,

            },
            (4, 9999): {
                1: 0,
                2: 0,
                5: 0,
                6: 0,
                7: 0,
                8: 0,
                9: 0,
                12: 0,
                13: 0,
                14: 0,
                15: 0,
                16: 0,
                19: 0,
                20: 0,
                21: 0,
                22: 0,
                23: 0,
                26: 0,
                27: 0,
                28: 0,
                29: 0,
                30: 0,

            },
            (12, 1700): {
                1: 0,
                2: 0,
                3: 0,
                6: 0,
                7: 0,
                8: 0,
                9: 0,
                10: 0,
                13: 0,
                14: 0,
                15: 0,
                16: 0,
                17: 0,
                20: 0,
                21: 0,
                22: 0,
                23: 0,
                24: 0,
                27: 0,
                28: 0,
                29: 0,

            },
        }
        for k, v in TEST_MASSIV.items():
            self.assertDictEqual(ManagerStudents.generate_work_days(k[0], k[1]), v)

    def test_generate_work_days_n(self):
        TEST_MASSIV = {
            (1, 1699): {
                        11: 0,
                        12: 0,
                        13: 0,
                        16: 0,
                        17: 0,
                        18: 0,
                        19: 0,
                        20: 0,
                        23: 0,
                        24: 0,
                        25: 0,
                        26: 0,
                        27: 0,
                        30: 0,
                        31: 0,
            },
            (-1, 2000): {
                11: 0,
                12: 0,
                13: 0,
                14: 0,
                17: 0,
                18: 0,
                24: 0,
                25: 0,
                26: 0,
                27: 0,
                28: 0,
                31: 0,
            },
            (0, 2022): {
                1: 0,
                2: 0,
                3: 0,
                25: 0,
                28: 0,

            },
            (13, 9999): {
                1: 0,
                2: 0,
                5: 0,
                6: 0,
                7: 0,
                8: 0,
                9: 0,
                12: 0,
                13: 0,
                14: 0,
                15: 0,
                16: 0,
                19: 0,
                20: 0,
                21: 0,
                22: 0,
                23: 0,
                26: 0,
                27: 0,
                28: 0,
                29: 0,
                30: 0,

            },
            (12, 10): {
                1: 0,
                2: 0,
                3: 0,
                6: 0,
                7: 0,
                8: 0,
                9: 0,
                10: 0,
                13: 0,
                14: 0,
                15: 0,
                16: 0,
                17: 0,
                20: 0,
                21: 0,
                22: 0,
                23: 0,
                24: 0,
                27: 0,
                28: 0,
                29: 0,

            },
        }
        for k, v in TEST_MASSIV.items():
            with self.assertRaises(ValueError):
                ManagerStudents.generate_work_days(k[0], k[1])

    def test_set_period_p(self):
        TEST_MASSIV = [
            (1, 1900), (1, 1800), (1, 9999)
        ]
        for i in TEST_MASSIV:
            period = self.manager.period
            self.manager.set_period(*i)
            self.assertEqual(self.manager.period, i)

    def test_set_period_n(self):
        TEST_MASSIV = [
            (1, '1900'), (1, 1699), (-1, 10000), ('dsfjsf', 'fdsf'),
        ]
        for i in TEST_MASSIV:
            period = self.manager.period
            with self.assertRaises(ValueError):
                self.manager.set_period(*i)

    def test_on_day_p(self):
        TEST_MASSIV = [(1, 6), (2, 0), (31, 6), (1, 10), (2, 0), (31, 5)]
        for k, v in TEST_MASSIV:
            self.manager.on_day(k, v)
            self.assertIn(k, self.manager.days)
            self.assertEqual(v, self.manager.days[k])

    def test_on_day_n(self):
        TEST_MASSIV = [(1, 11), (32, 0), ('31', 6), (1, '10'), (2, 1.6), (-31, 5)]

        for k, v in TEST_MASSIV:

            with self.assertRaises(ValueError):
                self.manager.on_day(k, v)

    def test_off_day_p(self):
        TEST_MASSIV = [1, 2, 31, 1, 2, 31]
        for k in TEST_MASSIV:
            self.manager.off_day(k)
            self.assertNotIn(k, self.manager.days)

    def test_off_day_n(self):
        TEST_MASSIV = [33, -10, '31', '10', 1.6, -31, 0]
        for k in TEST_MASSIV:

            with self.assertRaises(ValueError):
                self.manager.off_day(k)












