path = "Gossiping" #文件夹目录  
import os
import json
from operator import itemgetter
files= os.listdir(path) #得到文件夹下的所有文件名称  
gossiping_array = []
i=0
for file in files: #遍历文件夹  
	i=i+1
	if not os.path.isdir(file): #判断是否是文件夹，不是文件夹才打开  
		with open(path+"/"+file , 'r',encoding = 'utf8') as reader:
			jf = json.loads(reader.read())
			for j in jf:
				try:
					j["UpVote"] = int(j["UpVote"])
					j["NoVote"] = int(j["NoVote"])
					j["DownVote"] = int(j["DownVote"])
					gossiping_array.append(j)
				except :
					print("ERROR")
					
# for i in gossiping_array:
# 	try:
# 		print(i["UpVote"])
# 	except :
# 		print("GGGGGG")
# 		print(i)
gossiping_array_sorted = sorted(gossiping_array , key=lambda x:x["UpVote"], reverse=True)
print("================================")
print(gossiping_array_sorted[0])
# for 