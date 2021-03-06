import socket, codecs, time, re
from datetime import date, timedelta, datetime
from bs4 import BeautifulSoup
import os, glob, json, requests
import time, re#, post
from toolbox import exch_article, make_dict, kos_pi_daq
import post, math
from telebot import bot
import concurrent.futures



test ="""
..MT\x00\x00\x0000216T\x00\x02\x00W\x02UPJONG\x00\x00000015000211  
021100\x00\x00C33suhcrate000000000000020712211801695  S\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0000119$00000015000025                0@                                                                                 00000
"""


def chul_yeong_kos(kos, test=test):
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    ##화면번호 211
    if kos == 'kospi':
        a='fefd4d54000000303032353454000200570255504a4f4e4700003030303031353030303231312020303231313030000043333373756863726174653030303030303030303030303032303731323231313830313639352020000000000000000000000000000000003030313537393030317f3030311e393030387f3030311e243030303030303135303030303235202020202020202020202020202020203040202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020303030323032301f31301f32351f31311f31321f31331f3135' #4번
        ip = '211.115.74.81'
        name_h = '코스피'
        cm_num = '1'
    elif kos == 'kosdaq':
        time.sleep(1)
        a='fefd4d54000000303032353454000200570255504a4f4e4700003030303031353030303231312020303231313030000043333373756863726174653030303030303030303030303032313031323231333634313539392020000000000000000000000000000000003030313537393030317f3130311e393030387f3130311e243030303030303135303030303235202020202020202020202020202020203040202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020303030323032301f31301f32351f31311f31321f31331f3135'
        ip = '110.10.19.124'
        name_h = '코스닥'
        cm_num = '2'
    a= codecs.decode(a, 'hex')
    clientSocket.connect((ip, 14811))
    line_bf = ''
    tik_dick= {}
    n=0
    while True:
        clientSocket.send(a)
        data = clientSocket.recv(1024)
        # print(data.hex())
        data = data.hex()

        # print(codecs.decode(data, 'hex').decode('cp949'))
        line = []
        han = False
        line = ''
        han = False
        for i in range(len(data)//2):
            if han:
                han = False
            else:
                try:
                    ps =data[i*2:i*2+2]
                    if ps == '1f':
                        # print('|',end='')
                        line +='|'
                    else:
                        # print(codecs.decode(ps,'hex').decode('cp949')  ,end='')
                        line += codecs.decode(ps,'hex').decode('cp949')
                except:
                    # print('.',end='')
                    line += '.'
                    # try:
                    #     print(codecs.decode(data[i*2:i*2+4],'hex').decode('cp949')  ,end='')
                    #     han = True
                    # except:
                    #     print('.', end='')
        # print('')

        # line = test
        while n<5:
            line = test
            break
        n+=1
        print(n)

        if bool(re.search('MT', line)):
            pass
        else:
            line = line_bf + line
        print([line])
        line= line[line.index('MT'):]
        line_bf = line
        # print(bool(re.search('0B',line)))
        line= re.sub(r'.*0B','',line)
        # print(re.search(b'\x20\x20\x20\x20\x20','',line))
        # print(bool(re.search('                              ',line)))
        line= re.sub('.*                              ','',line)
        # line= re.sub('.*\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02','',line)
        line = line[5:]
        # print([line])
        line = line.split(sep='\n')

        tik_list = []
        tik_dick = {}
        for i in line:
            tik = i.split('|')
            if len(tik) == 7:
                tik_list.append(tik)
                tik_dick[tik[0]] = {}
                point = float(tik[3])
                if point > 0:
                    plma = True
                    plma_ment = '오른'
                elif point < 0:
                    plma = False
                    plma_ment = '내린'
                elif point == 0:
                    plma = 0
                    plma_ment = '보합'

                tik_dick[tik[0]]['num'] = tik[1].replace('-','').replace('+','')
                tik_dick[tik[0]]['point'] = tik[3].replace('-','').replace('+','')
                tik_dick[tik[0]]['rate'] = tik[4].replace('-','').replace('+','')
                tik_dick[tik[0]]['plma'] = plma
                tik_dick[tik[0]]['plma_ment'] = plma_ment

            else:
                break  #칼럼 7개 아니면 안먹음

        # print(tik_dick)

        # 888888 이 있으면 while 루프를 멈춤
        try:
            first_time = [*tik_dick][-1]
            print(first_time)
            time_temp = '09'

            if first_time[:2] == time_temp:
                print('here')
                g = tik_dick[first_time]
                print(g)
                print(first_time)
                print('yuu')
                break  #while루프 멈춤
        except:
            pass
        print("=====================================================================")
        time.sleep(3)

    chul_ma = '출발'
    today = date.today().day

    if plma == False:
        buho = '-'
    else:
        buho = ''


    title = f"""[{name_h}] {g['point']}p({buho}{g['rate']}%) {g['plma_ment']} {g['num']} {chul_ma} """
    article = f"""{today}일 {name_h} {chul_ma}"""

    grap = ''
    if kos == 'kospi':
        if plma:
            grap = """
                <table style="clear:both;margin:auto;" width="540" border="0" cellspacing="0" cellpadding="0" align="center" data-mce-style="clear: both; margin: auto;" class="mceItemTable"><tbody><tr><td style="padding:0 10px 5px 2px;" align="center" data-mce-style="padding: 0 10px 5px 2px;"><img id="belongs_photo_2860611" class="news1_photo" style="max-width:518px;padding:5px;border:1px solid #d7d7d7" src="http://i.news1.kr/system/photos/2017/12/7/2860611/article.jpg" alt="" align="absmiddle" border="0" data-mce-src="http://i.news1.kr/system/photos/2017/12/7/2860611/article.jpg" data-mce-style="max-width: 518px; padding: 5px; border: 1px solid #d7d7d7;"></td></tr><tr><td id="content_caption_id" style="padding-bottom:10px; color:#666; letter-spacing: -1px; font-size:11px; font-family:Dotum sans-serif;" align="center" data-mce-style="padding-bottom: 10px; color: #666; letter-spacing: -1px; font-size: 11px; font-family: Dotum sans-serif;">© News1 DB</td></tr></tbody></table>
                """+'<br><br>'

        else:
            grap ="""
                <table style="clear:both;margin:auto;" width="540" border="0" cellspacing="0" cellpadding="0" align="center" data-mce-style="clear: both; margin: auto;" class="mceItemTable"><tbody><tr><td style="padding:0 10px 5px 2px;" align="center" data-mce-style="padding: 0 10px 5px 2px;"><img id="belongs_photo_2860599" class="news1_photo" style="max-width:518px;padding:5px;border:1px solid #d7d7d7" src="http://i.news1.kr/system/photos/2017/12/7/2860599/article.jpg" alt="" align="absmiddle" border="0" data-mce-src="http://i.news1.kr/system/photos/2017/12/7/2860599/article.jpg" data-mce-style="max-width: 518px; padding: 5px; border: 1px solid #d7d7d7;"></td></tr><tr><td id="content_caption_id" style="padding-bottom:10px; color:#666; letter-spacing: -1px; font-size:11px; font-family:Dotum sans-serif;" align="center" data-mce-style="padding-bottom: 10px; color: #666; letter-spacing: -1px; font-size: 11px; font-family: Dotum sans-serif;">© News1 DB</td></tr></tbody></table>
                """+'<br><br>'
    elif kos == 'kosdaq':
        if plma:
            grap ="""
            <table style="clear:both;margin:auto;" width="540" border="0" cellspacing="0" cellpadding="0" align="center" data-mce-style="clear: both; margin: auto;" class="mceItemTable"><tbody><tr><td style="padding:0 10px 5px 2px;" align="center" data-mce-style="padding: 0 10px 5px 2px;"><img id="belongs_photo_2860604" class="news1_photo" style="max-width:518px;padding:5px;border:1px solid #d7d7d7" src="http://i.news1.kr/system/photos/2017/12/7/2860604/article.jpg" alt="" align="absmiddle" border="0" data-mce-src="http://i.news1.kr/system/photos/2017/12/7/2860604/article.jpg" data-mce-style="max-width: 518px; padding: 5px; border: 1px solid #d7d7d7;"></td></tr><tr><td id="content_caption_id" style="padding-bottom:10px; color:#666; letter-spacing: -1px; font-size:11px; font-family:Dotum sans-serif;" align="center" data-mce-style="padding-bottom: 10px; color: #666; letter-spacing: -1px; font-size: 11px; font-family: Dotum sans-serif;">© News1 DB</td></tr></tbody></table>
            """+'<br><br>'
        else:
            grap = """
                <table style="clear:both;margin:auto;" width="540" border="0" cellspacing="0" cellpadding="0" align="center" data-mce-style="clear: both; margin: auto;" class="mceItemTable"><tbody><tr><td style="padding:0 10px 5px 2px;" align="center" data-mce-style="padding: 0 10px 5px 2px;"><img id="belongs_photo_2860605" class="news1_photo" style="max-width:518px;padding:5px;border:1px solid #d7d7d7" src="http://i.news1.kr/system/photos/2017/12/7/2860605/article.jpg" alt="" align="absmiddle" border="0" data-mce-src="http://i.news1.kr/system/photos/2017/12/7/2860605/article.jpg" data-mce-style="max-width: 518px; padding: 5px; border: 1px solid #d7d7d7;"></td></tr><tr><td id="content_caption_id" style="padding-bottom:10px; color:#666; letter-spacing: -1px; font-size:11px; font-family:Dotum sans-serif;" align="center" data-mce-style="padding-bottom: 10px; color: #666; letter-spacing: -1px; font-size: 11px; font-family: Dotum sans-serif;">© News1 DB</td></tr></tbody></table>
                """+'<br><br>'

    article = grap +article
    print(title)
    print(article)

chul_yeong_kos(kos='kospi')