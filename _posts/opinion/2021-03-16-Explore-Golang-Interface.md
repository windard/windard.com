---
layout: post
title: 探究 Golang interface
description: Golang 中最灵活也是最神奇的接口
category: opinion
---

Golang 是一门强类型的高级编程语言，有人说
> 与 C++ 相比，Go语言并不包括如异常处理，继承，泛型，断言，虚函数等功能，但增加了 slice 型，并发，管道，垃圾回收，接口(interface) 等特性的语言级支持。

![](https://windard-blog.oss-cn-beijing.aliyuncs.com/1615860095083.png)

对于此，我只能说，Go 虽然没有这么多的高级功能，但是它难写难用吖，~~Go 是垃圾~~（并不）。

## interface
在 Golang 中的 interface 有两种意思，一种是和 Java 等语言中一样的接口 Interface 类似的含义，一种是和 Python 中的无指定基类对象 object 类似的含义。

### 接口定义

在 Golang 中虽然没有泛型，但是也可以定义 interface 接口，在函数中使用 interface 实现调用。

```golang
package main

import (
	"errors"
	"fmt"
	"log"
)

type Animal interface {
	call() string
	eat(string) error
}

func feedAnimal(animal Animal) {
	err := animal.eat("grass")
	if err != nil {
		log.Printf("eat error:%+v\n", err)
		err = animal.eat("meat")
		if err != nil {
			log.Printf("eat error again:%+v\n", err)
			fmt.Printf("animal %#v died", animal)
			return
		}
	}

	fmt.Printf("animal %#v eat finished\n", animal)
	fmt.Printf("animal call:%s\n", animal.call())
}

type Sheep struct {
}

func (sheep Sheep) call() string {
	return "Baa"
}

func (sheep Sheep) eat(food string) error {
	if food != "grass" {
		return errors.New("I dislike this")
	}
	return nil
}

type Tiger struct {
}

func (tiger Tiger) call() string {
	return "Wailing"
}

func (tiger Tiger) eat(food string) error {
	if food != "meat" {
		return errors.New("I need meat")
	}
	return nil
}

func main() {

	zoo := []Animal{Sheep{}, Tiger{}}
	for _, animal := range zoo {
		feedAnimal(animal)
	}
}

```

### 基类对象

Golang 是强类型语言，如果想把多种类型的数据放在一起，就需要使用 基类对象 interface,可以表示为任意对象类型。

对于 interface 类型，可以使用 `.` 来做类型校验和转换，也只有 interface 类型可以使用 `.` 方法校验转换。

```golang	
package main

import (
	"errors"
	"fmt"
)

type Bird interface {
	fly()
}

type Mahjong struct {
}

func (m Mahjong) fly() {}

type Pigeon struct {
}

func (p Pigeon) fly() {}

type Horse struct {
}

func guess(o interface{}) error {
	_, ok := o.(Pigeon)
	fmt.Printf("I guess it's a pigeon\n")
	if ok {
		fmt.Printf("Congratulations，you are right\n")
		return nil
	} else {
		fmt.Printf("Oops, you ares wrong.\n")
	}

	_, ok = o.(Horse)
	fmt.Printf("I guess it's a horse\n")
	if ok {
		fmt.Printf("Congratulations，you are right\n")
		return nil
	} else {
		fmt.Printf("Oops, you ares wrong.\n")
	}

	_, ok = o.(Bird)
	fmt.Printf("I guess it's a bird\n")
	if ok {
		fmt.Printf("Congratulations，you are right\n")
		return nil
	} else {
		fmt.Printf("Oops, you ares wrong.\n")
	}

	_, ok = o.(int)
	fmt.Printf("I guess it's int number\n")
	if ok {
		fmt.Printf("Congratulations，you are right\n")
		return nil
	} else {
		fmt.Printf("Oops, you ares wrong.\n")
	}

	_, ok = o.(string)
	fmt.Printf("I guess it's string\n")
	if ok {
		fmt.Printf("Congratulations，you are right\n")
		return nil
	} else {
		fmt.Printf("Oops, you ares wrong.\n")
	}

	_, ok = o.(map[interface{}]interface{})
	fmt.Printf("I guess it's map\n")
	if ok {
		fmt.Printf("Congratulations，you are right\n")
		return nil
	} else {
		fmt.Printf("Oops, you ares wrong.\n")
	}
	return errors.New("OMG, I don't known what's it")
}

func main() {
	mess := []interface{}{1, 2, "hello", Mahjong{}, Pigeon{}, Horse{}, map[string]string{}}
	for _, m := range mess {
		fmt.Printf("start to guess:%#v\n", m)
		err := guess(m)
		if err != nil {
			fmt.Printf("haha, you fail:%+v\n", err)
		}
	}
	
}

```

当然，如果只是为了判断类型，使用 switch 会更方便一些。

```golang
package main

import (
	"errors"
	"fmt"
)

type Bird interface {
	fly()
}

type Mahjong struct {
}

func (m Mahjong) fly() {}

type Pigeon struct {
}

func (p Pigeon) fly() {}

type Horse struct {
}

func switchGuess(o interface{}) error {
	switch o.(type) {
	case Pigeon:
		fmt.Printf("I guess it's a pigeon\n")
	case Horse:
		fmt.Printf("I guess it's a horse\n")
	case Bird:
		fmt.Printf("I guess it's a bird\n")
	case int, int8, int16, int32, int64:
		fmt.Printf("I guess it's int number\n")
	case string:
		fmt.Printf("I guess it's string\n")
	case map[interface{}]interface{}:
		fmt.Printf("I guess it's map\n")
	default:
		return errors.New("OMG, I don't known what's it")
	}
	return nil
}

func main() {
	mess := []interface{}{1, 2, "hello", Mahjong{}, Pigeon{}, Horse{}, map[string]string{}}
	for _, m := range mess {
		fmt.Printf("start to guess:%#v\n", m)
		err := switchGuess(m)
		if err != nil {
			fmt.Printf("haha, you fail:%+v\n", err)
		}
	}

}

```

使用 switch 就简洁很多了，而且不用一个一个判断，直接判断给出正确的类型，不过使用 switch 有几点需要注意
1. `o.(type)` 同样是只有 interface 才有的功能，其他的类型无法使用类型判断
2. 每个 case 中无需 break ，和其他的编程语言中的 switch 不太一样
3. 对于多个 case 合并，使用逗号 `,` 分割即可
	> 如果使用两个单独的空 case ，并不能合并，只是表示空 case 而已。
4. 对于 `list` 或者 `map` 类型的判断，是要求子元素的类型也要完全一致才匹配的，使用 `interface{}` 也不能做通用判断 

### 空值

对于 Golang 中的空值有两种含义
- 对于基础数据类型或者结构体来说，空值就是初始值，初始值就是零值。
- 对于指针类型来说，空指针就是 `nil`, 如果对 `nil` 进行操作，就会触发 `panic` ，类似于 Java 中的 `NPE`， 但是会更可怕。

一般的常见类型在初始化时就会赋予零值，包括在函数签名中定义的入参和出参，也会被自动初始化

```golang
package main

import "fmt"

type Phone struct {
	Brand string
}

func main() {
	var iphone Phone
	iphone.Brand = "Apple"
	fmt.Printf("introduce my phohe to you:%+v\n", iphone)

	miPhone := Phone{}
	miPhone.Brand = "mi"
	fmt.Printf("introduce another phohe to you:%+v\n", miPhone)

	var TempList []string
	TempList = append(TempList, "phone")
	fmt.Printf("temp list is:%+v\n", TempList)

	var TempInt int
	fmt.Printf("init int is:%+v\n", TempInt)

}
```

但是对于指针类型，并不会在初始化的时候赋值，需要先创建对象，然后赋值给指针，才能够使用.

创建指针类型的几种方式
1. 创建正常的对象数据结构，使用 `&` 取对象指针地址，在指针类型上，使用 `*` 取值
2. Golang 中的函数调用都是值传递，使用指针类型才能进行地址传递
3. 在创建对象指针时，还可以使用 `new` 方法直接进行创建，返回创建对象的指针
4. 特别需要注意的是，基础数据类型中的 `map` 结构的初始化并没有分配内存地址，`list` 结构的初始化有分配内存地址
5. 所以对于 `map` 类型初始化的之后需要分配地址才能使用，或者使用字面量初始化并分配地址的方式 `map[string]string{}`
4. 可以使用 `make` 创建 `map` 或者 `list` 类型数据结构，返回的是数据值而非数据指针。


```golang
package main

import "fmt"

type Phone struct {
	Brand string
}

func first() {
	var iphone Phone
	iphone.Brand = "Apple"
	fmt.Printf("introduce my phohe to you:%+v\n", iphone)

	miPhone := Phone{}
	miPhone.Brand = "mi"
	fmt.Printf("introduce another phohe to you:%+v\n", miPhone)

	var TempList []string
	TempList = append(TempList, "phone")
	fmt.Printf("temp list is:%+v\n", TempList)

	var TempInt int
	fmt.Printf("init int is:%+v\n", TempInt)

}

func main() {
	var iphone *Phone
	// panic: runtime error: invalid memory address or nil pointer dereference
	// iphone.Brand = "Apple"
	fmt.Printf("pointer not init:%+v\n", iphone)
	iphone = &Phone{}
	iphone.Brand = "Apple"
	fmt.Printf("introduce my phohe to you:%+v\n", iphone)

	miPhone := &Phone{}
	miPhone.Brand = "mi"
	fmt.Printf("introduce another phohe to you:%+v\n", miPhone)

	oPhone := new(Phone)
	oPhone.Brand = "OPPO"
	fmt.Printf("introduce Find X3 to you:%+v\n", oPhone)

	var TempList *[]string
	TempList = &[]string{}
	*TempList = append(*TempList, "phone")
	fmt.Printf("temp list is:%+v\n", TempList)

	var TempMap map[string]string
	fmt.Printf("map init with nil:%+v\n", TempMap)
	// panic: assignment to entry in nil map
	// TempMap["phone"] = "iphone"

	//TempMap = map[string]string{}
	TempMap = make(map[string]string)
	TempMap["phone"] = "iphone"
	fmt.Printf("temp map is:%+v\n", TempMap)

	OtherMap := map[string]string{}
	OtherMap["phone"] = "iphone"
	fmt.Printf("map value is:%+v\n", OtherMap)
}

```

好，以上只是一些基础知识都介绍完了，接下来要开始本文的重点部分。

![](https://windard-blog.oss-cn-beijing.aliyuncs.com/1615865541499.png)

### 判空

判空，意如其名，如何判断一个对象是否为空值，或者为空指针。

1. 如果是值类型，就直接判断是否为初始值即可。
2. 如果是指针类型，就判断是否为 `nil`

很快吖，就可以写出这样的两个方法

```golang
package main

import (
	"fmt"
	"log"
)

func checkValueEmpty(o interface{}) bool {
	switch o.(type) {
	case int:
		return o == 0
	case string:
		return o == ""
	case []interface{}:
		return len(o.([]interface{})) == 0
	case map[interface{}]interface{}:
		return len(o.(map[interface{}]interface{})) == 0
	default:
		log.Printf("can't detect o type:%#v\n", o)
		return false
	}
}

func checkPointerNil(o interface{}) bool {
	return o == nil
}

func main() {
	mess := []interface{}{0, 1, 2, "", "hello", map[string]string{}, []int{}, []interface{}{}}
	for _, m := range mess {
		fmt.Printf("%#v is zero:%+v\n", m, checkValueEmpty(m))
	}
	for _, m := range mess {
		fmt.Printf("%#v is nil:%+v\n", m, checkPointerNil(m))
	}
}

```

看起来都很完美，但是遥远的天边飘着两朵乌云
1. interface 的零值真的未 `nil` 么？
2. 如何判断是值类型还是指针类型呢？


在解决这个问题之前，我们先思考一个问题🤔，如果 `interface` 可以代表任意类型，那么它可以代表指针类型么？`*interface{}` 可以代表指针的指针类型么？
> 答案是可以的

```golang
package main

import "fmt"

func main() {
	var o interface{}
	var op *interface{}
	var i *int
	var j *int
	var s *string
	fmt.Printf("o:%#v is nil?:%#v\n", o, o == nil)
	fmt.Printf("op:%#v is nil?:%#v\n", op, op == nil)
	fmt.Printf("i:%#v is nil?:%#v\n", i, i == nil)
	fmt.Printf("j:%#v is nil?:%#v\n", j, j == nil)
	fmt.Printf("s:%#v is nil?:%#v\n", s, s == nil)
	i = j
	fmt.Printf("i:%#v is nil?:%#v\n", i, i == nil)

	o = op
	fmt.Printf("o:%#v is nil?:%#v\n", o, o == nil)
	o = i
	fmt.Printf("o:%#v is nil?:%#v\n", o, o == nil)
	o = s
	fmt.Printf("o:%#v is nil?:%#v\n", o, o == nil)
	o = (*int)(nil)
	fmt.Printf("o:%#v is nil?:%#v\n", o, o == nil)

	// panic: runtime error: invalid memory address or nil pointer dereference
	// 指针未初始化，无法重新赋值
	// *op = &i
	// fmt.Printf("op:%#v is nil?:%#v\n", op, op == nil)

}


```

输出结果是

```
o:<nil> is nil?:true
op:(*interface {})(nil) is nil?:true
i:(*int)(nil) is nil?:true
j:(*int)(nil) is nil?:true
s:(*string)(nil) is nil?:true
i:(*int)(nil) is nil?:true
o:(*interface {})(nil) is nil?:false
o:(*int)(nil) is nil?:false
o:(*string)(nil) is nil?:false
o:(*int)(nil) is nil?:false
```

为什么 `interface` 明明都是 `nil` ,但是最后四个的判断却是为 `false` 呢？

因为 `interface` 实际包含两个值，type 和 value；需要 type 和 value 都为 `nil` 才会与 `nil` 相等。

![](https://windard-blog.oss-cn-beijing.aliyuncs.com/XABsreOgH0.png)

注意，这里的 `interface` 只代表 `interface` 类型，也就是说其他的指针类型判断还是只校验 `nil`，当 `interface` 的指针校验就要判断 type 和 value 。

所以当对于 `interface` 的指针空值判断的时候，我们只需要使用反射取到其值的内容，然后判断是否为 `nil` 就可以了。

```golang
package main

import (
	"fmt"
	"reflect"
)


func isNil(o interface{}) bool {
	vi := reflect.ValueOf(o)
	if vi.Kind() == reflect.Ptr {
		fmt.Printf("vi kind is pointer\n")
		return vi.IsNil()
	}
	return false
}

func main() {
	var o interface{}
	var op *interface{}
	var i *int
	var j *int
	var s *string
	fmt.Printf("o:%#v is nil?:%#v\n", o, isNil(o))
	fmt.Printf("op:%#v is nil?:%#v\n", op, isNil(op))
	fmt.Printf("i:%#v is nil?:%#v\n", i, isNil(i))
	fmt.Printf("j:%#v is nil?:%#v\n", j, isNil(j))
	fmt.Printf("s:%#v is nil?:%#v\n", s, isNil(s))
	i = j
	fmt.Printf("i:%#v is nil?:%#v\n", i, isNil(i))

	o = op
	fmt.Printf("o:%#v is nil?:%#v\n", o, isNil(o))
	o = i
	fmt.Printf("o:%#v is nil?:%#v\n", o, isNil(o))
	o = s
	fmt.Printf("o:%#v is nil?:%#v\n", o, isNil(o))
	o = (*int)(nil)
	fmt.Printf("o:%#v is nil?:%#v\n", o, isNil(o))

	var tempList []interface{}
	var tempMap map[interface{}]interface{}

	fmt.Printf("tempList:%#v is nil?:%#v\n", tempList, isNil(tempList))
	fmt.Printf("tempMap:%#v is nil?:%#v\n", tempMap, isNil(tempMap))
	fmt.Printf("tempList:%#v is nil?:%#v\n", tempList, tempList == nil)
	fmt.Printf("tempMap:%#v is nil?:%#v\n", tempMap, tempMap == nil)

	var tempListPointer *[]interface{}
	var tempMapPointer *map[interface{}]interface{}

	fmt.Printf("tempListPointer:%#v is nil?:%#v\n", tempListPointer, isNil(tempListPointer))
	fmt.Printf("tempMapPointer:%#v is nil?:%#v\n", tempMapPointer, isNil(tempMapPointer))

}

```

结果是

```
o:<nil> is nil?:false
vi kind is pointer
op:(*interface {})(nil) is nil?:true
vi kind is pointer
i:(*int)(nil) is nil?:true
vi kind is pointer
j:(*int)(nil) is nil?:true
vi kind is pointer
s:(*string)(nil) is nil?:true
vi kind is pointer
i:(*int)(nil) is nil?:true
vi kind is pointer
o:(*interface {})(nil) is nil?:true
vi kind is pointer
o:(*int)(nil) is nil?:true
vi kind is pointer
o:(*string)(nil) is nil?:true
vi kind is pointer
o:(*int)(nil) is nil?:true
tempList:[]interface {}(nil) is nil?:false
tempMap:map[interface {}]interface {}(nil) is nil?:false
tempList:[]interface {}(nil) is nil?:true
tempMap:map[interface {}]interface {}(nil) is nil?:true
vi kind is pointer
tempListPointer:(*[]interface {})(nil) is nil?:true
vi kind is pointer
tempMapPointer:(*map[interface {}]interface {})(nil) is nil?:true
```

对于指针类型的判 `nil` 是准确的，但是对于值的判断有问题。

那我们对于判断 `empty` 和判断 `nil` 的两种判空场景都可以实现了，如何判断一个对象是指针还是值呢？
> 😂，这个不太好判断

不过我们可以根据 `reflect` 库中的 `IsZero` 方法进行一个差不多的预判

```golang
package main

import (
	"fmt"
	"reflect"
)

func isNilOrEmpty(o interface{}) bool {
	vi := reflect.ValueOf(o)
	// 对 interface 的特例
	if o == nil {
		return true
	}
	return vi.IsZero()
}

func main() {
	mess := []interface{}{0, 1, 2, "", "hello", map[string]string{}, []int{}, []interface{}{}}
	for _, m := range mess {
		fmt.Printf("%#v is empty:%+v, is nil:%+v\n", m, isNilOrEmpty(m), m == nil)
	}

	var o interface{}
	var op *interface{}
	var i *int
	var j *int
	var s *string
	//fmt.Printf("o:%#v is nil?:%#v\n", o, isNilOrEmpty(o))
	fmt.Printf("op:%#v is nil?:%#v\n", op, isNilOrEmpty(op))
	fmt.Printf("i:%#v is nil?:%#v\n", i, isNilOrEmpty(i))
	fmt.Printf("j:%#v is nil?:%#v\n", j, isNilOrEmpty(j))
	fmt.Printf("s:%#v is nil?:%#v\n", s, isNilOrEmpty(s))
	i = j
	fmt.Printf("i:%#v is nil?:%#v\n", i, isNilOrEmpty(i))

	o = op
	fmt.Printf("o:%#v is nil?:%#v\n", o, isNilOrEmpty(o))
	o = i
	fmt.Printf("o:%#v is nil?:%#v\n", o, isNilOrEmpty(o))
	o = s
	fmt.Printf("o:%#v is nil?:%#v\n", o, isNilOrEmpty(o))
	o = (*int)(nil)
	fmt.Printf("o:%#v is nil?:%#v\n", o, isNilOrEmpty(o))

	var tempList []interface{}
	var tempMap map[interface{}]interface{}

	fmt.Printf("tempList:%#v is nil?:%#v\n", tempList, isNilOrEmpty(tempList))
	fmt.Printf("tempMap:%#v is nil?:%#v\n", tempMap, isNilOrEmpty(tempMap))

	fmt.Printf("tempList:%#v is nil?:%#v\n", tempList, tempList == nil)
	fmt.Printf("tempMap:%#v is nil?:%#v\n", tempMap, tempMap == nil)

	var tempListPointer *[]interface{}
	var tempMapPointer *map[interface{}]interface{}

	fmt.Printf("tempListPointer:%#v is nil?:%#v\n", tempListPointer, isNilOrEmpty(tempListPointer))
	fmt.Printf("tempMapPointer:%#v is nil?:%#v\n", tempMapPointer, isNilOrEmpty(tempMapPointer))

}

```

其实有几点需要注意
1. `list` 和 `map` 初始化其实都是 `nil`, 但是 `list` 会自动扩容，`map` 不会。
2. `list` 和 `map` 在外面都是 `nil` 但是传入函数判断时就变成不是 `nil` 了。
3. 所有的 `nil` 对象都不能被取类型 `reflect.TypeOf`
4. `interface` 的 `nil` 在取值 `reflect.ValueOf` 得到的结果类型 `Kind` 是 `Invalid` ，不能判断零值。

真的是，不能深究，深究就有点乱。只需要记住两点
1. `nil` 不一定是 `nil`, 如果是有类型的 `nil` 不能直接用等号判断, 为什么会出现有类型的 `nil` ,就是因为将一个指针的 `nil` 传给了 `interface` 
2. `interface` 比较特殊有类型和值，如果值是指针的话，那就直接判断指针为 `nil` 就可以了。

## 参考链接
[Go 面试题：Go interface 的一个 “坑” 及原理分析](https://mp.weixin.qq.com/s/vNACbdSDxC9S0LOAr7ngLQ)            

