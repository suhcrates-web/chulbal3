import socket, codecs, time, re
from datetime import date, timedelta, datetime
from bs4 import BeautifulSoup
import os, glob, json, requests
import time, re#, post
from toolbox import exch_article, make_dict, kos_pi_daq
import post, math
from telebot import bot
import concurrent.futures

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

    grap = ''
    if g['kp_plma']:
        grap = """
            <table style="clear:both;margin:auto;" width="540" border="0" cellspacing="0" cellpadding="0" align="center" data-mce-style="clear: both; margin: auto;" class="mceItemTable"><tbody><tr><td style="padding:0 10px 5px 2px;" align="center" data-mce-style="padding: 0 10px 5px 2px;"><img id="belongs_photo_2860611" class="news1_photo" style="max-width:518px;padding:5px;border:1px solid #d7d7d7" src="http://i.news1.kr/system/photos/2017/12/7/2860611/article.jpg" alt="" align="absmiddle" border="0" data-mce-src="http://i.news1.kr/system/photos/2017/12/7/2860611/article.jpg" data-mce-style="max-width: 518px; padding: 5px; border: 1px solid #d7d7d7;"></td></tr><tr><td id="content_caption_id" style="padding-bottom:10px; color:#666; letter-spacing: -1px; font-size:11px; font-family:Dotum sans-serif;" align="center" data-mce-style="padding-bottom: 10px; color: #666; letter-spacing: -1px; font-size: 11px; font-family: Dotum sans-serif;">© News1 DB</td></tr></tbody></table>
            """+'<br>'

    else:
        grap ="""
            <table style="clear:both;margin:auto;" width="540" border="0" cellspacing="0" cellpadding="0" align="center" data-mce-style="clear: both; margin: auto;" class="mceItemTable"><tbody><tr><td style="padding:0 10px 5px 2px;" align="center" data-mce-style="padding: 0 10px 5px 2px;"><img id="belongs_photo_2860599" class="news1_photo" style="max-width:518px;padding:5px;border:1px solid #d7d7d7" src="http://i.news1.kr/system/photos/2017/12/7/2860599/article.jpg" alt="" align="absmiddle" border="0" data-mce-src="http://i.news1.kr/system/photos/2017/12/7/2860599/article.jpg" data-mce-style="max-width: 518px; padding: 5px; border: 1px solid #d7d7d7;"></td></tr><tr><td id="content_caption_id" style="padding-bottom:10px; color:#666; letter-spacing: -1px; font-size:11px; font-family:Dotum sans-serif;" align="center" data-mce-style="padding-bottom: 10px; color: #666; letter-spacing: -1px; font-size: 11px; font-family: Dotum sans-serif;">© News1 DB</td></tr></tbody></table>
            """+'<br>'
    article = grap +article

    # post.do_temp(title= title, article= article)
    post.do_mbot(title= title, article= article, rcept_no = str(today) + str(cm_num)+ '7', rm=rm)

    # bot('c' ,"2보 올렸습니다\n"+"http://testbot.ddns.net:5231/bot_v3")
    # print(title + article)
    return ("2보까지 완료")


def chul_second_alone():
    jisu_dict_s = make_dict()['jisu_dict_s']
    second_bo(jisu_dict_s, 'chul')
    return 'none'

chul_second_alone()