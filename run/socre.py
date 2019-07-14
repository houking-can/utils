# import os
# import json
# import shutil
# ground_truth = r'C:\Users\Houking\Desktop\CCKS\data\task1\json'
# model_output = r'C:\Users\Houking\Desktop\CCKS\output\task1'
# xlsx = r'C:\Users\Houking\Desktop\CCKS\data\task1\xlsx'
# model = os.listdir(model_output)
# cnt=0
# xx=0
# for each in model:
#     name,_ = os.path.splitext(each)
#     res = json.load(open(os.path.join(model_output,each),encoding='utf-8'))[name]
#     ground = json.load(open(os.path.join(ground_truth,each),encoding='utf-8'))[name]
#     log.write(each)
#     tmp = 0
#     for key, value in res.items():
#         if isinstance(value,dict):
#             m = value['项目']
#             xx+=len(m)
#             g = ground[key]['项目']
#             if len(m)!=len(g):
#                 cnt+=abs(len(m)-len(g))
#                 tmp+=abs(len(m)-len(g))
#                 log.write(key,len(m)-len(g))
#     if tmp>20:
#         shutil.move(os.path.join(xlsx,name+'.xlsx'),r'C:\Users\Houking\Desktop\a')
#         shutil.move(os.path.join(model_output,each),r'C:\Users\Houking\Desktop\a')
# log.write('')
# log.write(cnt,xx)
# log.write((xx-cnt)/xx)


import os
import json
import shutil

ground_truth = r'C:\Users\Houking\Desktop\CCKS\data\task1\json'
model_output = r'C:\Users\Houking\Desktop\error\json'
# model_output = r'C:\Users\Houking\Desktop\CCKS\output\task1'
xml = r'C:\Users\Houking\Desktop\error\error\xml'

model = os.listdir(model_output)
cnt = 0
xx = 0

log = open('log.txt','w',encoding='utf-8')
correct = 0
res_total = 0
gro_total = 0
for each in model:

    name, _ = os.path.splitext(each)
    res = json.load(open(os.path.join(model_output, each), encoding='utf-8'))[name]
    ground = json.load(open(os.path.join(ground_truth, each), encoding='utf-8'))[name]
    log.write(each+'\n')

    each_correct = 0
    each_res = 0
    each_gro = 0
    for key, value in res.items():
        if isinstance(value, dict):
            m = value['项目']
            res_total += len(m) + 1
            each_res+=len(m) + 1

            g = ground[key]['项目']
            gro_total += len(g) + 1
            each_gro+=len(g)+1
            if res[key]["单位"] == ground[key]["单位"]:
                correct += 1
                each_correct+=1
            for i_m in m:
                for i_g in g:
                    if i_m["名称"] == i_g["名称"]:
                        if i_m["附注"] == i_g["附注"] and i_m["年初至报告期末"] == i_g["年初至报告期末"] and i_m["上年年初至报告期末"] == i_g[
                            "上年年初至报告期末"]:
                            correct += 1
                            each_correct +=1
                        else:

                            log.write("%s" % (i_m["名称"])+'\n')
                            if i_m["附注"] != i_g["附注"]:
                                log.write("%s  %s" % (i_m["附注"],i_g["附注"])+'\n')
                            if i_m["年初至报告期末"] != i_g["年初至报告期末"]:
                                log.write("%s  %s" % (i_m["年初至报告期末"], i_g["年初至报告期末"])+'\n')
                            if i_m["上年年初至报告期末"] != i_g["上年年初至报告期末"]:
                                log.write("%s  %s" % (i_m["上年年初至报告期末"], i_g["上年年初至报告期末"])+'\n')
                        break

                    else:
                        continue

            # if len(m)!=len(g):
            #     cnt+=abs(len(m)-len(g))
            #     tmp+=abs(len(m)-len(g))
            #     log.write(key,len(m)-len(g))
        else:
            each_gro+=1
            each_res+=1
            res_total += 1
            gro_total += 1
            if ground[key] == value:
                each_correct+=1
                correct += 1
    # log.write(each)
    log.write('correct: %d\t res: %d\t ground: %d' % (each_correct, each_res, each_gro)+'\n\n')

    # if each_gro-each_correct>10:
    #     shutil.move(os.path.join(xml,name+'.xml'),r'C:\Users\Houking\Desktop\a')
    #     shutil.move(os.path.join(model_output,each),r'C:\Users\Houking\Desktop\a')
log.write('correct: %d\t res: %d\t ground: %d\n' % (correct, res_total, gro_total))
p = correct/res_total
r = correct/gro_total
log.write("p: %f\tr: %f\tf1: %f" % (p,r, 2*p*r/(p+r)))
# log.write(cnt, xx)
# log.write((xx - cnt) / xx)
