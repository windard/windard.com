---
layout: post
title: 关于引用类型和基本数据类型
category: project
description: 说起来很多高级程序语言里都没有了C语言的指针这样的有用而又难用的东西，但是实际上它只是换了个形式而已。
---

之前是在Python里面发现的引用类型和基本数据类型还是有一点区别的，因为引用的数据类型其实就是指针，可是却偏偏要那么含蓄，想要与C语言撇开关系死不承认是指针，因为Python的深拷贝与浅拷贝的区别，为了这个还专门弄了一个拷贝的库出来了，也是闲的慌。但是实际上我也还不太清楚Python中深拷贝与浅拷贝的关系，准备等期末考试结束了再好好的看一下。

今天在Java中也发现了这个鬼东西，也是奇怪的很，还没有给出什么详细的解释。

首先Java中的基本数据类型就是基本数据类型，主要包括boolean，int，byte，short，long，double，float，和char八种，其他的就是各种类了。Java中的类真是多。

Java里的类是引用数据类型，因为它不是直接声明就是能用的，像基本数据类型，直接声明就能够使用了，但是Java中的类需要实例化才能够使用，如果没有实例化，声明的变量是null。

这个不就是指针么？因为是需要实例化才能够使用的，如果不实例化就是一个引用调用，所以可以当做指针来用，就像这样。

```java
public class hello{
	public static void main(String args[]){
	world h = new world();
	h.x = 1;
	h.y = 2;
	world e;
	e = h;
	System.out.println(e.x); 
	System.out.println(e.y);
	e.x = 2;
	e.y = 1;
	System.out.println(h.x);
	System.out.println(h.y);
	h.x = 3;
	h.y = 4;
	System.out.println(e.x); 
	System.out.println(e.y);	
	System.out.println(h.x);
	System.out.println(h.y);	
	} 
}
class world{
	public int x;
	public int y;
	public void print(){
		System.out.println("hello world");
	}
}

```

输出为` 1 2 2 1 3 4 3 4`，这还是正常的。可是如果这样的话，为什么还是` 1 2 2 1 3 4 3 4` 。

```java
public class hello{
	public static void main(String args[]){
	world h = new world();
	h.x = 1;
	h.y = 2;
	world e = new world();
	e = h;
	System.out.println(e.x); 
	System.out.println(e.y);
	e.x = 2;
	e.y = 1;
	System.out.println(h.x);
	System.out.println(h.y);
	h.x = 3;
	h.y = 4;
	System.out.println(e.x); 
	System.out.println(e.y);	
	System.out.println(h.x);
	System.out.println(h.y);	
	} 
}
class world{
	public int x;
	public int y;
	public void print(){
		System.out.println("hello world");
	}
}
```

难道这也有深拷贝与浅拷贝？直接赋值的话默认是浅拷贝？可是那个实例化出来的对象呢？它们不应该是指向不同的内存地址了么？为什么还是连在一起了呢。。。

但是Java中的String，却可以不用实例化只需要声明就可以使用，真是奇怪，String不是应该也是一个类么？还有像包括ArrayList，各种List，Map，都可以直接声明就使用。也是奇怪的很。。。。

在Java中基本数据类型和引用数据类型都可以用== 或者！= 老比较是否相等但是 对于引用数据类型 它们比较的是地址还是值吖？

以下代码的结果为false，说明比较的是地址，因为两个对象的成员变量都是自动初始化赋值应该为0，那么返回false，说明不是比较的值，而是比较地址。

```java
public class hello{
	public static void main(String args[]){
	world w = new world();
	world o = new world();
	System.out.println(w==o);
}
}
class world{
	public int x;
	public int y;
}
```

但是理论上说equals是比较的值，因为它可以比较两个字符串的值，但是却无法比较类，两个对象比较还是false，而且无法比较数组，两个相同值的数组，==和equals比较都是false。
而且奇怪的是两个相同的值的String，为什么用==比较是true，如果是比较地址不应该不相同么？难道String是披着类之名的基本数据类型？



在数组或者是类中，直接进行两个对象的赋值操作= 只是将引用赋值过去了
也就是指针的操作，跟C语言一模一样
但是如果是仅声明而未实例化的类还好理解
可是已经声明并实例化的类 为什么还是指针赋值过去了？
就像在C语言中对一个指针分配了内存空间 就没有办法在对其赋值指针了 会报错
难道这就是Python中的深拷贝
就像Java中对数值的赋值需要一个专门的函数
System.arraycopy(Object source,int srcindex,Object destitation,int destindex,int length)

卧槽，equals方法默认也是比较对象的引用，和==效果一致。如果想要细致的比较两个对象，还是自己重写equals方法吧

但是对于两个不同的字符串，如果它们的值相等的话，无论是用==还是用equals 它们都是相等的。难道Java内部有这样一种机制，相同的String，直接放在同一个内存地址，反正也没有办法改变。

StringBuffer 就是一个货真价实的类了，需要声明实例化再创建，创建的方法也是那么别致。它的结果就是和其他的类一样。不同的StringBuffer相同的值的时候，==或者是equals都是false

终于发现问题的所在了。String的构造方法不同，结果也不同吖。

在上面的String都是这样构造出来的。

```java
String stra = "hello";
String strb = "hello";
```

这样构造出来的性质与基本数据类型一致，或者说它们就保存在了同一个内存位置。因此用==或者是equals都是true

但是String还可以这样构造。

```java
String stra = new String("hello");
String strb = new String("hello");
```

这样构造的是两个不同类，肯定是引用数据类型。==为false，equals为true。    
>奇怪，这个时候equals怎么就是在比较值了。

发现一个奇怪而又有趣的现象。

用第一种方法构造的String，如果它们的值是相同的，它们的内存地址就是相同的，如果它们的值不相同，它们的内存地址就不相同。或者换一种解释方法就是String变成了基本数据，在方法调用中的效果也是跟基本数据类型一样，并不会改变值。

```java
public class hello{
	public static void main(String args[]){
		String a = "hello";
		String b = "hello";
		System.out.println(a==b);
		System.out.println(a.equals(b));
		a = "world";
		System.out.println(a);
		System.out.println(b);
		System.out.println(a==b);
		System.out.println(a.equals(b));
		String c = "hello";
		String d = "world";
		System.out.println(c==d);
		System.out.println(c.equals(d));
		c = "world";
		System.out.println(c);
		System.out.println(d);
		System.out.println(c==d);
		System.out.println(c.equals(d));	
	} 
}		
```

就像这样的结果是

```java
true
true
world
hello
false
false
false
false
world
world
true
true
```

用第二种方法创建的String就是货真价实的类了，同样的代码，结果就不一样。

```java
public class hello{
	public static void main(String args[]){
		String a = new String("hello");
		String b = new String("hello");
		System.out.println(a==b);
		System.out.println(a.equals(b));
		a = "world";
		System.out.println(a);
		System.out.println(b);
		System.out.println(a==b);
		System.out.println(a.equals(b));
		String c = new String("hello");
		String d = new String("world");
		System.out.println(c==d);
		System.out.println(c.equals(d));
		c = "world";
		System.out.println(c);
		System.out.println(d);
		System.out.println(c==d);
		System.out.println(c.equals(d));	
	} 
}			
```

结果就是

```java
false
true
world
hello
false
false
false
false
world
world
false
true
```

不对，但是String是不变的，StringBuffer才是可变的。如果String的值被改变的话，就是一个新的String。

基于String是不变的这一点理论来看，所以在基本数据类型String被改变时，其内存地址被改变，在相同的值的时候，其内存地址是相同的。但是在引用数据类型String被改变时，其内存地址也发生了改变，其相同的值的时候，内存地址还是不同的。

String是不变的这一点方法调用时，表现的最为明显。无论是哪种方法构造出来的String，在经历以下这个函数调用时，值都不变。

```java
class world{
	static void Change(String str){
		str = "helloworld";
	}
}
```

代码是这样的

```java
public class hello{
	public static void main(String args[]){
		String c = "hello";
		String d = new String("hello");
		System.out.println(c==d);	
		System.out.println(c.equals(d));	
		world.Change(c);
		world.Change(d);
		System.out.println(c);
		System.out.println(d);
		System.out.println(c==d);
		System.out.println(c.equals(d));
	} 
}			
```

结果是

```java
false
true
hello
hello
false
true
```

可以看出来两种String的值都没有改变，而且两种String的值相等，但是内存地址不同。

而且就算是经过下面这种函数调用，String的值都不会变。

```java
class world{
	static void Change(String str){
		str = new String("helloworld");
	}
}
```

又知道了一件事，equals默认也是比较引用地址的，而不是比较引用的值，如果想要比较引用的值，请重写改方法。

但是，String Time Date Integer List 等类库已经重写了改方法，所以用这些比较的时候，已经是在比较引用的值了。