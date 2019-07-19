import json
import os
import re
import traceback
import jieba
from bs4 import BeautifulSoup
from tqdm import tqdm
from stanfordcorenlp import StanfordCoreNLP

nlp = StanfordCoreNLP(r'D:\Program Files\stanford-corenlp-full/', lang='zh')


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


def get_paragraph(soup):
    ps = soup.body.text.split('\n')
    tmp = ''
    flag = False
    for i in range(len(ps)):
        text = re.sub('\s', '', ps[i])
        if not flag and len(text) > flag_len:
            flag = True
        if flag:
            tmp += text + ' '
        if "特此公告" in text:
            break
    tmp = re.split('。|！|\!|？|\?', tmp)
    sentences = []
    entities = []
    for sent in tmp:
        sent = sent.strip()
        if sent != '':
            sentences.append(sent)
            entities.append(nlp.ner(sent))
    return sentences, entities


if __name__ == "__main__":
    path = r'C:\Users\Houking\Desktop\CCKS\data\task2\xml'
    save_path = r'C:\Users\Houking\Desktop\CCKS\output\task2'
    files = [file for file in iter_files(path) if file.endswith('.xml')]
    log = open('task2.log', 'w', encoding='utf-8')
    flag_len = len('本公司及董事会全体成员保证信息披露内容的真实、准确和完整，没有虚假记载、误导性陈述或重大遗漏。')
    cnt=0
    for file in files:
        try:
            res = dict()
            name = os.path.basename(file)
            name, _ = os.path.splitext(name)
            index = [i.start() for i in re.finditer('-', name)]
            code = name[:index[0]]
            company = name[index[0] + 1:index[1]]
            res[name] = dict()
            res[name]['证券代码'] = code
            res[name]['证券简称'] = company
            res[name]['人事变动'] = []
            # print(name)
            soup = BeautifulSoup(open(file, encoding='utf-8'), "lxml")
            sentences, entities = get_paragraph(soup)
            flag = False
            for i in range(len(sentences)):
                if len(re.findall('(因|由于).*?(辞去|不再担任)', sentences[i])) > 0 or \
                    len(re.findall('(先生|女士).*?(辞去|不再担任)', sentences[i])) > 0:
                    # print(entities[i])
                    flag = True
                if len(re.findall('(聘任|提名|选举|增补).*?(先生|女士).*?(为|担任)', sentences[i])) > 0:
                    # print(entities[i])
                    flag = True
            if not flag:
                print(name)
                cnt+=1
                # fire = re.findall('(.{4}[先生|女士]).*因(.*原因).*辞去(.*)[职务|之职|一职]',sent)
                # if len(fire) > 0 and fire[0] != ('', ''):
                #     print('fire', fire)

                # # (.*[先生|女士]).*因(.*原因).*辞去(.*)[职务|之职|一职]
                #
                # name = re.findall('收到(.*[先生|女士]).*?辞职.*?[，|。|！]', sent)
                # if len(name) > 0:
                #     print('name', name)
                # reason = re.findall('因(.*原因)', sent)
                # if len(reason) > 0:
                #     print('reason', reason)
                # title = re.findall('.*辞去(.*?)职务.*', sent)
                # if len(title) > 0:
                #     print('title', title)
                #
                # hire = re.findall('.*聘任(.*[先生|女士])为(.*?)[，|（|。|的].*', sent)
                # if len(hire) > 0 and hire[0] != ('', ''):
                #     print('hire', hire)
                log.write(name + '\n')
                log.write('\n'.join(sentences))
                log.write('\n')


        except Exception as e:
            print(file)
            traceback.print_exc()
    print(cnt)