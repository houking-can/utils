# -*- coding:utf8 -*-

import urllib.request
import re
import time

# headers = {
#     'Accept': '*/*',
#     'Accept-Language': 'zh-CN,zh;q=0.8',
#     'User-Agent': 'Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
#     'Hosts': 'hm.baidu.com',
#     'Referer': 'http://www.xicidaili.com/nn',
#     'Connection': 'keep-alive'
# }
#
# # 指定爬取范围（这里是第1~1000页）
# for i in range(295,1000):
#     try:
#         url = 'http://www.xicidaili.com/nn/' + str(i)
#         req = urllib.request.Request(url=url,headers=headers)
#
#         res = urllib.request.urlopen(req).read().decode('utf-8')
#
#         # 提取ip和端口
#         ip_list = re.findall("(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}).*?(\d{2,6})", res, re.S)
#
#         # 将提取的ip和端口写入文件
#         f = open("ip.txt","a+")
#         for li in ip_list:
#             ip = li[0] + ':' + li[1] + '\n'
#             print(ip)
#             f.write(ip)
#     except Exception as e:
#         print(e)
#     time.sleep(2)       # 每爬取一页暂停两秒


import urllib
import socket
import random
socket.setdefaulttimeout(3)

def user_proxy(proxy_address, url):
    proxy = urllib.request.ProxyHandler({'http': proxy_address})
    opener = urllib.request.build_opener(proxy, urllib.request.HTTPHandler)
    urllib.request.install_opener(opener)
    data = urllib.request.urlopen(url).read()
    return data

# proxys = []
# for i in range(0,len(lines)):
#     proxy_host = "http://" + lines[i]
#     proxy_temp = {"http":proxy_host}
#     proxys.append(proxy_temp)

# 用这个网页去验证，遇到不可用ip会抛异常
proxys = open('ip.txt','r').readlines()
proxys = proxys[0:5000]
urls = open('cs.DL.100.20','r').readlines()
print('start...')
cnt = 0
with open("ip", "w") as out:
    for proxy in proxys:
        print(str(cnt) + '/' +str(len(proxys)))
        cnt = cnt + 1
        k = random.randint(0,len(urls)-1)
        for _ in range(2):
            try:
                res = user_proxy(url=urls[k],proxy_address=proxy[:-1])
                print (proxy[:-1])
                out.write(proxy)
                break
            except Exception as e:
                print(e)
                continue
        time.sleep(1)

