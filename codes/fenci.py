# -*- coding: utf-8 -*-
"""
@ Author: Jun Sun {Python3}
@ E-mail: sunjunee@qq.com
@ Create: 2017-08-09 19:51

Descript: 
"""
import pymysql;
import jieba
from bs4 import BeautifulSoup;
import math;
import sys;

def view_bar(num, total):
    rate = num / total
    rate_num = int(rate * 40)
    rate_nums = math.ceil(rate * 100);
    r = '\r[%s%s]%d%%\t%d/%d\t' % (">"*rate_num, " "*(40-rate_num), rate_nums, num, total,)
    sys.stdout.write(r)
    sys.stdout.flush()

db = pymysql.connect("localhost", "root", "Admin123456!", "test", charset="utf8");
cursor = db.cursor();
cursor.execute("SELECT id, info FROM sxseng")
a = cursor.fetchall();

datas = {};
for i in range(len(a)):
	s = BeautifulSoup(a[i][1], 'html.parser').text;
	datas[i+1] = s.replace('\xa0','');

#分词、存储到mysql
seged = {};
for key in datas.keys():
	view_bar(key, len(datas))
	seg = jieba.cut(datas[key], cut_all=False)
	seg = [s for s in seg];
	seged[key] = seg;
	seg = '<cuts>'.join(seg);

	sql = "UPDATE sxseng set info_cut = '%s' where id = '%d'" % (seg, key);								
	try:
	   cursor.execute(sql)
	   db.commit()
	except:
		print('Error!');
#	   db.rollback()

db.close();
