---
layout: post
title: Linux 下 shell 命令的应用
description: 学习使用一些 Linux 高级命令。
category: opinion
---

在网上发现一本在线手册挺好的， [ Linux Tools Quick Tutorial](http://linuxtools-rst.readthedocs.io/zh_CN/latest/index.html)

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

常用命令 `ls -al|grep -i <name>`, `grep -P '^[\d]{3} [\w]{3} [\w]{5}' data.txt`, `grep <data> * -r`, `find $PWD -name "*.py"|grep -v ".venv"`, `ps -ef |grep flag |grep -v "grep" |wc -l`

### find

`find` 默认打印当前路径下的所有文件和文件夹

- `-name `  : 匹配文件名
- `-type`   : 匹配文件夹 `-type f` 即为 file 文件，`-type d` 即为 dir 文件夹
- `-user `  : 匹配用户
- `-ls`     : 对搜索结果使用 `ls` 显示
- `"regex"` : 使用引号匹配正则表达式
- `-exec`: 对匹配的内容做 shell 命令
- `-delete`: 删除匹配到的内容

常用命令 `find |grep <name>`, `find / -name <name>`, `find -user <user>`, `find -type f|wc`, `find ./ -name "*.md" |xargs cat|wc` 或者 `find . -name "*.md" -exec cat {} +|wc`, `find .  -path ./.git -prune -o  -name "*" -type f -print|xargs cat|wc -l`

### wc

`wc [option] [file]` 计算文件行数

- `-l` : 计算行数
- `-c` : 计算 bytes
- `-m` : 计算单词数

常用命令 `ls -al|wc`, `cat <name>|wc`

### awk

`awk [-F  field-separator]  'commands'  input-file(s)` 强大的文本分析工具
> 注意，输入的命令 commands 只能用单引号，不能用双引号 😂

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
- 查看 nginx 日志，并统计 HTTP code，根据 code 聚合 `cat access.log*|awk -F " " 'BEGIN {} {name[$11] ++}END{for(i in name) {printf "%s %d\n", i, name[i]}}'`
- 查看 nginx 日志，并统计 HTTP code，根据 code 聚合 `cat access.log*|awk -F " " '{print $11}'|sort|uniq -c` 

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

### nslookup

dig, host, nslookup 都是 DNS 查询工具。nslookup 是最久远的，也是过时的。

`nslookup -type=type domain [dns-server]` 

一般常用的就是 `nslookup online.windard.com` 或者 `nslookup online.windard.com 8.8.8.8`

### host

根据域名查询 ip 的参数是和 nslookup 一样的 `host -t type domain [dns-server]`

常用命令示例 `host -t aaaa www.windard.com`, `host windard.com 8.8.8.8`, `host -t cname status.windard.com`

不过，它还可以根据 ip 查询域名 `host ip`

比如 `host 8.8.8.8`

### dig

常用的 DNS 类型

| 类型      | 目的          |
|----------|---------------|
|A          |域名对应的 IPv4 地址|
|AAAA       |域名对应的 IPv6 地址|
|CNAME      |如果需要将域名指向另一个域名，可以做 CNAME 指定，并不会做真实跳转，只是作为替代|
|MX         |如果需要设置邮箱，需要设置 MX 记录|
|NS         |如果需要将子域名交给其他 DNS 服务器解析，需要设置 NS 记录|
|TXT        |一般 TXT 作为SPF，反垃圾邮件|
|SOA        |查找域内的SOA地址|

dig 是最常用的 DNS 记录查询工具，主要参数也还是 DNS 类型和指定的 DNS 服务器 `dig [type] domain [dns-server]`

但是它的返回值就非常的详细了,可以加上 `+short` 来获取简化记录，只有结果。

如果想要更详细的记录，可以加上 `+trace` 返回查询链路上的每一步。

在 CentOS 中通过 `yum install bind-utils` 安装，😭，竟然默认没有带。

常用命令 `dig status.windard.com @8.8.8.8 +short`, `dig  +short chatroom.windard.com`, `dig status.windard.com`, `dig aaaa windard.com`

也可以根据 ip 查询域名 `dig +x ip`

比如 `dig -x 202.182.110.237`

#### dig 返回信息

```
$ dig status.windard.com

; <<>> DiG 9.10.6 <<>> status.windard.com
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 30897
;; flags: qr rd ra; QUERY: 1, ANSWER: 2, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 4096
;; QUESTION SECTION:
;status.windard.com.    IN  A

;; ANSWER SECTION:
status.windard.com. 99  IN  CNAME stats.uptimerobot.com.
stats.uptimerobot.com.  99  IN  A 192.169.82.114

;; Query time: 68 msec
;; SERVER: 10.93.192.1#53(10.93.192.1)
;; WHEN: Tue Jun 30 14:56:26 CST 2020
;; MSG SIZE  rcvd: 95
```

返回结果中主要分为五个部分

1. 第一部分显示 dig 命令的版本和输入的参数。即返回值的前两行
2. 第二部分显示服务返回的一些技术详情，比较重要的是 status。如果 status 的值为 NOERROR 则说明本次查询成功结束。返回值第一段的后三行。
3. 第三部分中的 "QUESTION SECTION" 显示我们要查询的域名。 
4. 第四部分的 "ANSWER SECTION" 是查询到的结果。这里查询到两个结果，递归溯源，从 CNAME 查到了 A 记录。
5. 第五部分则是本次查询的一些统计信息，比如用了多长时间，查询了哪个 DNS 服务器，在什么时间进行的查询等等。

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

### 删除当前目录下的 python 运行脏数据

```
find . -name '*.pyc' -delete
find . -name __pycache__  -type d | xargs rm -rf
echo clean done
```

### 寻找当前目录下文件大小最大的文件

```
find . -name "*.md" -ls | sort -n -k7 | tail -n 1
```

### 查看登录失败用户和IP

```
lastb|awk '{print $1"\t"$3}' |sort|uniq -c|sort -n
```

### 判断程序是否运行

```
#!/bin/bash

COUNT=$(ps -ef |grep flag |grep -v "grep" |wc -l)
echo $COUNT
if [ $COUNT -eq 0 ]; then
        echo NOT RUN
else
        echo is RUN
fi
```

### 解压缩所有格式

```
ex ()
{
  if [ -f $1 ] ; then
    case $1 in
      *.tar.bz2)   tar xjf $1   ;;
      *.tar.gz)    tar xzf $1   ;;
      *.bz2)       bunzip2 $1   ;;
      *.rar)       unrar x $1     ;;
      *.gz)        gunzip $1    ;;
      *.tar)       tar xf $1    ;;
      *.tbz2)      tar xjf $1   ;;
      *.tgz)       tar xzf $1   ;;
      *.zip)       unzip $1     ;;
      *.Z)         uncompress $1;;
      *.7z)        7z x $1      ;;
      *)           echo "'$1' cannot be extracted via ex()" ;;
    esac
  else
    echo "'$1' is not a valid file"
  fi
}

```

### 爬取全站

```
wget -c -r -npH -k https://windard.com
```

- c：断点续传
- r：递归下载
- np：递归下载时不搜索上层目录
- nd：递归下载时不创建一层一层的目录,把所有文件下载当前文件夹中
- p：下载网页所需要的所有文件(图片,样式,js文件等)
- H：当递归时是转到外部主机下载图片或链接
- k：将绝对链接转换为相对链接,这样就可以在本地脱机浏览网页了

### 仅打印出文件第十行

```
awk  -F: 'BEGIN {count=0;} {name[count] = $1;count++;}; END{for (i = 0; i < NR; i++) if( i == 9) print name[i]}' file.txt
awk NR==10 file.txt
sed -n '10p' file.txt
```

### shell 中 FOR 循环

```
for i in `seq 10`; do echo "hello $i"+$i; done
```

## 其他

### 使用 UDP 请求数据

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

### 在内网中逃出生天

使用 反向 SSH 使外网服务器可以直接操纵内网服务器

内网主机，此处用户名密码和远程地址均为外网机器

```
ssh -f -N -R 2022:localhost:22 username@remote.freePC.com
```

在内网中，也可以使用 `autossh` ，可以保持连接，在断掉时自动重连，和监控连接情况。

```
autossh -M 33333 -NR 33334:localhost:22 ServerUser@Cloud_Server_IP -p [Server_port]
```

外网主机，此处用户名密码为内网机器

```
ssh username@localhost -p2022
```

也可以开启 socks5 转发，用来访问内网其他资源

```
ssh -g -D 33335 -p 33334 innerUser@localhost
```

设置本地与远端连接隧道,将远程端口映射到本地

```
ssh -L5984:127.0.0.1:5984 remote_user@remote_server
```

## OpenSSL 使用

### 生成随机随机字符串

```
> openssl rand 20
 �yR�Z�&�����%                                                                                            > openssl rand 20 -out rand.out
> openssl rand 20 -hex
2c345e2e7989d699e1e87923675959960f1493eb
> openssl rand 20 -base64
A3UYiELJdZdvHKFKDuNShpaxPXg=
```

### 哈希算法

```
> openssl dgst -sha1 test.in
SHA1(test.in)= 22596363b3de40b06f981fb85d82312e8c0ed511
> echo "hello world"|openssl dgst -sha1
(stdin)= 22596363b3de40b06f981fb85d82312e8c0ed511
> openssl dgst -out test.out -sha1 test.in
```

可选的哈希算法有

```
-md4            to use the md4 message digest algorithm
-md5            to use the md5 message digest algorithm
-mdc2           to use the mdc2 message digest algorithm
-ripemd160      to use the ripemd160 message digest algorithm
-sha            to use the sha message digest algorithm
-sha1           to use the sha1 message digest algorithm
-sha224         to use the sha224 message digest algorithm
-sha256         to use the sha256 message digest algorithm
-sha384         to use the sha384 message digest algorithm
-sha512         to use the sha512 message digest algorithm
-whirlpool      to use the whirlpool message digest algorithm
```

### 对称加解密算法

```
openssl enc -des3 -k openssl -in test.in -out test.out
openssl enc -des3 -d -k openssl -in test.out -out test.in
```

> 加上参数 `-a`, 表示输出结果经过 base64 编码

对称加密的算法可选的有

```
-aes-128-cbc               -aes-128-ccm               -aes-128-cfb
-aes-128-cfb1              -aes-128-cfb8              -aes-128-ctr
-aes-128-ecb               -aes-128-ofb               -aes-192-cbc
-aes-192-ccm               -aes-192-cfb               -aes-192-cfb1
-aes-192-cfb8              -aes-192-ctr               -aes-192-ecb
-aes-192-ofb               -aes-256-cbc               -aes-256-ccm
-aes-256-cfb               -aes-256-cfb1              -aes-256-cfb8
-aes-256-ctr               -aes-256-ecb               -aes-256-ofb
-aes128                    -aes192                    -aes256
-bf                        -bf-cbc                    -bf-cfb
-bf-ecb                    -bf-ofb                    -blowfish
-camellia-128-cbc          -camellia-128-cfb          -camellia-128-cfb1
-camellia-128-cfb8         -camellia-128-ecb          -camellia-128-ofb
-camellia-192-cbc          -camellia-192-cfb          -camellia-192-cfb1
-camellia-192-cfb8         -camellia-192-ecb          -camellia-192-ofb
-camellia-256-cbc          -camellia-256-cfb          -camellia-256-cfb1
-camellia-256-cfb8         -camellia-256-ecb          -camellia-256-ofb
-camellia128               -camellia192               -camellia256
-cast                      -cast-cbc                  -cast5-cbc
-cast5-cfb                 -cast5-ecb                 -cast5-ofb
-des                       -des-cbc                   -des-cfb
-des-cfb1                  -des-cfb8                  -des-ecb
-des-ede                   -des-ede-cbc               -des-ede-cfb
-des-ede-ofb               -des-ede3                  -des-ede3-cbc
-des-ede3-cfb              -des-ede3-cfb1             -des-ede3-cfb8
-des-ede3-ofb              -des-ofb                   -des3
-desx                      -desx-cbc                  -id-aes128-CCM
-id-aes128-wrap            -id-aes192-CCM             -id-aes192-wrap
-id-aes256-CCM             -id-aes256-wrap            -id-smime-alg-CMS3DESwrap
-idea                      -idea-cbc                  -idea-cfb
-idea-ecb                  -idea-ofb                  -rc2
-rc2-40-cbc                -rc2-64-cbc                -rc2-cbc
-rc2-cfb                   -rc2-ecb                   -rc2-ofb
-rc4                       -rc4-40                    -seed
-seed-cbc                  -seed-cfb                  -seed-ecb
-seed-ofb
```

### 非对称加解密算法

```
openssl genrsa -out pri.key 2048                                                    # 生成私钥
openssl rsa -in pri.key -pubout -out pub.key                                        # 生成公钥
openssl rsautl -in test.in -out test.out -inkey pub.key -pubin -encrypt             # 公钥加密
openssl rsautl -in test.out -out test.in -inkey pri.key -decrypt                    # 私钥解密
```

生成私钥时，这是未带加密的密钥的对称密钥，如果想要加密，可以使用的加密方式有

```
 -des            encrypt the generated key with DES in cbc mode
 -des3           encrypt the generated key with DES in ede cbc mode (168 bit key)
 -idea           encrypt the generated key with IDEA in cbc mode
 -seed
                 encrypt PEM output with cbc seed
 -aes128, -aes192, -aes256
                 encrypt PEM output with cbc aes
 -camellia128, -camellia192, -camellia256
                 encrypt PEM output with cbc camellia
```

使用加密的私钥

```
openssl genrsa -aes256 -out pri.key 2048
```

非对称加密算法还有 `dsa`

### 签名和验签

```
openssl rsautl -in test.in -out test.sig -inkey pri.key -sign
openssl rsautl -in test.sig -out test.in -inkey pub.key -pubin -verify
```
