import os
import json
import re
path = r'F:\Dataset\arxiv_json\cs.AI'

files =  os.listdir(path)

res = []
for each in files:
	with open(os.path.join(path,each)) as f:
		content = f.read()
		r = re.findall(r'"id": "(.*?)"',content)[0]
		res.append(r+'.tex')
	with open('res1.txt','w') as fw:
		fw.write('\n'.join(res))
