# -*- coding: utf-8 -*-
"""
@ Author: Jun Sun {Python3}
@ E-mail: sunjunee@qq.com
@ Create: 2017-08-07 19:52

Descript: 从实习僧网站爬取数据
"""

import requests;
from bs4 import BeautifulSoup;
import sys;
import math;
import pymysql;

def view_bar(num, total):
    rate = num / total
    rate_num = int(rate * 40)
    rate_nums = math.ceil(rate * 100);
    r = '\r[%s%s]%d%%\t%d/%d\t' % (">"*rate_num, " "*(40-rate_num), rate_nums, num, total,)
    sys.stdout.write(r)
    sys.stdout.flush()

source = 'http://www.shixiseng.com/interns?k=前端&p=';
pages = 37;
source2 = 'http://wap.shixiseng.com/app/intern/info?uuid=';

data = [];

for i in range(1, pages+1):
	view_bar(i, pages);
	try:
		r = requests.get(source + str(i));
		r.encoding = 'utf-8';
		
		soup = BeautifulSoup(r.text, 'html.parser')
		li = soup.find_all('div', attrs={'class':'list'});
																					
		#解析网页

		for j in range(len(li)):
			s = li[j];
			
			cag = (s.find('div', attrs = {'class':'part'}).text).split(' - ')[1];

			#链接：
			link = s.find('div', attrs = {'class':'names cutom_font'}).find('a').attrs['href']
			link = link.split('/')[2];

			r2 = requests.get(source2 + link);
			r2.encoding = 'utf-8';
			
			infos = eval(r2.text);
																											
			data.append(infos);
	except:
		print('Error!');

print('\n');
#存入mysql
db = pymysql.connect("localhost", "root", "Admin123456!", "test", charset="utf8");
cursor = db.cursor();
#cursor.execute("DROP TABLE IF EXISTS sxseng")
#
#sql = """CREATE TABLE sxseng (
#         cag CHAR(255),
#         iname CHAR(255),
#         industry CHAR(255),
#         cname CHAR(255),  
#         city CHAR(255),
#			address CHAR(255),
#			attraction CHAR(255),
#			chance CHAR(255),
#			degree CHAR(255),
#			maxsal CHAR(255),
#			minsal CHAR(255),
#			month CHAR(255),
#			scale CHAR(255),
#			info TEXT(2047),
#			url CHAR(255))"""
#
#cursor.execute(sql);

i = 0;
#Load to mysql:
for d in data:
	i+=1;
	view_bar(i, len(data));
	sql = "INSERT INTO sxseng(cag, iname, industry, cname, city, address, attraction, chance, degree, maxsal, minsal, month, scale, info, url) \
			  VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % \
	       (cag, d['msg']['iname'], d['msg']['industry'], d['msg']['cname'], d['msg']['city'], d['msg']['address'], d['msg']['attraction'], d['msg']['chance'],\
			  d['msg']['degree'], d['msg']['maxsal'], d['msg']['minsal'], d['msg']['month'], d['msg']['scale'], d['msg']['info'], d['msg']['url']);
	try:
		cursor.execute(sql)
		db.commit()
	except:
	   db.rollback()
db.close();
	