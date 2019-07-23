import requests
import json
import time
import os


url = 'http://10.108.17.11/ccks_pdf/'
# url = 'http://47.111.147.253/ccks_pdf/'

def test_annualreport(file):
    files = {'file': open(file, 'rb')}
    r = requests.post(url + 'annualreport/', files=files)
    print(r.text)


def test_hrreport(file):
    files = {'file': open(file, 'rb')}
    r = requests.post(url + 'hrreport/', files=files)
    print(r.text)


def iter_files(path):
    """Walk through all files located under a root path."""
    if os.path.isfile(path):
        yield path
    elif os.path.isdir(path):
        for dir_path, _, file_names in os.walk(path):
            for f in file_names:
                yield os.path.join(dir_path, f)
    else:
        raise RuntimeError('Path %s is invalid' % path)

if __name__ == '__main__':
    # print('Test annualreport...(60s)')
    # start_time = time.time()
    # test_annualreport()
    # print(time.time()-start_time)
    for file in iter_files(r'C:\Users\Houking\Desktop\CCKS\data\task2\pdf'):
        print(file)
        start_time = time.time()
        test_hrreport(file)
        print(time.time() - start_time)

