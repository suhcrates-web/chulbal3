from datetime import datetime
from chul_ma import chulbal, magam, chul_second
# import article
# from make_dict import make_dict, magam_check, yon_data
# import post
import time
from telebot import bot

def timeline():
    i=0
    while True:
        now= datetime.today().strftime(format='%H:%M')
        print('1/3')
        #출발
        if (now >= "09:00") and (now<="09:01"):
            chulbal()
            time.sleep(60)
        print('2/3')

        #출발2보
        if (now >= "09:05") and (now<="09:10"):
            chul_second()
            time.sleep(600)
        print('2.5/3')

        #마감
        if (now >= "15:30") and (now<="15:35"):
            magam()
            return print('출발마감봇 종료')

        print('3/3')
        i= i+1
        time.sleep(1)
        print(str(now)+' '+str(i))

if __name__ == '__main__':
    timeline()