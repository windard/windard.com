---
layout: post
title: Shell Tips
category: project
description: 随着 shell 用的越来越多，一些小的技巧，可以记录下来
---

## 参数列表

其实也写在 [gist](https://gist.github.com/windard/3c9bb3e0b88903b61d48feb068c07e30) 里了。

```bash
#!/bin/bash
#
msg1='$'
echo "Shell本身的PID（ProcessID）"
printf "The ${msg1}$ is %s\n" "$$"

echo "Shell最后运行的后台Process的PID"
printf "The ${msg1}! is %s\n" "$!"

echo "最后运行的命令的结束代码（返回值）"
printf "The ${msg1}? is %s\n" "$?"

echo "使用Set命令设定的Flag一览 "
printf "The ${msg1}- is %s\n" "$-"

echo

echo "参数相关，直接运行脚本 ./args.sh 或者 sh args.sh 结果一致"
echo '所有参数列表。如"$*"用「"」括起来的情况、以"$1 $2 … $n"的形式输出所有参数。 '
printf "The ${msg1}* is %s\n" "$*"

echo '所有参数列表。如"$@"用「"」括起来的情况、以"$1" "$2" … "$n" 的形式输出所有参数。'
printf "The ${msg1}@ is %s\n" "$@"

echo "添加到Shell的参数个数 "
printf "The ${msg1}# is %s\n" "$#"

echo "Shell本身的文件名 "
printf "The ${msg1}0 is %s\n" "$0"

echo "shell 第一个参数"
printf "The ${msg1}1 is %s\n" "$1"

echo "shell 第二个参数"
printf "The ${msg1}2 is %s\n" "$2"
```

运行结果

```
$ sh args.sh 1243 245451 46252323
Shell本身的PID（ProcessID）
The $$ is 14841
Shell最后运行的后台Process的PID
The $! is
最后运行的命令的结束代码（返回值）
The $? is 0
使用Set命令设定的Flag一览
The $- is hB

参数相关，直接运行脚本 ./args.sh 或者 sh args.sh 结果一致
所有参数列表。如"$*"用「"」括起来的情况、以"$1 $2 … $n"的形式输出所有参数。
The $* is 1243 245451 46252323
所有参数列表。如"$@"用「"」括起来的情况、以"$1" "$2" … "$n" 的形式输出所有参数。
The $@ is 1243
The $@ is 245451
The $@ is 46252323
添加到Shell的参数个数
The $# is 3
Shell本身的文件名
The $0 is args.sh
shell 第一个参数
The $1 is 1243
shell 第二个参数
The $2 is 245451
(byted)  $
(byted)  $
(byted)  $
(byted)  $ ./args.sh 123 134341ascsd 434523
Shell本身的PID（ProcessID）
The $$ is 14902
Shell最后运行的后台Process的PID
The $! is
最后运行的命令的结束代码（返回值）
The $? is 0
使用Set命令设定的Flag一览
The $- is hB

参数相关，直接运行脚本 ./args.sh 或者 sh args.sh 结果一致
所有参数列表。如"$*"用「"」括起来的情况、以"$1 $2 … $n"的形式输出所有参数。
The $* is 123 134341ascsd 434523
所有参数列表。如"$@"用「"」括起来的情况、以"$1" "$2" … "$n" 的形式输出所有参数。
The $@ is 123
The $@ is 134341ascsd
The $@ is 434523
添加到Shell的参数个数
The $# is 3
Shell本身的文件名
The $0 is ./args.sh
shell 第一个参数
The $1 is 123
shell 第二个参数
The $2 is 134341ascsd
```

## 上一个命令的返回码

```
$ echo $?
0
```

## 返回比较

gofmt 在使用时，对于存在需要 format 的 go 文件，返回错误码非零，需要做一个比较

```bash
test -z $(gofmt -s -l .)
```

## 时间戳转换

```
$ date +%s
1602342382
$ date -d @1602342382
Sat Oct 10 23:06:22 CST 2020
```

## Git Hash
Git 到目前为止，还是使用的 sha1 的哈希算法。所以在 Git 中的 commit, tree, blob 等所有用到哈希的地方，我们都可以尝试自己手动计算下。😝
> shell 中的 sha1 计算可以用 `shasum` 或者 `sha1sum`

- commit: 很简单，就是一次提交，就是一个 commit
- tree: 是一个文件夹
- blog: 即纯文件，包括文本文件和二进制文件

### commit

首先以 commit 为例 `git show` 查看最新的 commit 为 `9c1c73388c3e36c26acd1abfd30e3ec089396fd7`

查看下这个 commit 的信息

```
# 查看哈希类型
$ git cat-file -t 9c1c73388c3e36c26acd1abfd30e3ec089396fd7
commit
# 查看哈希大小
$ git cat-file -s 9c1c73388c3e36c26acd1abfd30e3ec089396fd7
710
# 查看哈希内容
$ git cat-file -p 9c1c73388c3e36c26acd1abfd30e3ec089396fd7
tree 425b33f1db8ee8ff9e0cbf85768167cac2bee694
parent b6b0982f634422905d295222a792b86ee7517323
author windard <windard@qq.com> 1602247223 +0800
committer windard <windard@qq.com> 1602247324 +0800
gpgsig -----BEGIN PGP SIGNATURE-----

 iQEzBAABCAAdFiEEQVM4nF5fpfq6j9nIPe0hn1v2TckFAl+AWpwACgkQPe0hn1v2
 TckTBwf/eNziydtDx7sV7q+ir6P5t/+Tlyswue97ybmiifFXB8vKK49Yk0EnA7UY
 xgy4UqfqQFDfWTU1Y+od56Hbec37oB3dBDgGHDAoZ3WzQHfW/Pesu1Nz42Q6Rkep
 5P4cspoNByxg3husdMlqcM4ldW9oi98DF7yQBkMy0gHBUxQ5hO3IqvNpiqxgBkzY
 5/c+Xvu9G4MjjUXUkmTixMxKYdHsq3onQjuG+rO/1ifLgx1kjlRwRPjMXpmfUy9c
 0kwcnhPtnyinUAWcPcW0DgmG6qtmBk36RpMAyMyV0ZSFHTiAbGYrQpiia6Gs2kK+
 D0+hE5Sb/jrX1zfVBI7KbF101ttlNw==
 =x4wX
 -----END PGP SIGNATURE-----

two blog
# 指定 commit 类型查看
$ git cat-file commit 9c1c73388c3e36c26acd1abfd30e3ec089396fd7
tree 425b33f1db8ee8ff9e0cbf85768167cac2bee694
parent b6b0982f634422905d295222a792b86ee7517323
author windard <windard@qq.com> 1602247223 +0800
committer windard <windard@qq.com> 1602247324 +0800
gpgsig -----BEGIN PGP SIGNATURE-----

 iQEzBAABCAAdFiEEQVM4nF5fpfq6j9nIPe0hn1v2TckFAl+AWpwACgkQPe0hn1v2
 TckTBwf/eNziydtDx7sV7q+ir6P5t/+Tlyswue97ybmiifFXB8vKK49Yk0EnA7UY
 xgy4UqfqQFDfWTU1Y+od56Hbec37oB3dBDgGHDAoZ3WzQHfW/Pesu1Nz42Q6Rkep
 5P4cspoNByxg3husdMlqcM4ldW9oi98DF7yQBkMy0gHBUxQ5hO3IqvNpiqxgBkzY
 5/c+Xvu9G4MjjUXUkmTixMxKYdHsq3onQjuG+rO/1ifLgx1kjlRwRPjMXpmfUy9c
 0kwcnhPtnyinUAWcPcW0DgmG6qtmBk36RpMAyMyV0ZSFHTiAbGYrQpiia6Gs2kK+
 D0+hE5Sb/jrX1zfVBI7KbF101ttlNw==
 =x4wX
 -----END PGP SIGNATURE-----

two blog

```

所以，我们可以自己计算下哈希结果是否和哈希值一致。

```
$ (printf "commit %s\0" $(git cat-file commit HEAD | wc -c); git cat-file commit HEAD) | shasum
9c1c73388c3e36c26acd1abfd30e3ec089396fd7  -
$ git cat-file commit 9c1c73388c3e36c26acd1abfd30e3ec089396fd7|git hash-object -t commit --stdin
9c1c73388c3e36c26acd1abfd30e3ec089396fd7
```

结果是一样的。

### blog

除了 commit，我们还可以查看文件的哈希值

```
$ git hash-object README.md
9c0867c1178f1e25729c7bedb1abf215343447f4
$ git cat-file -t 9c0867c1178f1e25729c7bedb1abf215343447f4
blob
$ git cat-file -s 9c0867c1178f1e25729c7bedb1abf215343447f4
280
$ git cat-file -p 9c0867c1178f1e25729c7bedb1abf215343447f4
## README

![blog status](https://img.shields.io/uptimerobot/status/m784052190-90c8437e8380f690adf3ecd6)
![blog uptime](https://img.shields.io/uptimerobot/ratio/7/m784052190-90c8437e8380f690adf3ecd6)

终究还是要有一个博客的，即使无人观赏，也要独立顽强。
```

那么文件的哈希值如何计算呢？

```
(printf "blob %s\0" $(cat README.md|wc -c); cat README.md) | shasum
```

### 规则

所以计算的内容是 `<type> <size>\0<content>` ，起码对于 commit 和 blob 都是如此，那么我们就可以通过哈希值计算哈希。

```
$ (printf "%s %s\0" $(git cat-file -t 9c0867c1178f1e25729c7bedb1abf215343447f4) $(git cat-file -s 9c0867c1178f1e25729c7bedb1abf215343447f4); git cat-file -p 9c0867c1178f1e25729c7bedb1abf215343447f4)|shasum
9c0867c1178f1e25729c7bedb1abf215343447f4  -
$ (printf "%s %s\0" $(git cat-file -t 9c0867c1178f1e25729c7bedb1abf215343447f4) $(git cat-file -s 9c0867c1178f1e25729c7bedb1abf215343447f4); git cat-file -p 9c0867c1178f1e25729c7bedb1abf215343447f4)|shasum
```

所以，我们可以从 commit 到 tree  到 blog 的根据哈希值索引查找。

```
$ git cat-file -p 9c1c73388c3e36c26acd1abfd30e3ec089396fd7
tree 425b33f1db8ee8ff9e0cbf85768167cac2bee694
parent b6b0982f634422905d295222a792b86ee7517323
author windard <windard@qq.com> 1602247223 +0800
committer windard <windard@qq.com> 1602247324 +0800
gpgsig -----BEGIN PGP SIGNATURE-----

 iQEzBAABCAAdFiEEQVM4nF5fpfq6j9nIPe0hn1v2TckFAl+AWpwACgkQPe0hn1v2
 TckTBwf/eNziydtDx7sV7q+ir6P5t/+Tlyswue97ybmiifFXB8vKK49Yk0EnA7UY
 xgy4UqfqQFDfWTU1Y+od56Hbec37oB3dBDgGHDAoZ3WzQHfW/Pesu1Nz42Q6Rkep
 5P4cspoNByxg3husdMlqcM4ldW9oi98DF7yQBkMy0gHBUxQ5hO3IqvNpiqxgBkzY
 5/c+Xvu9G4MjjUXUkmTixMxKYdHsq3onQjuG+rO/1ifLgx1kjlRwRPjMXpmfUy9c
 0kwcnhPtnyinUAWcPcW0DgmG6qtmBk36RpMAyMyV0ZSFHTiAbGYrQpiia6Gs2kK+
 D0+hE5Sb/jrX1zfVBI7KbF101ttlNw==
 =x4wX
 -----END PGP SIGNATURE-----

two blog
$ git cat-file -p b6b0982f634422905d295222a792b86ee7517323
tree c640fb453f0ca502477af2d496651c170e927994
parent 2f1b87d8129070232a4a0991f3a540625ed0287a
author windard <windard@qq.com> 1601361424 +0800
committer windard <windard@qq.com> 1602247324 +0800
gpgsig -----BEGIN PGP SIGNATURE-----

 iQEzBAABCAAdFiEEQVM4nF5fpfq6j9nIPe0hn1v2TckFAl+AWpwACgkQPe0hn1v2
 Tcn5RggAqRC/ZLkNvLdTLcNb9b1OfiAqK6n/hMaR0g3eKW1XkfxyAMQIkBb5FMFX
 abJtmNvM5zz/N9k9sPTGQtgnOfUdhjRpn2q1P86QgCxnADDLkob5W4Ahl6VftspO
 8R2kD0yo4dDH7n/Fsq+CeHCTIBMgvelBbc7TOYG5IHdDmScikexDXi0lrwgbsZXs
 CbYm1sWSVx8JCNrRdXwm9W7M7miQjxXpE0GxdGNTv1atPA8NTD9qxgoChkVBoCFA
 A8Cn1BIWVxNv1zHGFnvitogZ0p/0xlir7Ibts4ywRrBjaMzTZgTMihdrkj6sKEF9
 aCmsoQSw8D1YiBP+Dl/D46RL5lFNqA==
 =jdmW
 -----END PGP SIGNATURE-----

key and index in mysql
$ git cat-file -p c640fb453f0ca502477af2d496651c170e927994
100644 blob 47659eafe3614d58bbb82e804142478046c5b8ba	.gitignore
100644 blob 992ca1c7cc1d86e946f0c397509dcae8f589ff64	404.html
100644 blob 7fcb334d3d223246fa2f9eb29d3dc58a58c54554	CNAME
100644 blob 893a044816421a53bbbaa3d9d0e11c471d80ae97	Gemfile
100644 blob b9dc8575f24a3925341042850f0458511f2f7cdc	Gemfile.lock
100644 blob dd4226a83360b16f5eba7c2220a1ee61989ad79e	LICENSE
100644 blob 9c0867c1178f1e25729c7bedb1abf215343447f4	README.md
100644 blob ac92e8c2afbaa722f69eff32beaa46107204dc00	_config.yml
040000 tree c266b563981a2011f96ee1ac1fa1d7c71b76cd66	_layouts
040000 tree 698d701a2b332fb91add0aad9455f022abbdf936	_posts
100644 blob 70605b092ce1bd3ef8a5ec9b90f1a8b4ea105509	about.md
100644 blob 45b73ff9e98a5f8e8f569bd889089f8482bdd84f	archives.md
040000 tree 529a31a7196bb020c8fe883e2a362e5c446e1b08	css
100644 blob 6d53db0d54cc22916f5b96fd15bf444b86059cc1	favicon.ico
100644 blob a6628bd842af95a7f423155dd95510941d3a78dc	feed.xml
040000 tree cbb219d31e76d3ffb87a3217a37aafd6de701336	images
100644 blob a8eaefb67326ff20a24c560914a2846fb4b36725	index.md
040000 tree 08b7ce81b0c0cb810947c927008272686723059d	js
040000 tree da9b393e765c481c8b19f85922bd849cbc120c6b	lib
040000 tree ba3c93300b808d46404617a8668975a87dc581b9	opinion
040000 tree a0b04f81acca4c885bd25bf342cd0f81b931dedb	project
100644 blob 13710fec3959badea62bc3fee169a07543dc2dbe	robots.txt
040000 tree c9fb376184fede3b318fcf0e19418ca9c42e5af2	software
$ git cat-file -p 7fcb334d3d223246fa2f9eb29d3dc58a58c54554
windard.com
www.windard.com%                                                                                                                      $ git cat-file -p 698d701a2b332fb91add0aad9455f022abbdf936
040000 tree 88be3fea9c97e06b6f0a2c263a23534d94c2981f	blog
040000 tree be454b9a455ed4fe8b9c232ca70ae5601d7837fd	opinion
040000 tree 834c2d2102153a30c4ee2113b267be8b0541ac64	project
```

### 空树

每个 Git 仓库中都有这个神秘的 empty tree `4b825dc642cb6eb9a060e54bf8d69288fbee4904` 它是其实是一个空的内容

```
$ git cat-file -t 4b825dc642cb6eb9a060e54bf8d69288fbee4904
tree
$ git cat-file -p 4b825dc642cb6eb9a060e54bf8d69288fbee4904
$ git cat-file -s 4b825dc642cb6eb9a060e54bf8d69288fbee4904
0
$  echo -n '' | git hash-object -t tree --stdin
4b825dc642cb6eb9a060e54bf8d69288fbee4904
$ git hash-object -t tree /dev/null
4b825dc642cb6eb9a060e54bf8d69288fbee4904
$ git diff 4b825dc642cb6eb9a060e54bf8d69288fbee4904
$ git show 4b825dc642cb6eb9a060e54bf8d69288fbee4904
```

## shell 编程

### 查看 shell

```
# 查看当前使用的 shell
$ echo $SHELL
/bin/zsh
# 查看系统支持的 shell
$ cat  /etc/shells
# List of acceptable shells for chpass(1).
# Ftpd will not allow users to connect who are not using
# one of these shells.

/bin/bash
/bin/csh
/bin/dash
/bin/ksh
/bin/sh
/bin/tcsh
/bin/zsh
```

### 使用条件判断

> 一些注意点

1. `-n` 表示比较变量长度`不为零`，含义为 `not zero`
2. `-z` 表示比较变量长度`为零`, 含义为 `zero`
3. 字符串变量比较最好加引号
4. `[[]]` 与 `[]` 功能基本相同，但是 `[[]]` 的更加强大
	1. 可以多重比较,支持逻辑运算符比比较运算符
	2. 只能用于 `bash`, 不能用于 `sh`

```bash
#!/bin/bash 

echo $LOGIN

if [[ -n "$LOGIN" ]]
then
	echo "Welcome login"

	if [[ "$LOGIN" == "admin" ]]
	then
		echo "Yes, Admin"
	fi
else
	echo "Need login"
fi

```

可以这样查看效果

```
$ ./path_check.sh

Need login
$ ./path_check.sh

Need login
$ LOGIN=1 ./path_check.sh
1
Welcome login
$ LOGIN=2 ./path_check.sh
2
Welcome login
$ LOGIN=admin ./path_check.sh
admin
Welcome login
Yes, Admin
```	

### shell 脚本所在目录

如果直接使用 `.` 获取到的是运行时的当前路径，不是 shell 脚本所在文件路径。

```bash
#!/bin/bash

SHELL_FOLDER=$(cd "$(dirname "$0")";pwd)

echo $SHELL_FOLDER
cat "$SHELL_FOLDER/path_check.sh"
```

