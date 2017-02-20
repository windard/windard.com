---
layout: post
title: python继承中的构造方法和成员方法
description: java的继承比较复杂，也是最为全面，而Python的就单纯的多，然后就越来越复杂
category: blog
---

## Python的面向对象

无论是Java，还是Python，PHP，JavaScript等等面向对象语言，都肯定有构造方法，构造方法就是在某一个类在实例化的时候首先自动调用的方法。既然有构造方法，就有销毁方法，在PHP中称为析构方法，也就是在PHP的一个对象在消失的时候自动调用的方法。

还有就是Python和PHP都不支持构造方法重载或成员函数重载，不过能使用默认参数。

既然是面向对象，那么肯定就有类的继承，然后就是复杂的构造方法的继承，关于Java的构造方法的继承可以看我的另一篇博客，讲的还算全面，本篇博客里主要讨论一下Python继承中的构造方法。

Python由于历史遗留问题，在Python2于Python3中有较大差异，而且在面向对象时也出现一个新式类与旧式类的区别，如果一个类没有任何的父类，那么它就是新式类，如果有继承而来的父类，就是新式类，而所有类的父类就是object，也就是说如果一个类确实是没有父类的话，就可以继承object类来成为一个新式类。

关于新式类与旧式类的区别，本文不再做详细论述，全部使用新式类，因为只有新式类才能够使用super函数。

还有一点Python比较奇怪的地方就是Python在实例化一个类的时候不使用new关键字，直接像一个函数一样调用就可以了。

## Python继承中的构造方法

在Python的继承中如果子类重写了父类的构造方法，即显式书写了构造方法，那么它不会像Java会有一个隐式的super()来调用父类的无参构造方法。所以，如果在子类中需要父类的构造方法就需要显示的调用父类的构造方法，或者不重写父类的构造方法。

不然的话就不会调用父类的构造方法，这样的话就没有父类了，也就是说没有办法使用父类的成员方法和成员变量了。        

### 调用父类的构造方法的两种方法

#### 使用父类的类名

```python
#coding=utf-8

class Father(object):
	def __init__(self):
		print "I AM FATHER"

class Son(Father):
	def __init__(self):
		Father.__init__(self)		
		print "I AM SON"	

if __name__ == '__main__':
	s = Son()						
```

运行结果是：

```python
I AM FATHER
I AM SON
```

如果去掉继承父类的构造方法那一行

```python
#coding=utf-8

class Father(object):
	def __init__(self):
		print "I AM FATHER"

class Son(Father):
	def __init__(self):
		print "I AM SON"	

if __name__ == '__main__':
	s = Son()						
```

运行结果是：

```python
I AM SON
```

如果父类的构造方法是含参的话，调用父类的构造函数的那一行就是
```
Father.__init__(self,args)		
```
这种调用父类的构造方法的方式是在已知父类的构造方法或者是有多个父类的情况下只初始化某个父类

#### 使用子类的类名

```python
#coding=utf-8

class Father(object):
	def __init__(self):
		print "I AM FATHER"

class Son(Father):
	def __init__(self):
		super(Son,self).__init__()
		print "I AM SON"	

if __name__ == '__main__':
	s = Son()						
```

运行结果是：

```python
I AM FATHER
I AM SON
```

去掉继承父类的构造方法的那一行，结果是：

```python
I AM SON
```

如果父类的构造方法是含参的话，调用父类的构造函数的那一行就是
```
super(Son,self).__init__(args)	
```
这种调用父类的构造方法的方式是在父类的构造方法未知或者是一次性初始化所有的父类

----

可以看出来，因为没有构造方法重载，所以也没有自动调用父类的构造方法，这样的情况下，在Python继承中的构造方法就比Java继承中的构造方法要简单一些。       

同样的像在Java中非常复杂的关于子类与父类的构造方法分别含参与不含参的情况就很容易讨论了，一切取决于是否想要调用父类的构造方法，如果想要调用就调用，不想调用就不调用。      

当然如果子类中没有显式的书写构造方法，还是会自动调用父类的构造方法。

## Python继承中的销毁方法

销毁方法与构造方法相反，是在这个对象被销毁的时候被调用的。

```python
#coding=utf-8

class Father(object):
	def __del__(self):
		print "Father Over"

class Son(Father):
	def __del__(self):
		print "Son Over"

if __name__ == '__main__':	
	s = Son()	

```

运行结果是：

```python
Son Over
```

销毁方法也和构造方法一样，如果子类已经有了销毁方法就不会自动的调用父类的销毁方法，不过如果想要显式的调用父类的销毁方法就只有一种方法。

```python
#coding=utf-8

class Father(object):
	def __del__(self):
		print "Father Over"

class Son(Father):
	def __del__(self):
		super(Son,self).__del__()
		print "Son Over"

if __name__ == '__main__':	
	s = Son()	

```

运行结果是：

```python
Father Over
Son Over
```

在子类中调用父类的销毁方法只有一个办法，就是通过super来调用，而且在销毁方法中是不能够有参数的。

如果子类没有显式的书写销毁方法，那么在子类消失时，还是会自动的调用父类的销毁方法。

```python
#coding=utf-8

class Father(object):
	def __init__(self):
		print "I Am Father"

	def __del__(self):
		print "Father Over"

class Son(Father):
	def work(self):
		print "I work in compary" 

if __name__ == '__main__':	
	s = Son()	

```

运行结果是：

```python
I Am Father
Father Over
```

## Python中的特殊方法

|特殊方法 				|描述 											|
|------					|-----------									|
|`__init__(self[,args])`  | 这个方法在新建对象恰好要被返回使用之前被调用	|
|`__del__(self)`    |恰好在对象要被销毁之前调用							|			
|`__str__(self)`   |在我们对对象使用print语句或是使用str()时调用			|
|`__lt__(self,other)`   | 当使用 小于运算符（<）时调用。类似地，对于所有的运算符（+，>等等）都有特殊的方法	  											    |
|`__getitem__(self,key)` |   使用x[key]索引操作符时调用					|
|`__len__(self) `  | 对序列对象使用内建的len()函数时调用					|


## 继承中成员方法与成员变量

在上面的例子中可以看到，如果子类中没有重写父类的构造方法，或者是重写了父类的构造方法也显式的调用了而父类的构造方法，那么就会执行父类的构造方法。

执行父类的构造方法就意味着父类也被构造出来了，那么如果没有执行父类的构造方法，也就是说没有构造父类，那么还有父类么？

因为Python特殊的性质，如果在子类里重写了父类的构造方法，而且没有显式的调用父类的构造方法的话，还是可以调用父类的成员方法的，甚至在销毁方法中可以调用父类的销毁方法。


因为Python是弱语言类型，不需要在类的方法之外显式的声明成员方法，所以就不会像Java一样对成员变量的默认初始化。

虽然Python中没有public，protected，private等关键字来确定管理权限，不过可以通过使用双下划线`__`来表示私有变量或私有方法，相当于private。

在Java的成员方法里调用其他的成员方法和成员变量时使用this关键字不是必须的，但是在Python中调用同一个子类的其他的成员方法必须使用self关键字。

除了私有方法和私有变量，成员方法与成员变量是可以覆盖父类的同名成员方法或成员变量，如果在覆盖了之后还想要调用父类的成员方法或者是想要父类的成员变量，可以使用super关键字或是直接调用父类的方法，但是父类的成员变量就销毁了，无法再调用父类的成员变量。

除了可以在类的成员方法中调用父类的成员方法，也可以在子类的实例对象中调用父类的成员方法，只不过这两种调用有一点点不同。

```python
#coding=utf-8

class Father(object):

	def __init__(self,name):
		self.name = name
		print "I AM FATHER :"+self.name

	def work(self,name):
		print "I word in factory",name

	def __del__(self):
		print "Father Over"

class Son(Father):

	def __init__(self,name):
		super(Son,self).__init__(name+" . father")
		self.name = name
		print "I AM SON :"+self.name	
		super(Son,self).work("Working")
		self.work("Programing")

	def work(self,name):
		Father.work(self,name)
		print "I work in compary",name 

	def __del__(self):
		super(Son,self).__del__()
		print "Son Over"

if __name__ == '__main__':
	s = Son("Windard")	
	super(Son,s).work("Working")
```

运行结果是：

```python
I AM FATHER :Windard . father
I AM SON :Windard
I word in factory Working
I word in factory Programing
I work in compary Programing
I word in factory Working
Father Over
Son Over
```

如果把显示的调用父类的构造方法的话，就是将`super(Son,self).__init__(name+" . father")`去掉的话，结果为：

```python
I AM SON :Windard
I word in factory Working
I word in factory Programing
I work in compary Programing
I word in factory Working
Father Over
Son Over
```

在子类覆盖了父类的成员变量就无法再找到父类的成员变量了。

```python
#coding=utf-8

class Father(object):

  def __init__(self,name):
      self.name = name

class Son(Father):

  def __init__(self,name):
      super(Son,self).__init__(name+" . father")
      self.name = name
      print self.name
      #输出这一句会报错
      # print super(Son,self).name
      print dir(super(Son,self))
      print super(Son,self).__dict__

if __name__ == '__main__':
  s = Son("Windard")  
```

结果是：

```python
Windard
['__class__', '__delattr__', '__doc__', '__format__', '__get__', '__getattribute__', '__hash__', '__init__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__self__', '__self_class__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__thisclass__', 'name']
{'name': 'Windard'}
```

## 在继承的中构造方法和成员方法

如果某个成员方法在子类中被重写或者是调用了self自身的成员变量，那么无论这个成员方法在构造方法中还是在成员方法中，调用它的具体执行取决于是在父类还是在子类中。

无论是父类的成员方法或者构造方法，如果这个方法里调用到了self自身的成员方法而且这个方法在子类中被调用的，那么它不再调用自身的成员方法，而是调用子类的成员方法。

如果子类直接调用父类的成员方法，而且这个成员方法中用到了self自身的成员变量，那么它其实是调用子类的成员变量。

```python
#coding=utf-8

class Father(object):

	def __init__(self,name):
		self.name = name
		self.work("Working")

	def work(self,name):
		print "My name is :",self.name
		print "I word in factory",name

	def __del__(self):
		print "Father Over"

class Son(Father):

	def __init__(self,name):
		super(Son,self).__init__(name+" . father")
		self.name = name
		super(Son,self).work("Working")
		self.work("Programing")

	def work(self,name):
		Father.work(self,name)
		print "I work in compary",name 

	def __del__(self):
		super(Son,self).__del__()
		print "Son Over"

if __name__ == '__main__':
	s = Son("Windard")	
	super(Son,s).work("Working")
```

结果是：

```python
My name is : Windard . father
I word in factory Working
I work in compary Working
My name is : Windard
I word in factory Working
My name is : Windard
I word in factory Programing
I work in compary Programing
My name is : Windard
I word in factory Working
Father Over
Son Over
```

---

除了可以在子类的构造方法和成员方法中调用父类的成员方法之外，还可以在子类的销毁方法中调用父类的销毁方法，但是在子类的销毁方法中不能调用自己的成员方法。

如果某一个成员方法调用了其他的成员方法，并且这个被调用的成员方法在子类中被重写的话，那么在子类中调用父类的这个成员方法，这个成员方法就会调用子类的被重写之后的成员方法。

而如果这个成员方法调用的成员方法没有在子类中被重写，那么这个被调用的成员方法用的self自身的成员变量，还是调用父类的成员变量。

```python
#coding=utf-8

class Father(object):

	def __init__(self,name):
		self.name = name
		self.work("Working")

	def work(self,name):
		print "My name is :",self.name
		print "I word in factory",name

	def __del__(self):
		print "Father Over"

class Son(Father):

	def __init__(self,name):
		super(Son,self).__init__(name+" . father")
		self.name = name
		super(Son,self).work("Working")
		self.work("Programing")

	def __del__(self):
		# super(Son,self).work("Working")
		# self.work("Working")
		super(Son,self).__del__()
		print "Son Over"

if __name__ == '__main__':
	s = Son("Windard")	
	super(Son,s).work("Working")
```

结果是：

```python
My name is : Windard . father
I word in factory Working
My name is : Windard
I word in factory Working
My name is : Windard
I word in factory Programing
My name is : Windard
I word in factory Working
Father Over
Son Over
```

可是，如果这个成员方法调用的是私有方法，那么如果在子类中调用父类的这个方法的话，那么这个方法还是会调用父类的私有方法。

```python
#coding=utf-8

class Father(object):

	def __init__(self,name):
		self.name = name
		self.__work("Working")

	def __work(self,name):
		print "My name is :",self.name
		print "I word in factory",name

	def __del__(self):
		print "Father Over"

class Son(Father):

	def __init__(self,name):
		super(Son,self).__init__(name+" . father")
		self.name = name
		self.__work("Programing")

	def __work(self,name):
		print "I work in compary",name 

	def __del__(self):
		super(Son,self).__del__()
		print "Son Over"

if __name__ == '__main__':
	s = Son("Windard")	
```

结果是：

```python
My name is : Windard . father
I word in factory Working
I work in compary Programing
Father Over
Son Over
```
