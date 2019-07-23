import os
import re

from bs4 import BeautifulSoup

from ner.utils import get_entity


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
    tmp = re.split('。|！|\!|？|\?|;|；', tmp)
    sentences = []
    for sent in tmp:
        sent = re.sub('\s', '', sent)
        if sent != '':
            sentences.append(sent)
    return sentences


def fire_format(name, sex, title, reason):
    return {
        "离职高管姓名": name,
        "离职高管性别": sex,
        "离职高管职务": title,
        "离职原因": reason,
        "继任者姓名": None,
        "继任者性别": None,
        "继任者职务": None
    }


def hire_format(name, sex, title):
    return {
        "离职高管姓名": None,
        "离职高管性别": None,
        "离职高管职务": None,
        "离职原因": None,
        "继任者姓名": name,
        "继任者性别": sex,
        "继任者职务": title
    }


def get_fire(sent, PER, SEX, TIT, REA):
    name = ''
    sex = ''
    title = ''
    reason = ''
    events = []
    if len(SEX) == 0 and len(PER) == 0:
        return None
    if len(REA) == 0:
        rea = re.findall('(因|由于)(.*?)(原因|，|。|！|？|\!|\?|；|;|（|$)')
        if len(rea) > 0:
            reason = rea[0][1]
    if len(REA) > 0:
        reason = REA[0]
    if len(TIT) > 0:
        tit = re.findall('(%s)(.*?)(职务|，|。|！|？|\!|\?|；|;|（|$)' % TIT[0], sent)
        if len(tit) > 0:
            title = TIT[0] + tit[0][1]
        else:
            title = TIT[0]
    if len(SEX) > 0:
        sex = SEX[0]
    if len(PER) > 0:
        name = PER[0]
    if reason.endswith('等原因'):
        reason = reason[:-3]
    events.append(fire_format(name, sex, title, reason))

    return events


def get_hire(sent, PER, SEX, TIT):
    name = ''
    sex = ''
    title = ''
    events = []

    if len(SEX) == 0 and len(PER) == 0:
        return None
    if len(TIT) > 0:
        tit = re.findall('(%s)(.*?)(职务|，|。|！|？|\!|\?|；|;|（|$)' % TIT[0], sent)
        if len(tit) > 0:
            title = TIT[0] + tit[0][1]
        else:
            title = TIT[0]

    if len(set(PER)) == 1:
        name = PER[0]
        if len(SEX) > 0:
            sex = SEX[0]
    elif len(set(PER)) > 1:
        per = re.findall('(聘任|提名|选举|增补)(.*?)(先生|女士|同志)')
        if len(per) > 0:
            for p in PER:
                if p in per[0][1]:
                    name = p
                    sex = per[0][2]
                    if sex != '先生' or sex != '女士':
                        sex = ''
        else:
            name = PER[-1]
            if len(SEX) > 0:
                sex = SEX[-1]

    events.append(hire_format(name, sex, title))


def extract_event(file, model, sess):
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
        print(name)
        resignation = []
        appointment = []
        soup = BeautifulSoup(open(file, encoding='utf-8'), "lxml")
        sentences = get_paragraph(soup)
        for i, sent in enumerate(sentences):
            if len(re.findall('(因|由于).*?(申请辞去|辞去|不在担任|不再担任)', sent)) > 0:
                words = list(sent)
                data = [(words, ['O'] * len(words))]
                tag = model.demo_one(sess, data)
                PER, SEX, TIT, REA = get_entity(tag, words)
                events = get_fire(sent, PER, SEX, TIT, REA)
                if events:
                    resignation.extend(events)
                # print(events)
                # print(sent)
                # print('PER: {}\nSEX: {}\nTIT: {}\nREA: {}'.format(PER, SEX, TIT, REA))

            if len(re.findall('(聘任|提名|选举|增补).*?(先生|女士|同志).*?(为|担任|出任)', sentences[i])) > 0:
                words = list(sent)
                data = [(words, ['O'] * len(words))]
                tag = model.demo_one(sess, data)
                PER, SEX, TIT, _ = get_entity(tag, words)
                events = get_hire(sent, PER, SEX, TIT)
                if events:
                    appointment.extend(events)
                # print(events)
                # print(sent)
                # print('PER: {}\nSEX: {}\nTIT: {}'.format(PER, SEX, TIT))

        tmp = [0 for _ in range(len(appointment))]
        for r in resignation:
            flag = True
            for i, a in enumerate(appointment):
                if tmp[i] == 0 and r["离职高管职务"] == a["继任者职务"]:
                    r["继任者姓名"] = a["继任者姓名"]
                    r["继任者性别"] = a["继任者性别"]
                    r["继任者职务"] = a["继任者职务"]
                    res[name]['人事变动'].append(r)
                    flag = False
                    tmp[i] = 1
                    break
            if flag:
                res[name]['人事变动'].append(r)
        for i in range(len(tmp)):
            if tmp[i] == 0:
                res[name]['人事变动'].append(appointment[i])

        return res

    except Exception as e:
        print(e)
        return res
