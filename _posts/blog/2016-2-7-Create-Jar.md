---
layout: post
title: java打包为可执行jar文件
description: java好像不能做成exe文件么？
category: blog
---

看到网上不少教程，而且如果安装了java的话自带的jar也有帮助文档，但是不知道为什么都讲不清楚的感觉。

## 说明文档

```bash
windard@windard:~$ jar
用法: jar {ctxui}[vfmn0PMe] [jar-file] [manifest-file] [entry-point] [-C dir] files ...
选项:
    -c  创建新档案
    -t  列出档案目录
    -x  从档案中提取指定的 (或所有) 文件
    -u  更新现有档案
    -v  在标准输出中生成详细输出
    -f  指定档案文件名
    -m  包含指定清单文件中的清单信息
    -n  创建新档案后执行 Pack200 规范化
    -e  为捆绑到可执行 jar 文件的独立应用程序
        指定应用程序入口点
    -0  仅存储; 不使用任何 ZIP 压缩
    -P  保留文件名中的前导 '/' (绝对路径) 和 ".." (父目录) 组件
    -M  不创建条目的清单文件
    -i  为指定的 jar 文件生成索引信息
    -C  更改为指定的目录并包含以下文件
如果任何文件为目录, 则对其进行递归处理。
清单文件名, 档案文件名和入口点名称的指定顺序
与 'm', 'f' 和 'e' 标记的指定顺序相同。

示例 1: 将两个类文件归档到一个名为 classes.jar 的档案中: 
       jar cvf classes.jar Foo.class Bar.class 
示例 2: 使用现有的清单文件 'mymanifest' 并
           将 foo/ 目录中的所有文件归档到 'classes.jar' 中: 
       jar cvfm classes.jar mymanifest -C foo/ .
```

这是自带的jar帮助文档，但是这个只能打包为jar文件，也就是像zip或者是rar一样的打包压缩，并不能执行。

## 打包为可执行文件

那么如何打包为可执行jar文件呢？

### 创建java文件

假设我们在根目录下创建helloWorld.java,内容如下

```java
public class helloWorld{
	public static void main(String[] args) {
		System.out.println("Hello World");
	}	
}

```

### 编译class文件

```bash
windard@windard:~$ javac helloWorld.java 
windard@windard:~$ java helloWorld 
Hello World
```

### 创建配置文件

在根目录下创建MANIFEST.MF，内容如下

```bash
Manifest-Version: 1.0
Created-By: Windard Yang
Class-Path: .
Main-Class: helloWorld

```

#### 说明：

1. 第一行指定编译的版本，若无，则JDK默认生成：Manifest-Version: 1.0。

2. 第二行指定，创建的作者，若无，则JDK默认生成Created-By: 1.6.0_22(Sun Microsystems Inc.)。

3. 第三行指定主类所在类路径，若无，则默认当前目录。

4. 第四行指明程序运行的主类。

#### 重点

1. 以上四句只有最后一句是必需的，其他都可以省略。

2. 注意，配置文件最后必须空一行，即最后以回车结束新起一行。
>Warning: The text file must end with a new line or carriage return. The last line will not be parsed properly if it does not end with a new line or carriage return.

### 编译为hello.jar文件

```bash
jar cvfm hello.jar MANIFEST.MF helloWorld.class
```

### 查看效果

```bash
windard@windard:~$ jar cvfm hello.jar MANIFEST.MF helloWorld.class
已添加清单
正在添加: helloWorld.class(输入 = 425) (输出 = 288)(压缩了 32%)
windard@windard:~$ java -jar hello.jar 
Hello World
```

## 其他

如果是要打包当前目录下的bin目录下的所有class文件,jar打包命令为

```bash
jar cvfm hello.jar MANIFEST.MF -C bin .  
```

其实是可以将java文件打包为exe的，也就是在打包文件里加上一个小型的jre，也就是java running environment，只不过这样就比较复杂也没有必要了。