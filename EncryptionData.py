

class EncryptionData:
    SEP = '!'
    def __init__(self, key1, key2):
        self.key1 = key1
        self.key2 = key2


    def encode(self, data: str) -> tuple:
        """
        """
        table, psc, R = self.crate_encryption_table(data)
        result = ''
        for i in data:
            result += table.get(i, '')
        return result, psc, R

    def decode(self, data: str, psc: list) -> str:
        table, psc, R = self.crate_encryption_table(data, psc)
        result = ''
        for i in self.share_data(data, R):
            result += table.get(i, '')
        return result

    @classmethod
    def convert_list_to_str(cls, data:list):
        '''
        Преобразует данные в специальный фармат:
        "#!data[0]!data[1]!data[2]!data[3]! ... ... ... data[n]!data[n+1]!data[n+2]!data[n+3]!#"
        '''
        result = ['#']
        result.extend(data)
        result.append('#')

        return f'{cls.SEP}'.join(result)

    @classmethod
    def convert_str_to_list(cls, data: str) -> list:
        """Преобразует данные из convert_students обратно в список"""

        return data[2:-2].split(cls.SEP)

    @staticmethod
    def share_data(data: str, sep: int = 3) -> list:
        """Разделяет строковые данные на части равные по длине sep"""
        result = []
        for i in range(0, len(data), sep):
            result.append(data[i:i + sep])
        return result


    def crate_encryption_table(self, data: str, _psc=None):
        """Создает позиционную таблицу сопоставления прежнему значению, со смещенеием на UNICODE-значение символа из пороля"""

        def get_range(chars):
            r = len(chars)
            rangs = {
                'R1': (lambda x: 1 <= x <= 26, (1, 26), 1),
                'R2': (lambda x: 27 <= x <= 702, (27, 702), 2),
                'R3': (lambda x: 703 <= x <= 18278, (703, 18278), 3),
                'R4': (lambda x: 18279 <= x <= 475254, (18279, 475254), 4),
                'R5': (lambda x: 475255 <= x <= 11881376, (475255, 11881376), 5),
            }
            for k, v in rangs.items():
                if v[0](r):
                    return v[1:]
            return None

        table = {}

        p = self.crate_eternal_iter(self.key1)
        uid = self.crate_eternal_iter(self.key2)
        key_sum = sum([ord(i) for i in self.key1])

        if not _psc:
            chars = set(data)
            R = get_range(chars)
            p_s = [data.rindex(char) for char in chars]
            _psc = [
                self.get_number_by_chars(
                    (p_s[i] + len(p_s) + ord(next(p)) + key_sum, ord(data[p_s[i]]) + ord(next(uid))))
                for i in range(len(p_s))]

            cells = iter(range(1, R[0][-1]))
            for i in chars:
                table[i] = self.get_number_by_chars(next(cells)).rjust(R[-1], '_')
        else:

            psc = [(self.get_chars_by_number(_psc[i])[0] - (len(_psc) + ord(next(p)) + key_sum),
                    chr(self.get_chars_by_number(_psc[i])[-1] - ord(next(uid)))) for i in range(len(_psc))]
            R = get_range(psc)

            data = self.share_data(data, R[-1])
            chars = [data[i[0]] for i in psc]
            for c, p in zip(chars, psc):
                table[c] = p[-1]

        return table, _psc, R[-1]

    @staticmethod
    def crate_eternal_iter(data: str, indx: int = 0) -> str:
        """Создает из итерируемого объекта бесконечный итератор"""
        while True:
            yield data[indx]
            indx += 1
            if indx == len(data):
                indx = 0

    @staticmethod
    def get_number_by_chars(number: int | tuple) -> str:
        """Преобразует число в буквенное представление. Имеет два режима если передать целое число - просто вернет
        его буквенное представление, но при передаче картежа вернет представление с разделяющей точкой"""
        excel_col_name = lambda n: '' if n <= 0 else excel_col_name((n - 1) // 26) + chr((n - 1) % 26 + ord('A'))
        if isinstance(number, tuple):
            a, b = number[0], number[-1]
            return excel_col_name(a) + '.' + excel_col_name(b)

        return excel_col_name(number)

    @staticmethod
    def get_chars_by_number(chars: str) -> int | tuple:
        """Преобразует буквенное представление в число. Имеет два режима если передать буквенное представление без точки - просто вернет
                его числовое представление, но при передаче буквенного представление с разделяющей точкой вернет картеж из целых чисел"""
        excel_col_num = lambda a: 0 if a == '' else 1 + ord(a[-1]) - ord('A') + 26 * excel_col_num(a[:-1])
        if '.' in chars:
            a, b = chars.split('.')
            return excel_col_num(a), excel_col_num(b)
        return excel_col_num(chars)


if __name__ == "__main__":
    data = ['Привет', 'Яблоко', 'HelloWorld', 'NiceToMeetYou', 'Abama', 'Pop']

    parser = EncryptionData('1234', '1234')
    parser.convert_list_to_str(data)

    # assert EncryptionData.convert_str_to_list(EncryptionData.convert_list_to_str(data)) == data
    print(data)
    print(parser.convert_list_to_str(data))

    h_text, psc,*_ = parser.encode(EncryptionData.convert_list_to_str(data))
    print(h_text)

    print(parser.decode(h_text, psc))
    print(parser.convert_str_to_list(parser.decode(h_text, psc)))






