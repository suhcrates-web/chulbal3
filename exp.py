import concurrent.futures
from article import magam_kospi, magam_kosdaq, yon_exch




def chulbal():
    with concurrent.futures.ThreadPoolExecutor() as executor:#####
        f1 =executor.submit(magam_kospi)
        f2 =executor.submit(magam_kosdaq)
        f3 = executor.submit(yon_exch, 'ma')

        print(f1.result())
        print(f2.result())
        print(f3.result())
        print('끝')

