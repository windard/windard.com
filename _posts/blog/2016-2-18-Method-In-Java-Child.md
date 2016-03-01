---
layout: post
title: java继承中的构造方法和成员方法
description: java继承中的构造方法比较复杂，成员方法有重写与重载，如果在构造方法中有调用了成员方法，则更加复杂。
category: blog
---

##面向对象

###构造方法
java中所有的类都有构造方法，在每个类被创建时会自动调用构造方法来对对象进行初始化。

###super关键字
在java中使用super来引用父类的成分    
1. super可用于访问父类定义的属性
2. super可用于调用父类中定义的成员方法
3. super可用于在子类构造方法中调用父类的构造方法
4. super不仅能追溯到父类，还能追溯到父类的父类，直到object对象为止

###多态
面向对象的三大属性（继承，封装，多态）之一，多态的实现方式之一就是重载，重写是隐藏覆盖，*重写不是重载*。     

多态有两种实现方法：编译时多态和运行时多态。    
1. 编译时多态：通过方法重载来实现编译时多态，方法重载就是在同一个类中定义多个方法名相同，参数不同的方法，当调用不同参数的方法时执行不同的代码，方法重载的返回值，修饰符可以相同也可以不同。构造方法可以重载。   
2. 运行时多态：对外一个接口，内部多种实现，通过重写，向上转型，与动态绑定来实现运行时多态。即在父类中创建成员方法，在不同的子类中有各自实现不同的实现，在不同的子类中调用同一个成员方法，有不同的实现。     

####重写
重写即在子类中修改重写父类的方法实现，父类的方法如果在子类中被重写，在子类中就会被隐藏，不再执行父类的方法而执行子类的方法。    
在子类中可以通过super.方法（参数）来调用父类中的成员方法，通过super（参数）来调用父类中的构造方法。    
在子类的构造方法中会自动执行super（），即在子类的构造方法中会自动调用无参的父类构造方法，如果父类中有且仅有一个有参的构造方法，则需手动调用父类的构造方法super（参数），否则会报错。    
方法重写不能改变方法的名称，参数列表和返回值，方法的访问权限不能缩小，不能抛出新的异常。    
父类中的成员变量也可以被子类中的同名同类型的成员变量重写，在方法中使用的是父类的成员变量还是子类的成员变量取决于该方法是父类的方法还是子类的方法。        
父类中的private或final的成员变量或成员方法都不能被重写。   

####向上转型
子类对象既可以作为该子类的类型对待也可以作为其父类的类型对待。    
通过父类变量发出的方法调用，可能执行该方法在父类中的实现，也可能执行该方法在某子类中的实现，这只能在运行时根据该变量指向的具体对象类型决定。    

####动态绑定
动态绑定即动态联编技术，也叫做晚联编或运行时联编。联编就是将一个方法调用和一个方法体连接到一起，动态联编就是连接绑定在程序运行时根据对象的具体类型找到正确的方法体。       
java中，除了定义为final的方法，其他的方法都是采用晚联编技术。   

##java继承中的构造方法
构造方法可以重载。     
若未手动的添加构造方法，则会有一个默认的无参的内容为空的构造方法，若添加构造方法，则不会产生无参的内容为空的构造方法。      
java的构造方法中会自动执行super（），来调用父类的无参构造方法，如果父类有且仅有一个含参的构造方法，则在子类中必须手动的调用父类的构造方法super（参数），否则会报错。      
那么在子类与父类中就有四种情况（父类构造方法不含参，子类构造方法不含参；父类构造方法不含参，子类构造方法含参；父类构造方法含参，子类构造方法不含参；父类构造方法含参，子类构造方法含参），两种关系（希望调用父类的构造方法，不希望调用父类的构造方法）。

###父类构造方法与子类构造方法         

1. 父类构造方法不含参，子类构造方法不含参     
 1. 希望调用父类的构造方法     
 在子类的构造方法中会自动执行super（），所以在子类中肯定会调用父类的不含参的构造方法    
 2. 不希望调用父类的构造方法     
 在子类的构造方法中会自动执行super（），所以在子类中肯定会调用父类的不含参的构造方法，如果想要不调用父类的不含参的构造方法，可以将父类不含参的构造方法增加一个参数，虽然这个参数并没有实际作用，再在父类中添加一个无参的内容为空的构造方法，就可以在子类的构造方法中不调用父类的构造方法。    
2. 父类构造方法不含参，子类构造方法含参     
 1. 希望调用父类的构造方法     
 在子类的构造方法中会自动执行super（），所以在子类中肯定会调用父类的不含参的构造方法    
 2. 不希望调用父类的构造方法     
 在子类的构造方法中会自动执行super（），所以在子类中肯定会调用父类的不含参的构造方法，如果想要不调用父类的不含参的构造方法，可以将父类不含参的构造方法增加一个参数，虽然这个参数并没有实际作用，再在父类中添加一个无参的内容为空的构造方法，就可以在子类的构造方法中不调用父类的构造方法。    
3. 父类构造方法含参，子类构造方法不含参     
 1. 希望调用父类的构造方法     
 因为父类的构造方法含参，子类的构造方法不含参，会报错，如果父类的构造方法含参，子类的构造方法一定需要含参。    
 2. 不希望调用父类的构造方法     
 因为父类的构造方法含参，子类的构造方法不含参，会报错，如果父类的构造方法含参，子类的构造方法一定需要含参。     
4. 父类构造方法含参，子类构造方法含参     
 1. 希望调用父类的构造方法     
 虽然在子类的构造方法中会自动执行super（），但是这只能调用父类的无参构造方法，所以如果需要调用父类的含参构造方法需要手动的添加super（参数）语句。      
 2. 不希望调用父类的构造方法      
 如果直接在子类的构造方法中不添加super（参数）语句，会报错。我们可以在父类的构造方法中添加一个无参的内容为空的构造方法，这样的话在子类的构造方法中不添加super（参数）语句就不会报错了，而且也没有调用父类的含参构造方法。

##java继承中的成员方法
java中的成员方法可以重载，也可以被重写。   
成员方法被重写就会被隐藏，不再执行，不过可以通过手动的super.方法（参数）来调用，成员变量也是。  

##java构造方法中调用成员方法
不建议在java构造方法中调用成员方法。   
如果在构造方法中调用了成员方法，而在子类中成员方法被重写，那么父类的构造方法中的成员方法调用父类的成员方法，子类的构造方法中的成员方法调用子类中的成员方法。

##几个例子

###向上溯型

```java
class Basic{
    public void add(int i)
    {
        System.out.println("Basic add");
    }

    public Basic()
    {
        add('a');
    }
}

class A extends Basic{
    public void add(int i)
    {
        System.out.println("A add");
    }
}

class B extends Basic{
    public void add(char i)
    {
        System.out.println("B add");
    }
}

public class Main{
    public static void main(String[] args)
    {
        A a = new A();
        B b = new B();
    }
}
```

结果是

```java
A add
Basic add
```

为什么在子类B中add（）调用的是子类的方法，而子类A中调用的是父类的方法呢？其实如果我们把所有的add（）方法的参数去掉再试一下就清楚了。

```java
A add
B add
```

其实是在子类A与子类B的创建时自动调用了构造方法，在构造方法里自动调用了父类的构造方法，在父类的构造方法中调用了add（）方法，因为是在子类构造方法中，所以调用的就是子类的add（）函数，所以子类B的add（）方法被调用了，但是在子类A中，因为add（）方法的参数不符合，向上溯型调用父类的add（）函数，但是参数还是不符合，这时就会强制类型转换，因为char类型是可以自动向int类型转换的，所以调用了父类的add（）函数。

###成员变量覆盖

```java
public class ConstructSubObj{
	public static void main(String[] args) {
		Student st = new Student();
	}
}

class Person{
	String name="George";
	Person(){
		System.out.println("This is parent : "+this.name);
	}
}

class Student extends Person{
	String name="Tyler";
	Student(){
		System.out.println("This is child : "+this.name);
	}
} 
```

结果是

```java
This is parent : George
This is child : Tyler
```

###一个暂时不理解的例子

```java
public class ConstructSubObj{
	public static void main(String[] args) {
		Student st = new Student();
		st.show();
	}
}

class Person{
	public String name="George";
	Person(){
		show();
	}
	public void show(){
		System.out.println("This is parent : "+this.name);
	}
}

class Student extends Person{
	public String name="Tyler";
	public void show(){
		System.out.println("This is child : "+this.name);
	}
} 
```

结果是

```java
This is child : null
This is child : Tyler
```

可以看到确实是调用了子类的show（）函数，但是不知道为什么子类的show（）函数无法找到子类的成员变量，可是如果直接调用子类的show（）函数，却可以找到子类的成员方法。

###向上溯型

```java
class SuperClass {  
    private int number;  
  
    public SuperClass() {  
        this.number = 0;  
    }  
  
    public SuperClass(int number) {  
        this.number = number;  
    }  
  
    public int getNumber() {  
        number++;  
        return number;  
    }  
}  
  
class SubClass1 extends SuperClass {  
    public SubClass1(int number) {  
        super(number);  
    }  
  
}  
  
class SubClass2 extends SuperClass {  
    private int number;  
  
    public SubClass2(int number) {  
        super(number);  
    }  
  
}  
  
public class SubClass extends SuperClass {  
  
    private int number;  
  
    public SubClass(int number) {  
        super(number);  
    }  
  
    public int getNumber() {  
        number++;  
        return number;  
    }  
  
    public static void main(String[] args) {  
        SuperClass s = new SubClass(20);  
        SuperClass s1 = new SubClass1(20);  
        SuperClass s2 = new SubClass2(20);  
        System.out.println(s.getNumber());  
        System.out.println(s1.getNumber());  
        System.out.println(s2.getNumber());  
    }  
  
}  
```

结果是

```java
1
21
21
```

结论一：多态时，当子类覆盖了父类的方法，使用子类覆盖的方法  
结论二：当子类覆盖父类的成员变量时，父类方法使用的是父类的成员变量，子类方法使用的是子类的成员变量  

###this用于构造方法重载

```java
public class EmplyeeTest{
	public static void main(String[] args) {
		Emplyee e = new Emplyee();
		System.out.println("Name : "+e.name+"Salary : "+e.salary);
	}
}

class Emplyee{
	public String name;
	public int salary;
	public Emplyee(String name,int salary){
		this.name = name;
		this.salary = salary;
	}
	public Emplyee(String name){
		this(name,0);
	}
	public Emplyee(){
		this("Unknown");
	}
}
```

结果为

```java
Name : UnknownSalary : 0
```

该类在构造时先找无参的构造方法，无参的构造方法通过this（String name），再次调用含String的构造方法，通过this（String name,int salary），再次调用含String和int的构造方法，最终将name和salary赋初始值。       

注意使用this来调用构造方法或使用super来调用父类的构造方法，必须将this语句或super语句作为构造方法的第一条语句。      

###this调用其他构造方法

```java
public class ConstructSubObj{
	public static void main(String[] args) {
		Student st = new Student("School");
		st.show();
	}
}

class Person{
	private String name;
	private int age;
	Person(String name,int age){
		this.name = name;
		this.age = age;
	}
	void show(){
		System.out.println("This is parent "+name+"  "+age);
	}
}

class Student extends Person{
	private String school;
	Student(String school){
		this("George",10,school);
	}
	Student(String name,int age,String school){
		super(name,age);
		this.school = school;
	}
	public void show(){
		super.show();
		System.out.println("This is child "+this.school);
	}
} 
```

结果是

```java
This is parent George  10
This is child School
```

###禁用构造方法
1. 如果一个类允许其他程序用new语句构造它的实例，但不允许拥有子类，那就把类的所有构造方法声明为final类型。    
2. 如果一个类既不允许其他程序用new语句构造它的实例，又不允许拥有子类，那就把类的所有构造方法声明为private类型。    

