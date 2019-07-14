import os
import xlrd
import json
import re
from tqdm import tqdm
import shutil
import traceback


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


def float_str(num):
    if num == '-' or num == '—' or num == '':
        return '0.00'
    else:
        try:
            flag = ''
            num = "%.2f" % float(num)
            if num[0] == '-' or num[0] == '—':
                flag = num[0]
                num = num[1:]
            index = num.find('.')
            tmp = num[index:]
            for i in range(index, -1, -3):
                tmp = ',' + num[max(0, i - 3):i] + tmp
            return flag + tmp.strip(',')
        except:
            return num


def extract(row, ids):
    name = row[ids[0]].strip().replace('\n', '')
    appendix = row[ids[1]].strip().replace('\n', '')
    if appendix == '-' or appendix == '—':
        appendix = ''
    if name.endswith('：') or name.endswith(':'):
        num1 = None
        num2 = None
    else:
        num1 = float_str(row[ids[2]].strip().replace('\n', ''))
        num2 = float_str(row[ids[3]].strip().replace('\n', ''))

    return {"名称": name,
            "附注": appendix,
            "年初至报告期末": num1,
            "上年年初至报告期末": num2
            }


def clean_line(row):
    row = [str(each).strip().replace('\n', '') for each in row]
    line = ''.join(row)
    if line == '':
        return None
    try:
        float(line)
        return None
    except:
        line = line.replace('）', ' ')
        line = line.replace('（', ' ')
        line = line.replace('(', ' ')
        line = line.replace(')', ' ')
        return row, line


if __name__ == "__main__":
    path = r'C:\Users\Houking\Desktop\CCKS\data\task1\xlsx'
    save_path = r'C:\Users\Houking\Desktop\error\json'
    files = list(iter_files(path))
    for file in tqdm(files):
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

        book = xlrd.open_workbook(file)  # open the Excel spreadsheet as workbook
        sheet = book.sheet_by_index(0)  # get the first sheet

        rows = []
        for i in range(sheet.nrows):
            if i == 243:
                a=1
            row = clean_line(sheet.row_values(i))
            if row is None:
                continue
            rows.append(row)

        try:
            i = 0
            while i < len(rows):
                row = rows[i][0]
                line = rows[i][1].split(' ')
                if "母公司资产负债表" in line:
                    x = ''
                    ids = []
                    for k in range(0, 6):
                        if "单位：" in rows[i + k][1]:
                            _, x = rows[i + k][1].split('：')

                        if "项目" in rows[i + k][1] and "附注" in rows[i + k][1]:
                            try:
                                row = rows[i + k][0]
                                ids = [row.index('项目'), row.index('附注'), row.index('期末余额'), row.index('期初余额')]
                            except:
                                ids = [id for id, val in enumerate(row) if val != '']
                            i = i + k + 1
                            break

                    if len(ids) == 4:
                        res[name]['资产负债表（母公司）']['单位'] = x
                        while i < len(rows):
                            row = rows[i][0]
                            line = rows[i][1]
                            if "负债和所有者权益" in row[0]:
                                res[name]['资产负债表（母公司）']['项目'].append(extract(row, ids))
                                break
                            if "法定代表人" in row[0]:
                                break
                            if len(row[0]) > 1:
                                res[name]['资产负债表（母公司）']['项目'].append(extract(row, ids))
                            i += 1

                elif "合并资产负债表" in line or "资产负债表" in line:
                    x = ''
                    ids = []
                    for k in range(0, 6):
                        if "单位：" in rows[i + k][1]:
                            _, x = rows[i + k][1].split('：')

                        if "项目" in rows[i + k][1] and "附注" in rows[i + k][1]:
                            try:
                                row = rows[i + k][0]
                                ids = [row.index('项目'), row.index('附注'), row.index('期末余额'), row.index('期初余额')]
                            except:
                                ids = [id for id, val in enumerate(row) if val != '']
                            i = i + k + 1
                            break

                    if len(ids) == 4:
                        res[name]['资产负债表（合并）']['单位'] = x
                        while i < len(rows):
                            if i==245:
                                a=1
                            row = rows[i][0]
                            line = rows[i][1]
                            if "负债和所有者权益" in row[0]:
                                res[name]['资产负债表（合并）']['项目'].append(extract(row, ids))
                                break
                            if "法定代表人" in row[0]:
                                break
                            if len(row[0]) > 1:
                                res[name]['资产负债表（合并）']['项目'].append(extract(row, ids))
                            i += 1

                elif "母公司利润表" in line:
                    x = ''
                    ids = []
                    for k in range(0, 6):
                        if "单位：" in rows[i + k][1]:
                            _, x = rows[i + k][1].split('：')

                        if "项目" in rows[i + k][1] and "附注" in rows[i + k][1]:
                            try:
                                row = rows[i + k][0]
                                ids = [row.index('项目'), row.index('附注'), row.index('本期金额'), row.index('上期金额')]
                            except:
                                ids = [id for id, val in enumerate(row) if val != '']
                            i = i + k + 1
                            break

                    if len(ids) == 4:
                        res[name]['利润表（母公司）']['单位'] = x
                        while i < len(rows):
                            row = rows[i][0]
                            line = rows[i][1]
                            if "稀释每股收益" in row[0]:
                                res[name]['利润表（母公司）']['项目'].append(extract(row, ids))
                                break
                            if "法定代表人" in row[0]:
                                break
                            if len(row[0]) > 1:
                                res[name]['利润表（母公司）']['项目'].append(extract(row, ids))
                            i += 1

                elif "合并利润表" in line or "利润表" in line:
                    x = ''
                    ids = []
                    for k in range(0, 6):
                        if "单位：" in rows[i + k][1]:
                            _, x = rows[i + k][1].split('：')

                        if "项目" in rows[i + k][1] and "附注" in rows[i + k][1]:
                            try:
                                row = rows[i + k][0]
                                ids = [row.index('项目'), row.index('附注'), row.index('本期金额'), row.index('上期金额')]
                            except:
                                ids = [id for id, val in enumerate(row) if val != '']
                            i = i + k + 1
                            break

                    if len(ids) == 4:
                        res[name]['利润表（合并）']['单位'] = x
                        while i < len(rows):
                            row = rows[i][0]
                            line = rows[i][1]
                            if "稀释每股收益" in row[0]:
                                res[name]['利润表（合并）']['项目'].append(extract(row, ids))
                                break
                            if "法定代表人" in row[0]:
                                break
                            if len(row[0]) > 1:
                                res[name]['利润表（合并）']['项目'].append(extract(row, ids))
                            i += 1

                elif "母公司现金流量表" in line:
                    x = ''
                    ids = []
                    for k in range(0, 6):
                        if "单位：" in rows[i + k][1]:
                            _, x = rows[i + k][1].split('：')

                        if "项目" in rows[i + k][1] and "附注" in rows[i + k][1]:
                            try:
                                row = rows[i + k][0]
                                ids = [row.index('项目'), row.index('附注'), row.index('本期金额'), row.index('上期金额')]
                            except:
                                ids = [id for id, val in enumerate(row) if val != '']
                            i = i + k + 1
                            break

                    if len(ids) == 4:
                        res[name]['现金流量表（母公司）']['单位'] = x
                        while i < len(rows):
                            row = rows[i][0]
                            line = rows[i][1]
                            if "等价物余额" in row[0] and "期末现金" in row[0]:
                                res[name]['现金流量表（母公司）']['项目'].append(extract(row, ids))
                                break
                            if "法定代表人" in row[0]:
                                break
                            if len(row[0]) > 1:
                                res[name]['现金流量表（母公司）']['项目'].append(extract(row, ids))
                            i += 1

                elif "合并现金流量表" in line or "现金流量表" in line:
                    x = ''
                    ids = []
                    for k in range(0, 6):
                        if "单位：" in rows[i + k][1]:
                            _, x = rows[i + k][1].split('：')

                        if "项目" in rows[i + k][1] and "附注" in rows[i + k][1]:
                            try:
                                row = rows[i + k][0]
                                ids = [row.index('项目'), row.index('附注'), row.index('本期金额'), row.index('上期金额')]
                            except:
                                ids = [id for id, val in enumerate(row) if val != '']
                            i = i + k + 1
                            break

                    if len(ids) == 4:
                        res[name]['现金流量表（合并）']['单位'] = x
                        while i < len(rows):
                            row = rows[i][0]
                            line = rows[i][1]
                            if "等价物余额" in row[0] and "期末现金" in row[0]:
                                res[name]['现金流量表（合并）']['项目'].append(extract(row, ids))
                                break
                            if "法定代表人" in row[0]:
                                break
                            if len(row[0]) > 1:
                                res[name]['现金流量表（合并）']['项目'].append(extract(row, ids))
                            i += 1

                i += 1

            json.dump(res, open('%s/%s.json' % (save_path, name), 'w', encoding='utf-8'), indent=4, ensure_ascii=False)

        except Exception as e:
            print(file)
            traceback.print_exc()
