# -*- coding: utf-8 -*-
"""
@ Author: Jun Sun {Python3}
@ E-mail: sunjunee@qq.com
@ Create: 2017-08-13 10:10

Descript: 
"""

f = open('data.txt', 'r', encoding = 'utf-8');

datas = [];
while(True):
	line = f.readline();
	if(line):
		line = line.split('\t');	line[-1] = line[-1][0:-1];
		datas.append([line[0],line[1:]]);
	else:
		f.close();	break;

counts = {};
for i in range(len(datas)):
	for j in range(len(datas[i][1])):
		if datas[i][1][j] != '':
			if(datas[i][1][j] not in counts.keys()):
				counts[datas[i][1][j]] = eval(datas[i][0]);
			else:
				counts[datas[i][1][j]] += eval(datas[i][0]);

f = open('count_citys.txt', 'w');
for key in counts.keys():
	f.write(key + '\t' + str(counts[key]) + '\n');
f.close();