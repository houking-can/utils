import os
import re
import traceback

from bs4 import BeautifulSoup
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
    ps = soup.find_all('sect') + soup.find_all('part')
    text = ''
    for each in ps:
        text += each.text + ' '
    ps = text.split('\n')
    tmp = ''
    for p in ps:
        text = re.sub('\s', '', p)
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


def get_fire(sent, entity):
    for each in entity:
        if each[1] == 'PERSON':
            print(each[0])


def get_hire(sent, entity):
    for each in entity:
        if each[1] == 'PERSON':
            print(each[0])


def extract_event(file):
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
        soup = BeautifulSoup(open(file, encoding='utf-8'), "lxml")
        sentences, entities = get_paragraph(soup)
        flag = False
        for i, sent in enumerate(sentences):
            if len(re.findall('(因|由于).*?(辞去|不再担任)', sent)) > 0 or \
                    len(re.findall('(先生|女士|同志).*?(辞去|不再担任|请辞)', sent)) > 0:
                resignation = get_fire(sent, entities[i])
                # print(entities[i])
            if len(re.findall('(聘任|提名|选举|增补).*?(先生|女士|同志).*?(为|担任)', sentences[i])) > 0:
                appointment = get_hire(sent, entities[i])
                # print(entities[i])

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
                # log.write(name + '\n')
                # log.write('\n'.join(sentences))
                # log.write('\n\n')


    except Exception as e:
        print(file)
        traceback.print_exc()
