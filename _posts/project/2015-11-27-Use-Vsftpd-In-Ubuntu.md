---
layout: post
title: vsftpd 的配置和使用
category: project
description: 在服务器与客户端之间的文件传输一般都是采用 FTP 来上传下载， vsftpd 是非常好用的安全的 FTP 服务器软件。
---

## 安装 vsftpd            

FTP (File Transfer Protocol) 文件传输协议是互联网中非常重要的一个协议，在服务器与客户端之间进行文件操作。

`vsftpd` 即 `very security ftp`，这是一个主打安全的 FTP 服务器，各大 Linux 的发行版本都可以使用。

Ubuntu

```
sudo apt-get install vsftpd
```          

Cent OS

```
sudo yum install vsftpd
```

Ubuntu 下可以用 `dpkg -l|grep ftp` 来看一下。      

![vsftpd.jpg](/images/vsftpd.jpg)      

Cent OS 下可以使用 `rpm -qa |grep ftp` 来看一下。

![vsftpd_exists_centos.png](/images/vsftpd_exists_centos.png)

## 启动与关闭

启动

```
sudo service vsftpd start
```         

关闭

```
sudo service vsftpd stop
```         

查看 FTP 服务器状态和重启 FTP 服务器

```
sudo service vsftpd status
sudo service vsftpd restart
```

## 服务器端使用

vsftpd 的默认配置可以使用匿名用户登陆，没有其他用户账号，无法上传文件，所以需要做一下简单的配置，注释与NO的作用效果相同。

配置效果
1. 允许匿名用户登录，登录目录为 `/ftp/pub`，只能下载，不能上传，不能创建目录，不能超出登录目录。
2. 允许本地用户登录，如 windard 和 root ，登录目录分别是其根目录 `/home/windard` 和 `/root` ，可上传可下载可创建目录，甚至可以到达其根目录的上级目录。 
3. 允许虚拟用户登录，如 ftpuser，虚拟用户只能在 FTP 服务器中使用，不能登录服务器，登录目录为 `/ftp/ftpuser`，只能上传下载创建目录，不能超出登录目录。

### 关于匿名用户

```
# 是否允许匿名用户访问
anonymous_enable=YES
# 匿名用户登录目录
anon_root=/ftp/pub
# 是否允许匿名用户上传文件
anon_upload_enable=NO
# 是否允许匿名用户创建文件夹
anon_mkdir_write_enable=NO
```

### 关于本地用户

```
# 是否能够使用本地用户
local_enable=YES
# 是否用户用户上传文件
write_enable=YES
# 能否上传 ASCII 类型文件
ascii_upload_enable=YES
ascii_download_enable=YES
# 文件上传之后的文件状态
local_umask=022
# 需要加上这一句
# 不然就会 500 OOPS: vsftpd: refusing to run with writable root inside chroot()
allow_writeable_chroot=YES
# 是否能够切换到根目录之外
chroot_local_user=YES
# 只有目录中的账户才能切换
chroot_list_enable=YES
chroot_list_file=/etc/vsftpd/chroot_list
```

将 root 和 windard 加入 `/etc/vsftpd/chroot_list` 文件中，一行一个，若无则创建该文件。

root 用户是默认不能使用 FTP 登陆的，需要将 `/etc/vsftpd/user_list` 和 `/etc/vsftpd/ftpusers` 中的 root 注释掉。

> user_list 此文件中包含可能会被禁止的用户名，取决于配置文件中的 `userlist_enable=YES` <br>
> ftpusers 此文件中包含被禁止登陆的用户名。 

在 Cent OS 7 中，因为有安全内核 selinux 不允许使用 root 登陆 FTP，所以需要还需要配置安全内核开放权限。

```
setsebool -P ftpd_full_access 1
```

可以通过 `service vsftpd status -l` 查看完整 vsftpd 运行状态。

在 cent OS 7 中使用 `firewall-cmd` 将其加入永久防火墙规则。

```
firewall-cmd  --permanent --add-service=ftp
```

如果是 iptables 的话则是

```
iptables -A INPUT -m state --state NEW -m tcp -p tcp --dport 21 -j ACCEPT
```

在 Cent OS 7 中使用 `systemctl` 将其加入开机启动

```
systemctl enable vsftpd
```

### 关于虚拟用户

首先我们需要创建虚拟用户 `ftpuser` 并设定密码，其实这个也还是普通用户，只不过不能用来登陆，在 vsftpd 的教程中还有一种虚拟账户，需要使用数据库保存 FTP 专用账户，感觉比较复杂，暂时也没有什么用，就不做介绍。 

```
[root@localhost ~]# useradd -s /sbin/nologin -d /ftp/ftpuser ftpuser
[root@localhost ~]# passwd ftpuser
更改用户 ftpuser 的密码 。
新的 密码：
重新输入新的 密码：
passwd：所有的身份验证令牌已经成功更新。
```

### 其他

```
# 打开上传下载日志
xferlog_enable=YES
# 使用标志日志格式记录
xferlog_std_format=YES
# 日志保存位置
xferlog_file=/var/log/xferlog
# 用户登录时的欢迎信息
ftpd_banner=Welcome to blah FTP service.

```

还有其他的一些配置，基本可以不做修改，就不再介绍。

## 使用指南

`ftp XX.XX.XX.XX` 进入命令行模式的ftp，可以使用匿名登录，也可以使用帐号登录。                                  

如果是匿名登录的话，帐号就是 `anonymous` 密码随意写就可以了，匿名用户登录之后的根目录在 `/src/ftp`(Ubuntu) 或 `/var/ftp`(Cent OS) 。

一般登陆 vsftpd 用的不是 ftp, 而是 sftp 命令 `sftp root@XX.XX.XX.XX`, sftp = ssh + ftp。                   

在 Windows 下命令行中使用 FTP 连接上之后无法正常使用，使用 sftp 连接之后可以正常使用。

在 Windows 下使用 FTP 软件可以正常连接使用。

在 Windows 下使用资源管理器可以登陆 FTP ，默认使用匿名账户直接登陆，可以使用 ftp://username:password@XX.XX.XX.XX 来使用账户密码登陆，这样的登陆方式也可以在浏览器上使用。

在使用 FTP 登陆时有可能会遇到需要使用被动模式，在 Windows 下使用 `quote PASV` ，在 Linux 下使用 `passive` 来进行切换。

### 关于 主动模式和被动模式

FTP 默认采用 20,21 端口与客户端进行通信，20 端口进行建立控制和发送命令，21 端口进行数据传输。

主动（PORT）模式：首先由客户端向服务器的 21 端口建立 FTP 控制连接，当需要传输数据时，客户端以 PORT 命令告诉服务器本机开放一个较大的非特权端口，等待服务器从 20 端口到本机的指定端口进行数据连接。主动模式即服务器主动向客户端建立数据连接。

![FTP_PORT.png](/images/FTP_PORT.png)

被动（PASV）模式：首先由客户端想服务器的 21 端口建立 FTP 控制连接，当需要传输数据是，客户端提交 PASV 指令，服务器则开启一个较大的非特权端口，并将端口号发送给客户端，等待客户端连接数据连接。被动模式即服务器被动的等待客户端进行数据连接。

![FTP_PASV.png](images/FTP_PASV.png)

两种不同的工作模式是为了满足不同网络环境的需求，如果客户端的防火墙没有开放端口，则采用被动模式，如果服务器为了安全只开了 20,21 端口，则采用主动模式。一般 FTP 服务器是两种模式都支持，具体的使用那一种模式取决于客户端请求。

网上如果需要开启 FTP 被动模式，需要在配置文件中加入 

```
pasv_enable=YES
pasv_min_port=6000
pasv_max_port=7000
```

然后修改相关的防火墙配置。

```
iptables -A INPUT -m state --state NEW -m tcp -p tcp --dport 6000:7000 -j ACCEPT
```

然而我的 FTP 服务器并没有遇到这些问题，而且 被动模式 默认就是开启的。

这是在 Ubuntu 下 vsftpd 配置，基本与 Cent OS 一致。

```
listen=<YES/NO> :设置为YES时vsftpd以独立运行方式启动，设置为NO时以xinetd方式启动（xinetd是管理守护进程的，将服务集中管理，可以减少大量服务的资源消耗）                                                                        
listen_port=<port> :设置控制连接的监听端口号，默认为21                                          
listen_address=<ip address> :将在绑定到指定IP地址运行，适合多网卡                                                   
connect_from_port_20=<YES/NO> :若为YES，则强迫FTP－DATA的数据传送使用port 20，默认YES                                 
pasv_enable=<YES/NO> :是否使用被动模式的数据连接，如果客户机在防火墙后，请开启为YES                                
pasv_min_port=<n>                                                                                       
pasv_max_port=<m> :设置被动模式后的数据连接端口范围在n和m之间,建议为50000－60000端口                                          
message_file=<filename> :设置使用者进入某个目录时显示的文件内容，默认为 .message                                    
dirmessage_enable=<YES/NO> :设置使用者进入某个目录时是否显示由message_file指定的文件内容                            
ftpd_banner=<message> :设置用户连接服务器后的显示信息，就是欢迎信息                                          
banner_file=<filename> :设置用户连接服务器后的显示信息存放在指定的filename文件中                                 
connect_timeout=<n> :如果客户机连接服务器超过N秒，则强制断线，默认60                                                       
accept_timeout=<n> :当使用者以被动模式进行数据传输时，服务器发出passive port指令等待客户机超过N秒，则强制断线，默认60             
accept_connection_timeout=<n> :设置空闲的数据连接在N秒后中断，默认120                                     
data_connection_timeout=<n> : 设置空闲的用户会话在N秒后中断，默认300                                           
max_clients=<n> : 在独立启动时限制服务器的连接数，0表示无限制                                              
max_per_ip=<n> :在独立启动时限制客户机每IP的连接数，0表示无限制（不知道是否跟多线程下载有没干系）                                
local_enable=<YES/NO> :设置是否支持本地用户帐号访问                                            
guest_enable=<YES/NO> :设置是否支持虚拟用户帐号访问                                           
write_enable=<YES/NO> :是否开放本地用户的写权限                                            
local_umask=<nnn> :设置本地用户上传的文件的生成掩码，默认为077                                     
local_max_rate<n> :设置本地用户最大的传输速率，单位为bytes/sec，值为0表示不限制                          
local_root=<file> :设置本地用户登陆后的目录，默认为本地用户的主目录                                         
chroot_local_user=<YES/NO> :当为YES时，所有本地用户可以执行chroot                                   
chroot_list_enable=<YES/NO>                                                                                              
chroot_list_file=<filename> :当chroot_local_user=NO 且 chroot_list_enable=YES时，只有filename文件指定的用户可以执行chroot              
anonymous_enable=<YES/NO> :设置是否支持匿名用户访问                                   
anon_max_rate=<n> :设置匿名用户的最大传输速率，单位为B/s，值为0表示不限制                              
anon_world_readable_only=<YES/NO> 是否开放匿名用户的浏览权限                                   
anon_upload_enable=<YES/NO> 设置是否允许匿名用户上传                                   
anon_mkdir_write_enable=<YES/NO> :设置是否允许匿名用户创建目录                               
anon_other_write_enable=<YES/NO> :设置是否允许匿名用户其他的写权限,即删除重命名权限。    
anon_umask=<nnn> :设置匿名用户上传的文件的生成掩码，默认为077                                    
```

ftp 传输过程中状态码代表的意思：

```
110 重新启动标记应答。                                  
120 服务在多久时间内ready。                            
125 数据链路端口开启，准备传送。                                  
150 文件状态正常，开启数据连接端口。                              
200 命令执行成功。                                    
202 命令执行失败。                                    
211 系统状态或是系统求助响应。                                  
212 目录的状态。                                                
213 文件的状态。                                          
214 求助的讯息。                                             
215 名称系统类型。                                       
220 新的联机服务ready。                                            
221 服务的控制连接端口关闭，可以注销。                                 
225 数据连结开启，但无传输动作。                                       
226 关闭数据连接端口，请求的文件操作成功。                                              
227 进入passive mode。                                               
230 使用者登入。                                              
250 请求的文件操作完成。                                           
257 显示目前的路径名称。                                    
331 用户名称正确，需要密码。                                           
332 登入时需要账号信息。                                     
350 请求的操作需要进一部的命令。                                    
421 无法提供服务，关闭控制连结。                                   
425 无法开启数据链路。                                  
426 关闭联机，终止传输。                                   
450 请求的操作未执行。                                    
451 命令终止:有本地的错误。                                     
452 未执行命令:磁盘空间不足。                                
500 格式错误，无法识别命令。
501 参数语法错误。
502 命令执行失败。
503 命令顺序错误。
504 命令所接的参数不正确。
530 未登入。                              
532 储存文件需要账户登入。                                          
550 未执行请求的操作。                                      
551 请求的命令终止，类型未知。                                        
552 请求的文件终止，储存位溢出。                                            
553 未执行请求的的命令，名称不正确。                                           
```          

ftp 常用命令：

```
ftp XX.XX.XX.XX        #连接目标主机
open host  [port]      #进入ftp模式，连接目标主机
user XXX		       #切换用户
close|disconnect       #停止连接目标主机，进入ftp模式
bye|quit|!|exit        #退出ftp状态
！ XX			       #在自己的主机上执行XX命令
?|help [某个命令]	   #查看ftp帮助
ls|dir			       #查看ftp当前目录下文件
cd				       #ftp切换目录
lcd				       #在自己主机上切换目录
cdup			       #ftp进入父级目录
pwd				       #ftp当前目录
ascii			       #设置文件传输为ascii模式
binary|bi		       #设置文件传输为二进制模式
delete			       #删除ftp上文件
mkdir			       #在ftp上创建文件夹
get|recv XXX [XX]      #下载ftp服务器上的XXX文件，并以XX文件名保存在自己主机当前目录
put|send XX [XXX]      #上传自己主机当前目录下的XX文件，并以XXX文件名保存在ftp服务器上
mput                   #大量文件上传，ftp支持通配符×
mget			       #大量文件下载，ftp支持通配符×
status			       #当前ftp状态
system			       #查看ftp服务器主机
chmod				   #改变ftp服务器上文件权限
rename                 #改变ftp服务器上的某个文件名
size				   #查看ftp上某个文件大小
```
