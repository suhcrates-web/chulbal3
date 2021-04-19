import re
from datetime import date
import requests
from bs4 import BeautifulSoup



#연합 환율기사 작성 함수
def exch_article(tit, chul_ma):

    ###해체분류구간####
    tit = tit.replace(',','')  #쉼표 뗌
    if bool(re.search('내린|오른', tit)):  #내린/오른을 경계로 앞뒤로 나눔. '내린''오른'이 없으면 오류 처리.
        front = re.sub(r'[내린|오른].+','',tit)
        back = re.sub(r'.+[내린|오른]','',tit)
        point = re.findall(r'\d+\.?\d*?원',front)[0].replace('원','')
        num = re.findall(r'\d+\.?\d*?원', back)[0].replace('원','')
        plma_ment = re.findall('내린|오른',tit)[0]
        if plma_ment == '오른':
            plma = True
        elif plma_ment == '내린':
            plma = False
    else:
        raise('연합 환율 제목에 "내린", "오른"  없음.')
    jisu_dict_s = {}
    jisu_dict_s['원/달러'] = {'name': '원/달러', 'num': num, 'plma': plma, 'plma_ment': plma_ment, 'point': point, 'rate': '0'}


    ###작성구간####
    if chul_ma == 'chul':
        st_en = '출발'
    elif chul_ma == 'ma':
        st_en = '마감'
    today = date.today().day
    name_h = '달러/원'  #한글이름
    name = '원/달러'
    point = jisu_dict_s[name]['point'] # 원
    point = str(float(point))
    num = jisu_dict_s[name]['num']
    num = str(float(num))
    plma_ment = jisu_dict_s[name]['plma_ment']
    title = f"""[{name_h}] 환율 {point}원 {plma_ment} {num}원 {st_en} """
    article = f"""{today}일 {name_h}"""

    grap = ''
    if plma:
        grap= """
        <table style="clear:both;margin:auto;" width="540" border="0" cellspacing="0" cellpadding="0" align="center" data-mce-style="clear: both; margin: auto;" class="mceItemTable"><tbody><tr><td style="padding:0 10px 5px 2px;" align="center" data-mce-style="padding: 0 10px 5px 2px;"><img id="belongs_photo_4628344" class="news1_photo" style="max-width:518px;padding:5px;border:1px solid #d7d7d7" src="http://i.news1.kr/system/photos/2021/2/19/4628344/article.jpg" alt="" align="absmiddle" border="0" data-mce-src="http://i.news1.kr/system/photos/2021/2/19/4628344/article.jpg" data-mce-style="max-width: 518px; padding: 5px; border: 1px solid #d7d7d7;"></td></tr><tr><td id="content_caption_id" style="padding-bottom:10px; color:#666; letter-spacing: -1px; font-size:11px; font-family:Dotum sans-serif;" align="center" data-mce-style="padding-bottom: 10px; color: #666; letter-spacing: -1px; font-size: 11px; font-family: Dotum sans-serif;">© News1 최수아 디자이너</td></tr></tbody></table>
        """+'<br><br>'
    else:
        grap ="""
        <table style="clear:both;margin:auto;" width="540" border="0" cellspacing="0" cellpadding="0" align="center" data-mce-style="clear: both; margin: auto;" class="mceItemTable"><tbody><tr><td style="padding:0 10px 5px 2px;" align="center" data-mce-style="padding: 0 10px 5px 2px;"><img id="belongs_photo_4628343" class="news1_photo" style="max-width:518px;padding:5px;border:1px solid #d7d7d7" src="http://i.news1.kr/system/photos/2021/2/19/4628343/article.jpg" alt="" align="absmiddle" border="0" data-mce-src="http://i.news1.kr/system/photos/2021/2/19/4628343/article.jpg" data-mce-style="max-width: 518px; padding: 5px; border: 1px solid #d7d7d7;"></td></tr><tr><td id="content_caption_id" style="padding-bottom:10px; color:#666; letter-spacing: -1px; font-size:11px; font-family:Dotum sans-serif;" align="center" data-mce-style="padding-bottom: 10px; color: #666; letter-spacing: -1px; font-size: 11px; font-family: Dotum sans-serif;">© News1 최수아 디자이너</td></tr></tbody></table>
        """+'<br><br>'
    article = grap + article


    #return값 설정
    result = {}
    result['send'] ={'title':title, 'article':article}
    result['data'] = jisu_dict_s['원/달러']
    return result


#출발용 코스피 자료 가져오기
def make_dict(be_0 = 'None'):
    if be_0 =='None':
        url = 'https://www.kiwoom.com/nkw.HeroFrontJisu3.do'
        req = requests.post(url)
        be_0 = BeautifulSoup(req.text, 'html.parser')
        print(be_0)

    be = be_0.find_all('li')
    jisu_dict_s= {}
    for i in be:
        plma = None
        jisu_dict = {}
        jisu = i.get_text(separator='|').split('|')

        #이름 구간
        name = jisu[0].replace(' ','')
        jisu_dict['name'] = name

        #지수구간
        num_0 = jisu[1]
        if bool(re.search('▲',num_0)):
            plma = True
            plma_ment ='오른'
            num= num_0.replace(',','').replace('▲','').replace(' ','')

        elif bool(re.search('▼', num_0)):
            plma = False
            plma_ment = '내린'
            num= num_0.replace(',','').replace('▼','').replace(' ','')
        jisu_dict['num'] = num
        jisu_dict['plma'] = plma
        jisu_dict['plma_ment'] = plma_ment

        #포인트 구간
        point = jisu[2].replace(' ','')
        jisu_dict['point'] = point


        #증감율 구간
        try:
            rate = jisu[3].replace('%','').replace(' ','')
        except:
            rate= '0'
        jisu_dict['rate'] = rate

        name = name.lower()
        jisu_dict_s[name] =jisu_dict
    return {'jisu_dict_s':jisu_dict_s}

if __name__ == '__main__':
    make_dict()


#출발용 코스피 기사쓰기
def kos_pi_daq(jisu_dict_s=None, pi_daq = None, chul_ma = None):

    if pi_daq == 'kospi':
        name_h = '코스피'  #한글이름
        name = 'kospi'
    elif pi_daq == 'kosdaq':
        name_h = '코스닥'  #한글이름
        name = 'kosdaq'
    today = date.today().day

    if chul_ma:
        st_en = '출발'
    elif not chul_ma:
        st_en = '마감'
    point = jisu_dict_s[name]['point']
    num = jisu_dict_s[name]['num']
    rate = jisu_dict_s[name]['rate']
    plma_ment = jisu_dict_s[name]['plma_ment']
    if plma_ment == '오른':
        plma = True
        buho = ''
    elif plma_ment == '내린':
        plma = False
        buho = '-'

    title = f"""[{name_h}] {point}p({buho}{rate}%) {plma_ment} {num} {st_en} """
    article = f"""{today}일 {name_h} {st_en}"""

    #그래픽
    if pi_daq == 'kospi':
        if plma:
            grap = """
            <table style="clear:both;margin:auto;" width="540" border="0" cellspacing="0" cellpadding="0" align="center" data-mce-style="clear: both; margin: auto;" class="mceItemTable"><tbody><tr><td style="padding:0 10px 5px 2px;" align="center" data-mce-style="padding: 0 10px 5px 2px;"><img id="belongs_photo_2860611" class="news1_photo" style="max-width:518px;padding:5px;border:1px solid #d7d7d7" src="http://i.news1.kr/system/photos/2017/12/7/2860611/article.jpg" alt="" align="absmiddle" border="0" data-mce-src="http://i.news1.kr/system/photos/2017/12/7/2860611/article.jpg" data-mce-style="max-width: 518px; padding: 5px; border: 1px solid #d7d7d7;"></td></tr><tr><td id="content_caption_id" style="padding-bottom:10px; color:#666; letter-spacing: -1px; font-size:11px; font-family:Dotum sans-serif;" align="center" data-mce-style="padding-bottom: 10px; color: #666; letter-spacing: -1px; font-size: 11px; font-family: Dotum sans-serif;">© News1 DB</td></tr></tbody></table>
            """
        else:
            grap ="""
            <table style="clear:both;margin:auto;" width="540" border="0" cellspacing="0" cellpadding="0" align="center" data-mce-style="clear: both; margin: auto;" class="mceItemTable"><tbody><tr><td style="padding:0 10px 5px 2px;" align="center" data-mce-style="padding: 0 10px 5px 2px;"><img id="belongs_photo_2860599" class="news1_photo" style="max-width:518px;padding:5px;border:1px solid #d7d7d7" src="http://i.news1.kr/system/photos/2017/12/7/2860599/article.jpg" alt="" align="absmiddle" border="0" data-mce-src="http://i.news1.kr/system/photos/2017/12/7/2860599/article.jpg" data-mce-style="max-width: 518px; padding: 5px; border: 1px solid #d7d7d7;"></td></tr><tr><td id="content_caption_id" style="padding-bottom:10px; color:#666; letter-spacing: -1px; font-size:11px; font-family:Dotum sans-serif;" align="center" data-mce-style="padding-bottom: 10px; color: #666; letter-spacing: -1px; font-size: 11px; font-family: Dotum sans-serif;">© News1 DB</td></tr></tbody></table>
            """
    elif pi_daq == 'kosdaq':
        if plma:
            grap ="""
            <table style="clear:both;margin:auto;" width="540" border="0" cellspacing="0" cellpadding="0" align="center" data-mce-style="clear: both; margin: auto;" class="mceItemTable"><tbody><tr><td style="padding:0 10px 5px 2px;" align="center" data-mce-style="padding: 0 10px 5px 2px;"><img id="belongs_photo_2860604" class="news1_photo" style="max-width:518px;padding:5px;border:1px solid #d7d7d7" src="http://i.news1.kr/system/photos/2017/12/7/2860604/article.jpg" alt="" align="absmiddle" border="0" data-mce-src="http://i.news1.kr/system/photos/2017/12/7/2860604/article.jpg" data-mce-style="max-width: 518px; padding: 5px; border: 1px solid #d7d7d7;"></td></tr><tr><td id="content_caption_id" style="padding-bottom:10px; color:#666; letter-spacing: -1px; font-size:11px; font-family:Dotum sans-serif;" align="center" data-mce-style="padding-bottom: 10px; color: #666; letter-spacing: -1px; font-size: 11px; font-family: Dotum sans-serif;">© News1 DB</td></tr></tbody></table>
            """
        else:
            grap = """
            <table style="clear:both;margin:auto;" width="540" border="0" cellspacing="0" cellpadding="0" align="center" data-mce-style="clear: both; margin: auto;" class="mceItemTable"><tbody><tr><td style="padding:0 10px 5px 2px;" align="center" data-mce-style="padding: 0 10px 5px 2px;"><img id="belongs_photo_2860605" class="news1_photo" style="max-width:518px;padding:5px;border:1px solid #d7d7d7" src="http://i.news1.kr/system/photos/2017/12/7/2860605/article.jpg" alt="" align="absmiddle" border="0" data-mce-src="http://i.news1.kr/system/photos/2017/12/7/2860605/article.jpg" data-mce-style="max-width: 518px; padding: 5px; border: 1px solid #d7d7d7;"></td></tr><tr><td id="content_caption_id" style="padding-bottom:10px; color:#666; letter-spacing: -1px; font-size:11px; font-family:Dotum sans-serif;" align="center" data-mce-style="padding-bottom: 10px; color: #666; letter-spacing: -1px; font-size: 11px; font-family: Dotum sans-serif;">© News1 DB</td></tr></tbody></table>
            """
    article = grap +'<br><br>'+article


    return {'send': {'title': title, 'article': article}, 'data':{'name':name, 'num':num, 'plma':plma, 'plma_ment':
        plma_ment, 'point':point, 'rate':rate}}
