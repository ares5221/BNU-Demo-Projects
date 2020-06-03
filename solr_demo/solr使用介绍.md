## 1.Solr基本使用

**1.下载与安装**

​    官网地址：http://lucene.apache.org/solr/

![image-20200603154713039](C:\Users\12261\AppData\Roaming\Typora\typora-user-images\image-20200603154713039.png)

点击下载页面，

![image-20200603154806516](C:\Users\12261\AppData\Roaming\Typora\typora-user-images\image-20200603154806516.png)

将下载的压缩包直接解压即可

**2.服务启动**

​    **2.1进入****bin****目录，执行命令，启动solr服务**

```
solr start
```

​    其它常用命令：

```
solr start –p 端口号    #启动
solr restart –p 端口号  #重启
solr stop –p 端口号     #关闭
solr create –c 名称     #创建一个核心
```