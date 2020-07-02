---
layout: post
title: Makefile 的使用手记
description:  方便好用，简化构建，占坑预警。
category: opinion
---

## Make

make 是 Unix 上的构建工具，不是编译工具。有人看到 make 就想到了 c 项目编译。这是因为 make 是构建工具，可以指挥 gcc 来进行项目编译，自己本身并不参与。

所以 make 除了 c 项目外，在任何项目中都可以用来做 任务编排构建，类似的工具有很多，但 make 是历史最传统，应用最广泛的跨平台构建工具。

## Makefile

既然是构建工具，那么构建规则就是在 Makefile 中，先执行什么，再执行什么，都是 shell 命令，其实一条条的规则，就像一个个的 alias 缩写。


首先，规则文件命名为 `Makefile` ，一般 `makefile` 也可以，但是就不规范。然后，执行的命令 *必须* 要 Tab 开始，如果用四个空格就不行，会报错 `missing separator.  Stop.`。

```

server:
	python flasky.py

show:
	echo "hello world"

clean:
	@find . -name '*.pyc' -delete
	@echo done

```

比如一个 flask 项目中的几个常见命令。

```
$ make show
echo "hello world"
hello world
$ make clean
done
$ make server
python flasky.py
start
but long time
 * Serving Flask app "flasky" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
```


一个完整的规则分为三个部分，target ,prerequistes, command , 其中 prerequistes 和 commands 需要至少存在一个

```
<target> : <prerequisites> 
[tab]  <commands>
```

### target

执行目标，可以是一个任意的名字，或者是文件名。但是如果已经存在这个文件，则命令不会执行。

比如上面的 Makefile 中，如果当前文件夹下已经存在 `clean` 这个文件的话，执行是就会提示 `make: 'clean' is up to date.`

这时可以将其设置伪目标，表示我们其实并不是想要这个文件。


```

clean:
	@find . -name '*.pyc' -delete
	@echo done

.PHONY: clean

```

### prerequisites

如果在 make 的时候没有带具体的命令，会默认执行第一个命令。所以，我们也可以将第一个命令设置为我们想要执行的命令，如果清理并启动服务。

```

all: show clean server

server:
	python flasky.py

show:
	echo "hello world"

clean:
	@find . -name '*.pyc' -delete
	@echo done

.PHONY: clean

```

prerequisites 是命令依赖的前置条件，一般也用来连续执行多个任务。

### commands

具体执行的命令部分，必须用 Tab 开头，也可以使用 `.RECIPEPREFIX` 设置。

在 commands 可以写多条命令，但是各个命令之间并不关联，变量作用域也仅限于单条命令。

比如

```
calc:
	export a=2
	export b=1
	echo $(a):$(b)

```

的结果并不是 `2:1` 而是孤零零的 `:` ，那么如何设置作用域呢？

1. 使用反斜线将命令相连

```
calc:
	export a=2; \
	export b=1; \
	echo $$a:$$b
```

2. 设置为全局变量

```
a=1
b=2
calc:
	echo $(a):$(b)
```

3. 设置为命令变量

```
calc: a=1
calc: b=2
calc:
	echo $(a):$(b)
```

但是这种方式不能传入到具体执行的命令中

4. 设置为命令依赖的环境变量

```
calc: export a=1
calc: export b=2
calc:
	echo $(a):$(b)
```

在单个命令中
- 用 `@` 开头用来控制回显，即是否展示该条命令，还是直接执行
- 用 `#` 开头用来表示注释
- 在原来 shell 命令中需要使用 `$` 的地方，需要用两个 `$$` 来替换

在 命令中的其他规则 和 shell 一样，变量，循环都可以使用。

## 参考链接

[Make 命令教程](https://www.ruanyifeng.com/blog/2015/02/make.html) <br>
[跟我一起写Makefile](https://seisman.github.io/how-to-write-makefile/overview.html) <br>
[Bash 脚本教程](https://wangdoc.com/bash/)
