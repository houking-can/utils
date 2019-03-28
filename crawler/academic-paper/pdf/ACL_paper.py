# coding=utf-8

from selenium import webdriver
import codecs
import time
import requests


options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])
driver = webdriver.Chrome(executable_path="./chromedriver.exe",
                          chrome_options=options)

def crawl_url(url):
    result_url = []
    try:
        driver.get(url)
        # driver.implicitly_wait(120)

    except:
        print("time out")
        return result_url
    try:
        # print('Start sleep 8 secs...')
        # sleep(8)
        # print('Begin crawl abstract')

        # temp = driver.find_elements_by_xpath('//div[@class="abstract-text ng-binding"]')
        temp = driver.find_elements_by_xpath('//*[@href]')

        # print(len(temp))
        # for i in range(len(temp)):
        #     print(temp[i].text)
        for each in temp:
            result_url.append(each.get_attribute('href'))
        return result_url
    except:
        return result_url


if __name__ == '__main__':

    fp = open('./EMNLP_url.txt', 'r')
    url_list = fp.readlines()
    length = len(url_list)
    # print(length)
    fp.close()

    # fs = open('./start.txt', 'r')
    # big = fs.readline()
    start = 0
    minlen=len('http://www.aclweb.org/anthology/P/P98/P98-1012.pdf')
    print('--------------------------------------------------------------------')
    print('Start with ' + str(start))
    print('--------------------------------------------------------------------')
    fpa = open("./EMNLP_paper_url.txt", 'a+')
    for i in range(start, length):
        print(url_list[i])
        # html=requests.get('http://www.aclweb.org/anthology/P/P99/')
        # print html.text
        # break
        total_url = crawl_url(url_list[i])
        # for j in range(len(total_url)):
        #     if j >= len(total_url):
        #         break

        for url in total_url:
            if "1000" in url:
                continue
            if len(url)<minlen:
                continue
            if ".pdf" in url:
                # print(url)
                fpa.write(url + '\n')
        time.sleep(2)
    fpa.close()

    driver.quit()