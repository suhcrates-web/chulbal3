###집배신에 올리기 ####
import requests, json
from datetime import datetime

def do_temp(op=None, title = '제목없음', article = '내용없음', info = '내용없음'):
    info = json.dumps({"rcept_no":"", "bogoNm":"", "url":"", "url0":""})
    with open('C:/stamp/port.txt', 'r') as f:
        port = f.read().split(',')#노트북 5232, 데스크탑 5231
        port = port[1]  # http://172.30.1.53:5232/bot_v3/

    today = datetime.today().strftime("%Y-%m-%d")
    url= port + str(today) +'/'
    data = {
        'title':title,
        'article':article,
        'repl':'',
        'desk':'',
        'info': info
    }
    requests.post(
        url,
        data = data,)

def do_mbot(op='set_disc', title = '((((테스트2)))', article = '내용없음2', rcept_no = None, stock_code='111', corp_cls =
"None", ori_url = "None", article_content_type= "8", category_ids = "211", corp_name = None, rm =" "):

    with open('C:/stamp/port.txt', 'r') as f:
        port = f.read().split(',')#노트북 5232, 데스크탑 5231
        port = port[0]  # http://172.30.1.53:5232/bot_v3/
    if port =='5232':
        print('집배신엔 안보냄')
        return "집배신엔 안보냄"

    url = 'http://alpha.news1.kr/ajax/article_api.php'
    today = datetime.today().strftime("%Y%m%d")
    if op=='set_disc':
        data = {
            "access_token" : '7ECEB18CF30C48038076225884432F0D',
            "cmd" : "disc",
            "op" : "set_disc",
            "rcept_no" : rcept_no,
            "report_nm": title,
            "kind" : "1",
            "corp_code": stock_code,
            "corp_name": corp_name,
            "corp_cls" : corp_cls,
            "stock_code" : stock_code,
            "flr_nm" : "테스트",
            "rcept_dt" : today,
            "rm" : rm,
            "ori_url" : ori_url,
            "content" : article,
            "article_content_type" : article_content_type,
            "category_ids" : category_ids
        }
        a = requests.post(
            url,
            data = data,)
        print(a.content)
        print(a.headers)



def do_mbot2(op='제목없음', title = '제목없음', article = '내용없음', rcept_no = None, stock_code='111', corp_cls =
"None", ori_url = "None", article_cotent_type= "8", category_id = "83", corp_name = None):
    url = 'http://talpha.news1.kr/ajax/article_api.php'
    today = datetime.today().strftime("%Y%m%d")

    data = {
        "access_token":"7ECEB18CF30C48038076225884432F0D",
        "cmd" : "article",
        "op" : "moneybot_article",
        "title" : "test",
        "content" : "test",
        "department_id" : "118",
        "category_id": "83",


    }
    requests.post(
        url,
        data = data,)




def do(op='new_article', title = '제목없음', article = '내용없음', rcept_no = None):
    #세션열기
    session_requests = requests.session()
    #로그인정보
    payload = {
        'cmd' : 'member',
        'op' : 'alpha_login',
        'uid' : 'suhcrates' ,
        'pwd' : 'sbtmdnjs1'
    }
    #로그인, 기사 보내는 ajax url.
    login_url ='http://alpha.news1.kr/ajax/ajax.php'

    if op=='new_article':
        data = {
            'cmd' : 'article',
            'op' : 'new_article',
            'autosave': '',
            'articles_num' : '',
            'article_status' : '9',
            'article_org_status': '0',
            'regist_status': '' ,
            'result_category_selected' : '83',
            'result_byline_selected':'1128',
            'result_keyword_selected': '',
            'result_keyword_str': '',
            'result_article_relation_value':'9' ,
            'article_foreign_photo_id_arr':'',
            'article_photo_id_arr':'',
            'article_movie_id_arr':'',
            'result_hotissue_selected':'',
            'user_job_title' : '5',
            'article_title' : title,
            'subSubjectChk' : '1',
            'subSubject[]' : '(테스트)',
            'article_byline_area' : '(세종=뉴스1)',
            'article_byline_selected' : '1128',
            'contentArea' : article,
            'article_editor_email' : 'suhcrates@news1.kr',
            'article_embargo_hour' : '',
            'article_embargo_min' : '',
            'department_id':'5',
            'source_id' : '10',
            'article_category_id' : '83',
            'article_category_selected' : '83',
            'article_kindof' : '1',
            'article_cotent_type[]' : '7',
            'keyword':'',
            'www_only' : '0',
            'exclude_images' : '0',
            'article_bundle_id' : '24',
            'article_bundle_selected' : '24',
            'is_edit_title':'1',
            'bundle_edited_title':'',
            'breaking' : '2',
            'article_relation_value' :'1',
            'id': '4139089',
            'code' : '1000',
            'mode' : '',
            'user_id' :'1128',
            'msg': 'OK',
            'status' : '1',

        }
    elif op=='edit_article':
        data = {
            'cmd' : 'article',
            'op' : 'edit_article',
            'autosave': '', #이거 넣으면 작동 안함. 그냥 공란으로 비워두길.
            'articles_num' : '4140779',
            'article_status' : '91',  #1  #수정완료 버튼을 누르면 91에서 11로 바꾸도록 함
            # 근데 11을 넣으면 '예약요청'이 되고 91을 넣으면 '수정완료'가 됨
            'article_org_status': '91', # 수정버튼 누르면 91 -> 11 하도록 함. 근데 막상 열어서 보면 1임
            'regist_status': '11' , #공란
            'result_category_selected' : '83',
            'result_byline_selected':'1128',
            'result_keyword_selected': '',
            'result_keyword_str': '',
            'result_article_relation_value':'' ,
            'article_foreign_photo_id_arr':'',
            'article_photo_id_arr':'',
            'article_movie_id_arr':'',
            'result_hotissue_selected':'',
            'user_job_title' : '5',
            'article_title' : title,
            'subSubjectChk' : '1',
            'subSubject[]' : '(테스트)',
            'article_byline_area' : '(세종=뉴스1)',
            'article_byline_selected' : '1128',
            'contentArea' : article,
            'article_editor_email' : 'suhcrates@news1.kr',
            'article_embargo_hour' : '',
            'article_embargo_min' : '',
            'department_id':'5',
            'source_id' : '10',
            'article_category_id' : '83',  #카테고리 설정. 5번은 '청와대' . 산업일반 83
            'article_category_selected' : '83',
            'article_kindof' : '1',
            'article_cotent_type[]' : '7',#article_cotent_type[] / content가 아니라 cotent임 / 7번이 발생
            'keyword':'',
            'www_only' : '0',
            'exclude_images' : '0',
            'article_bundle_id' : '24',
            'article_bundle_selected' : '24',
            'is_edit_title':'1',
            'bundle_edited_title':'',
            'breaking' : '2',
            'article_relation_value' :'1',
            'id': '4140779',
            'code' : '03',
            'tp' : 'edit',
            'mode' : '',
            'user_id' :'1128',
            'msg': 'OK',
            'status' : '1',
        }



    # data0['contentArea'] = content_n1
    session_requests.post(
        login_url,
        data = payload,
    )
    session_requests.post(
        login_url,
        data = data,)


#송고해버림
#집배신 쿠키. 쿠키 작동 안함. 쿠키 빼고 보내면 기사 안뜸.
def do_songo_old(op='new_article', title = '제목없음', article = '내용없음', rcept_no = None):

    with open('C:/stamp/port.txt', 'r') as f:
        port = f.read().split(',')#노트북 5232, 데스크탑 5231
        port = port[0]  # http://172.30.1.53:5232/bot_v3/
    if port =='5232':
        print('집배신엔 안보냄')
        return "집배신엔 안보냄"
    #세션열기
    session_requests = requests.session()
    #로그인정보
    payload = {
        'cmd' : 'member',
        'op' : 'alpha_login',
        'uid' : 'suhcrates' ,
        'pwd' : 'sbtmdnjs1'
    }
    #로그인, 기사 보내는 ajax url.
    login_url ='http://alpha.news1.kr/ajax/ajax.php'

    article ="""
    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html>
<head>
</head>
<body>
    """ + article + """
    </body>
    </html>
    """
    day_name =datetime.today().strftime("%A")[:3]
    month_name = datetime.today().strftime("%B")[:3]
    date_header = datetime.today().strftime(f"{day_name}, %d {month_name} %Y 08:31:05 GMT")
    date_cookie = datetime.today().strftime(f"%d-{month_name}-%Y %H:%M:%S GMT")
    set_cookie = f"""journal_news1=6ywi%2Bi1EUDgHHe%2Be0HwOuzjEkXRi3n31kC0w7E9gG%2F91Ln7SBpd2BVSeCMpbOQFmUh0IF2qR82cddTRUevXruKd%2B5AoLAn67ZVf%2Bk%2FZTjRDUnE0L6tYCpHs6t8q%2BoEObkMsKEAk417%2FJlIspbzQ3hZxjKBU%2FQ4bawsxLsyvRpT1K1zBuWXomawl6%2BFY1LHGPbnbTGRkrEhbY4QpmV2jmMETh0NWh4Pa%2B%2FxQ4cUpEXwHVfSCPSQKVUoI54fIq75j0EjYO0u2XF%2B%2Fp4kgN13ZycFb65SfZab8gCNk4ys0unpyRVZQIHfQJ0jVexksE5g8btMSUdAcEyskrwNjOCtHwsjiMAsZFjVfy8FMVqSiMiAXVz1iJvv8aEwQO0KF8JzJfdpW4ySf6sYYzczGkyPujFjQne%2FldZ7hB7ZWTF9GuCqTS94Q3AGAgc051vRwDXJ%2BHz6yS8r21oBSXwkHHBiSz2YM9QXKMvlJiSYYe8UgIAHPzswX838RJlnKn%2FfZoK565UMMnMwxXxR2ZEf3Qt4rX2BRCJ%2FKG8fwhNnqvcc8hUZ%2Fjbm%2F%2BVnWEEjYVJYatoBuavMzNegi9qfWwGcwlsrLI8eoimTTzfZW38kD2hqkan5hCzH0JqdTbd4HSmkM8Z%2B%2FLModeQxjCnFRv9enaQEpP8B110aI7w7VBjWTrymagfoCudULTLYDVpEOBhKX5jRdTrpc2HWQ1dOmcM1sYPw6aDmAjEyZbnHJoKns%2FkPz0jTqiSn24lt039%2BZ2elCTvwzM5aB6ajyWK3c9lQX%2B1SV%2FVyEFBZeOQbpZ0dsZTcckkXON1YTUJErA3uHEoo04GHV9ODdRw1kfvsmVzXWxDGvG%2F%2BE%2BBD29XdorhgAyOxAp19hwdmTQaU7Tas%2F4z41pyIdQcHPjyV4jtrA7cRf5ANg97OwaPlcOLWuLeCfWGfuAXGlPi8QZKExq4Im1CxK9s1oVMatYfleEAYCaF74hgp%2FUkhy%2BFGWpp1OyzfwQoZXed3AoBlMuH19Uw37HFVUuowMJWLgTu4jVTD4uAavtAQ1ag51YYu6GnCKh8XJ2lOtFyN8%3D; expires={day_name}, {date_cookie}; path=/; domain=alpha.news1.kr"""

    header ={
        'Connection': 'Keep-Alive',
        'Content-Length': '26',
        'Content-Type': 'application/json',
        'Date': date_header,
        'Expires': 'Fri, 01 Jan 2010 00:00:00 GMT',
        'Keep-Alive': 'timeout=30, max=10000',
        'Server': 'Apache',
        'Set-Cookie': set_cookie
    }


    if op=='new_article':
        data = {
            'cmd' : 'article',
            'op' : 'new_article',
            'autosave': '',
            'articles_num' : '',
            'article_status' : '99',
            'article_org_status': '0',
            'regist_status': '99' ,  # ''에서 '99'로
            'result_category_selected' : '83',
            'result_byline_selected':'317', ##
            'result_keyword_selected': '',
            'result_keyword_str': '',
            'result_article_relation_value':'' , #9인거 지움.
            'article_foreign_photo_id_arr':'',
            'article_photo_id_arr':'',  ##이거 해야되는듯.
            'article_movie_id_arr':'',
            'result_hotissue_selected':'',
            'user_job_title' : '98',
            'article_title' : title,
            'subSubjectChk' : '1',
            'subSubject[]' : '',
            'article_byline_area' : '(서울=뉴스1)',
            'article_byline_selected' : '317', #응진선배 317.   나는 1128
            'contentArea' : article,
            'article_editor_email' : 'suhcrates@news1.kr',
            'article_embargo_hour' : '',
            'article_embargo_min' : '',
            'department_id':'98',
            'source_id' : '10',
            'article_category_id' : '211',
            'article_category_selected' : '211',
            'article_kindof' : '2',
            'article_cotent_type[]' : '7',
            'keyword':'',
            'www_only' : '0',
            'exclude_images' : '0',
            'article_bundle_id' : '24',
            'article_bundle_selected' : '24',
            'is_edit_title':'1',
            'bundle_edited_title':'',
            'breaking' : '2',
            'article_relation_value' :'1',
            # 'id': '4139089',
            # 'code' : '1000',
            'mode' : '',
            'user_id' :'1128',
            'msg': 'OK',
            'status' : '1',

        }


    # data0['contentArea'] = content_n1
    session_requests.post(
        login_url,
        data = payload,
    )
    session_requests.post(
        login_url,
        data = data,
        headers=header)

#공시창 쿠키 사용. 이건 됨.
def do_songo(op='new_article', title = '제목없음', article = '내용없음', rcept_no = None, byline=''):

    with open('C:/stamp/port.txt', 'r') as f:
        port = f.read().split(',')#노트북 5232, 데스크탑 5231
        port = port[0]  # http://172.30.1.53:5232/bot_v3/
    if port =='5232':
        print('집배신엔 안보냄')
        return "집배신엔 안보냄"

    with open('C:/stamp/dangbun_id.txt', 'r') as f:
        byline = str(f.read())
    #세션열기
    session_requests = requests.session()
    #로그인정보
    payload = {
        'cmd' : 'member',
        'op' : 'alpha_login',
        'uid' : 'min785' ,
        'pwd' : 'sbtmdnjs1!'
    }
    #로그인, 기사 보내는 ajax url.
    login_url ='http://alpha.news1.kr/ajax/ajax.php'

    article ="""
    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html>
<head>
</head>
<body>
    """ + article + """
    </body>
    </html>
    """


    header = {  #바이라인 서영빈
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'ko,en-US;q=0.9,en;q=0.8,ko-KR;q=0.7',
        'Connection': 'keep-alive',
        'Content-Length': len(article),
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': '_ga=GA1.2.1978667146.1545832163; dable_uid=31188705.1553472886532; '
                  '_ss_pp_id=a07ad53b6b5b3268f674db58043e890d; _gid=GA1.2.1846676616.1615272236; HttpOnly; PHPSESSID=d24fvdf7it0oe0pe06vh420tb5; journal_news1=6ywi%2Bi1EUDgHHe%2Be0HwOuzjEkXRi3n31kC0w7E9gG%2F91Ln7SBpd2BVSeCMpbOQFmUh0IF2qR82cddTRUevXruKd%2B5AoLAn67ZVf%2Bk%2FZTjRDUnE0L6tYCpHs6t8q%2BoEObkMsKEAk417%2FJlIspbzQ3hZxjKBU%2FQ4bawsxLsyvRpT1K1zBuWXomawl6%2BFY1LHGPbnbTGRkrEhbY4QpmV2jmMETh0NWh4Pa%2B%2FxQ4cUpEXwHVfSCPSQKVUoI54fIq75j0EjYO0u2XF%2B%2Fp4kgN13ZycFb65SfZab8gCNk4ys0unpyRVZQIHfQJ0jVexksE5g8btMSUdAcEyskrwNjOCtHwsjiMAsZFjVfy8FMVqSiMiAXVz1iJvv8aEwQO0KF8JzJfdpW4ySf6sYYzczGkyPujFjQne%2FldZ7hB7ZWTF9GuCqTS94Q3AGAgc051vRwDXJ%2BHz6yS8r21oBSXwkHHBiSz2YM9QXKMvlJiSYYe8UgIAHPzswX838RJlnKn%2FfZoK565UMMnMwxXxR2ZEf3Qt4rX2BRCJ%2FKG8fwhNnqvcc8hUZ%2Fjbm%2F%2BVnWEEjYVJYatoBuavMzNegi9qfWwGcwlsrLI8eoimTTzfZW38kD2hqkan5hCzH0JqdTbd4HSmkM8Z%2B%2FLModeQxjCnFRv9enaQEpP8B110aI7w7VBjWTrymagfoCudULTLYDVpEOBhKX5jRdTrpc2HWQ1dOmcM1sYPw6aDmAjEyZbnHJoKns%2FkPz0jTqiSn24lt039%2BZ2elCTvwzM5aB6ajyWK3c9lQX%2B1SV%2FVyEFBZeOQbpZ0dsZTcckkXON1YTUJErA3uHEoo04GHV9ODdRw1kfvsmVzXWxDGvG%2F%2BE%2BBD29XdorhgAyOxAp19hwdmTQaU7Tas%2F4z41pyIdQcHPjyV4jtrA7cRf5ANg97OwaPlcOLWuLeCfWGfuAXGlPi8QZKExq4Im1CxK9s1oVMatYfleEAYCaF74hgp%2FUkhy%2BFGWpp1OyzfwQoZXed3DExuw7%2FrDbDe4X4LFU%2FKTiqJ23%2BCZ1TDg4hFPZ3B9EYtEXCDSD32wYNkMORnxJtrw%3D; _td=4a06d3c1-7974-4b42-977e-2d9ec769d32e; __gads=ID=aaad8bfa1da87c47:T=1615452219:S=ALNI_MYODb2-nk_DELlMN7vb01riiYrX3g',
        'Host': 'alpha.news1.kr',
        'Origin': 'http://alpha.news1.kr',
        'Referer': 'http://alpha.news1.kr/view/report/disclosureinfo/dart/article_writing.php?id=700',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/89.0.4389.82 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }

    header = {  #바이라인 전민
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'ko,en-US;q=0.9,en;q=0.8,ko-KR;q=0.7',
        'Connection': 'keep-alive',
        'Content-Length': str(len(article)),
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': 'HttpOnly; PHPSESSID=9chnncf40pdr669aeb6k23jd82; journal_news1=RM2N7EVHyqL7gpEKsWfNoOT8MuaOoRx%2FYsjTEQLk6FDql5Nf%2Bs8WEHdxVpS22DWJoKYp5NJfszs7osjLexvd249MLIeL%2FqvY2Gz1MQjIFJUcKVq79vGq52DD0c1t2iY41G9JPabcpr%2FxpohjbYMs4tpiN0FSRmROat6tVNSmyJRw1G81va32j8mU8xcNzyYo7l6Us%2BcWJBuPdluhf1SKlVc3j%2BRmP0vFBoMi3H3jTzI5p8jh1bLvE8%2BUUQHu01j%2BZQbMc6Wuy8h5CLoyDaeRCYp5YNgMkd5dS8gnwpLsGCM3ucTNcSquSPrA8XMvxofCSTN4uivx2Th5AqkSqC5Eda%2BZ%2Bv4PNxgjZBm8eqFQs%2F%2F5B6DsSP2vS%2B%2BpL51svVr9l5TS60FDR2zCxti3UNW9Xahap7AAZq49qK5Il1Nz6sylqjL2b2y2nZd6wSPbzN5RFvitH3WYJYPOuCcDME6exFM6YS56Yd4e7M1sSdvNY9uRTh%2F7EwwL4dccl%2FEdNTYHHaR9vu%2BQJsr%2BrXW%2FNzrMv1hxWFjkLdAG%2Fe1hNaUong43bkTuiMw9KVBDs%2FP40KJmn4f7gCJuavrLbRV%2B83PadHddxxMCO%2BXm0II1AH%2Bq0YJiyilW44bPZW8Y1fPez4UgbZMeVCLv0b8leEfh2yMBne0NMEzaLd7NRiolXR8eKUWdzCepG17x6UHGZREMx5atOY7bA0OlZluBOHejdkaeWbiDs9MBEiWE4GjtxjN0T1O%2FxZWdpnrfEYxQMAUo%2BdrBeiNmmKFk%2Bez5brtOzo8x4kzqnQkzolwNsmahfvWlqDoTz0abfPEF%2FFPP3ClNwYYhAPcwv%2BW5xO3UzKuEM1CYRFp9vYhanHjJ5FGr3K3xRfKC3WZR2OKbfIAZm2dyepdSYC5jiSZdax%2Fspc%2F8pE%2BxUG58C1xuwiLUyB8D1SHMtZ9hlT7tPtJCAM6O8iP8XgmR27ijQmSuREXvKxmUzEIFgREBChs2hDlc5WfC8qlkTUepL8eyiq23iSfoDL%2B3PCgMl4iP8S2qWD5SD4c3rua%2Bt%2BwqMnGLd9CrJDOAkG8ccBWcwHBf2p8HN9oqvf27jfHUe38sKtJPZE%2Fngi2q0%2F%2BJT622y0NW4lZfyOiEIz6uquWcCO945FXRVz0AkFH0AcOG',
        'Host': 'alpha.news1.kr',
        'Origin': 'http://alpha.news1.kr',
        'Referer': 'http://alpha.news1.kr/view/report/disclosureinfo/dart/article_writing.php?id=1630',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) C\
                      hrome/90.0.4430.93 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    }

    data = {
        'cmd': 'article',
        'op': 'new_article',
        'autosave':'',
        'articles_num':'',
        'article_status': '99',
        'article_org_status': '0',
        'regist_status':'',
        'result_category_selected':'',
        'result_byline_selected':'',
        'result_keyword_selected':'',
        'result_keyword_str':'',
        'result_article_relation_value':'',
        'article_foreign_photo_id_arr':'',
        'article_photo_id_arr':'',
        'article_movie_id_arr':'',
        'result_hotissue_selected':'',
        'user_job_title': '98',
        'article_title': title,
        'editerComment':'',
        'article_byline_area': '(서울=뉴스1)',
        'article_byline_special':'',
        'article_byline_selected': byline,  #서영빈 1128  / 전민 959
        'article_byline_selector': '98',
        'contentArea': article,
        'article_editor_email': 'min785@news1.kr',
        'article_private_comment':'',
        'article_embargodate':'',
        'article_embargo_hour':'',
        'article_embargo_min':'',
        'department_id': '98',
        'source_id': '10',
        'article_category_id':'',
        'article_category_selected': '211',
        'article_kindof': '0',
        'article_cotent_type[]': '8',
        'keyword':'',
        'add_keyword_issue':'',
        'main_issue_keyword':'',
        'www_only': '0',
        'exclude_images': '0',
        'article_bundle_id':'',
        'article_bundle_selected':'',
        'breaking': '2',
        'article_relation_value':''
    }


    session_requests.post(
        login_url,
        data = payload,
    )
    session_requests.post(
        login_url,
        data = data,
        headers=header)


if __name__ == "__main__":
    today = datetime.today().strftime("%Y%m%d")

    # do_mbot(rcept_no=str(today) +'99', title="[인사]신한금융투자")
    # do_songo(title='[인사]미래에셋증권', article = """◆미래에셋증권 <br><신임> <br>▷대표 △디지털부문 안인성""")