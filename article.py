import socket, codecs, time, re
from datetime import date, timedelta, datetime
from bs4 import BeautifulSoup
import os, glob, json, requests
import time, re#, post
from toolbox import exch_article, make_dict, kos_pi_daq
import post, math
from telebot import bot
import concurrent.futures


#영웅문 tcp에서 받아온 코스피, 코스닥 출발.
def chul_yeong_kos(kos):
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
        first_time = [*tik_dick][-1]
        if first_time[:2] == '15':
            print('here')
            g = tik_dick[first_time]
            print(g)
        print(first_time)
        print('yuu')
        break  #while루프 멈춤
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

    post.do_temp(title= '(test)'+title, article= article)
    # post.do_mbot(title= title, article= article, rcept_no = str(today) + '2'+ str(cm_num), rm='출발')
    # bot('c' ,"코스피 올렸습니다\n"+"http://testbot.ddns.net:5231/bot_v3")
    print(title)
    print(article)
    return g


#코스피, 코스닥 출발
def chulbal_kos():
    #개장시 cm_num 1
    cm_num = '4' #임시변경

    #출발이니까 True
    chul_ma = True
    rm = '출발'

    banbok = True
    while banbok:
        try:
            now= datetime.today().strftime(format='%H:%M')
            today = datetime.today().strftime("%Y%m%d")

            dict_made = make_dict()['jisu_dict_s']
            banbok = False
        except:
            time.sleep(3)

    try:
        #코스피 출발
        kospi_result = kos_pi_daq(jisu_dict_s=dict_made, pi_daq='kospi', chul_ma=chul_ma)
        art_pi = kospi_result['send']
        data_pi = kospi_result['data']

        #post
        post.do_temp(title=art_pi['title'], article=art_pi['article'])
        post.do_mbot(title=art_pi['title'], article=art_pi['article'], rcept_no = str(today) + cm_num+ '1', rm=rm)
    except:
        print('출발 코스피 문제발생')

    try:
    #코스닥 출발
        kosdaq_result =kos_pi_daq(jisu_dict_s=dict_made, pi_daq='kosdaq', chul_ma=chul_ma)
        # print(kosdaq_result)
        art_daq= kosdaq_result['send']
        data_daq = kosdaq_result['data']
        #post
        post.do_temp(title=art_daq['title'], article=art_daq['article'])
        post.do_mbot(title=art_daq['title'], article=art_daq['article'], rcept_no = str(today) + cm_num+'2', rm=rm)
    except:
        print('출발 코스닥 문제발생')

    bot('c' ,"코스피,코스닥 올렸습니다\n"+"http://testbot.ddns.net:5231/bot_v3")
    return {'kospi': data_pi, 'kosdaq':data_daq}


#마감 코스피 코스닥
def magam_kospi():
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    ##화면번호 211

    a='fefd4d54000000303032353454000200570255504a4f4e4700003030303031353030303231312020303231313030000043333373756863726174653030303030303030303030303032303731323231313830313639352020000000000000000000000000000000003030313537393030317f3030311e393030387f3030311e243030303030303135303030303235202020202020202020202020202020203040202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020303030323032301f31301f32351f31311f31321f31331f3135' #4번
    a= codecs.decode(a, 'hex')
    clientSocket.connect(('211.115.74.81', 14811))
    line_bf = ''
    tik_dick= {}
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
        if '888888' in [*tik_dick]:
            g = tik_dick['888888']
            print('yuu')
            break  #while루프 멈춤
        print("=====================================================================")
        time.sleep(3)
    name_h = '코스피'
    chul_ma = '마감'
    today = date.today().day

    if plma == False:
        buho = '-'
    else:
        buho = ''


    title = f"""[{name_h}] {g['point']}p({buho}{g['rate']}%) {g['plma_ment']} {g['num']} {chul_ma} """
    article = f"""{today}일 {name_h} {chul_ma}"""

    grap = ''
    if plma:
        grap = """
            <table style="clear:both;margin:auto;" width="540" border="0" cellspacing="0" cellpadding="0" align="center" data-mce-style="clear: both; margin: auto;" class="mceItemTable"><tbody><tr><td style="padding:0 10px 5px 2px;" align="center" data-mce-style="padding: 0 10px 5px 2px;"><img id="belongs_photo_2860611" class="news1_photo" style="max-width:518px;padding:5px;border:1px solid #d7d7d7" src="http://i.news1.kr/system/photos/2017/12/7/2860611/article.jpg" alt="" align="absmiddle" border="0" data-mce-src="http://i.news1.kr/system/photos/2017/12/7/2860611/article.jpg" data-mce-style="max-width: 518px; padding: 5px; border: 1px solid #d7d7d7;"></td></tr><tr><td id="content_caption_id" style="padding-bottom:10px; color:#666; letter-spacing: -1px; font-size:11px; font-family:Dotum sans-serif;" align="center" data-mce-style="padding-bottom: 10px; color: #666; letter-spacing: -1px; font-size: 11px; font-family: Dotum sans-serif;">© News1 DB</td></tr></tbody></table>
            """+'<br><br>'

    else:
        grap ="""
            <table style="clear:both;margin:auto;" width="540" border="0" cellspacing="0" cellpadding="0" align="center" data-mce-style="clear: both; margin: auto;" class="mceItemTable"><tbody><tr><td style="padding:0 10px 5px 2px;" align="center" data-mce-style="padding: 0 10px 5px 2px;"><img id="belongs_photo_2860599" class="news1_photo" style="max-width:518px;padding:5px;border:1px solid #d7d7d7" src="http://i.news1.kr/system/photos/2017/12/7/2860599/article.jpg" alt="" align="absmiddle" border="0" data-mce-src="http://i.news1.kr/system/photos/2017/12/7/2860599/article.jpg" data-mce-style="max-width: 518px; padding: 5px; border: 1px solid #d7d7d7;"></td></tr><tr><td id="content_caption_id" style="padding-bottom:10px; color:#666; letter-spacing: -1px; font-size:11px; font-family:Dotum sans-serif;" align="center" data-mce-style="padding-bottom: 10px; color: #666; letter-spacing: -1px; font-size: 11px; font-family: Dotum sans-serif;">© News1 DB</td></tr></tbody></table>
            """+'<br><br>'
    article = grap +article

    post.do_temp(title= title, article= article)
    post.do_mbot(title= title, article= article, rcept_no = str(today) + '21', rm='마감')
    bot('c' ,"코스피 올렸습니다\n"+"http://testbot.ddns.net:5231/bot_v3")
    return g

def magam_kosdaq():
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    ##화면번호 211

    a='fefd4d54000000303032353454000200570255504a4f4e4700003030303031353030303231312020303231313030000043333373756863726174653030303030303030303030303032313031323231333634313539392020000000000000000000000000000000003030313537393030317f3130311e393030387f3130311e243030303030303135303030303235202020202020202020202020202020203040202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020303030323032301f31301f32351f31311f31321f31331f3135'
    a= codecs.decode(a, 'hex')
    clientSocket.connect(('110.10.19.124', 14811))

    tik_dick= {}
    time.sleep(1)
    line_bf = ''
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
        print([line])
        if bool(re.search('MT', line)):
            pass
        else:
            line = line_bf + line

        print([line])
        line= line[line.index('MT'):]
        line_bf = line
        line= re.sub(r'.*0B','',line)
        # print(re.search(b'\x20\x20\x20\x20\x20','',line))
        line= re.sub('.*                              ','',line)
        # line= re.sub('.*\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02','',line)
        line = line[5:]
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
                break

        # print(tik_dick)

        # 888888 이 있으면 while 루프를 멈춤
        if '888888' in [*tik_dick]:
            g = tik_dick['888888']
            print('daq yuu')
            break

        print("=====================================================================")
        time.sleep(3)
    name_h = '코스닥'
    chul_ma = '마감'
    today = date.today().day

    if plma == False:
        buho = '-'
    else:
        buho = ''


    title = f"""[{name_h}] {g['point']}p({buho}{g['rate']}%) {g['plma_ment']} {g['num']} {chul_ma} """
    article = f"""{today}일 {name_h} {chul_ma}"""

    grap =''
    if plma:
        grap ="""
            <table style="clear:both;margin:auto;" width="540" border="0" cellspacing="0" cellpadding="0" align="center" data-mce-style="clear: both; margin: auto;" class="mceItemTable"><tbody><tr><td style="padding:0 10px 5px 2px;" align="center" data-mce-style="padding: 0 10px 5px 2px;"><img id="belongs_photo_2860604" class="news1_photo" style="max-width:518px;padding:5px;border:1px solid #d7d7d7" src="http://i.news1.kr/system/photos/2017/12/7/2860604/article.jpg" alt="" align="absmiddle" border="0" data-mce-src="http://i.news1.kr/system/photos/2017/12/7/2860604/article.jpg" data-mce-style="max-width: 518px; padding: 5px; border: 1px solid #d7d7d7;"></td></tr><tr><td id="content_caption_id" style="padding-bottom:10px; color:#666; letter-spacing: -1px; font-size:11px; font-family:Dotum sans-serif;" align="center" data-mce-style="padding-bottom: 10px; color: #666; letter-spacing: -1px; font-size: 11px; font-family: Dotum sans-serif;">© News1 DB</td></tr></tbody></table>
            """+'<br><br>'
    else:
        grap = """
            <table style="clear:both;margin:auto;" width="540" border="0" cellspacing="0" cellpadding="0" align="center" data-mce-style="clear: both; margin: auto;" class="mceItemTable"><tbody><tr><td style="padding:0 10px 5px 2px;" align="center" data-mce-style="padding: 0 10px 5px 2px;"><img id="belongs_photo_2860605" class="news1_photo" style="max-width:518px;padding:5px;border:1px solid #d7d7d7" src="http://i.news1.kr/system/photos/2017/12/7/2860605/article.jpg" alt="" align="absmiddle" border="0" data-mce-src="http://i.news1.kr/system/photos/2017/12/7/2860605/article.jpg" data-mce-style="max-width: 518px; padding: 5px; border: 1px solid #d7d7d7;"></td></tr><tr><td id="content_caption_id" style="padding-bottom:10px; color:#666; letter-spacing: -1px; font-size:11px; font-family:Dotum sans-serif;" align="center" data-mce-style="padding-bottom: 10px; color: #666; letter-spacing: -1px; font-size: 11px; font-family: Dotum sans-serif;">© News1 DB</td></tr></tbody></table>
            """+'<br><br>'
    article = grap +article

    post.do_temp(title= title, article= article)
    post.do_mbot(title= title, article= article, rcept_no = str(today) + '22', rm='마감')
    bot('c' ,"코스닥 올렸습니다\n"+"http://testbot.ddns.net:5231/bot_v3")
    return g

# if __name__ == '__main__':
#     with concurrent.futures.ThreadPoolExecutor() as executor:#####
#         f1 =executor.submit(magam_kospi)
#         f2 =executor.submit(magam_kosdaq)
#
#         kospi_data = f1.result()
#         kosdaq_data = f2.result()


#연합에서 환율 가져옴. 출발 마감 공통
def yon_exch(chul_ma):
    exch_did = False
    exch_up = False

    jisu_dicts = {} # 2보 작성을 위한 정보
    #출발마감 여부
    if chul_ma == "chul":
        ko_word = '개장'
        ex_word = '개장'
        cm_num = '4' #임시변경
        rm = '출발'
    elif chul_ma =="ma":
        ko_word = '장종료'
        ex_word = '마감'
        cm_num = '2'
        rm = '마감'
    today = datetime.today().strftime("%Y%m%d")
    n = 1

    while not exch_up:
        if n % 2 == 1:
            url = 'https://www.yna.co.kr/news/1'  # 전체 '최신기사'에 먼저 뜨고 '경제 전체기사'에는 좀 나중에 듬.
        else:
            url ='https://www.yna.co.kr/economy/all/1'
        n+=1

        req = requests.get(url)
        be_0 = BeautifulSoup(req.text, 'html.parser')
        li_list = be_0.find('div', {'class':'section01'}).find_all('li')

        if li_list == []: #이러면 뭔가 잘못된거임.
            raise Exception("연합 클래스 바뀜")

        #1면 제목리스트 만들어짐
        tit_list = []
        li_er_n=0
        for i in li_list:
            try:
                i = i.strong.text
                tit_list.append(i)
                # print(i)

                ##코스피, 코스닥, 외환 제제목 있는지 확인.
                if bool(re.search('\[외환\]',i)) and bool(re.search('\('+ex_word+'\)',i)) :
                    print('연합 환율 뜸')
                    exch_up = True
                    exch_tit= i

            except:
                li_er_n +=1
                pass #중간에 광고 껴있어서.
        print(f'li 중 에러 {li_er_n}개 있음')

        if exch_up:
            break
        else:
            print('연합 환율 안뜸')
            time.sleep(5) #5초 간격으로 수행.


    result = exch_article(exch_tit, chul_ma)
    art = result['send']
    data = result['data']
    exch_did = True  # 작성 완료

    #post
    post.do_temp(title=art['title'], article=art['article'])
    post.do_mbot(title=art['title'], article=art['article'], rcept_no = str(today) + str(cm_num)+ '3', rm=rm)
    bot('c' ,"환율 올렸습니다\n"+"http://testbot.ddns.net:5231/bot_v3")
    print('연합 환율 -> 작성 완료')

    return data




#2보
def second_bo(jisu_dict_s=None, chul_ma = None):

    today = date.today().day
    yesterday = (date.today() - timedelta(days=1)).day
    now_0 = str(datetime.now().hour) +'시' + str(datetime.now().minute) +'분'
    g = {} #글로벌
    ##
    n = {
        'kp':'kospi',
        'kd':'kosdaq',
        'ex':'원/달러'
    }
    for i in ['kp','kd','ex']:
        ind = n[i]
        temp = jisu_dict_s[ind]['point'] # 코스피 변동폭
        g[i+'_point'] = str(float(temp))
        temp = float(jisu_dict_s[ind]['num']) #코스피 얼마
        g[i+'_sun'] = math.floor(temp/10)*10
        g[i+'_num'] = str(temp)
        g[i+'_plma'] = jisu_dict_s[ind]['plma'] #증감여부

        g[i+'_plma_ment'] = jisu_dict_s[ind]['plma_ment']
        g[i+'_rate'] = float(jisu_dict_s[ind]['rate']) #변동폭
        #
        if g[i+'_rate'] < 0.5 :
            g[i+'_how'] = '소폭 '
            g[i+'_how2'] = ''
        elif g[i+'_rate'] <2:
            g[i+'_how'] = ''
            g[i+'_how2'] = ''
        elif g[i+'_rate'] >2:
            g[i+'_how'] = '대폭 '
            g[i+'_how2'] = '급격히 '
        #
        if g[i+'_plma']:
            g[i+'_ment_sang'] = '상승'
            g[i+'_ment_se'] = '오름세'
            g[i+'_ment_jin'] = '높아진'
            g[i+'_arr'] = '↑'
        elif not g[i+'_plma']:
            g[i+'_ment_sang'] = '하락'
            g[i+'_ment_se'] = '내림세'
            g[i+'_ment_jin'] = '떨어진'
            g[i+'_arr'] = '↓'

    ks_kd = '은' #코스피 코스닥 같으면 '도'
    if g['kp_plma'] == g['kd_plma']:
        ks_kd = '도'
    if chul_ma == 'chul': #출발
        cm_num =1
        rm = '출발'

        title = f"""코스피, 장초반 {g['kp_how']}{g['kp_ment_sang']} {g['kp_sun']}선...코스닥 {g['kd_rate']}%{g['kd_arr']}(2보)"""
        article = f"""{today}일 장초반 코스피 지수는 
{g['kp_rate']}% {g['kp_how']}{g['kp_plma_ment']} {g['kp_sun']}선을 가리키고 있다. 코스닥{ks_kd} 
{g['kd_ment_se']}다. <br><br>이날 오전 {now_0} 기준 코스피는 전날 종가와 비교해 {g['kp_point']}포인트(p)({g['kp_rate']}%) {g['kp_plma_ment']}
{g['kp_num']}를 기록 중이다.<br><br>코스닥은 전날보다 {g['kd_point']}p({g['kd_rate']}%) {g['kd_ment_jin']} {g['kd_num']}를 가리키고 있다.<br><br>서울외환시장에서 달러/원 환율은 전날 대비 {g['ex_point']}원 {g['ex_plma_ment']} {g['ex_num']}원으로 거래를 시작했다."""

    elif chul_ma == 'ma': #마감
        cm_num =2
        rm = '마감'

        title = f"""코스피 {g['kp_rate']}% {g['kp_how']}{g['kp_ment_sang']} {g['kp_sun']}선...코스닥 {g['kd_rate']}%{g['kd_arr']}(2보)"""
        article = f"""{today}일 코스피 지수가 {g['kp_rate']}% {g['kp_how']}{g['kp_ment_sang']}해 {g['kp_sun']}선으로 마감했다. 코스닥
{ks_kd} {g['kd_ment_se']}였다. <br><br>이날 코스피 지수는 {g['kp_point']}포인트(p)({g['kp_rate']}%) {g['kp_plma_ment']} 
{g['kp_num']}로 거래를 마쳤다.<br><br>코스닥 지수는 {g['kd_point']}p({g['kd_rate']}%) {g['kd_plma_ment']}{g['kd_num']}로 
마감했다.<br><br>달러/원 환율은 {g['ex_point']}원 {g['ex_plma_ment']} {g['ex_num']}원을 기록했다."""


    post.do_temp(title= title, article= article)
    post.do_mbot(title= title, article= article, rcept_no = str(today) + str(cm_num)+ '4', rm=rm)
    bot('c' ,"2보 올렸습니다\n"+"http://testbot.ddns.net:5231/bot_v3")
    # print(title + article)
    return ("2보까지 완료")



def chul_second_alone():
    jisu_dict_s = make_dict()['jisu_dict_s']
    second_bo(jisu_dict_s, 'chul')
    return 'none'
