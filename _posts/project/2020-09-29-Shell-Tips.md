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

