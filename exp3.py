import time
from datetime import datetime
import concurrent.futures
from article import magam_kospi, magam_kosdaq, yon_exch, chulbal_kos, second_bo, chul_second_alone, chul_yeong_kos



def chulbal():
    with concurrent.futures.ThreadPoolExecutor() as executor:#####
        f0 = executor.submit(chul_yeong_kos, 'kospi') #영웅문 tcp
        f1 = executor.submit(chul_yeong_kos, 'kosdaq')
        # f1 = executor.submit(chulbal_kos) #영웅문 프로트페이지
        f2 = executor.submit(yon_exch, 'chul')
        kospi_result = f0.result()
        kosdaq_result = f1.result()
        # kos_data = f1.result()
        exch_data = f2.result()
        print('출발 끝')
    time.sleep(1)
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open('C:/stamp/sihwang.csv', 'w') as f:
        f.writelines['1,',now] #0은 장전 1은 장중 0은 마감과 개장전
    # chul_dict = {}
    # chul_dict['kospi'] = kos_data['kospi']
    # chul_dict['kosdaq'] = kos_data['kosdaq']
    # chul_dict['원/달러'] = exch_data
    # second_bo(chul_dict, 'chul')
    return print('코스피, 코스닥, 환율 끝')

#출발 2보
def chul_second():
    chul_second_alone()




def magam():
    with concurrent.futures.ThreadPoolExecutor() as executor:#####
        f1 =executor.submit(magam_kospi)
        f2 =executor.submit(magam_kosdaq)
        f3 = executor.submit(yon_exch, 'ma')

        kospi_data = f1.result()
        kosdaq_data = f2.result()
        exch_data = f3.result()
        print('마감 끝')
    time.sleep(1)


    ma_dict = {}
    ma_dict['kospi'] = kospi_data
    ma_dict['kosdaq'] = kosdaq_data
    ma_dict['원/달러'] = exch_data
    second_bo(ma_dict, 'ma')
    # print(kospi_data)
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open('C:/stamp/sihwang.csv', 'w') as f:
        f.writelines(['2,',now,',',kospi_data['num'],',',kospi_data['point'],',',kospi_data['rate'],',',str(kospi_data[
            'plma']),',',kospi_data['plma_ment'],',',kosdaq_data['num'],',',kosdaq_data['point'],',',kosdaq_data[
            'rate'],',',str(kosdaq_data['plma']),',',kosdaq_data['plma_ment'],exch_data['num'],\
            exch_data['point'], exch_data['plma']])
        #0은 장전 1은 장중 2는 마감
        # 개장전
    return print('2보 끝')

print(magam())