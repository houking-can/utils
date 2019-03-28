# coding=utf-8

from selenium import webdriver
import codecs
import time


options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])
driver = webdriver.Chrome(executable_path="./chromedriver.exe",
                          chrome_options=options)


def crawl_introduction(url):
    introduction = ""
    try:
        driver.get(url)
        driver.implicitly_wait(120)

    except:
        print("crawl_introduction time out")
        return introduction
    try:

        temp = driver.find_elements_by_xpath('//div[@class="kicker"]')
        title = driver.find_elements_by_xpath('//div[@class="header article-hdr"]')
        for i in range(len(title)):
            # print(url)
            # print(title[i].text)
            if "introduction" in title[i].text.lower():
                strr = temp[i].text.replace(' ', '')
                print(strr)
                if "SECTIONI" == strr or "SECTIONI." == strr:
                    xtr = driver.find_elements_by_xpath('//div[@id="sec1"]//p')
                    for answer in xtr:
                        introduction = introduction + answer.text
                elif "SECTIONII" == strr or "SECTIONII." == strr:
                    xtr = driver.find_elements_by_xpath('//div[@id="sec2"]//p')
                    for answer in xtr:
                        introduction = introduction + answer.text
                elif "SECTIONIII" == strr or "SECTIONIII." == strr:
                    xtr = driver.find_elements_by_xpath('//div[@id="sec3"]//p')
                    for answer in xtr:
                        introduction = introduction + answer.text
                elif "SECTIONIV" == strr or "SECTIONIV." == strr:
                    xtr = driver.find_elements_by_xpath('//div[@id="sec4"]//p')
                    for answer in xtr:
                        introduction = introduction + answer.text
                elif "SECTIONV" == strr or "SECTIONV." == strr:
                    xtr = driver.find_elements_by_xpath('//div[@id="sec5"]//p')
                    for answer in xtr:
                        introduction = introduction + answer.text
                elif "SECTIONVI" == strr or "SECTIONVI." == strr:
                    xtr = driver.find_elements_by_xpath('//div[@id="sec6"]//p')
                    for answer in xtr:
                        introduction = introduction + answer.text
                elif "SECTIONVII" == strr or "SECTIONVII." == strr:
                    xtr = driver.find_elements_by_xpath('//div[@id="sec7"]//p')
                    for answer in xtr:
                        introduction = introduction + answer.text
                elif "SECTIONVIII" == strr or "SECTIONVIII." == strr:
                    xtr = driver.find_elements_by_xpath('//div[@id="sec8"]//p')
                    for answer in xtr:
                        introduction = introduction + answer.text
                elif "SECTIONIX" == strr or "SECTIONIX." == strr:
                    xtr = driver.find_elements_by_xpath('//div[@id="sec9"]//p')
                    for answer in xtr:
                        introduction = introduction + answer.text
                elif "SECTIONX" == strr or "SECTIONX." == strr:
                    xtr = driver.find_elements_by_xpath('//div[@id="sec10"]//p')
                    for answer in xtr:
                        introduction = introduction + answer.text
                break
        return introduction
    except:
        return introduction




def crawl_url(url):
    result_url = []
    try:
        driver.get(url)
        driver.implicitly_wait(120)

    except:
        print("crawl_introduction time out")
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

    fp = open('./nipsUrl.txt', 'r')
    url_list = fp.readlines()
    length = len(url_list)
    # print(length)
    fp.close()

    # fs = open('./start.txt', 'r')
    # big = fs.readline()
    start = 0

    print('--------------------------------------------------------------------')
    print('Start with ' + str(start))
    print('--------------------------------------------------------------------')
    fp = open("./paper_url.txt", 'a+')
    for i in range(start, length):
        print(url_list[i])
        total_url = crawl_url(url_list[i])

        # for j in range(len(total_url)):
        #     if j >= len(total_url):
        #         break

        for url in total_url:
            if "author" in url:
                continue
            elif "book" in url:
                continue
            elif url == "https://papers.nips.cc/":
                continue
            fp.write(url + '.pdf' + '\n')
        time.sleep(2)
    fp.close()
        # if len(url_list[i]) > 0:

            # introduction = ""
            # abstract = ""
            # title = ""
            #
            # print('Title...')
            # temp = crawl_title(url_list[i])
            # tempF = str(temp).split('\n')
            # title = tempF[0]
            #
            #
            # # print('Title is: ' + title)
            # print('--------------------------------------------------------------------')
            # print('Abstract...')
            # if "xpls" not in url_list[i]:
            #     abstract = crawl_abstract(url_list[i])
            # else:
            #     abstract = tempF[1]
            #
            # # print('Abstract : ' + abstract)
            # print('--------------------------------------------------------------------')
            # print('Introduction...')
            # introduction = crawl_introduction(url_list[i])
            #
            # # print('Introduction : ' + introduction)
            # print('--------------------------------------------------------------------')
            #
            # if len(abstract) > 0 and len(title) > 0 and len(introduction) > 0:
            #     save_abstract = './abstract/' + str(i) + '.txt'
            #     fpA = codecs.open(save_abstract, 'w', 'utf-8')
            #     contentA = url_list[i] + '\r\n' + title + '\r\n' + abstract
            #     fpA.write(contentA)
            #     fpA.close()
            #
            #     save_introduction = './introduction/' + str(i ) + '.txt'
            #     fpI = codecs.open(save_introduction, 'w', 'utf-8')
            #     contentI = url_list[i] + '\r\n' + title + '\r\n' + introduction
            #     fpI.write(contentI)
            #     fpI.close()
            #     print(str(i)+'/'+str(length))
            #     print('--------------------------------------------------------------------')
            #     print('--------------------------------------------------------------------')
    driver.quit()