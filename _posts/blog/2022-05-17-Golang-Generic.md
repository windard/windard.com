---
layout: post
title: Golang 泛型实践
description: Go 1.18 正式发布泛型，可以考虑用起来了。
category: blog
---

## 泛型

### 泛型是什么

> 开宗明义，泛型，类型形参和类型实参

在函数定义中，定义要求的参数叫形参，实际传入的参数叫实参，在强类型编程语言中要求形参和实参的类型一致。

这样就会有一个问题，导致我们的函数限制非常强，特别是在 Golang 的数字类型有很多种的情况下。

```go
package main

import "fmt"

func MinInt(a, b int) int {
    if a <= b {
        return a
    } else {
        return b
    }
}

func main() {
    fmt.Println(MinInt(1, 2))
}
```

像这样比较大小的函数，(a,b) 就是形参，(1,2) 就是实参，我们可能对于不同的类型都要分别再写一个函数。

如果能够不限制形参类型，在函数调用的时候再指定具体类型，这个问题是不是就可以解决了呢？

那么我们就需要引入类型形参 (Type Parameter) 和类型实参 (Type Argument) 的概念。

---

假设有这样一个函数，就是在函数定义的时候使用类型形参，然后将参数类型也当成参数传入，进行类型的参数化。

在函数调用的时候，不但需要传入参数，还需要传入参数的类型，可以把类型像方法的参数那样传递，指定实际执行的参数类型。

```go
func min[T Numeric](a, b T) T {
    if a < b {
        return a
    }
    return b
}

func main() {
    fmt.Println(min[int](45, 74))
    fmt.Println(min[float64](4.141, 2.01))
}
```

这样就能让一个函数处理多种不同类型数据，可以在函数调用的时候再明确参数类型，这种方式就被称为泛型编程。

那么其实并不是泛型编程中就不需要关心参数类型，只是将参数类型进行后验确定，在 Golang 编译时还是会根据实际参数类型对函数进行展开编译。

所以在 Go1.18 引入泛型之后，对编译性能会一定的影响，[大概会有 18% 的性能下降](https://blog.csdn.net/EDDYCJY/article/details/121484720)，但是对运行性能无影响。

引入泛型的好处
1. 在编译期间对类型进行检查以提高类型安全
2. 通过指定类型消除强制类型转换
3. 能够减少代码重复性，提供更通用的功能函数。

但是也泛型也不是银弹，不是所有场景下都需要泛型编程，主要在针对不同类型的数据写完全相同的逻辑代码的情况下，可以考虑使用泛型。

### 泛型怎么用

泛型就是泛指的类型，即类型参数化，在定义时无需确定参数的类型，可以在调用的时候再指定参数类型。

在这里我们去掉了函数，因为实际泛型的用处不止在函数中，也可以在类型，接口，函数等各种地方。

泛型的应用主要有三种
1. 泛型类型
2. 泛型接口
3. 泛型函数

#### 泛型类型

常用于一些集合类型，比如使用泛型栈的设计，因为 Golang 强类型语言，一般的栈只能是固定类型，泛型栈可以在实例化的再确定具体的元素类型。

比如设计一个支持整形和字符串的列表和字典，这里的泛型占位符 `T`,`K`,`V` 都可以，只需要保持在同一个定义中前后一致就可以。

```go
package main

import "fmt"

type ListType[T int | int32 | int64 | string] []T

type MapType[K int | int32, V int64 | string] map[K]V

func main() {
    var intList ListType[int]
    intList = []int{1, 2, 3}
    fmt.Println(intList)
    strList := ListType[string]{"1", "2", "3"}
    fmt.Println(strList)

    intMap := MapType[int, string]{1: "1", 2: "2"}
    int32Map := MapType[int32, int64]{1: 2, 3: 4}
    fmt.Println(intMap)
    fmt.Println(int32Map)
}
```

还有一个简单的泛型类的例子
```go

```

这里的泛型占位符 `T` 就是类型形参，在 T 的可选类型中，`int | int32` 就是 `T` 的类型约束 (Type Constraint)

就是在实际传入类型实参的时候，只能使用类型参数列表中限定的类型，其中 `any` 表示任意类型，同 `interface{}`。

#### 泛型接口
接口是对类的进一步抽象，~~将类抽象为接口是一种基本技能~~，在接口定义时只需要给出函数签名而无需完成其具体逻辑。

Golang 中会自动查找类上定义的方法，如果某个类实现了接口定义的全部函数，即可认为类实现了这个接口。
> 在面向对象的编程语言中，使用接口的时，在函数定义中无需指定其具体的实现类，只需要传入参数对象实现了接口定义的方法即可。

在函数定义的时候，也可以将接口作为参数类型，这样就可以传入任意一个实现了该接口的对象。

**注意**
在这里的接口都是指 `interface`, 而非 `interface{}`.

因为 `interface{}` 作为一个空接口在 Golang 中也被认为是基础对象类型，类似于 Java 中的 `Object`

所以为了避免歧义以及减少书写成本， 在 Go1.18 之后，新增 `any` 类型代替 `interface{}` 类型，可以在代码中做全量替换。
> 可以使用这行代码进行全量替换 `gofmt -w -r 'interface{} -> any' ./...`

对于一个泛型接口，可以在接口定义的时候声明泛型，不限制其具体的实现类型。

同样的像上面提到的泛型栈，就可以使用泛型接口来进行抽象。

```go
type GenericStackInterface[T any] interface {
    Push(element T)
    Pop() T
}
```

除了泛型接口，在 Golang 1.18 中 `interface` 还新增了类型集合的概念，可以在接口定义中添加多种类型。

注意相当于之前的接口是函数集合，可以用来声明一些函数，但是在 Go1.18 中扩充了类型集合，可以在接口中声明一些类型，在同一个接口中，可以同时存在类型集合和函数集合。

```go
type Numeric interface {
    int | int8 | int16 | int32 | int64 | uint | uint8 | uint16 | uint32 | uint64 | float32 | float64
}
```

像这种就是类型集合，以前的接口就是原始的方法集合，也被称为基本接口，基本接口也是一个空的类型集合。

在类型集合中，在同一行内的多种类型，使用 `|` 相连，表示类型取并集，如果分成多行，则各行之间取交集。

如果交集为空，则为取空集，空集不等于空接口，空接口表示可以使用任意类型，空集表示无法使用任何类型。

在泛型接口定义时，泛型类型集合与接口集合，不能同时使用类型形参和类型集合，在类型集合中也不能使用递归定义。

#### 泛型函数

泛型除了可以在类定义和接口定义中，可以在函数定义中使用，作为入参或出参的类型。

比如在上面泛型栈的设计中，对于入栈和出栈的操作，就已经用到了泛型函数的定义。

再比如，一开始就提到的比较大小的场景，我们可以定义类型形参，允许多种不同类型的整形比较

```go
func minInt[T int | int8 | int16 | int32](a, b T) T {
    if a < b {
        return a
    }
    return b
}

func maxInt[T int | int8 | int16 | int32](a, b T) T {
    if a > b {
        return a
    }
    return b
}
```

但是这样的话，每个函数中都需要对各种数字类型给排列一遍，我们可以使用类型集合，将所有数字类型先定义出来。

比如优化后的比大小操作

```go
package main

type Numeric interface {
    int | int8 | int16 | int32 | int64 | uint | uint8 | uint16 | uint32 | uint64 | float32 | float64
}

func min[T Numeric](a, b T) T {
    if a < b {
        return a
    }
    return b
}

func max[T Numeric](a, b T) T {
    if a > b {
        return a
    }
    return b
}
```

这里的所有的数字类型，都被包含在 `Numric` 中，这样就可以在泛型函数中比较大小，这种带类型形参的函数被称为泛型函数。

前面提到泛型函数在调用的时候是需要指定其具体类型的，但是对于某些简单类型也会自动推导，可以省略。

```go
func main() {
    maths.MinInt(1, 2)
    fmt.Println(min(45, 74))
    fmt.Println(min[int](45, 74))
    fmt.Println(min[int32](45, 74))
    fmt.Println(max(4.141, 2.01))
    fmt.Println(max[float64](4.141, 2.01))
    // 编译报错：cannot use 4.141 (untyped float constant) as int64 value in argument to max[int64] (truncated)
    fmt.Println(max[int64](4.141, 2.01))
    // IDE报错：Cannot use string as the type Numeric
    // 编译报错：string does not implement Numeric
    fmt.Println(max[string](4.141, 2.01))
}
```

但是注意两点
1. 可以执行类型，如果指定类型和实际传入参数类型不一致，就有编译报错
2. 不指定类型，编译器会自动识别类型，如果类型不一致，也会有编译报错

因为 Golang 的泛型是在编译时会根据指定的具体类型将泛型确定下来，运行时还是有强类型限制的

对于在通用的数字类型，Golang 1.18 中也内置了 `constraints.Ordered` 表示所有可供排序的内置类型，所以上面的泛型函数可以改写成这样

```go
package main

import (
    "golang.org/x/exp/constraints"
)

func minType[T constraints.Ordered](a, b T) T {
    if a < b {
        return a
    }
    return b
}

func maxType[T constraints.Ordered](a, b T) T {
    if a > b {
        return a
    }
    return b
}
```

如果进入源代码查看其具体代码的话，会发现在 `Ordered` 类型中也是有各种数字类型组合起来的。

但是有一点奇怪的地方就是这里的类型集合中，各种类型前加了一个波浪线`~`, 表示衍生类型，即使用 `type` 自定义的类型也可以被识别到，只要底层类型一致即可。

比如 `~int` 可以包含 `int` 和 `type MyInt int` 等多种类型

```go
// Signed is a constraint that permits any signed integer type.
// If future releases of Go add new predeclared signed integer types,
// this constraint will be modified to include them.
type Signed interface {
	~int | ~int8 | ~int16 | ~int32 | ~int64
}

// Unsigned is a constraint that permits any unsigned integer type.
// If future releases of Go add new predeclared unsigned integer types,
// this constraint will be modified to include them.
type Unsigned interface {
	~uint | ~uint8 | ~uint16 | ~uint32 | ~uint64 | ~uintptr
}

// Integer is a constraint that permits any integer type.
// If future releases of Go add new predeclared integer types,
// this constraint will be modified to include them.
type Integer interface {
    Signed | Unsigned
}

// Float is a constraint that permits any floating-point type.
// If future releases of Go add new predeclared floating-point types,
// this constraint will be modified to include them.
type Float interface {
    ~float32 | ~float64
}

// Complex is a constraint that permits any complex numeric type.
// If future releases of Go add new predeclared complex numeric types,
// this constraint will be modified to include them.
type Complex interface {
    ~complex64 | ~complex128
}

// Ordered is a constraint that permits any ordered type: any type
// that supports the operators < <= >= >.
// If future releases of Go add new ordered types,
// this constraint will be modified to include them.
type Ordered interface {
    Integer | Float | ~string
}
```

除了 `Ordered` 类型之外，还提供了一个内置接口类型， `comparable` ，这里的可比较指
的是可以用 `==` 和 `!=` 是否相同进行比较，而非可以进行 `>` 和 `<` 进行大小比较，但是注意在接口集合中，不能使用 comparable 接口和其他类型的并集。

在泛型的使用时，可以用在类型定义和接口定义中，作为类型约束和类型集合使用，也可以用在通道 (Channel) 中。

但是也有一些不能用的时候，比如
1. 不能单独定义泛型，
2. 比如匿名结构体不能使用泛型，
3. 比如匿名函数不能自己定义类型形参。
4. 有就是只能在泛型类中使用泛型方法，不能在非泛型类中使用泛型方法。

类型形参只能被定义一次，类型实参也只能被传入确定一次，不能用类型实参确认多次。

## 参考链接
[Go 1.18 泛型全面讲解：一篇讲清泛型的全部](https://segmentfault.com/a/1190000041634906)    
[泛型的作用与定义](https://anymarvel.github.io/AndroidSummary/book/java/deepIntoJavaGenerics/roleAndSignificanceOfGenerics.html)   
[泛型是双刃剑？Go1.18 编译会慢近 20%](https://blog.csdn.net/EDDYCJY/article/details/121484720)    
[Go 1.18 正式发布了！支持泛型、性能优化...](https://www.oschina.net/news/186664/go-1-18-released)    
[浅谈Go1.18中的泛型编程](https://www.qetool.com/scripts/view/3641.html)    
[Golang 泛型浅析](https://xie.infoq.cn/article/0eeb0f970043bafb42622c5d6)  
[Java 泛型优点之编译时类型检查](https://developer.aliyun.com/article/617432)  
[为什么要使用泛型？](https://zq99299.github.io/java-tutorial/java/generics/why.html)   
[秒懂Java之泛型](http://shusheng007.top/2021/09/09/031-2/)   
[Go语言泛型设计](https://taoshu.in/go/generics/design.html)   
[函数式编程在 Go 泛型下的实用性探索](https://silverrainz.me/blog/funtional-programming-in-go-generics.html)  
[Go泛型快速入门](https://juejin.cn/post/7042344142281637895)   
[Go 泛型简明教程](https://jiajunhuang.com/articles/2022_03_17-go_generics.md.html)  
[Go 泛型初步](https://gopherd.com/posts/go/generic-get-started/)   
[Go 1.18新特性学习笔记04: Go泛型的基本语法](https://blog.frognew.com/2022/03/go-1.18-notes-04.html)  
[Go 泛型的这 3 个核心设计，你都知道吗？](https://segmentfault.com/a/1190000041227815)   
[Go泛型介绍](https://tonybai.com/2022/03/25/intro-generics/)   
[Tutorial: Getting started with generics](https://go.dev/doc/tutorial/generics)   
[An Introduction To Generics](https://go.dev/blog/intro-generics)    
