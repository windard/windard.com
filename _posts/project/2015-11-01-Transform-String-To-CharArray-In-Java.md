---
layout: post
title: Java的字符串与字符数组的转化
category: project
description: 字符串String是类，字符数组是基本数据类型
---

今天在做Java作业的时候发现这个问题，觉得有必要记录一下。  

String字符串是类，而字符数组char[]是基本数据类型，但是for循环可以直接遍历数组但是不能遍历字符串。

解决办法：  
1. String.toCharArray()
```java
String str = "abcdefg";
str1 = str.toCharArray();
for(char cc:str1){
	system.out.print(cc);
}
```
2. String.charAt()
```java
String str = "abcdefg";
for(int i=0;i<str.length;i++){
	char ch = str.charAt(i);
	system.out.print(ch);
}
```
3. String.substring()
```java
String str="abcdefg";
for(int i=0;i<str.length;i++){
	String ch = str.substring(i,i+1);
    system.out.print(ch);
}
```