import os

files = os.listdir('cs.DS.1700.0')
cs = open('cs','r').readlines()
print(len(cs))
print(files[0])
for file in files:
    for line in cs:
        if file in line:
            cs.remove(line)
            print('ok')
            break


print(len(cs))
with open('a','w') as f:
    for each in cs:
        f.write(each)
# for line in cs:
#     print(line[:-1])
