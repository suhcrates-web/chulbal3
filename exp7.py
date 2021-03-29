import time
from datetime import datetime
import concurrent.futures
from article import magam_kospi, magam_kosdaq, yon_exch, chulbal_kos, second_bo, chul_second_alone, chul_yeong_kos


def fuck(a,b):
    print(a)
    time.sleep(3)
    print(b)


def chulbal():
    with concurrent.futures.ThreadPoolExecutor() as executor:#####
        f0 = executor.submit(fuck,a='shit',b='fuck') #영웅문 tcp
        kospi_result = f0.result()

chulbal()