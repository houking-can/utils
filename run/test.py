import shutil
import os
import random
import xlrd
import json


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


# path = r'C:\Users\Houking\Desktop\CCKS\data\task1\json'
# error = r'C:\Users\Houking\Desktop\error\json'
# word = r'C:\Users\Houking\Desktop\error\word'
#
# for file in iter_files(path):
#     basename = os.path.basename(file)
#     name, _ = os.path.splitext(basename)
#     res = json.load(open(file, encoding='utf-8'))[name]
#     cnt=0
#     for key, value in res.items():
#         if isinstance(value, dict):
#             # print(len(value['项目']))
#             cnt+=len(value['项目'])
#     e_cnt = 0
#     model = json.load(open(os.path.join(error,basename),encoding='utf-8'))['tables']
#     for each in model:
#         e_cnt+=len(each)
#     if abs(cnt-e_cnt)>10:
#         shutil.move(os.path.join(error,basename),r'C:\Users\Houking\Desktop\a')
#         shutil.move(os.path.join(word,name+'.docx'),r'C:\Users\Houking\Desktop\a')


path = r'C:\Users\Houking\Desktop\CCKS\data\task1\json'
error = r'C:\Users\Houking\Desktop\error\json'
word = r'C:\Users\Houking\Desktop\error\word'

nn = 0
for file in iter_files(error):
    basename = os.path.basename(file)
    name, _ = os.path.splitext(basename)
    print(name)

    e_cnt = 0
    model = json.load(open(file,encoding='utf-8'))['tables']
    for each in model:
        e_cnt += len(each)
        # print(len(each))

    res = json.load(open(os.path.join(path, basename), encoding='utf-8'))[name]

    cnt = 0
    for key, value in res.items():
        if isinstance(value, dict):
            # print(len(value['项目']))
            cnt += len(value['项目'])
            # print(len(value['项目']))
    print('model:%d  ground:%d' % (e_cnt, cnt))
    nn+=abs(cnt-e_cnt)
print(nn)
    # if abs(cnt-e_cnt)>10:
    #     shutil.move(os.path.join(error,basename),r'C:\Users\Houking\Desktop\a')
    #     shutil.move(os.path.join(word,name+'.docx'),r'C:\Users\Houking\Desktop\a')
