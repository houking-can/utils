# from aip import AipOcr
#
# """ APPID AK SK """
# APP_ID = '15461069'
# API_KEY = 'SCxkTL6Hj387RtSgokUozVnW'
# SECRET_KEY = 'hXdnqmDP0NcaxhwfzDXDGiIPxVnW8WGq'
#
# client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
#
# # """ 读取图片 """
# def get_file_content(filePath):
#     with open(filePath, 'rb') as fp:
#         return fp.read()
#
# # image = get_file_content('example.jpg')
#
# # """ 调用通用文字识别, 图片参数为本地图片 """
# # # client.basicGeneral(image);
# #
# # """ 如果有可选参数 """
# # options = {}
# # options["language_type"] = "CHN_ENG"
# # options["detect_direction"] = "true"
# # options["detect_language"] = "true"
# # options["probability"] = "true"
# #
# # """ 带参数调用通用文字识别, 图片参数为本地图片 """
# # res = client.basicAccurate(image, options)
#
# path  = r'C:\Users\Houking\Desktop\latex'
# import os
# images = os.listdir(path)
# """ 调用通用文字识别, 图片参数为远程url图片 """
# latex = ''
#
# for file in images:
#     image = get_file_content(os.path.join(path,file))
#
#     """ 如果有可选参数 """
#     options = {}
#     options["language_type"] = "CHN_ENG"
#     # options["detect_direction"] = "true"
#     # options["detect_language"] = "true"
#     # options["probability"] = "true"
#
#     """ 带参数调用通用文字识别, 图片参数为远程url图片 """
#     res = client.basicAccurate(image, options)
#     for i in range(1,res['words_result_num']):
#         latex = latex + ' '+ res['words_result'][i]['words']
#
# with open('latex.txt','w') as f:
#     f.write(latex)

with open('latex.txt') as f:
    latex = f.read()
    latex = latex.split()
    res = []
    for each in latex:
        if len(each)>=3:
            flag=1
            for ch in each:
                if '\u4e00' <= ch <= '\u9fff':
                    flag=0
                    break
            if flag:
                res.append(each)
import re
tmp=[]
aa=[]
bb=[]
for each in res:
    if '\\' in each:
        a = re.findall('\\\\(.*)\{',each)
        if len(a)==0:
            a = re.findall('\\\\(.*)',each)
        if len(a)!=0:
            tmp.append(a[0])
    else:
        bb.append(each)
        a = re.findall(r'([a-z].*)]',each)
        if len(a) > 0:
            tmp.append(a[0])
with open('b.txt','w') as f:
    f.write('\n'.join(tmp))


