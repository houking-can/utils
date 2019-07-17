import json
import os
import re
import traceback

from bs4 import BeautifulSoup
from tqdm import tqdm


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


def format_row(columns):

    name = columns[0].replace('\n', '').strip()
    appendix = re.sub('\s', '', columns[1])
    num1 = columns[2].replace('\n', '').strip()
    num2 = columns[3].replace('\n', '').strip()

    if appendix == '-' or appendix == '—':
        appendix = ''

    if (name.endswith('：') or name.endswith(':')):
        if num1 in ['-', '', '—', '--'] and num2 in ['-', '', '—', '--']:
            num1 = None
            num2 = None
    else:
        if num1 in ['-', '', '—', '--']:
            num1 = '0.00'
        if num2 in ['-', '', '—', '--']:
            num2 = '0.00'
    return {"名称": name,
            "附注": appendix,
            "年初至报告期末": num1,
            "上年年初至报告期末": num2
            }


def find_unit(text):
    text = re.sub('\s', '', text)
    units = ["单位：元", "单位:元", "单位：美元", "单位:美元", "单位：港元", "单位:港元",
             "单位：欧元", "单位:欧元", "单位：日元", "单位:日元", "单位：英镑", "单位:英镑",
             "单位：加元", "单位:加元", "单位：澳元", "单位:澳元", "单位：卢布", "单位:卢布",
             "单位：韩元", "单位:韩元"]
    for unit in units:
        if unit in text:
            return unit[3:]
    return ''


def find_name(node):
    text_num = 3
    unit = ''
    names = ['母公司资产负债表', '合并资产负债表', '母公司利润表', '合并利润表', '母公司现金流量表', '合并现金流量表']
    for element in node.previous_elements:
        if text_num < 0:
            return None
        if isinstance(element, str):
            element = element.replace('\n', '')
            if element == '':
                continue
            if unit == '':
                unit = find_unit(element)
            for name in names:
                if name in element:
                    if "母公司" in name:
                        return unit, name[3:] + "（母公司）"
                    else:
                        return unit, name[2:] + "（合并）"
            if "利润表" in element:
                return unit, "利润表（合并）"
            if "流量表" in element:
                return unit, "流量表（合并）"
            text_num -= 1


def get_flags(name):
    # head = head.text.split('\n')
    # head = [re.sub('\s', '', each) for each in head]
    # if "负债表" in name:
    #     try:
    #         ids = [head.index('项目'), head.index('附注'), head.index('期末余额'), head.index('期初余额')]
    #     except:
    #         ids = [id for id, val in enumerate(head) if val != '']
    # else:
    #     try:
    #         ids = [head.index('项目'), head.index('附注'), head.index('本期金额'), head.index('上期金额')]
    #     except:
    #         ids = [id for id, val in enumerate(head) if val != '']

    if "负债表" in name:
        tails = ['负债和所有者权益']
    elif "利润表" in name:
        tails = ['稀释每股收益']
    else:
        tails = ['等价物余额', '期末现金']

    return tails


def check_name(table, index):
    tmp = ' '.join([each["名称"] for each in table])

    # 资产负债表（合并）
    cnt = 0
    flags = ['归属于母公司所有者权益合计', '少数股东权益']
    for flag in flags:
        if flag in tmp:
            cnt += 1
    if cnt >= 1:
        return "资产负债表（合并）"

    flags = ['固定资产', '应付债券', '短期借款', '应付职工薪酬', '资本公积', '递延所得税资产', '递延所得税负债', '应交税费', '盈余公积',
             '资产总计', '长期借款', '负债合计', '可供出售金融资产', '无形资产']
    cnt = 0
    for flag in flags:
        if flag in tmp:
            cnt += 1
    if cnt >= 3:
        return "资产负债表（母公司）"

    # # 现金流量表（合并）
    # cnt = 0
    # flags = ['筹资活动产生的现金流量净额', '发行债券收到的现金', '支付其他与筹资活动有关的现金']
    # for flag in flags:
    #     if flag in tmp:
    #         cnt += 1
    # if cnt >= 2:
    #     return "现金流量表（合并）"
    #
    # # 利润表（合并）
    # cnt = 0
    # # flags = ['归属于母公司所有者的综合收益总额',, '七、综合收益总额', '六、其他综合收益的税后净额',]
    # for flag in flags:
    #     if flag in tmp:
    #         cnt += 1
    # if cnt >= 2:
    #     return "利润表（合并）"
    #
    # income = ['财务费用', '资产减值损失']
    # cash_flow = ['购建固定资产、无形资产和其他长期资产支付的现金', '取得投资收益收到的现金', '偿还债务支付的现金', '六、期末现金及现金等价物余额', '收到其他与投资活动有关的现金',
    #              '五、现金及现金等价物净增加额', '支付其他与经营活动有关的现金', '分配股利、利润或偿付利息支付的现金', '吸收投资收到的现金', '支付的各项税费', '支付给职工以及为职工支付的现金',
    #              '收到其他与筹资活动有关的现金', '经营活动产生的现金流量净额', '收到其他与经营活动有关的现金', '收回投资收到的现金', '投资活动产生的现金流量净额']

    names = ['资产负债表（合并）', '资产负债表（母公司）', '利润表（合并）', '利润表（母公司）', '现金流量表（合并）', '现金流量表（母公司）']
    return names[index]


def extract(table, start=1):
    rows = table.find_all('tr')
    table = []
    for row in rows[start:]:
        columns = row.find_all('th') + row.find_all('td')
        columns = [each.text for each in columns]

        if len(columns) > 4:
            columns = columns[:4]
        elif len(columns) < 4:
            for _ in range(4-len(columns)):
                columns.append('')
        table.append(format_row(columns))

    # 确定是合格的表格
    cnt = 0
    names = []
    global names_str
    for each in table:
        names.append(each['名称'])
        if each['名称'] in names_str:
            cnt += 1
    if cnt < int(0.8 * len(table)):
        table = []

    return table


def end(name, tails, head):
    for flag in tails:
        if flag not in name:
            if start(head):
                return True
            return False
    return True


def start(head):
    if head:
        title = re.sub('\s', '', head.text)
        if '项目附注' in title:
            info = find_name(head)
            if info:
                return info
    return None


if __name__ == "__main__":
    path = r'C:\Users\Houking\Desktop\error\xml'
    save_path = r'C:\Users\Houking\Desktop\error\json'
    files = [file for file in iter_files(path) if file.endswith('.xml')]
    global names_str
    names_str = open('names_str.txt', encoding='utf-8').read()
    for file in tqdm(files):
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
            res[name]['现金流量表（母公司）'] = {'单位': '', '项目': []}
            res[name]['现金流量表（合并）'] = {'单位': '', '项目': []}
            res[name]['利润表（母公司）'] = {'单位': '', '项目': []}
            res[name]['利润表（合并）'] = {'单位': '', '项目': []}
            res[name]['资产负债表（母公司）'] = {'单位': '', '项目': []}
            res[name]['资产负债表（合并）'] = {'单位': '', '项目': []}

            soup = BeautifulSoup(open(file, encoding='utf-8'), "lxml")

            tables = soup.find_all('table')
            i = 0
            index = -1
            while i < len(tables):
                head = tables[i].tr
                info = start(head)

                if info:
                    index += 1
                    unit, table_name = info
                    res[name][table_name]['单位'] = unit
                    tails = get_flags(table_name)
                    table = extract(tables[i], start=1)

                    i += 1
                    tmp_name = ''
                    while i < len(tables):
                        if table != []:
                            attribute = table[-1]["名称"]
                            head = tables[i].tr
                            if end(attribute, tails, head):
                                res[name][table_name]['项目'] = table
                                break
                        tmp = extract(tables[i], start=0)
                        table.extend(tmp)
                        i += 1

                    continue

                i += 1

            json.dump(res, open('%s/%s.json' % (save_path, name), 'w', encoding='utf-8'), indent=4, ensure_ascii=False)

        except Exception as e:
            print(file)
            traceback.print_exc()
