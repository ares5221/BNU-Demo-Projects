## 数据预处理

preprocess_data中的代码文件对raw_data中数据进行预处理

### forum_data 

#### 数据读取

forum_data_clean.py 

读取论坛导出数据：问答数据导出_summary.xlsx：

数据信息维度如下：

问题ID	问题标题	问题描述	问题栏目	提问时间	问题用户ID	问题用户	问题用户工号	回答用户ID	回答用户	回答用户工号	回答用户单位	回答时间	回答内容	点赞数		

#### 数据清理

读取数据时，通过ID来标识不同问答信息；

同样的问题后接不定个数的答案，需要做答案筛选；

问题的描述采用 问题标题 的信息，若为空则使用 问答描述信息 ；
同一个问题后接不定个数的答案list，保存 回答内容 点赞数 信息。

```
dic={quesiongID:'d5233fdsgs', 
questionTxt:'孩子不写作文', 
answersDictList:[
{ans1:'xxx',supportNum:2}
{ans2:'xxx',supportNum:4}
{ans3:'xxx',supportNum:0}
]}
```

#### 答案筛选

对同一个问题的不同答案，筛选答案列表使得仅保留最优答案

当前用点赞个数来筛选答案，优先选择点赞个数高的答案；

若点赞数相同， 则选 答案内容 较长的；

若两个或多个答案内容长度仍然相同则随机选一个。

#### 保存数据

将最终数据保存在forum_data.csv，如：

```
评价一个好老师的标准是什么？,首先要有高尚的人格，其次是一颗爱孩子的心，然后是教学能力。
```

forum_data_pro.csv为原来的数据backup



### web_data 

#### 数据读取

forum_data_clean.py 

读取整理的docx文件：教育咨询师常见的10个经典问题解答.docx：

问题及答案按段落分开

#### 数据清理

数据存储在列表中，共9个问题18项

偶数项为问题内容，奇数项为答案

#### 数据保存

将最终数据保存在web_data.csv，如：

```
我的孩子不愿学习，经常出现厌学的情况，我想问问怎么办？,通过您所提供的孩子的信息可以初步判断，孩子的学习动机与兴趣没有得到充分激发与利用，还尚未培养出良好的学习习惯，这对他今后的学习无疑的产生较大的负面影响，这需要及时正确的引导。
```



### book_data

#### 数据读取

解析读取处理后的docx文件：book-work.docx：

#### 数据解析

book_data_phrase.py 

根据文档中问题为标题headline 1 格式，答案为Normal格式的不同，解析问题内容与答案内容

将问题内容的标号 1.xxx的“1.”去除掉，将答案中字符串合并为一个字符串，去除空字符与换行

todo-具体对答案进一步清理后面可能还需要处理



#### 数据保存

将最终数据保存在book_data.csv，如：

```
如何管理上课不带学习用具的学生？,"这似乎是一个不太重要的行为管理问题，但..."
如何管理学生的不良言语？,"总有一些学生试图问一些私人、不恰当、..."
```



### scrapy_data 

#### 数据采集

从网站先爬取数据，存储在raw_data/scrapy_data

scrapy_src 文件夹中为爬取网站的代码，主要爬取两个网站，分别在两个不同的文件夹中

##### 中国德育网

http://www.seewww.cn/

爬取红框标注部分内容

![image-20200527234705427](C:\Users\12261\AppData\Roaming\Typora\typora-user-images\image-20200527234705427.png)

\preprocess_data\scrapy_data_process\scrapy_src\seewww\scripy_main.py

爬取的数据保存在raw_data\scrapy_data\seewww



##### 班主任之友

http://www.bzrzy.cn/bbs/boards.asp?assort=2

爬取本页面的教育大家谈所有内容

![image-20200527144555310](C:\Users\12261\AppData\Roaming\Typora\typora-user-images\image-20200527144555310.png)

\preprocess_data\scrapy_data_process\scrapy_src\bzrzy\scripy_main.py

爬取的数据保存在raw_data\scrapy_data\bzrzy