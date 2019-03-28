import os
import json
import re
path = r'F:\Dataset\arxiv_tex\1\cs.AI'
des_path = r'F:\Dataset\complete_text\cs.AI'

import shutil

files =  open('res1.txt').readlines()

for each in files:
	try:
		shutil.move(os.path.join(path,each[:-1]),os.path.join(des_path))
	except:
		continue
	
