这是一个爬取**实习僧**网站信息 [截止2017年8月8日] 的爬虫，并对爬取的结果做了一些简单的处理。

使用的工具是python，用到了requests和Beautifulsoup来进行网页爬取，jieba进行分词处理。

## 爬虫
这里想爬的是实习僧网站上，所有互联网相关的实习招聘信息。打开网站可以看到目录：

![Image text](http://i2.nbimg.com/604893/410ce31f5cfba20a.jpg)

点开一个目录，其跳转的链接为：
https://www.shixiseng.com/interns?k=关键词&p=页码

于是可以通过上述链接，来获取所有互联网相关实习信息的列表，我在这里只取了该实习的链接，因为仔细观察可以发现，网页上的文字爬取下来都是乱码的，这可能是使用了特殊的字体和编码的原因。

不得不说，这一招用来反爬虫还是很有效的。打开每个实习地详情页，也都存在各种乱码。

![Markdown](http://i2.nbimg.com/604893/76cb45e1a461c5e0s.jpg)

但是，如果是乱码就完全不能分析了啊。然而，毕竟是，道高一尺魔高一丈，电脑端不行，我们转战手机网页端。

然后，就欣喜地发现，wwap网站有一个专门用来传递信息的API，真是得来全不费工夫啊，直接用API，解析的功夫都省了：

![Markdown](http://i4.nbimg.com/604893/ba0fb178da4c6871.jpg)

其用法是http://wap.shixiseng.com/app/intern/info?uuid=实习id
前面已经通过检索，爬到了所有互联网相关的实习链接，链接里面，就包含实习id，于是，数据就很方便地爬下来了~

```python
import requests;
from bs4 import BeautifulSoup;

source = 'http://www.shixiseng.com/interns?k=前端&p=';  pages = 37;
source2 = 'http://wap.shixiseng.com/app/intern/info?uuid=';
data = [];
for i in range(1, pages+1):
	try:
		r = requests.get(source + str(i));  r.encoding = 'utf-8';
		soup = BeautifulSoup(r.text, 'html.parser')
		li = soup.find_all('div', attrs={'class':'list'});																			
		#解析网页
		for j in range(len(li)):
			s = li[j];  cag = (s.find('div', attrs = {'class':'part'}).text).split(' - ')[1];
			#链接：
			link = s.find('div', attrs = {'class':'names cutom_font'}).find('a').attrs['href']
			link = link.split('/')[2];
			r2 = requests.get(source2 + link);  r2.encoding = 'utf-8';
			infos = eval(r2.text);																							
			data.append(infos);
	except:
		print('Error!');
```

## 分词

这里做分词的目的，主要是因为爬取下来的结构化信息确实不多，于是对职位描述这个字段进行分词，用到的工具是jieba。

使用的方法也很简单,分词后，使用<cuts>对结果进行分割，存储到了mysql中。

```python
import jieba
from bs4 import BeautifulSoup;

datas = {};
for i in range(len(a)):
	s = BeautifulSoup(a[i][1], 'html.parser').text;
	datas[i+1] = s.replace('\xa0','');

#分词
seged = {};
for key in datas.keys():
	view_bar(key, len(datas))
	seg = jieba.cut(datas[key], cut_all=False)
	seg = [s for s in seg];
	seged[key] = seg;
	seg = '<cuts>'.join(seg);

```

## 后续分析
使用mysql进行查询、Excel简单地可视化。

