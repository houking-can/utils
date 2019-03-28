import os
import json
import re
import shutil
path = r'F:\Dataset\arxiv_json\cs.AI'

files =  os.listdir(path)

for each in files:
	with open(os.path.join(path,each)) as f:
		content = f.read()
		name = re.findall(r'"id": "(.*?)"',content)[0]
	shutil.move(os.path.join(path,each),os.path.join(path,name+'.json'))
