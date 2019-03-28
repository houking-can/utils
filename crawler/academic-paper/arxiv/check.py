import os
import urllib.request
import time
from multiprocessing.dummy import Pool as ThreadPool


path = r'C:\Users\Administrator\Desktop\get_url\urls'
base_path = r'F:\source'
one_dir = ''
import random

inf = open("ip")     # 这里打开刚才存ip的文件
ips = inf.readlines()
skip = open('skip','a+')


def user_proxy(proxy_address, url):
    proxy = urllib.request.ProxyHandler({'http': proxy_address})
    opener = urllib.request.build_opener(proxy, urllib.request.HTTPHandler)
    urllib.request.install_opener(opener)
    data = urllib.request.urlopen(url).read()
    return data

def downloader(file,des_path):
    file_path = path + '\\' + dir + '\\' + file
    def download_url(url,proxy_address=""):
        for _ in range(2):
            try:
                data = user_proxy(proxy_address[:-1],url)
                # data = urllib.request.urlopen(url).read()
                filename = des_path + '\\' + os.path.basename(url)
                with open(filename, 'wb') as f:
                    f.write(data)
                print(url+" "+ proxy_address)
                time.sleep(2)
                return True
            except Exception as e:
                # print(e)
                time.sleep(2)
                continue

        print('skip url:'+url)
        skip.write(one_dir + '#' +url+'\n')
        skip.flush()
        # print('remove ip:'+proxy_address)
        # ips.remove(proxy_address)
        return False

    with open(file_path) as f:
        print(file_path)
        lines = f.readlines()
        lines[-1] = lines[-1] + '\n'

        pool = ThreadPool(processes=2)
        for each in lines:
            url = each[:-1]
            url = url.replace("abs", "e-print")

            proxy_address = ips[0]
            # proxy_address = ""

            pool.apply_async(download_url, (url,proxy_address,))
        pool.close()
        pool.join()


if __name__ == '__main__':

    dirs = os.listdir(path)
    for dir in dirs:
        files = os.listdir(path+'\\'+dir)
        one_dir = dir
        print(dir)
        for file in files:
            des_path = base_path + '\\' + one_dir + '\\' + file + '\\'
            if not os.path.exists(des_path):
                os.makedirs(des_path)
            downloader(file,des_path)
            cnt = len(os.listdir(des_path))
            os.remove(path + '\\' + dir + '\\' + file)
            if cnt < 85:
                print('arxiv refuse to connect, sleep 5 min...')
                time.sleep(500)
            else:
                print('sleep 30 seconds')
                time.sleep(30)
    inf.close()
    skip.close()