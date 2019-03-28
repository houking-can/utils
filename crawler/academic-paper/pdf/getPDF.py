import time
import urllib
import sys

if __name__ == '__main__':

    fp = open('./ACL_paper_url.txt', 'r')
    url_list = fp.readlines()
    length = len(url_list)
    # print(length)
    fp.close()

    # fs = open('./start.txt', 'r')
    # big = fs.readline()
    xx = sys.argv[1]
    start = int(xx)

    print('Start with ' + str(start))
    print('--------------------------------------------------------------------')
    path=r'./ACL-python-1/'
    for i in range(start, 1000):
        print(url_list[i].replace('\n',' '))
        data = urllib.urlopen(url_list[i]).read()

        f = file(path+str(i+1)+'.pdf', "wb")
        f.write(data)
        print 'write sucessful '+str(i+1)
        f.close()
        time.sleep(1)
    print('finish')
