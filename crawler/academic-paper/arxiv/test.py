import urllib.request

def user_proxy(proxy_address, url):
    proxy = urllib.request.ProxyHandler({'http': proxy_address})
    opener = urllib.request.build_opener(proxy, urllib.request.HTTPHandler)
    urllib.request.install_opener(opener)
    data = urllib.request.urlopen(url).read()
    return data

proxy_address = "120.24.152.123:3128"
data = user_proxy(proxy_address, "http://arxiv.org/abs/1605.05863v1")
with open('a', 'wb') as f:
    f.write(data)
# print(data)
# print(len(data))


