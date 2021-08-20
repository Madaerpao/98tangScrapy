**版权申明：笔记==入门部分内容==来源于[Python网络爬虫与信息提取_北京理工大学_中国大学MOOC(慕课) (icourse163.org)]，基于课程内容整理。全文由阿泰尔整理，仅供个人学习、研究，不得用于营利性目的。**

## 网络爬虫入门

**信息提取步骤：**

**Requests 库 ----请求获取信息**

**robots协议 ----依据协议是否可爬取 （合法性）**

**Request爬取 + bs4分析信息**

**MySQL Or Excel 存储信息**

---

### Requests 库入门

更多信息：https://www.python-requests.org

命令安装：

```shell
pip install requests
```

启动 Pycharm 测试：

```python
import requests
r = requests.get("https://www.baidu.com")
r.encoding = "utf-8"
x = r.status_code
print(x)
y = r.text
print(y)
```

![image-20210517191342937](C:\Users\ZK\AppData\Roaming\Typora\typora-user-images\image-20210517191342937.png)

---

#### Requests 方法介绍

![image-20210517184814576](C:\Users\ZK\AppData\Roaming\Typora\typora-user-images\image-20210517184814576.png)

----

##### 1.requests.get()

###### 主要功能

> 1.构造请求资源的**Request**对象（Python大小写敏感，因此构造的Request对象的R大写）2.返回的内容 r = requests.get(url) ，r 实质上是一个**Response**对象，包含从服务器返回的所有资源。

###### 常用参数

```python
requests.get(url,params=None,**kwargs)
```

> **url** ：指拟获取页面的链接
>
> **params **：指的是 **url** 中的额外参数 ，可以是字典、字节流（可选）
>
> **kwargs** : 12个其他参数（控制访问用途，可选）

![image-20210517190035415](C:\Users\ZK\AppData\Roaming\Typora\typora-user-images\image-20210517190035415.png)

requests.get() 的底层代码

封装形式如图所示，return就是封装的内容

```python
import requests
r = requests.get("https://www.baidu.com")
x = type(r)
y = r.headers
print(x)
print(y)
```

![image-20210517191717284](C:\Users\ZK\AppData\Roaming\Typora\typora-user-images\image-20210517191717284.png)

上述内容表明，返回对象为Response

###### Response对象的属性

![image-20210517191805096](C:\Users\ZK\AppData\Roaming\Typora\typora-user-images\image-20210517191805096.png)



> **r.encoding** : 如果返回的headers中没有charset，那么默认的编码方式ISO-8859-1
>
> **r.apparent_encoding** : 不依赖headers，根据返回的内容确定编码

原则上后者更加准确，基于内容分析的编码会更加准确

![image-20210517192837637](C:\Users\ZK\AppData\Roaming\Typora\typora-user-images\image-20210517192837637.png)

----

###### **爬取网页的通用代码框架**

一般使用`requests.get()`方法爬取网页，但是并不是一切皆可request的，需要先处理Requests库的异常处理。

![image-20210517193255700](C:\Users\ZK\AppData\Roaming\Typora\typora-user-images\image-20210517193255700.png)

```python
import requests
def getHTMLText(url):
    try:
        r = requests.get(url,timeout = 30)
        r.raise_for_status()    #如果返回的状态码不是200，引发HttpError异常
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return "产生异常"

if __name__ == '__main__':
    url = "https://www.baidu.com"
    m = getHTMLText(url)
    print(m)
```

>**Http协议**：响应和请求
>
>**URL** ： http://host:[port]/[path]  (资源定位)
>
>Get Head 都是纯获取  ，Patch Delete Put Post 都是提交
>
>PS ： Patch和Put都是对URL位置内容的更改，Patch仅上传覆盖被修改的局部，Put每次都是全局覆盖（无论是局部修改还是全局修改）。Patch更加节省带宽！

HTTP协议与Requests库的方法一一对应

---

##### 2.requests.request()

###### 主要功能

基础方法

###### 常用参数

```python
requests.request(method,url,**kwargs)
```

> **method** : 请求方式，对应get、post、put之类的http协议内容  OPTIONS为特有method
>
> **url** : 请求目标位置，拟获取页面的链接
>
> **kwargs** : 13个其他参数 控制访问 

| kwargs          | 类型                                                         |
| --------------- | ------------------------------------------------------------ |
| params          | 字典或字节序列，==作为参数增加到URL链接中==                  |
| json            | JSON格式数据                                                 |
| headers         | 字典，==头部信息（HTTP协议定制头部信息时可用）==             |
| cookies         | 字典或CookieJar                                              |
| auth            | 元组，HTTP认证功能                                           |
| data            | 字典、字节或文件对象，向服务器提交，作为Request的内容        |
| files           | 字典，向服务器传输文件时适用 如定义一个 fs = {'file':open('data.xls','rb')} |
| timeout         | 以秒为单位，计时                                             |
| proxies         | 字典，==设定访问代理服务器，增加登录认证信息==               |
| allow_redirects | True/False，默认Ture，重定向开关                             |
| stream          | 开关字段                                                     |
| verify          | 开关字段                                                     |
| cert            | 本地SSL认证文件路径字段                                      |

---

##### 3.requests.head()

###### 主要功能

获取头部信息

###### 常用参数

```python
requests.head(url,**kwargs)
```

> **url** : 页面链接
>
> **kwargs** ：13个访问控制参数，同上

---

##### 4.requests.post()

###### 主要功能

发送Post请求以获取信息，区别于get的纯获取，Post要传送一些信息上去，可能是Head、data之类的

###### 常用参数

```python
requests.post(url,data=None,json=None,**kwargs)
```

> **url** : 页面链接  
>
> **data** : 字典、字节序列或文件，Request内容
>
> **json** : JSON格式数据
>
> **kwargs **: 11个访问控制参数

---

##### 5.requests.put()

###### 主要功能

上传覆盖指定url位置的信息

###### 常用参数

```python
requests.put(url,data=None,**kwargs)
```

>**url** : 页面链接
>
>**data** : 字典、字节序列或文件，作为Request的内容
>
>**kwargs**  ：12个访问控制参数

---

##### 6.requests.patch()

###### 主要功能

上传覆盖功能类似于put，但是仅覆盖变动部分，不是全局覆盖

###### 常用参数

```python
requests.patch(url,data=None,**kwargs)
```

>**url** : 页面链接
>
>**data** : 字典、字节序列或文件，作为Request的内容
>
>**kwargs**  ：12个访问控制参数

---

##### 7.requests.delete()

###### 主要功能

删除指定页面的信息内容资源

###### 常用参数

```python
requests.delete(url,**kwargs)
```

> **url** :页面链接
>
> **kwargs** : 13个访问控制参数

--------

### 网络爬虫的“盗亦有道”

#### 1.网络爬虫带来的问题

根据尺寸分类、调用的库不同

| 爬虫特征                                     | 功能     | 调用的库       |
| -------------------------------------------- | -------- | -------------- |
| 小规模，数据量小，爬取速度不明感             | 爬取网页 | Request        |
| 中规模，数据规模大，爬取速度敏感             | 爬取网站 | Scrapy         |
| 大规模，搜索引擎（全Internet），爬取速度关键 | 全网     | 不存在第三方库 |

**1.爬虫可能带来网络“骚扰”，给服务器带来巨大压力**

**2.爬虫的法律风险：著作权归属，爬取内容后不能用于牟利（民事巨额赔偿）**

**3.隐私泄露：网络爬虫有突破能力，突破简单的访问控制，获取他人隐私**

----

#### 2.网络爬虫的限制

>**1.来源审查：Http协议头部信息，user-agent的限制，只对浏览器和友好的爬虫开放访问相应**
>
>**2.发布公告：rebots协议，告知所有爬虫相应策略，要求爬虫遵守（只是发布，是否遵守全靠爬虫自身是否遵守）**

==robots协议：网络爬虫排除标准，告知其可抓取和不可抓取的页面，在网站根目录下放入robots.txt文件描述。==

```she
User-Agent: * 	#爬虫类型（名称）
Disallow: /     #不允许爬取的目录
```

------

### Request爬虫实例练习

#### 1.爬取指定商品网页信息

链接：https://item.jd.com/100014348492.html

```python
import requests
def getHTMLText(url):
    try:
        r = requests.get(url,timeout = 30)
        r.raise_for_status()    #如果返回的状态码不是200，引发HttpError异常
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return "产生异常"

if __name__ == '__main__':
    url = "https://item.jd.com/100014348492.html"
    m = getHTMLText(url)
    print(m)
```

```html
<!DOCTYPE HTML>
<html lang="zh-CN">
<head>
    <!-- shouji -->
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <title>【小米Redmi 9A】Redmi 9A 5000mAh大电量 大屏幕大字体大音量 1300万AI相机 八核处理器 人脸解锁 4GB+64GB 砂石黑 游戏智能手机 小米 红米【行情 报价 价格 评测】-京东</title>
    <meta name="keywords" content="MIRedmi 9A,小米Redmi 9A,小米Redmi 9A报价,MIRedmi 9A报价"/>
    <meta name="description" content="【小米Redmi 9A】京东JD.COM提供小米Redmi 9A正品行货，并包括MIRedmi 9A网购指南，以及小米Redmi 9A图片、Redmi 9A参数、Redmi 9A评论、Redmi 9A心得、Redmi 9A技巧等信息，网购小米Redmi 9A上京东,放心又轻松" />
    <meta name="format-detection" content="telephone=no">
    <meta http-equiv="mobile-agent" content="format=xhtml; url=//item.m.jd.com/product/100014348492.html">
    <meta http-equiv="mobile-agent" content="format=html5; url=//item.m.jd.com/product/100014348492.html">
    <meta http-equiv="X-UA-Compatible" content="IE=Edge">
    <link rel="canonical" href="//item.jd.com/100014348492.html"/>
        <link rel="dns-prefetch" href="//misc.360buyimg.com"/>
    <link rel="dns-prefetch" href="//static.360buyimg.com"/>
    <link rel="dns-prefetch" href="//img10.360buyimg.com"/>
    <link rel="dns-prefetch" href="//img11.360buyimg.com"/>
    <link rel="dns-prefetch" href="//img13.360buyimg.com"/>
    <link rel="dns-prefetch" href="//img12.360buyimg.com"/>
    <link rel="dns-prefetch" href="//img14.360buyimg.com"/>
    <link rel="dns-prefetch" href="//img30.360buyimg.com"/>
   …………
   …………
```

其他商品也可以通过上述代码爬取到！！！

#### 2.爬取亚马逊商品信息

链接：https://www.amazon.cn/gp/product/B01M8L5Z3Y

先用上面的代码测试一下：

```python
import requests
def getHTMLText(url):
    try:
        r = requests.get(url,timeout = 30)
        r.raise_for_status()    #如果返回的状态码不是200，引发HttpError异常
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return "产生异常"

if __name__ == '__main__':
    url = "https://www.amazon.cn/gp/product/B01M8L5Z3Y"
    m = getHTMLText(url)
    print(m)
```

由于是Python爬虫header信息，所以会被亚马逊拒绝爬取指定网页，虽然能够收到网页信息，但是会收到API不支持的页面，而不是商品信息页面！

需要写一个键值对作为Header信息封装到Request里，伪装成浏览器。

```python
header = {"User-Agent" : "Mozilla/5.0"}
```

request.get()的方法也可以访问，但是要把header封装进去

```python
r = requests.get(url,headers = header,timeout = 30)
```

完整框架如下：

```python
import requests
def getHTMLText(url):
    try:
        header = {"User-Agent": "Mozilla/5.0"}  #伪装自己是浏览器
        r = requests.get(url,timeout = 30, headers = header) #封装请求
        r.raise_for_status()    #如果返回的状态码不是200，引发HttpError异常
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return "产生异常"

if __name__ == '__main__':
    url = "https://www.amazon.cn/gp/product/B01M8L5Z3Y"
    m = getHTMLText(url)
    print(m)
```

#### 3.百度/360关键词提交获取搜索结果

先找到对应的关键词接口：

百度：https://www.baidu.com/s?wd=

360：https://www.so.com/s?q=

构造对应的url链接，通过params的键值对加入对应链接中，以百度为例：

```python
kw1 = { 'wd' : 'Python' }   #针对百度而言，前面是接口wd，后面是关键词
```

360同理：

```python
kw2 = {'q':'Python'}
```

只需要将上述信息用params封装进请求里就可以了

完整代码如下：

```python
import requests
def getHTMLText():
    try:
        url1 = "http://www.baidu.com/s"
        url2 = "https://www.so.com/s"
        kw1 = {"wd":"Python"}
        kw2 = {'q':'Python'}
        header = {"User-Agent": "Mozilla/5.0"}
        r1 = requests.get(url1,timeout = 30,headers=header,params=kw1)
        r1.raise_for_status()    
        r1.encoding = r1.apparent_encoding
        r2 = requests.get(url2,timeout = 30,headers=header,params=kw2)
        r2.raise_for_status()    
        r2.encoding = r2.apparent_encoding
        return r1.text + r2.text
    except:
        return "产生异常"
if __name__ == '__main__':
    m = getHTMLText()
    print(m)
```

检测请求网址的代码：

```python
r1.request.url
r2.request.url
```

检测内容长度代码：

```python
len(r1.text)
```

def可以调整变量

```python
import requests
def getHTMLText(baidu,so):
    try:
        url1 = "http://www.baidu.com/s"
        url2 = "https://www.so.com/s"
        kw1 = {"wd":baidu}  #替换为变量
        kw2 = {'q':so}		#同上
        header = {"User-Agent": "Mozilla/5.0"}
        r1 = requests.get(url1,timeout = 30,headers=header,params=kw1)
        r1.raise_for_status()    
        r1.encoding = r1.apparent_encoding
        r2 = requests.get(url2,timeout = 30,headers=header,params=kw2)
        r2.raise_for_status()    
        r2.encoding = r2.apparent_encoding
        return r1.text + r2.text
    except:
        return "产生异常"
if __name__ == '__main__':
    x = 'Python'
    y = 'Python'
    m = getHTMLText(x,y)
    print(m)
```

#### 4.网络图片的爬取和存储

分析图片链接的格式：

往往是` url+picture.jpg`的格式，是一个文件，这就涉及两个问题：

##### （1）如何爬取？

图片是二进制内容 这就涉及到返回**Response对象的属性**（详见前文requests.get()部分的内容），采用r.content可以返回对应的二进制数据，因此，爬取图片可以用以下代码：

```python
r = requests.get(url)
r.raise_for_status()
r.encoding = r.apparent_encoding
return r.content
```

##### （2）如何保存？

保存问题的解决 需要考虑两个方面，一是保存路径，二是保存文件的代码怎么写：

就保存路径而言，我们可以自己定义一个绝对路径（相对路径也是可以的），我定义了D盘，将其保存为abc.jpg:

```python
path = "d://abd.jpg" 			# // 为了防止转译，需要用两个
```

那我如果不想指定名字呢？只想让它保存在某个目录下：

```python
import os           #引入OS库 判断文件是否存在、新建目录时使用
root = "d://pics//" #保存在d盘的pics目录下 
path = root + url.split('/')[-1]          #根目录+url，按照"/"区分，按内容的倒数第一个命名（就是末尾）
if not os.path.exists(root):             #判断是否存在根目录
	os.mkdir(root)                      #不存在就创建
```

保存文件的代码怎么写？首先，以可写的二进制方式，打开一个文件（不存在的话，不用担心会自动新建），然后写入二进制信息：

```python
if not os.path.exists(path): 		#也可以判断一下是否已经有同名文件存在，避免随意覆盖
	with open(path,"wb") as f :  	#w代表以可写的方式打开，b代表以二进制方式打开
    	f.write(r.content)		 	# .write就是写入了（这里必须后面是二进制内容，因为以二进制打开的）
    	f.close()					#记得写完关闭，否则会因为占用而影响其他程序使用该文件
else:
    print("已经有文件存在了！！")
```

完整代码：

```python
import requests
import os          				#引入OS库，用来判断路径是否存在，不存在可以创建，对存在的同名文件可以跳过
def getHTML(url):
    try:
        header = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url,headers=header)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.content
    except:
        return "产生异常"
def save(root,path,content):
    try:
        if not os.path.exists(root):             #判断是否存在根目录
            os.mkdir(root)                      #不存在就创建
        if not os.path.exists(path):            #判断是否有同名文件存在，没有才会继续执行
            with open(path,"wb") as f :
                f.write(content)
                f.close()
                print("文件写入成功")
        else:
            print("文件已经存在")
    except:
        print("文件写入失败")
if __name__ == "__main__":
    root  = "D://pics//"                       #写了一个根目录
    url = 'https://www.zkwd888.ltd/bbs/data/attachment/forum/202104/14/221155wbtialbxgbrxgge1.jpg'
    path = root + url.split('/')[-1]          #按照"/"区分的倒数第一个命名221155wbtialbxgbrxgge1.jpg
    content = getHTML(url)
    save(root,path,content)
```

爬取动画、视频同样的道理，二进制文件写入即可！！！

----

### BeautifulSoup库

#### `BeautifulSoup`库入门

解析数据需要使用`bs4`库：https://www.crummy.com/software/Beautifulsoup

安装`bs4`库

```python
pip install beautifulsoup4
```

测试：

使用指定HTML页面：http://python123.io/ws/demo.html

```python
import requests
from bs4 import BeautifulSoup
url = "http://python123.io/ws/demo.html"
r = requests.get(url)
r.encoding = r.apparent_encoding
demo = r.text
soup = BeautifulSoup(demo,"html.parser")			#解析器是HTML
print(soup.prettify())
```

得到的结果：

```html
<html>
 <head>
  <title>
   This is a python demo page
  </title>
 </head>
 <body>
  <p class="title">
   <b>
    The demo python introduces several python courses.
   </b>
  </p>
  <p class="course">
   Python is a wonderful general-purpose programming language. You can learn Python from novice to professional by tracking the following courses:
   <a class="py1" href="http://www.icourse163.org/course/BIT-268001" id="link1">
    Basic Python
   </a>
   and
   <a class="py2" href="http://www.icourse163.org/course/BIT-1001870001" id="link2">
    Advanced Python
   </a>
   .
  </p>
 </body>
</html>
```

BeautifulSoup库是对标签树的解析、遍历、维护，只要是标签类型的数据，这个库就都能解析处理。

![image-20210518134037115](C:\Users\ZK\AppData\Roaming\Typora\typora-user-images\image-20210518134037115.png)

最常用的引入方式：

```python
from bs4 import BeautifulSoup
```

从`bs4`库中引入了一个类型`BeautifulSoup`，每一个标签树都会被转换成`BeautifulSoup`类数据。

---

##### `BeautifulSoup`库的解析器（parser）

![image-20210518134447585](C:\Users\ZK\AppData\Roaming\Typora\typora-user-images\image-20210518134447585.png)

##### `BeautifulSoup`类的基本元素

![image-20210518134652407](C:\Users\ZK\AppData\Roaming\Typora\typora-user-images\image-20210518134652407.png)

==格式：是获得对应内容的方式，如获取<p>内容，就是`soup.p`，获取<p>的名称，就是`soup.p.name`，但是，这种方法都只能获得数据中第一个对应的标签的内容。==

> 以demo为例，获取页面的各种元素。

###### 获取标签、标签名、父标签名（包含标签的标签）

```python
import requests
from bs4 import BeautifulSoup
url = "http://python123.io/ws/demo.html"
r = requests.get(url)
r.encoding = r.apparent_encoding
demo = r.text
soup = BeautifulSoup(demo,"html.parser")
title = soup.title			#获取标题内容
a = soup.a					#获取标签为a的内容
name = soup.a.name						#获得标签的名字
pname = soup.a.parent.name				#获得其父标签的内容
print("-"*50+"\n"+"标题信息:",title)
print("-"*50+"\n"+"a的标签内容:",a)
print("-"*50+"\n"+"a的标签名:",name)
print("-"*50+"\n"+"a的父标签名:",pname)
```

###### 获取标签的属性（可用于img标签）

```python
import requests
from bs4 import BeautifulSoup
url = "http://python123.io/ws/demo.html"
r = requests.get(url)
r.encoding = r.apparent_encoding
demo = r.text
soup = BeautifulSoup(demo,"html.parser")
tag = soup.a
print(tag.attrs)
```

得到以下内容：

```python
{'href': 'http://www.icourse163.org/course/BIT-268001', 'class': ['py1'], 'id': 'link1'}
```

这是一个字典，以键值对的方式呈现，因此，可以通过键读取到值：

```python
class = tag.attrs["class"] #读取class对应的值
print(class)
herf = tag.attrs["herf"]	#同理
print(herf)
```

无论有实际的标签无属性，都可以获得一个对应的字典，无属性会获得空字典。

###### 获得标签包裹的字符串

```python
import requests
from bs4 import BeautifulSoup
url = "http://python123.io/ws/demo.html"
r = requests.get(url)
r.encoding = r.apparent_encoding
demo = r.text
soup = BeautifulSoup(demo,"html.parser")
string = soup.a.string
print(string)
```

得到结果：

```python
Basic Python
```

**注意**：

如果有\<p>\<b>string\</b>\</p>多标签叠加的情况，string也是可以跨越获取内部的数据的。

\<b>\<!--内容-->\</b>，这样的形式下，`soup.b.string`获取的内容只有“内容”二字，但不会包括叹号和尖括号以及其他字符。

---

##### 基于`bs4`库的HTML遍历方法

![image-20210518145252302](C:\Users\ZK\AppData\Roaming\Typora\typora-user-images\image-20210518145252302.png)

###### 下行遍历

| .contents                        | .children                                       | .decedents                       |
| -------------------------------- | ----------------------------------------------- | -------------------------------- |
| 获取标签树下子节点，形成一个列表 | 类似于.contents，获取标签树下的子节点，形成列表 | 获取标签树下的所有节点，形成列表 |

举例：

```python
import requests
from bs4 import BeautifulSoup
url = "http://python123.io/ws/demo.html"
r = requests.get(url)
r.encoding = r.apparent_encoding
demo = r.text
soup = BeautifulSoup(demo,"html.parser")
head = soup.head			#获取Head标签的信息
son1 = soup.head.contents			#获取Head的子节点的信息（子标签），内含字符串节点，例如\n
son2 = soup.head.children			#同上
decedent = soup.head.decdents		#获取所有子孙节点的信息 形成列表 
print(son1)
print(son2)
print(decedent)
```

对于\<body>\</body>这种比较多的，可能会形成一个大列表，可通过 **for循环** 遍历读取其中的每个内容。例如：

```python
import requests
from bs4 import BeautifulSoup
url = "http://python123.io/ws/demo.html"
r = requests.get(url)
r.encoding = r.apparent_encoding
demo = r.text
soup = BeautifulSoup(demo,"html.parser")
body = soup.body			#获取body标签的信息
content = soup.body.contents			#获取body的子节点的信息（子标签），内含字符串节点，例如\n
for child in content:
    print(child)
```

###### 上行遍历

| .parent      | .parents                         |
| ------------ | -------------------------------- |
| 节点的父标签 | 节点的先辈标签（可用于循环遍历） |

###### 平行遍历

| .next_sibling                                    | .previous_sibling  | .next_siblings         | .previous_siblings     |
| ------------------------------------------------ | ------------------ | ---------------------- | ---------------------- |
| 找到下一个平行节点（同级标签以及其包含的字符串） | 找到上一个平行节点 | 找到后面的其他平行节点 | 找到前面的其他平行节点 |

平行遍历是有条件的：所有平行遍历必须发生在一个父节点下

![image-20210518145422579](C:\Users\ZK\AppData\Roaming\Typora\typora-user-images\image-20210518145422579.png)

举例，以body下的a为例：

```python
import requests
from bs4 import BeautifulSoup
url = "http://python123.io/ws/demo.html"
r = requests.get(url)
r.encoding = r.apparent_encoding
demo = r.text
soup = BeautifulSoup(demo,"html.parser")
a = soup.a						#获取a标签的信息
next = soup.a.next_sibiling 	#获取a的下一个平行子标签
print(next)
```

---

##### 基于`bs4`库的HTML格式的输出

考虑一个问题，如何使HTML更加友好的让人阅读？需要一个方法：

```python
from bs4 import BeautifulSoup
import requests
url = "http://python123.io/ws/demo.html"
r = requests.get(url)
r.encoding = r.apparent_encoding
demo = r.text
soup = BeautifulSoup(demo,"html.parser")
pretty = soup.prettify()
print(pretty)
```

> **.prettify()**是`BeautifulSoup`类型下的一个方法，能够自动为标签添加回车符，显示出来的内容会更加容易阅读
>
> 这种方法对单独的某个标签也可以处理哦！~（默认解码`utf-8`，无需转换）

---

#### 信息组织和提取

##### 信息标记

通过标记信息，使得我们能够理解信息反馈的含义，例如：name:阿泰尔 addr:China ，这样的标记告诉我们，阿泰尔是名字，中国是地址。

###### 信息标记的形式

| html                                                    | xml                                                          | yaml                   | json                 |
| ------------------------------------------------------- | ------------------------------------------------------------ | ---------------------- | -------------------- |
| \<p>声音、图像、视频等\</p>，通过标签组织的形式得到标记 | 类似于html，也是通过标签来实现标记，但是它可以缩写\<img scr="1234.jpg" />，当标签中不需要包含内容时，只用一个尖括号就可以完美结束。也可以增加注释\<!--123--> | 无数据类型的键值对方式 | 有类型的键值对的方式 |

##### 信息提取一般方法

> 方法一：
>
> 1.完整解析信息的标记形式，再提取关键信息
>
> XML JSON YAML
>
> 2.需要标记解析器，如上述的bs4的标签树遍历方式
>
> 优点：准确、完整
>
> 缺点：麻烦、耗时耗力

>方法二：
>
>1.无视标记形式，直接信息搜索
>
>2.需要用查找函数.find_all()
>
>优点：快速、简单
>
>缺点：准确性相比一较差，其准确性依赖明确的信息内容

> 融合方法：
>
> 实质上是解析+搜索
>
> 1.具备标记解析器的能力
>
> 2.能够对文本进行查找
>
> 思路：
>
> 首先，用搜索方式找到指定标签如\<a>
>
> 然后，解析\<a>标签，提取对应的内容

举例：

```python
from bs4 import BeautifulSoup
import requests
url = "http://python123.io/ws/demo.html"
r = requests.get(url)
r.encoding = r.apparent_encoding
demo = r.text
soup = BeautifulSoup(demo,"html.parser")
for link in soup.find_all("a"):
    print(link.get("href"))
```

###### .find_all()函数

常用变量分析：

```python
soup.find_all(name,attrs,recursive,string,**kwargs)
```

| 变量                  | 内涵                                                         |
| --------------------- | ------------------------------------------------------------ |
| name（标签名，如'a'） | 对标签名的检索字符串，可以有多个标签名.find_all(["a","b"])，**.find_all(Ture)可以获得所有标签名** |
| attrs （标签属性值）  | 对标签属性值的检索字符串，如p标签的course属性值，.find_all("p","course"),也可定义.find_all(course="1") |
| recursive             | 是否对子孙进行搜索的开关，默认是Ture，关闭后只检索子标签     |
| string                | 对字符串域的检索                                             |

举例：

```python
.find_all(True)
```

----

### 实例：中国大学排名爬虫

网站：(页面已经改变，无法静态爬取，代码仅供参考)

特点：静态网页

调用的库：bs4\requests\from bs4 import BeautifulSoup

输出方式：整齐打印

###### 补充输出的format方法

| 数字       | 格式                                                         | 输出                   | 描述                         |
| :--------- | :----------------------------------------------------------- | :--------------------- | :--------------------------- |
| 3.1415926  | {:.2f}                                                       | 3.14                   | 保留小数点后两位             |
| 3.1415926  | {:+.2f}                                                      | +3.14                  | 带符号保留小数点后两位       |
| -1         | {:+.2f}                                                      | -1.00                  | 带符号保留小数点后两位       |
| 2.71828    | {:.0f}                                                       | 3                      | 不带小数                     |
| 5          | {:0>2d}                                                      | 05                     | 数字补零 (填充左边, 宽度为2) |
| 5          | {:x<4d}                                                      | 5xxx                   | 数字补x (填充右边, 宽度为4)  |
| 10         | {:x<4d}                                                      | 10xx                   | 数字补x (填充右边, 宽度为4)  |
| 1000000    | {:,}                                                         | 1,000,000              | 以逗号分隔的数字格式         |
| 0.25       | {:.2%}                                                       | 25.00%                 | 百分比格式                   |
| 1000000000 | {:.2e}                                                       | 1.00e+09               | 指数记法                     |
| 13         | {:>10d}                                                      | 13                     | 右对齐 (默认, 宽度为10)      |
| 13         | {:<10d}                                                      | 13                     | 左对齐 (宽度为10)            |
| 13         | {:^10d}                                                      | 13                     | 中间对齐 (宽度为10)          |
| 11         | `'{:b}'.format(11) '{:d}'.format(11) '{:o}'.format(11) '{:x}'.format(11) '{:#x}'.format(11) '{:#X}'.format(11)` | `1011 11 13 b 0xb 0XB` | 进制                         |

>  **^**, **<**, **>** 分别是居中、左对齐、右对齐，后面带宽度， **:** 号后面带填充的字符，只能是一个字符，不指定则默认是用空格填充。
>
> **+** 表示在正数前显示 **+**，负数前显示 **-**； （空格）表示在正数前加空格
>
> b、d、o、x 分别是二进制、十进制、八进制、十六进制。

代码如下：

```python
import bs4
import requests
from bs4 import BeautifulSoup

def getHTMLText(url):
    try:
        r = requests.get(url,timeout=30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
	except:
        return ""
def putlist(list,html):
    soup = BeautifulSoup(html,"html.parser")
    for tr in soup.find("tbody").children:
        if isinstance(tr,bs4.element.Tag):
            tds = tr("td")
            list.append([tds[0].string,tds[1].string,tds[2].string])
def printls(list,num):
    t = "{0:^10}\t{1:{3}^10}\t{2:^10}"
    print(t.format("排名","名称","所在地",char(12288)))
    for i in range(num) :
        u = list[i]
        print(t.format(u[0],u[1],u[2]))
if __name__ == "__main__":
    url = "http://www.zuihaodaxue.cn/zuihaodaxuepaiming2019.html"
    list = []
    num = 20
    html = getHTMLText(url)
    putlist(list,html)
    printls(list,num)
```

----

### 正则表达式入门

re库用于表达一组字符串（将字符串公式化），表示一组字符串的特征或模式，实现简洁化处理——一行胜千言，可用于匹配搜索、判断。

例如：

```shell
"PY"
"PYY"
"PYYY"
"PYYYY"
…………
"PYYYYYYYYYY……"
#上述字符串正则表达式为：
PY+

#以PY开头。后续存在不多于10个字符，但是其中不能存在字符“P”或“Y”
"PYABC"  ✔
"PYXYZ"  ✖
#正则表达式为：
PY[^PY]{0,10}
```

#### 正则表达式的使用

使用的前提：将字符串编译，抽象出其特征。

##### 正则表达式的语法和方法：

> 函数式用法：
>
>  rst = re.search(r'[1-9]\d{5}',"BIT100081")
>
> 面向对象的用法：
>
> pat = re.compile(r'[1-9]\d{5}')   #意指pattern
>
> rst = pat.search("BIT100081")

###### re.complie(pattern,flags)

将正则表达式的字符串形式----编译----正则表达式对象

字符+操作符

![image-20210521192725502](C:\Users\ZK\AppData\Roaming\Typora\typora-user-images\image-20210521192725502.png)

![image-20210521193155995](C:\Users\ZK\AppData\Roaming\Typora\typora-user-images\image-20210521193155995.png)

> 原生字符串类型：避免转译，只需要在正则表达式前面加r即可，r"d:/pics"可以等价于:"d://pics"

![image-20210521152948877](C:\Users\ZK\AppData\Roaming\Typora\typora-user-images\image-20210521152948877.png)

###### re.search(pattern,string,flags=0)

> pattern:正则表达式的字符串或原生字符串
>
> string:表示要与正则表达式匹配的字符串，待匹配的字符串（类似于概念——库）
>
> flags:控制标记

![image-20210521195921377](C:\Users\ZK\AppData\Roaming\Typora\typora-user-images\image-20210521195921377.png)

例子：

```python
import re
match = re.search(r"[1-9]\d{5}","BIT 100081")
if match :				#如何判断match与否？用if语句就可以了
    match.group(0)
```

###### re.match(pattern,string,flags=0)

变量参数类似于re.search()

```python
import re
match = re.match(r"[1-9]\d{5}","BIT 100081")
if match :
    match.group(0)
#没有输出任何结果，空变量

#如果不使用if语句：
match.group(0)
#报错

```

###### re.findall(pattern,string,flags=0)

返回的是**列表类型**，参数类似以上，可以将所有匹配的字符串整合出来

```python
import re 
ls = re.findall(r"[1-9]\d{5}","BIT100081 TSU100084")
ls
#输出结果：
["100081","100084"]
```

###### re.split(pattern,string,maxsplit=0,flags=0)

功能：分割字符串、返回一个列表

> maxsplit：最大分割数，超出最大分割数部分则作为整体，放在最后

```python
import re 
re.split(r'[1-9]\d{5}',"BIT100081 TSU100084")
#将匹配的地方去掉，剩下的部分作为返回的列表
['BIT','TSU','']
re.split(r'[1-9]\d{5}',"BIT100081 TSU100084",maxspilt=1)
#最大分割数为1，则只分割一次
['BIT',"TSU100084"]
```

###### re.finditer(pattern,string,flags=0)

返回一个**迭代类型**，每个都是match对象，一般用for循环出来。**注意对比findall.**

```python
import re 
for m in re.finditer(r'[1-9]\d{5}',"BIT100081 TSU100084"):
    if m:
        print(m.group(0))
#返回的不是列表，而是列表里的每个迭代。
100081
100084
```

###### re.sub(pattern,repl,string,flags=0,count=0)

> repl：替换匹配字符串的字符串
>
> count：替换的最大次数

```python
import re 
re.sub(r'[1-9]\d{5}',":zipcode","BIT100081 TSU100084")
#输出
"BIT:zipcode TSU:zipcode"
```

---

##### Match对象的属性

![image-20210522134531819](C:\Users\ZK\AppData\Roaming\Typora\typora-user-images\image-20210522134531819.png)

```python
import re 
m = re.search(r"[1-9]\d{5}","BIT 100081")
m.string
#输出
"BIT 100081"
m.re
#输出
re.compilr("[1-9]\\d{5}") #输出的带compile，程序认为只有经过compile的才是正则表达式，未经过的，只能算是一种表示
m.pos
#输出
0
m.endpos
#输出
9
```

##### Match对象的方法

![image-20210522134636658](C:\Users\ZK\AppData\Roaming\Typora\typora-user-images\image-20210522134636658.png)

```python
import re 
m = re.search(r"[1-9]\d{5}","BIT 100081")
m.group(0)
"100081"
m.start()
3
m.end()
9
m.span()
(3,9)
```

#### 贪婪匹配和最小匹配

不加任何标识，使用search函数，会默认是贪婪匹配

![image-20210522135548793](C:\Users\ZK\AppData\Roaming\Typora\typora-user-images\image-20210522135548793.png)

![image-20210522135603246](C:\Users\ZK\AppData\Roaming\Typora\typora-user-images\image-20210522135603246.png)

增加了?，本质上还是正则表达式的语法内容：

![image-20210522135655053](C:\Users\ZK\AppData\Roaming\Typora\typora-user-images\image-20210522135655053.png)

---

### 实例：淘宝商品比价定向爬虫

> 功能描述：获取商品搜索页面信息，提取价格进行比较
>
> 思路：
>
> 1.获取淘宝搜索接口
>
> 2.翻页的处理
>
> 技术路线：
>
> requests库+re库

搜索起始页链接：

```shell
https://s.taobao.com/search?q=书包&js=1&stats_click=search_radio_all%3A&initiative_id=staobaoz_20170105&ie=utf8
```

接口：https://s.taobao.com/search?q=书包

第二页和第三页：

```shell
https://s.taobao.com/search?q=书包&js=1&stats_click=search_radio_all%3A&initiative_id=staobaoz_20170105&ie=utf8&bcoffset=0&ntoffset=0&p4ppushleft=1%2C48&s=44

https://s.taobao.com/search?q=书包&js=1&stats_click=search_radio_all%3A&initiative_id=staobaoz_20170105&ie=utf8&bcoffset=0&ntoffset=0&p4ppushleft=1%2C48&s=88
```

末尾数字变化为44\88，每页恰好44商品，s可能表示每页的**起始商品**的编号（从0开始标记，第一页是0-43，第二页为44-87）

> 程序设计：
>
> 1.提交搜索请求，**循环获取**页面
>
> 2.对于每个页面提取商品名称和价格信息
>
> 3.将名称和价格输出到屏幕上

```python
import requests
import re

def getHTMLText(url):				#爬取页面
    try:
        r = requests.get(url, timeout = 30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ""
    
def parsePage(ilt,html):			#解析页面信息，由于淘宝的页面是脚本语言，不是传统的html页面，故不调用bs4库
    try:
        plt = re.findall(r'\"view_price\":\"[\d\.]*\"',html)
    	# \表示在正则表达式内引入双引号，因此双引号都用\"来表示，我们的字符串是通过上面那个函数获取到的r.text=html
    	tlt = re.findall(r'"\raw_title\":\".*?"',html)
        # *?表示最小匹配，表明只取得一个双引号的内容，后面的东西即使有双引号 也不提取
    
        for i in range(len(plt)):
            price = eval(plt[i].split(':')[1])
            #通过eval函数 ，去掉内容中的单引号和斜杠   通过split，以：为分割点（0，1），取1位置的信息，就是价格
            title = eval(tlt[i].split(':')[1])
            #因为len(plt)和len(tlt)的长度应该是相等的，所以这个也能写在一个循环里
            ilt.append([price,title])
    except:
        print("发生异常")
        
def printGoodsList(ilt)：			#输出页面到屏幕上
	#定义一个信息输出的模板,\t表示在字符中间有一段小小的间距" "，形成表格形态，{:4}表示字符长度4
    tplt = "{:4}\t{:8}\t{:16}"
    #format表格形式 ， 设置输出信息的表头，count计数
    print(tplt.format("序号","价格","商品名"))
    count = 0
    for g in ilt :
        count += 1
        print(tplt.format(count,g[0],g[1]))

def main() :
    goods = '书包'
    depth = 2 						#爬取的深度，比如爬取两个页面的信息
    start_url = 'https://s.taobao.com/search?q=goods'		#起始页面链接
    info_list = []					#商品列表
    for i in range(depth):
        try:
            url = start_url + "&s=" + str(44*i)				#第一页为0 第二页为44 
            html = getHTMLText(url)
            parsePage(info_list,html)
        except:
            continue										#当某页面出现问题，continue会跳过此页面，继续执行
	printGoodsList(info_list)
    
main()
```

==总结：==

1.Request库是获取信息的关键

2.正则表达式是分析信息、提取关键信息的最重要的手段

---

### 实例：股票信息定向爬虫

>功能目的：
>
>获取上交所、深交所所有的股票交易信息
>
>交易信息包括当前交易价格、上一日成交价等其他交易数据
>
>输出：
>
>将所有信息保存到文件中
>
>技术路线：
>
>requests+bs4+re

获取数据的候选网站：

新浪股票：[股票首页_新浪财经_新浪网 (sina.com.cn)](https://finance.sina.com.cn/stock/)

东方财富网：[国证煤炭 2871.45 41.60(1.47%) _ 股票行情 _ 东方财富网 (eastmoney.com)](http://quote.eastmoney.com/zs399436.html)

个股的编号在连接中体现出来

百度股票：暂时进不去

选取原则：

股票信息静态存在于HTML页面中，非js代码生成，无robots协议限制（通过源代码可查看）

```python
import requests 
from bs4 import BeautifulSoup
import traceback

def getHTMLText(url):
    try:
        r = requests.get(url,timeout=30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        print("Error!!!")
        
def getStockList(lst,stockURL):
    html = getHTMLText(stockURL)
    soup = BeautifulSoup(html,"html.parser")
    #找到soup里的所有a标签
    a = soup.find_all("a")
        #开始遍历
    for i in a :
        try:
            href = i.attrs['href']
                #通过.attrs得出每个a里的属性【“href=……”】 "………"的信息就是返回的内容
            lst.append(re.findall(r"[s][hz]\d{6}",href))
                #通过正则表达式取得对应内容
		except:
        		#如果a中没有href属性，也不要紧，继续执行
        	continue

def getStockInfo(lst,stockURL,fpath):
    count = 0 
    for i in lst:
        url = stockURl + i + ".html"
        html =getHTMLText(url)
        try:
            if html =="":
                continue
            infodict = {}
            soup = BeautifulSoup(html,"html.parser")
            stockinfo = soup.find("div",attrs={"class":"stock-bets"})
            name = stockinfo.find_all(attrs={"class":"bets-name"})[0]
            infodict.update({"股票名称":name.text.split()[0]})
            keylist = stockinfo.find_all("dt")
            vallist = stockinfo.find_all("dd")
            for m in range(len(keylist)):
                key = keylist[m].text
                val = vallist[m].text
                infodict[key] = val
                #或者是 infodict.update({key:val})
            with open(fpath,"a",encoding="utf-8") as f:
                f.write(str(infodict) + "\n")
                f.close()
                #增加进度条，可以确定当前进展状态
                count += 1
                print("\r当前进度为：{:.2f}%".format(count*100/len(lst)),end = "")
        except:
			count += 1
            print("\r当前进度为：{:.2f}%.format(count*100/len(lst))",end = "")
            continue
            
def main():
    stocklisturl = ""
    stockinfourl = ""
    fpath = "d://info.txt"
    slist = []
    getStockList(slist,stocklisturl)
    getStockInfo(slist,stockinfourl,fpath)
    
    
    
main()
```

----

### Scrapy框架（专业）

```shell
pip install scrapy
```

#### Scrapy爬虫框架结构

爬虫框架是一个半成品，能够根据需求快速实现专业爬虫。框架内包含各种功能和结构，共7部分（5+2）：

![image-20210522174119420](C:\Users\ZK\AppData\Roaming\Typora\typora-user-images\image-20210522174119420.png)

内容在结构间流动，形成数据流

----

数据路径1：

![image-20210522174307548](C:\Users\ZK\AppData\Roaming\Typora\typora-user-images\image-20210522174307548.png)

Request可以理解为一个URL，通过Spiders得到爬取请求，再透过Engine到Scheduler（调度）

数据路径2：

![image-20210522174707759](C:\Users\ZK\AppData\Roaming\Typora\typora-user-images\image-20210522174707759.png)

由Scheduler发出一个真实的请求至Engine，Engine将请求送至Downloader真实访问互联网，获得Response对象传回Engine，最终到达Spiders.

数据路径3：

![image-20210522175159916](C:\Users\ZK\AppData\Roaming\Typora\typora-user-images\image-20210522175159916.png)

Spiders将从Downloader处获取的Response进行处理，产生两种类型ITEM（爬取项）和Requests（新的爬取请求，对新的链接再次爬取），通过Engine分别将这两种数据送至ITEM PIPELINES和Scheduler.

![image-20210522175627706](C:\Users\ZK\AppData\Roaming\Typora\typora-user-images\image-20210522175627706.png)

![image-20210522175911895](C:\Users\ZK\AppData\Roaming\Typora\typora-user-images\image-20210522175911895.png)

> 1.Downloader Middleware：
>
> 实现Engine、Downloader、Scheduler可配置控制，通过编写，可以实现修改、丢弃、新增请求或响应
>
> 2.Spider Middleware：
>
> 对Spider产生的请求和爬取项再处理，修改丢弃新增请求或爬取项

==重点编写两个模块，辅以两个中间键控制，对Requests、Response、item进行配置调整==

#### Requests库与Scrapy库的比较

相同点：

1.都可以对页面进行爬取，是python爬虫的两个重要技术路径。

2.两者可用性很好，文档丰富，入门不难

3.两者单独都不能处理js、表单提交、验证码等情况（需要扩展用其他库）

区别：

![image-20210522193304747](C:\Users\ZK\AppData\Roaming\Typora\typora-user-images\image-20210522193304747.png)

> 总结：
>
> 小需求适用Request
>
> 但是较为麻烦的建议适用Scrapy（持续、不间断、积累、形成爬取库）
>
> 更高级的需求需要自行搭建框架，可能需要自行设计Request编写爬虫框架。

#### Scrapy爬虫常用命令

在cmd命令下输入以下命令可以查看相关信息：

```she
scrapy -h
```

大部分的scrapy爬虫的操作其实是通过命令行来实现的，scrapy命令行的大致结构：

> \>scrapy\<command\>\[options][args]

![image-20210524215945666](C:\Users\ZK\AppData\Roaming\Typora\typora-user-images\image-20210524215945666.png)

本质上scrapy库是给程序员使用的，没有图形界面，主要靠命令行。

##### Scrapy实例

```shell
#生成一个工程
scrapy startproject pythondemo123
```

![image-20210524223833070](C:\Users\ZK\AppData\Roaming\Typora\typora-user-images\image-20210524223833070.png)

```shell
#产生一个爬虫 名称为demo的爬虫 爬取的主域名是百度
cd pythondemo123
scrapy genspider demo baidu.com
```

此时，在Spiders目录下就多出了一个叫demo.py的文件，内容如下：

```python
import scrapy


class DemoSpider(scrapy.Spider):
    name = 'demo'
    allowed_domains = ['baidu.com']
    start_urls = ['http://baidu.com/']

    def parse(self, response):
        pass
```

其中，parse()用于处理响应，解析页面形成字典，发现新的URL请求。

经过修改后的文件内容:

```python
import scrapy


class DemoSpider(scrapy.Spider):
    name = 'demo'
    allowed_domains = ['baidu.com']
    start_urls = ['http://python123.io/ws/demo.html']

    def parse(self, response):
        fname = response.url.split("/")[-1]
        with open(fname,"wb") as f :
            f.write(response.body)
            f.close()
        self.log("Save files %s"%fname)
        pass

```

可以启动这个爬虫试一下：

```shell
cd pythondemo123
scrapy crawl demo
```

---

##### yield关键字的使用

生成器的概念：它是一个不断产生值的函数，包含yield语句的函数，就是一个生成器。生成器每次运行都产生一个值，之后函数被冻结，直到再次被唤醒后产生下一个值。局部变量在此过程中不变。

###### 生成器的写法

```python
def gen(n):
    for i in range(n):
        yield i**2
#调用定义的gen函数
for i in gen(5):
    print(i," ",end="")
0 1 4 9 16
```

生成器每次返回一个值，在for循环时，一个一个调用。

**对比普通写法**:

```python 
def square(n):
    ls = [i**2 for i in range(n)]
    return ls
for i  in square(5):
    print(i," ",end="")
```

先在square()函数里完全遍历完n，再通过for显示出来。

因此，生成器节省存储空间，更加快速


如果请求URL链接过多，可以将上面的代码完整化，提升运行速度：

```python
import scrapy


class DemoSpider(scrapy.Spider):
    name = 'demo'
    allowed_domains = ['baidu.com']
    start_urls = ['http://python123.io/ws/demo.html']
	for url in start_urls :
        yield scrapy.Request(url=url,callback=self.parser)
    def parse(self, response):
        fname = response.url.split("/")[-1]
        with open(fname,"wb") as f :
            f.write(response.body)
            f.close()
        self.log("Save files %s"%fname)
        pass
```

![image-20210524235017933](C:\Users\ZK\AppData\Roaming\Typora\typora-user-images\image-20210524235017933.png)

##### Request类

```python
class scrapy.http.Request()
```

> Request对象表示一个Http请求
>
> Spider生成 由Downloader调用处理

![image-20210524235211336](C:\Users\ZK\AppData\Roaming\Typora\typora-user-images\image-20210524235211336.png)

##### Response类

```python
class scrapy.http.Response()
```

> Response对象表示一个HTTP响应
>
> 由Downloader生成，由Spider处理

![image-20210524235409244](C:\Users\ZK\AppData\Roaming\Typora\typora-user-images\image-20210524235409244.png)

##### Item类

```python
class scrapy.item.Item()
```

> 表示从一个HTML页面提取的信息内容
>
> 由Spider生成，并且由item pipeline最终处理

Item类下的多种解析方法：

包括BeautifulSoup、lxml、re、Xpath Selector、CSS Selector

**CSS Selector的使用**

```python
<html>.css("a::attr(href)").extract()
#通过输入标签名称a、标签属性href获得对应的标签信息,由国际公认W3C维护
```

----

#### Scrapy爬出实例：股票信息爬虫

首先建立工程、生成模板，编写ITEM PIPELINE处理数据

```shell
scrapy startproject baidugupiao
cd baidugupiao
scrapy genspider stocks baidu.com
```

在spider目录下修改stocks.py文件

```python
import scrapy
import re

class DemoSpider(scrapy.Spider):
    name = 'demo'
    #allowed_domains = ['baidu.com']
    start_urls = ['需要定义的股票列表的url（如东方财富网）']
    def parse(self, response):
        for href in response.css("a::attr(href)").extract():
            try:
                stockindex = re.findall(r"[s][hz]\d{6}",href)[0]
        		url = "https://gupiao.baidu.com/stock/"+stockindex +".html"
        		yield scrapy.Request(url,callback=self.parser_stock)
            except:
                continue
	def parser_stock(self,response):
        indct = {}
        stockinfo = response.css(".stock-bets")
    	name = stockinfo.css(".bets-name").extract()[0]
        keylist = stockinfo.css("dt").extract()
        valuelist = stockinfo.css("dd").extract()
        for i in range(len(keylist)):
            key = re.findall(r">.*</dt>",keylist[i])[0][1:-5]
            try:
                val = re.findall(r">.*</dd>",valuelist[i])[0][1:-5]
            except:
                val = "--"
            indct[key] = val  
        indct.update({"股票名":re.findall("\s.*\(",name).split()[0]+re.findall("\>.*\<",name)[0][1:-1]}) 
		yield infoDict
```

修改ITEM PIPELINE.py文件，配置数据处理：

```python
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class Pythontest1Pipeline:
    def process_item(self, item, spider):
        return item
class baidustockpipline:
    def open_ietm(self,spider):
        self.f = open("baidustock.txt","w")
	def close_item(self,spider):
        self.f.close()
	def process_item(self,item,spider):
        try:
            line = str(dict(item)) + "\n"
            self.f.write(line)
		except:
            pass
        return item
```

在setting.py中找到对应的设置，使得爬虫可以找到对应的类：

```python
# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'pythontest1.pipelines.baidustockpipline': 300,
}
```

![image-20210525135814331](C:\Users\ZK\AppData\Roaming\Typora\typora-user-images\image-20210525135814331.png)

-----

# 网络爬虫进阶

## Ajax动态页面爬虫进阶

### requests库温习

#### 实例1 破解百度翻译

```python
import requests
import json

if __name__ == "__main__":
    kw = input("请输入要翻译的英语单词：")
    url = "https://fanyi.baidu.com/sug"
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.864.37'}
    data = {"kw":kw}
	response = requests.post(url=url,headers=header,data=data).json()
    fp = open("./%s.json"%kw,"w",encoding="utf-8")
    json.dump(response,fp=fp,ensure_ascii=False)

print("over!!!")
```

#### 实例2 豆瓣分类电影排名

```python
import requests
import json

if __name__ =="__main__":
    url = "https://movie.douban.com/j/chart/top_list"
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.864.37'}
    r = []
    for i in range(0,28):
        param = {
        'type': '24',
        'interval_id': '100:90',
        'action':"",
        'start': i*20,
        'limit': '20'
        }
        response = requests.get(url=url,headers=header,params=param).json()
        r.extend(response)
    fp = open("./movie.json","w",encoding="utf-8")
    json.dump(r,fp=fp,ensure_ascii=False)
    print("over!!!")
```

#### 实例3 肯德基餐厅位置信息

```python
import requests
import json
if __name__ == "__main__":
    url = 'http://www.kfc.com.cn/kfccda/ashx/GetStoreList.ashx?op=keyword'
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.864.37'}
    r = []
    for i in range(1,3):
        data = {
            'cname':'',
            'pid':'',
            'keyword': '重庆',
            'pageIndex': i,
            'pageSize': '10'
        }
        response = requests.post(url=url,headers=header,data=data).text
        response = json.loads(response)	#将字符串转化为Json，可以使用json.loads()，也可以使用eval()，但是后者需要内容中的键值对必须有双引号，且不支持null值。因此适用前者好点
        r.append(response)
    fp = open("./餐厅.json","w",encoding="utf-8")
    json.dump(r,fp=fp,ensure_ascii=False)
    print("over!!!")
```

#### 实例4 药监总局化妆品详情信息

```python
import requests
import json
if __name__ == "__main__":
    url = 'http://scxk.nmpa.gov.cn:81/xk/itownet/portalAction.do?method=getXkzsList'
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.864.37'}
    a = []
    for i in range(1,10):
        data = {
            'on': 'true',
            'page': i,
            'pageSize': '15',
            'productName':'',
            'conditionType': '1',
            'applyname':'',
            'applysn':''
        }
        response = requests.post(url=url,data=data,headers=header).json()
        for name in response['list']:
            url_post = 'http://scxk.nmpa.gov.cn:81/xk/itownet/portalAction.do?method=getXkzsById'
            id = str(name['ID'])
            iddata = {
                'id':id
            }
            r = requests.post(url=url_post,headers=header,data=iddata).json()
            a.append(r)
    fp = open("./药监局.json","w",encoding='utf-8')
    json.dump(a,fp=fp,ensure_ascii=False)
```

### 总结

requests库可以爬取静态的HTML，也可以Post爬取动态的页面（基于ajax），得到对应的json后，可以视为字典使用。但其中需要注意两个问题：

> 1.如果页面原始提供的只是text字符串，那么就涉及到字符串到字典的转换问题。response = json.loads(response)	#将字符串转化为Json，可以使用json.loads()，也可以使用eval()，但是后者需要内容中的键值对必须有双引号，且不支持null值。因此适用前者好点
>
> 2.对字典内容的增删改查，可能涉及到“套娃”，列表中的字典，字典中的字典，需要用对应的下角标查找数据，特别是要加强掌握字典的键值对的查询。

## 数据解析进阶

### 实例 re库实现图片爬取

```python
import re
import requests
import os

if __name__ == "__main__":
    for i in range(1,10):
        url = "https://www.qiushibaike.com/imgrank/page/%d/"%i
        header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.864.37'}
        response = requests.get(url=url,headers=header).text
        ex = '<div class="thumb">.*?<img src="(.*?)".*?height="auto">.*?</div>'
        try:
            img_links = re.findall(ex,response,re.S)
            if not os.path.exists('./pics'):
                os.mkdir('./pics')
            for link in img_links:
                pic_link ='https:' + link
                pic_data = requests.get(pic_link).content
                pic_name = pic_link.split('/')[-1]
                if not os.path.exists('./pics/%s'%pic_name):
                    path  = './pics/%s'%pic_name
                else:
                    path = './pics/%s%s'%('重复',pic_name)
                with open(path,'wb') as fp :
                    fp.write(pic_data)
                    fp.close()
                    print(pic_name,"爬取完成")
        except:
            print("出现异常！！！！")
```

### bs4库温习

#### 环境安装

```shell
pip install bs4
pip install lxml #一个数据解析器，不同于html.parser
```

通过入门部分的学习，我们知道：

```python
import bs4 
import lxml
fp = open('./demo.html','r',encoding="utf-8")
soup = BeautifulSoup(fp,'lxml')

soup.a
soup.find('a')
#二者都是只找到对应标签名的第一个标签内容，实质上的功能是一致的
soup.find('a',class_='song')
#二者区别在于，find方法可以增加具体的属性，找到对应属性的第一个标签内容
soup.find_all('a')
#返回一个列表，所有符合要求的标签，同理，里面可以加属性限制
```

这里再学习一下select方法使用：

```python
import bs4 
import lxml
fp = open('./demo.html','r',encoding="utf-8")
soup = BeautifulSoup(fp,'lxml')
#Select需要有对应的选择器，例如class选择器，返回一个列表,如下：
soup.select('.song')
#如果我想获得class属性标签下的子标签的内容，在这种层级选择的情况下如何操作：
soup.select('.song > ul > li > a') #最终返回所有a为列表，一个大于号代表一级
soup.select('.song > ul  a') #最终返回所有a，一个大于号代表一级，空格代表多个层级
```

定位到指定标签后，获取其包含的字符串，**返回的不是列表，是字符串**：

```python
soup.soup.select('.song > ul  a')[0].stringsoup.soup.select('.song > ul  a')[0].textsoup.soup.select('.song > ul  a')[0].get_text()#string只能获取自己的文本内容，但是后两个，可以获取直系、子标签、孙标签全部的文本内容
```

获取**定位标签的属性值**内容，用**中括号**就可以了：

```python
soup.a['href']
```

### 实例 三国演义全本获取

[《三国演义》全集在线阅读_史书典籍_诗词名句网 (shicimingju.com)](https://www.shicimingju.com/book/sanguoyanyi.html)

```python
import requestsfrom bs4 
import BeautifulSoupimport lxml
if __name__ == "__main__":    
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.864.37'}    
    home_url = 'https://www.shicimingju.com/book/sanguoyanyi.html'    
    home_text = requests.get(url=home_url,headers=header).content    
    hsoup = BeautifulSoup(home_text,'lxml')    
    book_mulu = hsoup.find('div',class_='book-mulu')    
    li_list = book_mulu.find_all('li')    
    fp = open("./sanguo.txt",'w',encoding='utf-8')    
    for li in li_list:        
        title =  li.a.string        
        href = "https://www.shicimingju.com/" + li.a['href']        
        contents = requests.get(href,headers=header).content        
        csoup = BeautifulSoup(contents,'lxml')        
        text = csoup.find('div',class_="chapter_content").text        
        content = title+":"+text+"\n"        
        fp.write(content)        
        print("获取完毕！！！",title)
```

### Xpath库学习

一般原理：

==Xpath匹配不到tbody,在表达式中如果涉及到tbody，直接换成//就好了==

1.将页面实例化为一个etree对象。

```python
from lxml import etree#如果HTML在本地：tree = etree.parse(filepath)#如果HTML在网络：tree = etree.HTML(page_text)
```

2.写好表达式，在etree中使用xpath解析。

```python
tree.xpath('表达式')
```

### xpath表达式

> '/html/body/div'    表示从根节点开始，遍历定位
>
> 'html//div' 表示从HTML节点开始，在指定下面多层级定位
>
> '//div' 表示任意位置开始定位，类似于findall
>
> '//div[@class="song"]' 属性定位
>
> '//div[@class="song"]/p[1]' 索引定位，这里注意是从1开始，而不是0 ，【1】

**通过xpath表达式获取标签的内容**

```shell
tree.xpath('//div[@class="song"]/p[1]/a/text()' )
#这样就可以获取包含的内容了，但是返回的是一个列表,可以通过[0]获取其中内容
tree.xpath('//div[@class="song"]/p[1]/a/text()' )[0]
#获取的只能是自己包含的，如果要获取子标签的，则需要//text()
tree.xpath('//div[@class="song"]/p[1]/a//text()' )[0]
```

**通过xpath表达式获取标签的属性**

```python 
tree.xpath('//div[@class="song"]/p[1]/a/@href' )[0]
```

### 实例 58同城二手房名称信息

```python
import requests
from lxml import etree
if __name__ == "__main__":
    url = "https://cn.58.com/ershoufang/"
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.864.37'}
    response = requests.get(url,headers=header)
    response.encoding = response.apparent_encoding
    tree = etree.HTML(response.text)
    titles = tree.xpath('//div[@class="property-content-title"]/h3/text()')
    for title in titles:
        print(title,end="\n")
```

### 实例  Xpath图片爬取

```python
import requests
from lxml import etree
import os
if __name__ == "__main__":
    url = 'https://pic.netbian.com/4kmeinv/'
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.864.37'}
    response = requests.get(url=url,headers=header)
    response.encoding = response.apparent_encoding
    response = response.text
    print(response)
    tree = etree.HTML(response)
    li_list = tree.xpath('//ul[@class="clearfix"]/li')
    print(li_list)
    if not os.path.exists("./4k"):
        os.mkdir('./4k')
    for li in li_list:
        link = "https://pic.netbian.com" + li.xpath('./a/img/@src')[0]
        pic_data = requests.get(url=link,headers=header).content
        pic_name = li.xpath('./a/img/@alt')[0] + '.jpg'
        with open('./4k/%s'%pic_name,"wb") as fp :
            fp.write(pic_data)
            print(pic_name,"保存完成！！！！")
```

这里要注意两个点：

> 第一、li.xpath('./a/img/@src')返回的是一个列表，想要合成对应的链接，需要先通过下角标[0]取得其中字符串。
>
> 第二、**层级化**利用xpath返回的内容。

### 实例 PM2.5历史数据全部城市名称信息

```python
import requests
from lxml import etree

if __name__ == "__main__":
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.864.37'}
    url = 'https://www.aqistudy.cn/historydata/'
    r = requests.get(url=url,headers=header)
    r.encoding = r.apparent_encoding
    tree = etree.HTML(r.text)
    li_list = tree.xpath('//div[@class="all"]/div[@class="bottom"]//li | //div[@class="hot"]/div[@class="bottom"]//li')
    all = []
    for li in li_list:
        city = []
        hname = li.xpath('./a/text()')[0]
        hlink = 'https://www.aqistudy.cn/historydata/' + li.xpath('./a/@href')[0]
        city.append(hname)
        city.append(hlink)
        all.append(city)
    print(all)
```

这里学习到一点：

> 一个xpath想要解析两个表达式 可以用 | 隔开；另外，**层级千万不要写乱**，凡是出现空列表的，先检查一下层级有没有错，特别是class内容的上下级是否正确。

## 模拟登陆的问题

### 验证码识别

两种路径：

1.自己肉眼识别

2.基于深度学习的脚本自动识别（使用第三方平台，或==自行写脚本==）----计划中…………

这里先以第三方平台为例（超级鹰）：

首先，注册超级鹰账号，点击该网站的开发文档，获取chaojiying.py文件，拷贝到我们的项目所在目录下，然后import引入。

其次，对超级鹰的信息进行部分修改，账号、密码、应用ID等（应用ID需要自己在超级鹰网站创建哦）

```python
import requests
from chaojiying import Chaojiying_Client
header = {
'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.864.37'
}
session = requests.Session()
def getimg(src_link):
    response = session.get(url=src_link, headers=header)
    response.raise_for_status()
    response.encoding = response.apparent_encoding
    src_data = response.content
    print(src_data)
    with open('./code.png', 'wb') as f:
        f.write(src_data)
def getcode(imgpath):
    chaojiying = Chaojiying_Client('zk442443131', 'me1a1qin9.', '917825')  # 用户中心>>软件ID 生成一个替换 96001
    im = open('code.png', 'rb').read()  # 本地图片文件路径 来替换 a.jpg 有时WIN系统须要//
    return chaojiying.PostPic(im, 1902)['pic_str']
def getlogin(login_link,code):
    data = {
        '__VIEWSTATE': 'f0iYv6taDwgQbywFU7jDWc7B253AJQ40Zd1DkEw8teMd/K9y70//NoU76EQywEVMKda8lHvktza/RWcq0IWeSPhHD41IIpHy3xbZdVcXJU+2uZPuyfrBulQI62M=',
        '__VIEWSTATEGENERATOR': 'C93BE1AE',
        'from':'http://so.gushiwen.cn/user/collect.aspx',
        'email': '442443131@qq.com',
        'pwd': '12345678',
        'code': code,
        'denglu': '登录'
    }
    response = session.post(url=login_link,headers=header,data=data)
    response.encoding=response.apparent_encoding
    return response.text


if __name__ == "__main__":
    src_link = 'https://so.gushiwen.cn/RandCode.ashx'
    login_link = 'https://so.gushiwen.cn/user/login.aspx'
    getimg(src_link)
    code = getcode(r'.//code.png')
    html = getlogin(login_link,code)
    print(html)
    with open('./test.html','w',encoding='utf-8') as f:
        f.write(html)
```

识别后将验证码与用户信息一起封装进Post请求中即可。

### Cookie的问题

cookie可保证多次访问的登录状态不失效，对于模拟登陆后的一系列操作至关重要。

可以通过查看Response Header自行封装进后续的Post请求中，但是更高效的方法是自动获取cookie。具体如下：

> 引入一个对象session，其作用：
>
> 1.可以进行请求发送
>
> 2.可以自动存储、携带产生的cookie

因此，用session对象模拟登陆，发送Post请求后，自动存储携带cookie，后续再通过session向服务器发送get请求时，就不需要考虑登陆状态的问题了。

```python
session = requests.Session()
response = session.post(url=url,headers=header)
response = session.get(url=url,headers=header)
```

### 代理

存在反扒机制，限制IP访问次数的情况下，需要使用IP代理。

```python
session.post(url=url,header=header,data=data,proxies={'https':'你的代理Ip地址'})
#这里的协议不能写错，支持的协议与Ip地址对应。
```

# 异步爬取实现

**一般的同步爬取**

```python
import requests
import lxml
import xlwt
urls = ['https://www.baidu.com','https://www.zkwd888.ltd','https://www.qq.com']
path = './test.xls'
def get_content(url):    
    session = requests.Session()  
    response = session.get(url=url)    
    response.encoding = response.apparent_encoding  
    return response.text
def parse_content(text):   
    data = []   
    soup = BeautifulSoup(text,'lxml') 
    al = soup.find_all('a')   
    for a in al:     
        a_data = []    
        link = a['href']      
        title = a.string      
        a_data.append[link]      
        a_data.append[title]     
        data.append[a_data]	
    return data
def save_content(data,savepath):	
    book = xlwt.Workbook(encoding = "utf-8")    
    sheet = book.add_sheet('sheet1')    
    for i in range(len(data)) :     
        content = data[i]       
        for j in len(content) :    
            sheet.write(i,j,content[j])  
    book.save(savepath)   
if __name__ == "__main__":  
    for url in urls :      
        text = get_content(url)	
        data = parse_content(text)   
        save_content(data,path)
```

单线程模式下，只能一个一个执行，已经在解析第一个URL了，那么第二个URL就必须等着，因为线程被第一个占用了，产生阻塞。综合下来的运行时间就会变长。

## 线程池、进程池模式

**线程池、进程池爬虫实例**

#### 爬取梨视频

```python
import requests
from lxml import etree
import re
from multiprocessing.dummy import Pool
header = {
'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.864.37'
}
def get_vlink(url):
    try:
        all_links = []
        response = requests.get(url=url,headers=header)
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        response = response.text
        tree = etree.HTML(response)
        li_list = tree.xpath('//li[@class="categoryem"]')
        for li in li_list:
            # print(li)
            ex = 'video_(\d+)'
            # print(li.xpath('.//div[@class="vervideo-bd"]/a/@href')[0])
            code = re.findall(ex,li.xpath('.//div[@class="vervideo-bd"]/a/@href')[0])[0]
            # print(code)
            link = 'https://www.pearvideo.com/'+ li.xpath('.//div[@class="vervideo-bd"]/a/@href')[0]
            id = link.split('_')[1]
            title = li.xpath('.//div[@class="vervideo-title"]/text()')[0]
            data = {
                'contId': code,
                'mrd': '0.3765420530133352'
            }

            vheader = {
                'Referer': link,
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.864.37'
            }
            r_details = requests.get(url='https://www.pearvideo.com/videoStatus.jsp',headers=vheader,params=data)
            r_details.raise_for_status()
            r_details.encoding = r_details.apparent_encoding
            srcUrl = r_details.json()['videoInfo']['videos']['srcUrl']
            systemtime = r_details.json()['systemTime']
            project ={
                'id': id,
                'title' : title,
                'link' : srcUrl,
                'systemTime': systemtime
            }
            all_links.append(project)

        return all_links
    except:
        pass
def getvideo(link):
    code = link['id']
    systemtime = link['systemTime']
    srclink = link['link']
    srclink = srclink.replace(systemtime,'cont-%s'%code)
    print(srclink)
    title = link['title'] + '.mp4'
    response = requests.get(url=srclink,headers=header)
    response.encoding = response.apparent_encoding
    vdata = response.content
    with open('./%s'%title,'wb') as f :
        f.write(vdata)
alllink = get_vlink('https://www.pearvideo.com/category_9')
# print(alllink)
pool = Pool(9)
pool.map(getvideo,alllink)
pool.close()
pool.join()
```

具体而言：

线程池、进程池要先导入一个库：**from multiprocessing.dummy import Pool**

创建一个对象pool = Pool(9)，括号中代表线程进程数量。

通过map方法处理（函数，可迭代的内容），其中函数必须有一个参数，这个参数就要调用后面迭代出来的每一个内容，参数有且只能有一个，若考虑到多个参数，可以变成字典形式，让可迭代的内容迭代出来的是一个个字典。

运行完毕后要close线程进程池，使其不再接受新任务，另外，join可以让主进程阻塞后，让子进程继续运行完成，子进程运行完后，再把主进程全部关掉。

> 这里有两个需要注意的：
>
> 爬取梨视频时，某些Header需要附带请求基于的网站 'Referer' ，否则得不到对应json**（感叹于防盗链技术）**
>
> Post链接和真实链接对比：
>
> https://video.pearvideo.com/mp4/adshort/20210604/cont-1731295-15688496_adpkg-ad_hd.mp4
>
> https://video.pearvideo.com/mp4/adshort/20210604/1622804934795-15688496_adpkg-ad_hd.mp4

## 多任务异步协程

需要导入一个模块：pip install asyncio

> 特殊函数：特殊函数调用后，不会立即执行其内的代码。调用后，就产生一个协程对象（很像生成器啊！！！）**获取其内返回值的话，需要任务对象，然后绑定回调，通过回调函数的参数+.result()获取其返回值。**
>
> 协程对象：通过调用特殊函数返回的对象。**协程对象=特殊函数调用=一组特定的操作（尚未执行）**
>
> 任务对象：是对协程对象的进一步封装，可以绑定回调。**任务对象=协程对象=一组特定操作**
>
> 事件循环对象：其实就是任务循环，可将多个任务对象注册装载到循环对象中。如果开启事件循环，那么其内装载的任务操作就会被异步执行。

### 多任务操作准备

多任务的封装：将列表封装为asyncio.wait(任务列表)，注册到时间循环中执行。

wait的作用是将阻塞操作挂起，避免CPU占用导致其他的操作无法执行。

【关键】await修饰：特殊函数中凡是有阻塞的情况，就必须用这个关键字修饰，否则异步操作中会跳过阻塞操作。

例如：

open、write都可能不支持异步模块，发请求和获取相应操作都是阻塞，都需要加await。

==requests模块不支持异步，所以异步就不能继续使用Requests库作为爬虫库了。==

注：绑定回调的含义，指在任务对象执行完毕后，再调用某一函数。参数只能有一个，其表示的就是调用者——任务对象。

```python
import asyncio
import aiohttp

async def geturl(url):
    print("正在请求",url)
    await asyncio.sleep(2)
    print("请求完毕",url)
    return 'testOK'

def task_callback(t):
    print('im callback,the arg is :',t)     #这个t其实就是调用者————任务对象
    print('this is 协程对象的特殊函数返回值：',t.result())
if __name__ == "__main__":
    urls = ['www.1.com',
           'www.2.com',
           'www.3.com',
           'www.4.com']
    tasks = []
    for url in urls:

        c = geturl(url)
    # print(c) 发现报错await，就是说函数尚未执行，但已经变成了一个协程对象

    #创建一个任务对象，并且把c这个协程对象封装进去
        task = asyncio.ensure_future(c)

    #给这个任务绑定一个回调函数,这个函数可以给多个任务绑定进去
        task.add_done_callback(task_callback)
        tasks.append(task)
    #创建一个循环对象
    loop = asyncio.get_event_loop()

    #将任务注册进循环对象中，并且启动run，多任务必须要用asyncio.wait()封装
    loop.run_until_complete(asyncio.wait(tasks))

    #这次运行后发现，可以执行了，没有await报错
```

### aiohttp模块

由于Request库不支持异步，所以需要用aiohttp模块。

```shell
pip install aiohttp
```

使用方式：

```python
from lxml import etree
import asyncio
import aiohttp
header = {
'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.864.37'
}
async def getpage(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url,headers=header) as page:
            #text获取文字数据
            #read获取二进制图片、视频
            page_text = await page.text()
            return page_text

def parse_text(page):
    tree = etree.HTML(page.result())
    a = tree.xpath('//a')
    print(a)

if __name__ == "__main__":
    urls = [
        'https://www.baidu.com',
        'https://www.qq.com',
        'https://www.sina.com'
    ]
    tasks = []
    loop = asyncio.get_event_loop()
    for url in urls:
        content = getpage(url)
        task = asyncio.ensure_future(content)
        task.add_done_callback(parse_text)
        tasks.append(task)
    loop.run_until_complete(asyncio.wait(tasks))
```

由上可见，多用with as的语句！

**另外，在所有with前必须加async关键词，在请求和相应前必须加await。**

# selenium模块应用

**实质上是模拟浏览器的实际操作**————**所见即所得**，可以用来获取动态数据（用requests爬取有困难的动态数据）

## 介绍

环境安装

```shell
pip install selenium
```

浏览器驱动下载（浏览器驱动一定要与自己的浏览器安装版本匹配）

[Selenium 与 浏览器驱动 - Chrome 驱动下载 (liushilive.github.io)](https://liushilive.github.io/github_selenium_drivers/md/Chrome.html)

将驱动拷贝至项目目录下

代码编写

```python
from selenium import webdriver
from lxml import etree
url = 'https://www.baidu.com'
bro = webdriver.Edge(executable_path='msedgedriver.exe')
bro.get(url)
search = bro.find_element_by_xpath('//*[@id="kw"]')
search.send_keys('美女')
bro.find_element_by_xpath('//*[@id="su"]').click()
```

以上代码可以实现简单的selenium操作，更多操作如下代码所示：

```python
from selenium import webdriver
from time import sleep
bro = webdriver.Edge(executable_path='msedgedriver.exe')
bro.get('https://www.taobao.com/')

#找到搜索框输入内容、点击搜索
search = bro.find_element_by_id('q')
search.send_keys('天龙单机')
bn = bro.find_element_by_css_selector('.btn-search')

bro.execute_script('window.scrollTo(0,document.body.scrollHeight)')  #滚轮向下滚动——借助JS代码执行实现
sleep(5)
bn.click()

#再次请求一个页面，并前进、回退操作。

bro.get("https://www.baidu.com")
sleep(3)
bro.back()
sleep(3)
bro.forward()

bro.quit()
```

### 无头浏览器代码

```python
'''谷歌无头浏览器代码：
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
driver = webdriver.Chrome(    executable_path='E:\chromedriver.exe', chrome_options=chrome_options)    '''
#Edge 无头浏览器
# EDGE = {
#     "browserName": "MicrosoftEdge",
#     "version": "",
#     "platform": "WINDOWS",
#
#     # 关键是下面这个
#     "ms:edgeOptions": {
#         'extensions': [],
#         'args': [
#             '--headless',
#             '--disable-gpu',
#             '--remote-debugging-port=9222',
#         ]}
# }
```

### 隐藏navigator代码

```python
from selenium.webdriver 
import Chromedriver = Chrome('./chromedriver')
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", { 
    "source": """    
    Object.defineProperty(navigator, 'webdriver', 
    { 
    get: () => undefined
    })  """})
driver.get('http://exercise.kingname.info')
```

## 实例 药监局网站selenium新路径

```python
from selenium import webdriver
from lxml import etree
bro = webdriver.Edge(executable_path='msedgedriver.exe')
bro.get('http://scxk.nmpa.gov.cn:81/xk/')
page_text = bro.page_source
tree = etree.HTML(page_text)
li_list =tree.xpath('//*[@id="gzlist"]/li')
for  li in li_list:
    name = li.xpath('./dl/@title')[0]
    print(name)

bro.quit()
```

## 实例 鼠标点击、拖动的实现(iframe标签)

当标签被包含在《iframe》内部时，其实是在一个子页面内部，需要切换到对应的子页面ID里，才能进行定位。

```python
from selenium import webdriver
from selenium.webdriver import ActionChains
from time import sleep
bro = webdriver.Edge(executable_path='msedgedriver.exe')
bro.get('https://www.runoob.com/try/try.php?filename=jqueryui-api-draggable')
bro.switch_to.frame('iframeResult')
pic = bro.find_element_by_xpath('//*[@id="draggable"]')

act = ActionChains(bro)  #这个动作链里面的传参一定不要忘记填写
act.click_and_hold(pic)
for i  in range(5):
    act.move_by_offset(17,0).perform()  #这里是move
    sleep(3)

act.release()

sleep(6)
bro.quit()
```

## 实例 12306模拟登录

```python
from selenium import webdriver
from selenium.webdriver import ActionChains

from time import sleep
from chaojiying import Chaojiying_Client


chaojiying = Chaojiying_Client('zk442443131', 'me1a1qin9.', '917825')  # 用户中心>>软件ID 生成一个替换 96001
bro = webdriver.Edge(executable_path='msedgedriver.exe')
bro.command_executor
bro.get('https://kyfw.12306.cn/otn/resources/login.html')
sleep(2)
bro.find_element_by_xpath('/html/body/div[2]/div[2]/ul/li[2]/a').click()
sleep(3)
im = bro.find_element_by_xpath('//*[@id="J-loginImg"]')
locations = chaojiying.PostPic(im.screenshot_as_png, 9004)['pic_str'].split('|')
bro.find_element_by_xpath('//*[@id="J-userName"]').send_keys('442443131@qq.com')
sleep(0.5)
bro.find_element_by_xpath('//*[@id="J-password"]').send_keys('me1a1qin9.')
sleep(0.5)

for location in locations:
    x = int(location.split(',')[0])
    y = int(location.split(',')[1])
    act = ActionChains(bro)
    act.move_to_element_with_offset(im,x,y).click().perform()
    sleep(1)
bro.find_element_by_xpath('//*[@id="J-login"]').click()
sleep(5)
btn = bro.find_element_by_xpath('//*[@id="nc_1_n1z"]')
ActionChains(bro).drag_and_drop_by_offset(btn,300,0).perform()
```

# scrapy重温

环境安装

```python 
pip install scrapy #win还需要安装以下内容pip install twistedpip install wheelpip install pywin32
```

创建工程--创建爬虫--编辑配置文件--修改Spider--修改item--修改Pipeline：

```shell
scrapy startproject Learning
cd Learningscrapy 
genspider learning www.baidu.com
```

```python
#spider下新建的learning的爬虫文件内容：
import scrapy
class LearningSpider(scrapy.Spider):   
    name = 'learning'   
    # allowed_domains = ['www.baodu.com']    
    start_urls = ['http://www.baodu.com/']   
def parse(self, response):   
    pass
```

```python
#setting.py文件的内容，修改robots协议：
# Obey robots.txt rules
ROBOTSTXT_OBEY = False
#增加日志信息配置为“只打印
Error”LOG_LEVEL = 'ERROR'
#UA伪装
```

测试：scrapy crawl (spidername) --nolog 不显示日志

## Scrapy爬取糗事百科内容

### Scrapy.Xpath的特殊之处

> 1.返回的同样是列表，使用方法基本类似于一般方法。
>
> 2.返回列表的内容变成了一个个Selector对象，想要通过print获取内容，就要extract（）
>
> ```python
> name = div.xpath('./div[1]/a[2]/h2')[0].extract() 
> #对单个可用，取出内部字符串，同extract_first()
> content = div.xpath('.//div[@class="content"]/span').extract() 
> #直接提取全部，但是返回的还是列表
> content = "".join(content) 
> #将列表转换为一个整体的字符串
> ```

基于命令的持久化存储和过滤

```shell
scrapy crawl (spidername) -o *.csv
```

基于Item和Pipeline的存储和过滤

item文件里面定义属性：

```python
class LearningItem(scrapy.Item):   
    # define the fields for your item here like:   
    name = scrapy.Field()  
    content = scrapy.Field()   
    pass
```

爬虫的py文件里面增加：

```python
from Learning.items import LearningItem
# from    项目名      import    （Items.py文件中的类）
#在Spider的py中，解析数据的函数那里增加：            
item = LearningItem()    
#实例化一个对象           
item['name'] = name   
#将内容封装进对象里，前面是之前item定义的属性，后面就是我们的内容       
item['content'] = content      
yield item        
#将Item提交给Pipeline
```

Spider里面的代码内容：

```python
import scrapyfrom Learning.items 
import LearningItem
class LearningSpider(scrapy.Spider):   
    name = 'learning'  
    # allowed_domains = ['www.baodu.com']   
    start_urls = ['https://www.qiushibaike.com/text/'] 
    def parse(self, response):       
        div_list = response.xpath('//div[@class="col1 old-style-col1"]/div')   
        # print(div_list)     
        # all_content = []   
        for  div in div_list:    
            name = div.xpath('./div[1]/a[2]/h2/text()')[0].extract()      
            content = div.xpath('.//div[@class="content"]/span//text()').extract()    
            content = "".join(content)          
            print(content)       
            print(name)     
            item = LearningItem()      
            item['name'] = name           
            item['content'] = content      
         yield item
```

## 全站爬取：校花网图片名称

```python
import scrapy

# from Learning.items import LearningItem

class LearningSpider(scrapy.Spider):
    name = 'learning'
    # allowed_domains = ['www.baodu.com']
    start_urls = ['http://www.521609.com/daxuexiaohua/']
    url_num = 2
    new_url = "http://www.521609.com/daxuexiaohua/list3%d.html"
    def parse(self, response):
        li_list = response.xpath('//*[@id="content"]/div[2]/div[2]/ul/li')
        for li in li_list :
            title = li.xpath('./a[2]/b/text() | ./a[2]/text()').extract_first()
            print(title)
        if self.url_num <= 11  :
            url = format(self.new_url%self.url_num)
            self.url_num += 1
            yield scrapy.Request(url=url,callback=self.parse)
```

## 涉及请求传参的全站爬取（首页、分页内容的爬取）

```python
import scrapy
from bossPro.items import BossproItem

class BossSpider(scrapy.Spider):
    name = 'boss'
    # allowed_domains = ['www.boss.com']
    start_urls = ['https://www.sdfdsfdsasd.xyz/forum-103-1.html']
    url = 'https://www.sdfdsfdsasd.xyz/forum-103-%d.html'
    num = 2
    def parse_detail(self,response):
        item = response.meta['item']
        td = response.xpath('//body/div[6]/div[6]/div[2]/div[1]//table[1]//div[@class="t_fsz"]//table/tr/td')
        # print(td)
        fm_img_link = td.xpath('./img/@file').extract_first()
        ny_name = td.xpath('.//text()[2]').extract_first().replace("\n", "").replace("\r", "").replace(' ', '')
        img_link = td.xpath('.//ignore_js_op/img/@file').extract_first()
        magenet = td.xpath('./div/div/ol/li/text()').extract_first()
        # print(ny_name,img_link,magenet)
        item['fm_img_link'] = fm_img_link
        item['ny_name'] = ny_name
        item['img_link'] = img_link
        item['magenet'] = magenet
        yield item
        pass
    def parse(self, response):
        tbs = response.xpath('//*[@id="threadlisttableid"]/tbody')
        for tb in tbs:
            item = BossproItem()
            title = tb.xpath('.//tr/th/a[2]/text()').extract()
            if len(title) == 0 or title[0] == '隐藏置顶帖':
                continue
            href = 'https://www.sdfdsfdsasd.xyz/' + tb.xpath('.//tr/th/a[2]/@href').extract()[0]
            type = tb.xpath('.//tr/th/em/a/text()').extract()
            hot = tb.xpath('.//tr/td[@class="num"]/em/text()').extract()
            item['title'] = title[0]
            if len(type) == 0 :
                type = ['有码高清']
                item['type'] = type[0]
            else:
                item['type'] = type[0]
            item['href'] = href
            item['hot'] = hot[0]
            yield scrapy.Request(url=href,callback=self.parse_detail,meta={'item':item})
        if self.num <= 452:
            n_url = format(self.url%self.num)
            self.num += 1
            yield scrapy.Request(url=n_url,callback=self.parse)

```

```python
#pipline数据存储，特别是写入表格的代码 需要处理（添加一个计数器）
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import xlwt
import re
# import pymysql
ex = re.compile('【出演女优】：(.+)')
class BossproPipeline:
    workbook = None
    wuma_times = 1
    youma_times = 1
    def open_spider(self,spider):
        print("开始…………")
        self.workbook = xlwt.Workbook(encoding='utf-8')
        self.sheet1 = self.workbook.add_sheet('sheet1')
        self.sheet2 = self.workbook.add_sheet('sheet2')
        col = ['编号','类型','女优','片名','热度','种子链接','封面链接','预览链接','原帖链接']
        for i in range(0,9):
            self.sheet1.write(0,i,col[i])
            self.sheet2.write(0,i,col[i])
        # self.conn = pymysql.connect(user='root',password='me1a1qin9.',host='159.75.49.102',database='spider',port=3306)
        # self.curser = self.conn.cursor()
        # print("数据库链接成功，开始写入信息！！！！")
    def process_item(self, item, spider):
        if item['type'] == '无码高清':
            content = []
            count = self.wuma_times
            content.append(count)
            type = item['type']
            content.append(type)
            if len(re.findall(ex,item['ny_name'])) != 0:
                ny_name = re.findall(ex,item['ny_name'])[0]
            content.append(ny_name)
            title = item['title']
            content.append(title)
            hot = int(item['hot'])
            content.append(hot)
            magenet = item['magenet']
            content.append(magenet)
            fm_img_link = item['fm_img_link']
            content.append(fm_img_link)
            img_link = item['img_link']
            content.append(img_link)
            href = item['href']
            content.append(href)
            for i in range(0,9):
                self.sheet2.write(count,i,content[i])
            self.wuma_times += 1
            return item
            # content = []
            # # count = self.wuma_times
            # # content.append(count)
            # # type = item['type']
            # # content.append(type)
            # if len(re.findall(ex, item['ny_name'])) != 0:
            #     ny_name = "'" + re.findall(ex, item['ny_name'])[0] + "'"
            # else:
            #     ny_name = "' '"
            # content.append(ny_name)
            # title = "'"+ item['title'] +"'"
            # content.append(title)
            # hot = "'"+ str(item['hot'])+ "'"
            # content.append(hot)
            # magenet = "'"+str(item['magenet'])+"'"
            # content.append(magenet)
            # if type(item['fm_img_link']) != 'NoneType':
            #     fm_img_link = "'"+str(item['fm_img_link'])+"'"
            # else:
            #     fm_img_link = "' '"
            # content.append(fm_img_link)
            # if type (item['img_link']) != 'NoneType':
            #     img_link = "'"+str(item['img_link'])+"'"
            # else:
            #     img_link = "' '"
            # content.append(img_link)
            # href = "'"+str(item['href'])+"'"
            # content.append(href)
            # sql = '''
            #     INSERT INTO wuma (actress,title,hot,magnet,fmlink,link,href)
            #     VALUE (%s)
            #     '''%",".join(content)
            # self.curser.execute(sql)
            # # self.wuma_times += 1
            # self.conn.commit()
            # return item
        else:
            content = []
            count = self.youma_times
            content.append(count)
            type = item['type']
            content.append(type)
            if len(re.findall(ex,item['ny_name'])) != 0:
                ny_name = re.findall(ex,item['ny_name'])[0]
            content.append(ny_name)
            title = item['title']
            content.append(title)
            hot = int(item['hot'])
            content.append(hot)
            magenet = item['magenet']
            content.append(magenet)
            fm_img_link = item['fm_img_link']
            content.append(fm_img_link)
            img_link = item['img_link']
            content.append(img_link)
            href = item['href']
            content.append(href)
            for i in range(0, 9):
                self.sheet1.write(count, i, content[i])
            self.youma_times += 1
            return item
            # content = []
            # count = self.youma_times
            # content.append(count)
            # type = item['type']
            # content.append(type)
            # if len(re.findall(ex, item['ny_name'])) != 0:
            #     ny_name = "'" + re.findall(ex, item['ny_name'])[0] + "'"
            # else:
            #     ny_name = "' '"
            # content.append(ny_name)
            # title = "'" + item['title'] + "'"
            # content.append(title)
            # hot = "'" + str(item['hot']) + "'"
            # content.append(hot)
            # magenet = "'" + str(item['magenet']) + "'"
            # content.append(magenet)
            # if type(item['fm_img_link']) != 'NoneType':
            #     fm_img_link = "'" + str(item['fm_img_link']) + "'"
            # else:
            #     fm_img_link = "' '"
            # content.append(fm_img_link)
            # if type(item['img_link']) != 'NoneType':
            #     img_link = "'" + str(item['img_link']) + "'"
            # else:
            #     img_link = "' '"
            # content.append(img_link)
            # href = "'" + str(item['href']) + "'"
            # content.append(href)
            # sql = '''
            #     INSERT INTO youma (actress,title,hot,magnet,fmlink,link,href)
            #     VALUE (%s)
            #     '''%",".join(content)
            # self.curser.execute(sql)
            # # self.youma_times += 1
            # self.conn.commit()
            # return item
    def close_spider(self,spider):
        # self.curser.close()
        # self.conn.close()
        self.workbook.save('./高清中文字幕.xls')
        print("结束…………")
```

## ImagesPipline(图片全站爬取)

- 在scrapy中我们之前爬取的都是基于字符串类型的数据，那么要是基于图片数据的爬取，那又该如何呢？
  - 其实在scrapy中已经为我们封装好了一个专门基于图片请求和持久化存储的管道类ImagesPipeline，那也就是说如果想要基于scrapy实现图片数据的爬取，则可以直接使用该管道类即可。
  
    ```python
    import scrapy
    from imgSpider.items import ImgspiderItem
    
    class ImgSpider(scrapy.Spider):
        name = 'img'
        # allowed_domains = ['www.xxx.com']
        start_urls = ['https://sc.chinaz.com/tupian/']
    
        def parse(self, response):
            div_list = response.xpath('//*[@id="container"]/div')
            for div in div_list:
                src = 'https:'+div.xpath('./div/a/img/@src2').extract_first()
                item = ImgspiderItem()
                item['src'] = src
                yield item
            pass
    ```
  
    
- ImagesPipeline使用流程
  - 在配置文件中进行如下配置：
    IMAGES_STORE = ‘./imgs’：表示最终图片存储的目录
  - 管道类的编写：

```python
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


# class ImgspiderPipeline:
#     def process_item(self, item, spider):
#         return item
from scrapy.pipelines.images import ImagesPipeline
import scrapy

# ImagesPipeline专门用于文件下载的管道类，下载过程支持异步和多线程
class ImgPipeLine(ImagesPipeline):
    # 对item中的图片进行请求操作
    def get_media_requests(self, item, info):
        yield scrapy.Request(item['src'])

    # 定制图片的名称
    def file_path(self, request, response=None, info=None):
        url = request.url
        file_name = url.split('/')[-1]
        return file_name

    def item_completed(self, results, item, info):
        return item
        # 该返回值会传递给下一个即将被执行的管道类
```

-----

# 爬虫进阶

## CrawlSpider类的全站数据爬取

创建

```python
scrapy genspider -t crawl XXX www.XXX.com
```

链接提取器的概念和规则

```python
import scrapy
from scrapy.linkextractors 
import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from XXX.items import Itemclass1
from XXX.items import Itemclass2
class XxxSpider(CrawlSpider):    
    name = 'XXX'  
    allowed_domains = ['www.XXX.com']   
    start_urls = ['http://www.XXX.com/']   
    rules = (       
        Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
        #可以用来获取页码链接        
        #Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),此处可以放多个rule,用于获取页面里面其他的链接)    
    )
def parse_item(self, response):        
    item = Itemclass1()       
    #item = {}      
    #item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()     
    #item['name'] = response.xpath('//div[@id="name"]').get()   
    #item['description'] = response.xpath('//div[@id="description"]').get()   
    return item    
def parse_detail(self, response):     
    item = Itemclass2()    
    #item = {}  
    #item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()    
    #item['name'] = response.xpath('//div[@id="name"]').get()   
    #item['description'] = response.xpath('//div[@id="description"]').get()    
    return item
```

在CrawlSpider类无法实现请求传参。因此，只能给两个Item的Class，在管道中，通过class名区分item来源，从而进行处理。

```python
#item里的代码：
class Itemcalss1(scrapy.Item):   
    # define the fields for your item here like:    
    src = scrapy.Field()   
    pass
class Itemcalss2(scrapy.Item):   
    # define the fields for your item here like:   
    src = scrapy.Field()   
    pass
#Pipline里的代码
class XXXspiderPipeline:  
    def process_item(self, item, spider):   
        if item.__class__.__name__ == 'Itemclass1':     
            # ………………这里是解析的方法     
            return item
```

