---
layout: post
title: Linux 下 shell 命令的应用
description: 学习使用一些 Linux 高级命令。
category: opinion
---

## Linux 高级命令

### cat

`cat [option] [file]` 查看文件内容，如果没有 file，则从屏幕输入。

- `-E` : 在每一行结尾加上 `$`
- `-T` : 使用 `^T` 代替 Tab
- `-v` : 使用 `^M` 代替 Windows 行结束符 (\r\n)
- `-e` : 相当于 `-vE`
- `-A` : 查看全部文件内容，相当于 `-vET`
- `-t` : 相当于 `-vT`
- `-n` : 输出行号，包括空行
- `-b` : 输出行号，不包括空行

常用命令 `cat <filename>` , `cat -n <filename>|tail -n1`, `cat prefix* >all`, `cat last>>first`

### tail

`tail [option] [file]` 打印文件倒数十行，如果没有 file，则从屏幕输入。

- `-n` : 输出倒数 n 行
- `-f` : 监视文件修改

常用命令 `tail -n100 <filename>`, `tail -f <filename>`

### head

`tail [option] [file]` 打印文件前十行，如果没有 file，则从屏幕输入

- `-n` : 输出前 n 行
- `-c` : 输出前 c 个字节

常用命令 `head <filename>`

### grep

`grep [option] pattern [file]` 正则匹配查找，查找所有行使用`''` 而不是 `*`

- `-P` : 使用 Perl 语法正则表达式
- `-i` : 忽略大小写
- `-A` : 找到匹配之后，多输出匹配下 n 行
- `-n` : 找到匹配之后，输出匹配所在行数，使用 `-n5` 的话输出上下 5 行
- `-v` : 找到不匹配的值

常用命令 `ls -al|grep -i <name>`, `grep -P '^[\d]{3} [\w]{3} [\w]{5}' data.txt`, `grep <data> * -r`, `find $PWD -name "*.py"|grep -v ".venv"`

### find

`find` 默认打印当前路径下的所有文件和文件夹

- `-name `  : 匹配文件名
- `-type`   : 匹配文件夹 `-type f` 即为 file 文件，`-type d` 即为 dir 文件夹
- `-user `  : 匹配用户
- `-ls`     : 对搜索结果使用 `ls` 显示
- `"regex"` : 使用引号匹配正则表达式
- `-exec`: 对匹配的内容做 shell 命令
- `-delete`: 删除匹配到的内容

常用命令 `find |grep <name>`, `find / -name <name>`, `find -user <user>`, `find -type f|wc`, `find ./ -name "*.md" |xargs cat|wc` 或者 `find . -name "*.md" -exec cat {} +|wc`

### wc

`wc [option] [file]` 计算文件行数

- `-l` : 计算行数
- `-c` : 计算 bytes
- `-m` : 计算单词数

常用命令 `ls -al|wc`, `cat <name>|wc`

### awk

`awk [-F  field-separator]  'commands'  input-file(s)` 强大的文本分析工具

- `-F ` : 修改分割符，默认分割符为空格或者 Tab
- `$0`  : 所有域，类似的 `$1` 第一个域
- `-f`  : 使用文件中的 awk 命令

常用命令

- 显示系统账户 `cat /etc/passwd |awk  -F ':'  '{print $1}' `
- 显示 root 账户内容 `awk -F: '/^root/{print $0}' /etc/passwd`
- 显示系统账户和其使用的 shell，账户与 shell 之间使用 Tab 分割 `cat /etc/passwd |awk  -F ':'  '{print $1"\t"$7}'`
- 显示系统账户和其使用的 shell，账户与 shell 之间使用 逗号 分割，在输出前加上标题，在输出后加上结束 `cat /etc/passwd |awk  -F ':'  'BEGIN {print "name, shell"}  {print $1", "$7} END {print "end ..."}'`
- 显示系统账户和其序号 `awk -F ':' 'BEGIN {count=0;} {name[count] = $1;count++;}; END{for (i = 0; i < NR; i++) print i, name[i]}' /etc/passwd`

- 查看日志并找出异常请求 `cat access.log |awk '{if($9!=200) print $0}'`
- 查看日志并找出所有请求 IP 和总请求次数 `cat access.log |awk '{count++; print $1;} END{printf "Totally %4d requests\n", count}'`
- 查看日志并找出所有请求 IP 和其请求次数 `cat access.log |awk '{data[$1]++} END{for(i in data) print data[i],i}'`

- 统计目录下所有文件的大小，不包括文件夹 `ls -al|awk 'BEGIN {size=0} {if($1!~/^d/){size=size+$5}} END{print "Totally ", size, " bytes" }'`

awk 内置变量

- ARGC               命令行参数个数
- ARGV               命令行参数排列
- ENVIRON            支持队列中系统环境变量的使用
- FILENAME           awk 浏览的当前文件名
- NF                 浏览当前行的域的个数
- NR                 浏览当前文件已读的行数
- FNR                浏览多个文件的总行数
- FS                 输入域分隔符，等价于命令行 -F 选项, 默认为空格
- OFS                输出域分隔符 默认为空格
- RS                 输入行分隔符 默认为 \n
- ORS                输出行分隔符 默认为 \n
- LENGTH             当前行长度

### sed

sed [options] [function] [file] 强大的文本编辑器

options:
- `-n` : 安静 (silent) 模式。仅显示处理行
- `-e` : 多个 sed 动作时，在每一个动作前加参数
- `-i` : 直接在源文件上修改
- `-f` : 读取文件中的 sed 动作

function:
- `a` : 新增，在当前行的下一行新增 `/<匹配字符串>/a\<新增内容>`
- `c` : 取代，取代指定行 `/<匹配字符串>/c\<取代内容>`
- `d` : 删除  `/<匹配字符串>/d`
- `p` : 展示第 n 行 `/<匹配字符串>/p`
- `i` : 插入，在当前行的上一行 `/<匹配字符串>/i\<插入内容>`
- `s` : 正则匹配取代字符串 `s/<匹配字符串>/<目标字符串>/g`

常用命令

- 显示第一行 `sed  -n '1p' test`
- 删除 1-4 行 `sed '1,4d' test`
- 删除 2-最后一行 `sed '2,$d' test`
- 删除匹配字符串所在的行 `sed '/aaa/d' test`
- 显示最后一行 `sed -n '$p' test`

- 查询关键字所在行 `sed -n '/aaa/p' test`
- 正则查询指定行 `sed -rn '/^[ab]{3}/p' test`

- 在第一行后增加字符串 `sed '1a abb bba' test`
- 在 1-3 行后增加字符串 `sed '1,3a abb bba aaa' test`
- 在最后一行后增加两行 `sed '$a aaa\nbbb' test`
- 在最后一行上插入一行 `sed '$i aaa' test`

- 修改第一行 `sed '1c fuck' test`
- 修改指定字符串,将 aaa 替换为 aba `sed -n '/aaa/p' test |sed 's/aaa/aba/g'`
- 修改最后一行中的指定部分 `sed -n '$p' test |sed 's/asd/aaa/g'`

### uniq

`uniq [option] [file]` 去掉文件中的相同行，但是它只能识别临近的相同行。

- `-i` : 不区分大小写
- `-c` : 计算相同行数并展示在行首
- `-u` : 去掉所有的相同行
- `-d` : 仅输出有重复的行，每样输出一行
- `-D` : 仅输出有重复的行，有几行输出几行
- `-f` : 跳过前 f 块元素，如 `-f1` 即从第二块元素开始比较
- `-s` : 跳过第 s 个字符之后的内容
- `-w` : 仅检查前 w 个字符

常用命令 `cat test |awk '{print $1}'|uniq -c`, `cat test |awk '{print $1}'|uniq -u`

查看日志并找出所有请求 IP 和其请求次数 `cat access.log |awk '{print $1}'|sort |uniq -c`

### sort

`sort [option] [file]` 对文件内容进行排序

- `-r` : 逆序输出
- `-t` : 指定分隔符
- `-k` : 排序的键，如 `-k2` 按第二位排序
- `-n` : 按数值大小排序，不然的话可能 `10` 会比 `2` 更小，因为按照首字母比较
- `-u` : 去重，功能同 `uniq`，但它是全文本去重

常用命令 `sort <file>`

### split

`split [option] [file] (prefix)` 对文件内容进行切分

- `-l` : 每一段输出的行数，默认为 1000 行
- `-b` : 每一段输出的大小，单位为  byte
- `-C` : 每一段输出的大小，但是在切割时尽量维持每行的完整性
- `-d` : 切割后文件名按 数字顺序递增
- `-a` : 后缀系数位数，默认有两位
- `(prefix)` : 切割后文件名前缀，默认为 aa，按字母顺序递增

常用命令 `split <file>`, `split -2000 <file>`, `split -b 1m <file>`, `split -C 1m <file>`, `split <file> -d -a 4 prefix_`

### curl

`curl [option] [url]` 高超的命令行网络请求命令

- `-O` : 保存请求内容到文本
- `-L` : 跟随跳转，如 302
- `-c` : 保存 cookie 到文件
- `-b` : 指定 cookie ，可以使用上面保存的 cookie 文件
- `-i` : 显示返回响应头部信息
- `-I` : 使用 HEAD 请求方式请求头部信息
- `-G` : 使用 GET 请求方式，默认
- `-v` : 查看完整的请求流程
- `-d` : 请求的数据
- `-H` : 指定请求头部信息
- `-u` : 指定用户名和密码，用于 HTTP Auth 登陆或者 ftp 登陆
- `-D` : 将返回响应头输出到文件
- `-0` : 使用 HTTP 1.0 协议
- `-x` : 使用代理
- `-X` : 指定 HTTP 请求方式，如 GET, POST, PUT, DELETE

常用命令 `curl -x 127.0.0.1:1080 http://httpbin.org/ip` `curl -X POST -d "username=username&password=password" http://127.0.0.1:5000/login` `curl -b "session=cookieinfo" http://127.0.0.1:5000/status`


### netstat

`netstat [option]` 查看服务及监听端口

- `-t` : 指明显示 TCP 端口
- `-u` : 指明显示 UDP 端口
- `-l` : 仅显示监听套接字(所谓套接字就是使应用程序能够读写与收发通讯协议(protocol)与资料的程序)
- `-p` : 显示进程标识符和程序名称，每一个套接字/端口都属于一个程序。
- `-n` : 不进行DNS轮询(可以加速操作)
- `-a` : 查看所有端口

常用命令 `netstat -an|grep 8080` 查看占用端口的服务 `netstat -anp|grep 8080`

## 实际应用

### 去重

去掉重复行

```
aaa
bbbbb
ccccc
123
aaaaa
123
bbb
aaa
```

shell

```
sort -u repeatxt
```

```
sort repeatxt |uniq
```

```
awk '{if(!data[$0]){print $0;data[$0]=1}}' repeatxt
```

### 部分去重

用 shell 处理一个文本文件，内容如下：

```
fdf     284
asd     112
adf     146
csb     513
dfg     576
asd     346
adf     263
csb     092
dfg     547
```

根据第一列去重，相同的保留第二列值最大的那个，结果：

```
fdf    284
asd    346
adf    263
csb    513
dfg    576
```

shell

```
cat txtfile | sort -rnk2 | awk '{if (!keys[$1]) print $0; keys[$1] = 1;}'
```

```
sort -r txtfile | awk '{print $2, $1}' | uniq -f1 | awk '{print $2, $1}'
```

```
cat txtfile |awk '{if($2>data[$1]) data[$1]=$2} END{for(i in data) print i,data[i]}'
```

```
sort txtfile|uniq -w3
```

### 输出重复

有一个文件如下

```
asd aaa
asd bbb
bbb aaa
bbb bbb
ccc ddd
```

希望输出第一列重复的所有行（第一列永远是3个字符）输出结果如下

```
asd aaa
asd bbb
bbb aaa
bbb bbb
```

shell

```
awk 'NR==FNR{a[$1]++}NR>FNR&&a[$1]>1' test test
```

### 统计求和

统计以下文件最后数字之和

```
1 one 3
2 two 3
3 three 5
4 four 4
5 five 4
6 six 3
7 seven 5
8 eight 5
9 nine 4
10 ten 3
...
990 nine hundred and ninety 20
991 nine hundred and ninety-one 23
992 nine hundred and ninety-two 23
993 nine hundred and ninety-three 25
994 nine hundred and ninety-four 24
995 nine hundred and ninety-five 24
996 nine hundred and ninety-six 23
997 nine hundred and ninety-seven 25
998 nine hundred and ninety-eight 25
999 nine hundred and ninety-nine 24
1000 one thousand 11
```

```
cat data11.txt |awk 'BEGIN {count=0} {count +=$NF} END{print count}'
```

### 统计平均

统计文件中所有数字的平均值

```
1.021 33
1#.ll   44
2.53 6
ss    7
```

```
awk 'BEGIN{sum=0;len=0} {for(i=1;i<=NF;i++){if($i~/^[0-9]+[\.0-9]*$/){sum+=$i;len++}}} END{print sum/len}' num.txt
```

### 获取文件行数

1. `awk '{print NR}' test |tail -n1`
2. `awk 'END{print NR}' test`
3. `awk 'BEGIN{count=0} {count++} END{print count}' test`
4. `cat test |wc -l`
5. `cat -n test |tail -n1`
6. `wc -l test`
7. `grep -n '' test |tail -n1`
8. `grep -n '' test |awk -F: '{print $1}'|tail -n1`
9. `sed -n '$=' test`

### 输出文件前十行

1. `head test`
2. `sed -n '1,10p' test`
3. `awk '{if(NR<11)print $0}' test`

### Nignx 日志切割

```
#!/bin/bash

prefix=error_`date +%Y%m%d`_
split error.log -10000 -d $prefix
for i in `ls |grep $prefix`;
do
    gzip $i;
done

last=`ls|grep $prefix|tail -n1`
gzip -d $last

last=`ls|grep $prefix|tail -n1`
mv $last error.log

kill -USR1 $(cat /var/logs/nginx.pid)
```

或者

```
#!/bin/bash
#cut nginx access.log

LOGS_PATH=/var/log/nginx
yesterday=`date  +"%F" -d  "-1 days"`
mv ${LOGS_PATH}/nginx.log  ${LOGS_PATH}/nginx-${yesterday}.log
kill -USR1 $(cat /var/logs/nginx.pid)
```

## 删除当前目录下的 python 运行脏数据

```
find . -name '*.pyc' -delete
find . -name __pycache__  -type d | xargs rm -rf
echo clean done
```

## 寻找当前目录下文件大小最大的 md 文件

```
find . -name "*.md" -ls | sort -n -k7 | tail -n 1
```


## 使用 UDP 请求数据

```
#!/bin/bash

def_host=localhost
def_port=43211

HOST=${2:-$def_host}
PORT=${3:-$def_port}

echo -n "$1" | nc -4u -w1 $HOST $PORT
```

或者

```
echo "This is my data" > /dev/udp/127.0.0.1/3000
```