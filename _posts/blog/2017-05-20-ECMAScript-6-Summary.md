---
layout: post
title: 学习了一下 ECMAScript 6，总结笔记
description: 古语有云，士别三日当刮目相待。JavaScript 已经不再是当年那个 JavaScript 了。
category: blog
---

## 神奇的 ES6

总结自 infoQ [深入浅出 ES6](http://www.infoq.com/cn/es6-in-depth/)

### ECMAScript 6， Amazing ！

### 遍历数组

以前你可能会这样

    for (var index = 0; index < myArray.length; index++) {
      console.log(myArray[index]);
    }

或者是这样，只能遍历对象

    for (var index in myArray) { // 千万别这样做
        console.log(myArray[index]);
    }

在 ES 5 中还可以这样，不能 break 和 continue

    myArray.forEach(function (value) {
        console.log(value);
    });

现在你可以这样了，简直完美

    for (var value of myArray) {
        console.log(value);
    }

### 生成器

在 JavaScript 中也有 yield 关键字了，使用和 Python 一致，还能通过 yield 从函数外向函数内传值。

    function* quips(name) {
        yield "你好 " + name + "!";
        yield "希望你能喜欢这篇介绍ES6的译文";
        if (name.startsWith("X")) {
            yield "你的名字 " + name + "  首字母是X，这很酷！";
        }
        yield "我们下次再见！";
    }

然后使用 next 函数获得输出

    class RangeIterator {
        constructor(start, stop) {
            this.value = start;
            this.stop = stop;
        }

        [Symbol.iterator]() { return this; }

        next() {
            var value = this.value;
            if (value < this.stop) {
                this.value++;
                return {done: false, value: value};
            } else {
                return {done: true, value: undefined};
            }
        }
    }

    // 返回一个新的迭代器，可以从start到stop计数。
    function range(start, stop) {
        return new RangeIterator(start, stop);
    }

感觉已经跟 Python 很相似了，以上可以写成如下形式，效果一致。

> 不知道 JavaScript 什么时候已经加入了 class 和 constructor

    function* range(start, stop) {
        for (var i = start; i < stop; i++)
            yield i;
    }

### 模板字符串

> 不知道什么时候 JavaScript 还能抛出异常和捕捉异常

    function authorize(user, action) {
        if (!user.hasPrivilege(action)) {
            throw new Error(
                `用户 ${user.name} 未被授权执行 ${action} 操作。`
            );
        }
    }

字符串终于能够跨行了

    $("#warning").html(`
        <h1>小心！>/h1>
        <p>未经授权打冰球可能受罚
        将近${maxPenalty}分钟。</p>
    `);

一般的字符串拼接都会太安全，比如 XSS 什么的，可以使用过滤器。

    function SaferHTML(templateData) {
        var s = templateData[0];
        for (var i = 1; i < arguments.length; i++) {
            var arg = String(arguments[i]);

            // 转义占位符中的特殊字符。
            s += arg.replace(/&/g, "&")
                    .replace(/</g, "<")
                    .replace(/</g, ">");

            // 不转义模板中的特殊字符。
            s += templateData[i];
        }
        return s;
    }

    function greet(name) {
        console.log(SaferHTML`you name ${name} is beautifule`)
    }

在 markdown 中也要使用 反斜杠 来表示引用，所以那就只能使用``双反斜杠``了

    To display a message, write ``alert(`hello world!`)``.

### 不定参数和默认参数

实现一个检测一个字符串中是否包含其他若干个字符串的函数可以这样写

> 不知道 JavaScript 中什么时候还有了一个 arguments 的内建对象，包含所有的参数

    function containsAll(haystack) {
        for (var i = 1; i < arguments.length; i++) {
            var needle = arguments[i];
            if (haystack.indexOf(needle) === -1) {
                return false;
            }
        }
        return true;
    }

    containsAll("banana", "b", "nan") // true
    containsAll("banana", "c", "nan") // false

现在可以使用不定长参数

    function containsAll(haystack, ...needles) {
        for (var needle of needles) {
            if (haystack.indexOf(needle) === -1) {
                return false;
            }
        }
        return true;
    }

现在也可以设置默认参数了

    function animalSentence(animals2="tigers", animals3="bears") {
        return `Lions and ${animals2} and ${animals3}! Oh my!`;
    }

    animalSentence();                       // Lions and tigers and bears! Oh my!
    animalSentence("elephants");            // Lions and elephants and bears! Oh my!
    animalSentence("elephants", "whales");  // Lions and elephants and whales! Oh my!

甚至可以一边设置，一边使用

    function animalSentenceFancy(animals2="tigers",
        animals3=(animals2 == "bears") ? "sealions" : "bears")
    {
        return `Lions and ${animals2} and ${animals3}! Oh my!`;
    }

### 解构赋值

以前你是这样赋值的

    var first = someArray[0];
    var second = someArray[1];
    var third = someArray[2];

现在可以这样的了

    var [first, second, third] = someArray;

震惊不震惊，意外不意外？虽然 Python 中早就可以了，所以 JavaScript 也就可以直接交换赋值。

    [a, b] = [b, a]

解构赋值还能在对象中解构

    var robotA = { name: "Bender" };
    var robotB = { name: "Flexo" };
    var { name: nameA } = robotA;
    var { name: nameB } = robotB;
    console.log(nameA);
    // "Bender"
    console.log(nameB);
    // "Flexo"

甚至这样解构

    var { foo, bar } = { foo: "lorem", bar: "ipsum" };
    console.log(foo);
    // "lorem"
    console.log(bar);
    // "ipsum"

还能深入嵌套解构

    var complicatedObj = {
      arrayProp: [
        "Zapp",
        { second: "Brannigan" }
      ]
    };
    var { arrayProp: [first, { second }] } = complicatedObj;
    console.log(first);
    // "Zapp"
    console.log(second);
    // "Brannigan"

最后，在解构函数中也可以使用默认值

    var [missing = true] = [];
    console.log(missing);
    // true
    var { message: msg = "Something went wrong" } = {};
    console.log(msg);
    // "Something went wrong"
    var { x = 3 } = {};
    console.log(x);
    // 3

所以在函数返回时也可以使用解构函数

    function returnMultipleValues() {
      return [1, 2];
    }
    var [foo, bar] = returnMultipleValues();

或者是返回对象

    function returnMultipleValues() {
      return {
        foo: 1,
        bar: 2
      };
    }
    var { foo, bar } = returnMultipleValues();

### 箭头函数

单箭头函数 趋向于操作符

    function countdown(n) {
      while (n --> 0)  // "n goes to zero"
        alert(n);
      blastoff();
    }

等号箭头函数 匿名函数

    // 六种语言中的简单函数示例
    function (a) { return a > 0; } // JS
    [](int a) { return a > 0; }  // C++
    (lambda (a) (> a 0))  ;; Lisp
    lambda a: a > 0  # Python
    a => a > 0  // C#
    a -> a > 0  // Java

JavaScript 选择了 C# 的道路，如这样

    // ES5
    var selected = allJobs.filter(function (job) {
      return job.isSelected();
    });
    // ES6
    var selected = allJobs.filter(job => job.isSelected());

或者这样

    // ES5
    var total = values.reduce(function (a, b) {
      return a + b;
    }, 0);
    // ES6
    var total = values.reduce((a, b) => a + b, 0);

还能这样

    // ES5
    $("#confetti-btn").click(function (event) {
        playTrumpet();
        fireConfettiCannon();
    });
    // ES6
    $("#confetti-btn").click(event => {
        playTrumpet();
        fireConfettiCannon();
    });

### Symbol

Symbol 的含义是符号或图标，不过你肯定知道，它不是这个意思。或者唯一性标志，更符合它的定义。

它是 JavaScript 中的第七种类型，前六种是

- 未定义 Undefined
- 空     Null
- 布尔值 Boolean
- 数字   Number
- 字符串 String
- 对象   Object

珍贵的第七种 JavaScript 数据类型的功能就是为了唯一性标志，保证不会冲突重复。

    var mySymbol = Symbol();
    obj[mySymbol] = "ok!";  // 保证不会冲突
    console.log(obj[mySymbol]);  // ok!

Symbol 被创建后就不可更改，也不能设置属性，不能与其他类型连接。

    > typeof Symbol()
    "symbol"
    > var sym = Symbol("<3");
    > "your symbol is " + sym
    // TypeError: can't convert symbol to string
    > `your symbol is ${sym}`
    // TypeError: can't convert symbol to string

### Babel

将 ES6 的新语法，JSX 的新语法 转译老浏览器能够支持的老式 JavaScript 语法。

    npm install -g babel
    babel src --out-dir build

### 集合

JavaScript 中已经数组和对象。数组不是对象。

    // This is Array
    > new Array(1,2,3)
    (3) [1, 2, 3]
    > ['1', '2', '3']
    (3) ["1", "2", "3"]

    // This is Object
    > a = {name:'windard', year:12}
    Object {name: "windard", year: 12}
    > a
    Object {name: "windard", year: 12}
    > a.name
    "windard"
    > a['name']
    "windard"

现在还有 Set (集合), Map (字典),  WeakSet, WeakMap.

集合中无重复元素，无索引，其他的与数组基本一致。

    > var s = new Set([1,2,3,4])
    > s.add(1)
    Set(4) {1, 2, 3, 4}
    > s.size
    4
    > s.has(3)
    true
    > s.delete(4)
    > s.keys()
    SetIterator {1, 2, 3}
    > s.values()
    SetIterator {1, 2, 3}
    > s.forEach(item => {console.log(item)})
    1
    2
    3
    > s.clear()
    Set(0) {}

> 哇，现在的 JavaScript 数据已经有 `Array.map()`, `Array.filter()`, `Array.some()`, `Array.every()` 函数。

字典不能直接设置获取值，只能通过 set 或 get 函数进行设置获取值。

    > d = new Map([['name','windard'],['year',23]])
    Map(2) {"name" => "windard", "year" => 23}
    > d.size
    2
    > d.has('year')
    true
    > d.get('year')
    23
    > d.set('location','shannxi')
    Map(3) {"name" => "windard", "year" => 23, "location" => "shannxi"}
    > d.keys()
    MapIterator {"name", "year", "location"}
    > d.values()
    MapIterator {"windard", 23, "shannxi"}
    > d.delete('name')
    // Map(2) {"year" => 23, "location" => "shannxi"}
    > d.clear()
    // Map(0) {}

> 可惜了，没有默认字典

WeakSet 与 Set ， WeakMap 与 Map 基本一致，某些特性不再具备。

### Generators

再谈生成器，再怎么谈，也是和 Python 越来越像。

    function* somewords() {
      yield "hello";
      yield "world";
    }
    for (var word of somewords()) {
      alert(word);
    }

使用 next 函数从上次停止的地方继续，直至返回 `{value: undefined, done: true}`

两个生成器可以重叠

    function* concat(iter1, iter2) {
        for (var value of iter1) {
            yield value;
        }
        for (var value of iter2) {
            yield value;
        }
    }

可以写成这样

    function* concat(iter1, iter2) {
        yield* iter1;
        yield* iter2;
    }

### 代理

Proxy 相当于为 对象 (Object) 引入了虚拟化支持。

对象是什么？对象是属性的集合。对象有属性，对象有原型。

代理接收两个参数，目标对象 和 句柄对象。代理可以将所有的内部方法转发至目标，简单的说就是调用代理的方法，即调用对象的方法。

    var target = {}, handler = {};
    var proxy = new Proxy(target, handler);
    proxy.color = "pink";
    > target.color
        "pink"

默认的代理的 set 方法和 get 方法是这样的

    var obj = new Proxy({}, {
        get: function (target, key, receiver) {
            console.log(`getting ${key}!`);
            return Reflect.get(target, key, receiver);
        },
        set: function (target, key, value, receiver) {
            console.log(`setting ${key}!`);
            return Reflect.set(target, key, value, receiver);
        }
    });

设置的时候使用 set 方法，获取的时候使用 get 方法。

    > obj.count = 1;
        setting count!
    > ++obj.count;
        getting count!
        setting count!
        2

使用代理句柄可以覆盖对象的内部方法。

    var target = {};
    var handler = {
        set: function (target, key, value, receiver) {
            throw new Error("请不要为这个对象设置属性。");
        }
    };
    var proxy = new Proxy(target, handler);
    > proxy.name = "angelina";
        Error: 请不要为这个对象设置属性。

使用代理实现自动填充

    function Tree() {
        return new Proxy({}, handler);
    }
    var handler = {
        get: function (target, key, receiver) {
            if (!(key in target)) {
                target[key] = Tree();  // 自动创建一个子树
            }
            return Reflect.get(target, key, receiver);
        }
    };

就是这样，效果比较像 Python 中的默认字典，自动嵌套赋值。

    > var tree = Tree();
    > tree
        { }
    > tree.branch1.branch2.twig = "green";
    > tree
        { branch1: { branch2: { twig: "green" } } }
    > tree.branch1.branch3.twig = "yellow";
        { branch1: { branch2: { twig: "green" },
                     branch3: { twig: "yellow" }}}

使用代理实现只读视图

    function NOPE() {
        throw new Error("can't modify read-only view");
    }
    var handler = {
        // 覆写所有五种可变方法。
        set: NOPE,
        defineProperty: NOPE,
        deleteProperty: NOPE,
        preventExtensions: NOPE,
        setPrototypeOf: NOPE,
        // 在只读视图中包裹其它结果。
        get: function (target, key, receiver) {
            // 从执行默认行为开始。
            var result = Reflect.get(target, key, receiver);
            // 确保返回一个不可变对象！
            if (Object(result) === result) {
                // result是一个对象。
                return readOnlyView(result);
            }
            // result是一个原始原始类型，所以已经具备不可变的性质。
            return result;
        },
    };
    function readOnlyView(target) {
        return new Proxy(target, handler);
    }

只读对象，不可设置。

    > var newMath = readOnlyView(Math);
    > newMath.min(54, 40);
        40
    > newMath.max = Math.min;
        Error: can't modify read-only view
    > delete newMath.sin;
        Error: can't modify read-only view

代理在一定程度上类似于子类的方法重载，使用一个代理钩子来改变父类方法。

### 类

在 JavaScript 中是有类的，虽然以前它的写法繁琐晦涩，这是一个 Circle 类。

    function Circle(radius) {
        this.radius = radius;
        Circle.circlesMade++;
    }
    Circle.draw = function draw(circle, canvas) { /* Canvas绘制代码 */ }
    Object.defineProperty(Circle, "circlesMade", {
        get: function() {
            return !this._count ? 0 : this._count;
        },
        set: function(val) {
            this._count = val;
        }
    });
    Circle.prototype = {
        area: function area() {
            return Math.pow(this.radius, 2) * Math.PI;
        }
    };
    Object.defineProperty(Circle.prototype, "radius", {
        get: function() {
            return this._radius;
        },
        set: function(radius) {
            if (!Number.isInteger(radius))
                throw new Error("圆的半径必须为整数。");
            this._radius = radius;
        }
    });

类的类属性和实例属性都需通过 `Object.defineProperty()` 来定义，类的方法通过 `Circle.prototype()` 来定义。

或者稍微简化一点点

    function Circle(radius) {
        this.radius = radius;
        Circle.circlesMade++;
    }
    Circle.draw = function draw(circle, canvas) { /* Canvas绘制代码 */ }
    Object.defineProperty(Circle, "circlesMade", {
        get: function() {
            return !this._count ? 0 : this._count;
        },
        set: function(val) {
            this._count = val;
        }
    });
    Circle.prototype = {
        area() {
            return Math.pow(this.radius, 2) * Math.PI;
        },
        get radius() {
            return this._radius;
        },
        set radius(radius) {
            if (!Number.isInteger(radius))
                throw new Error("圆的半径必须为整数。");
            this._radius = radius;
        }
    };

感觉区别不大，还是比较复杂。

    class Circle {
        constructor(radius) {
            this.radius = radius;
            Circle.circlesMade++;
        };
        static draw(circle, canvas) {
            // Canvas绘制代码
        };
        static get circlesMade() {
            return !this._count ? 0 : this._count;
        };
        static set circlesMade(val) {
            this._count = val;
        };
        area() {
            return Math.pow(this.radius, 2) * Math.PI;
        };
        get radius() {
            return this._radius;
        };
        set radius(radius) {
            if (!Number.isInteger(radius))
                throw new Error("圆的半径必须为整数。");
            this._radius = radius;
        };
    }

这样子看上去才是真正的函数，连静态方法，魔术方法都有了，还有私有变量和类变量。

在使用时，类的成员一定要在花括号中，花括号表示类的构造器和类方法和类属性。

### 变量定义

JavaScript 是动态脚本语言，可以先定义变量再使用，也可以直接使用。但是有一个问题就是如果使用 `var` 定义变量的话，变量的作用域是全局变量，如果不预定义变量的话，变量的作用域是局部的。

还有就是 JavaScript 的变量作用域一直有问题，虽然我也不太清楚问题出在哪里，但是需要使用大量的闭包和匿名函数和自启动函数来保证完成。

ES 6 中提供了一个新的变量定义关键字 `let` , let 是更完美的 var。

ES 6 中还提供了一个变量定义关键字 `const` , 定义静态变量，定义之后不可改变，其他与 let 一致。

### 子类

在 ES6 中有了 类的概念之后，接下来就是子类了。

继承父类使用关键字 extends ， 调用父类的方式使用关键字 super 。

    class Shape {
        constructor(color) {
            this._color = color;
        }
    }
    class Circle extends Shape {
        constructor(color, radius) {
            super(color);
            this.radius = radius;
        }
        // 与上文中代码相同
    }

### 模块

模块系统，提供相互调用。 export 提供引用， import 使用引用。

    // kittydar.js - 找到一幅图像中所有猫的位置
    // （事实上是Heather Arthur写的这个库）
    // （但是她没有使用ES6中新的模块特性，因为那时候是2013年）
    export function detectCats(canvas, options) {
        var kittydar = new Kittydar(options);
        return kittydar.detectCats(canvas);
    }
    export class Kittydar {
        ... 处理图片的几种方法 ...
    }
    // 这个helper函数没有被export。
    function resizeCanvas() {
        ...
    }
    ...

上文提供引用，下文使用引用

    // demo.js - Kittydar的demo程序
    import {detectCats} from "kittydar.js";
    function go() {
        var canvas = document.getElementById("catpix");
        var cats = detectCats(canvas);
        drawRectangles(canvas, cats);
    }

在提供引用的时候，只需写出提供引用的引用列表即可。提供引用也可以放在文末。

    export {detectCats, Kittydar};
    // 此处不需要 `export`关键字
    function detectCats(canvas, options) { ... }
    class Kittydar { ... }

使用引用时可以对引用模块进行重命名

    // suburbia.js
    // 这两个模块都会导出以`flip`命名的东西。
    // 要同时导入两者，我们至少要将其中一个的名称改掉。
    import {flip as flipOmelet} from "eggs.js";
    import {flip as flipHouse} from "real-estate.js";
    ...

在提供引用的时候也可以重命名

    // unlicensed_nuclear_accelerator.js - 无DRM（数字版权管理）的媒体流
    // （这不是一个真实存在的库，但是或许它应该被做成一个库）

    function v1() { ... }
    function v2() { ... }

    export {
        v1 as streamV1,
        v2 as streamV2,
        v2 as streamLatestVersion
    };

还有默认引用和全部引用，不再详叙，如果在引用时没有使用花括号，则为默认引用。

### 还有什么

Reflect, Promise, Decorator, async, await 等。。。

可以看一下 [ES6 全套教程 ECMAScript6 (原著:阮一峰)](http://jsrun.net/tutorial/cZKKp)
