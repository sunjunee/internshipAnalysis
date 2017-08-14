# -*- coding: utf-8 -*-
"""
@ Author: Jun Sun {Python3}
@ E-mail: sunjunee@qq.com
@ Create: 2017-08-09 20:54

Descript: 统计词频
"""

import pymysql;
import sys;
import math;

def view_bar(num, total):
    rate = num / total
    rate_num = int(rate * 40)
    rate_nums = math.ceil(rate * 100);
    r = '\r[%s%s]%d%%\t%d/%d\t' % (">"*rate_num, " "*(40-rate_num), rate_nums, num, total,)
    sys.stdout.write(r)
    sys.stdout.flush()

db = pymysql.connect("localhost", "root", "Admin123456!", "test", charset="utf8");
cursor = db.cursor();
cursor.execute("SELECT id, info_cut FROM sxseng")
datas = cursor.fetchall();
db.close();

wordBook = [];	count = [];
for i in range(len(datas)):
	data = datas[i][1];
	data = data.split('<cuts>');
	view_bar(i, len(datas));
	for word in data:
		if word not in wordBook:
			wordBook.append(word);
			count.append(1);
		else:
			count[wordBook.index(word)] += 1;

#存储到mysql：
db = pymysql.connect("localhost", "root", "Admin123456!", "test", charset="utf8");
cursor = db.cursor();
cursor.execute("DROP TABLE IF EXISTS wordFreq")

sql = """CREATE TABLE wordFreq (
         word CHAR(255),
			freq int)"""

cursor.execute(sql);

#Load to mysql:
for i in range(len(wordBook)):
	view_bar(i, len(wordBook));
	sql = "INSERT INTO wordFreq(word, freq) \
			  VALUES ('%s', '%d')" % \
	       (wordBook[i], count[i]);
	try:
		cursor.execute(sql)
		db.commit()
	except:
	   db.rollback()
db.close();
	