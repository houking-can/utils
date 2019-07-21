import requests
import json

url = 'http://10.108.17.11:5000/ccks_pdf/'

def test_annualreport():

    files = {'file': open(r'C:\Users\Houking\Desktop\CCKS\data\task1\pdf\430558-均信担保-2017年年度报告.pdf', 'rb')}
    r = requests.post(url + 'annualreport/', files=files)
    print(r.status_code)
    print(r.text)

def test_hrreport():

    # files = {'file': open(r'C:\Users\Houking\Desktop\CCKS\data\task1\pdf\000026-飞亚达A-关于公司独立董事辞职的公告.pdf', 'rb')}
    # r = requests.post(url + 'hrreport/', files=files)
    # print(r.status_code)
    # print(r.text)
    # print(r.content)
    pass

if __name__ == '__main__':
   test_annualreport()
   test_hrreport()