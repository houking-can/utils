import time
import urllib.request
import os
import re
max_results = 100
base = 'http://export.arxiv.org/api/query?search_query=cat:'
category = open("cs.category",'r').readlines()
# category = list(set(category))
for each in category:
    print(each)
    start = 0
    sub_dir = os.getcwd() + '\\urls\\'+each[:-1]
    if not os.path.exists(sub_dir):
        os.makedirs(sub_dir)
    index = 0
    while(True):
        url = base + each[:-1] + '&start=' + str(start) +  '&max_results=' + str(max_results)
        print(url)
        time.sleep(2)
        try:
            with urllib.request.urlopen(url) as res:
                data = res.read()
                urls = re.findall(r'<id>(.*)</id>', data.decode('utf-8'))
                urls.remove(urls[0])
                with open(sub_dir + '\\' + each[:-1] + '.' + str(len(urls))+'.'+str(index),'w') as fw:
                    fw.write('\n'.join(urls))
                    if len(urls)==0:
                        continue
                    if len(urls) < max_results:
                        print("this website is ok!")
                        break
            index = index + 1
            start = start + max_results
        except:
            continue
    print("sleep 20 seconds...")
    time.sleep(20)











# data = urllib.urlopen("https://arxiv.org/e-print/1808.03611").read()
# f = file("test", "wb")
# f.write(data)
# f.close()