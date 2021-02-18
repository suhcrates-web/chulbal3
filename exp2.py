import json, math
from datetime import date, timedelta
import datetime

def kos_pi_daq(jisu_dict_s=None, pi_daq = None, chul_ma = None):

    if pi_daq == 'kospi':
        name_h = '코스피'  #한글이름
        name = 'KOSPI'
    elif pi_daq == 'kosdaq':
        name_h = '코스닥'  #한글이름
        name = 'KOSDAQ'
    today = date.today().day

    if chul_ma:
        st_en = '출발'
    elif not chul_ma:
        st_en = '마감'
    point = jisu_dict_s[name]['point']
    num = jisu_dict_s[name]['num']
    rate = jisu_dict_s[name]['rate']
    plma_ment = jisu_dict_s[name]['plma_ment']

    title = f"""[{name_h}] {point}p({rate}%) {plma_ment} {num} {st_en} """
    article = f"""{today}일 {name_h} {st_en}"""

    return {'title':title, 'article':article}