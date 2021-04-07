import re
from typing import Union, List
from decimal import Decimal
from datetime import datetime
from requests import Response
from types import FunctionType
from typing import ItemsView


def extract_number_from_string(string: str) -> int:
    str_number = ''.join(
        filter(
            lambda s: s.isdigit(), string
        )
    )
    return int(str_number)


def empty_string_set_none(string: str) -> str:
    if string == '':
        string = None
    return string


def get_only_price_number(string: str) -> Union[int, None]:
    if string != '':
        return int(string.replace(',', '').replace('원', '').strip())
    else:
        return None


def int_with_none(string: str) -> Union[int, None]:
    try:
        if string != '':
            return int(string)
        else:
            return None
    except ValueError:
        return None


def remove_square_brackets(string: str) -> str:
    return string.replace('[', '').replace(']', '')


def remove_angle_brackets(string: str) -> str:
    return string.replace('(', '').replace(')', '')


def remove_all_brackets(string: str) -> str:
    return string.replace('(', '').replace(')', '').replace('[', '').replace(']', '').replace('{', '').replace('}', '')


def remove_whitespaces_and_newline(string: str) -> str:
    return " ".join(string.split())


def remove_escape_sequences(string: str) -> str:
    return string.replace('\n', '').replace('\t', '').replace('\xa0', '')


def convert_date_format(string_date: str) -> datetime.strptime:
    date = string_date.replace('.', '-')
    return datetime.strptime(date, '%Y-%m-%d').date()


def convert_date_format_string(string_date: str) -> str:
    return string_date.replace('.', '-')


def sorted_dictionary(items: ItemsView, key: FunctionType) -> dict:
    items = sorted(items, key=key)
    return dict((key, value) for key, value in items)


def get_url(text: str) -> str:
    start = "(\'"
    end = "\')"
    regex = re.findall((re.escape(start)) + "(.+?)" + re.escape(end), text, re.DOTALL)
    url = regex[0]
    return url


def reformat_date(text: str) -> str:
    date = datetime.strptime(text, '%Y%m%d').date().strftime("%Y-%m-%d")
    return date


def get_document_location(response: Response) -> str:
    base_url = 'http://ca.kapanet.or.kr'
    text = response.text
    start = "document.location ='"
    end = "';"
    regex = re.findall((re.escape(start)) + "(.+?)" + re.escape(end), text, re.DOTALL)
    document_location = regex[0]
    url = base_url + document_location
    return url


def reformat_datetime(raw_datetime: str) -> Union[datetime.strptime, None]:
    """
    날짜시간을 MYSQL datetime str으로 변환
    '2016.11.10(10:00)' -> '2020-11-10 10:00'
    """
    if raw_datetime is not None:
        formatted_datetime = datetime.strptime(raw_datetime, '%Y.%m.%d(%H:%M)')
        res = formatted_datetime.strftime('%Y-%m-%d %H:%M:%S')
        return res
    else:
        return None


def throw_away_below_7digit_decimal_point(decimal_point: any) -> Decimal:
    split_point = str(decimal_point).split('.')
    split_point = (split_point[0], split_point[1][:7])
    return Decimal(".".join(split_point))


def remove_html_tag(html_code: str) -> str:
    return re.sub(re.compile('<.*?>'), '', html_code)


def get_split_data(raw_data, split_tag: str) -> List[str]:
    split_data = str(raw_data).split(split_tag)
    return [remove_html_tag(item).strip() for item in split_data]


def extract_incident_number_text(txt: str) -> str:
    regex = re.compile(r'[0-9]{4}타경[0-9]+')
    return regex.search(txt).group()


def remove_string_index_range(string: str, string_range: tuple) -> str:
    start, end = string_range
    if len(string) > end:
        string = string[0: start:] + string[end + 1::]
        return string
    raise ValueError('자르고자 하는 범위를 다시 한번 확인해주세요.')


if __name__ == '__main__':
    print(remove_string_index_range("20180130027692", (4, 8)))
