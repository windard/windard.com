---
layout: post
title: 实现 socks5 代理
description: 现在很多人都在用，天天用的软件，却对它的实现协议却知之甚少。
category: blog
---

socks5 协议继承自 socks 协议。

> 竟然是两年前的旧文，终于要来填坑了。

## 正向代理和反向代理

反向代理就医院里的挂号处，公司里的行政前台，你不需要关心具体的处理人，不用关心内部逻辑，只需要找到对接人就可以了，反向代理服务器就是这个对接人。

正向代理像是你的望远镜，就是你的皮夹克，穿戴上他，你可以伪装成另一个人，甚至就像附身在你的小跟班身上，通过另一双眼镜去看世界，隐藏自己的身份，逃出生天，正向代理服务器就是这个伪装。

## 反向代理

首先我们看下最简单的反向代理实现，简单的请求转发。你以为你请求的是A，实际上调用的是B，即B被反向代理到了A上，A的请求被转发到了B上。

```python
# -*- coding: utf-8 -*-

import socket
import threading

source_host = '127.0.0.1'
source_port = 5002

desc_host = '127.0.0.1'
desc_port = 8099


def send(sender, recver):
    while 1:
        try:
            data = sender.recv(2048)
        except:
            print("recv error")
            break
        if not data:
            break

        try:
            recver.sendall(data)
        except:
            print("send error")
            break
    sender.close()
    recver.close()


def proxy(client):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect((source_host, source_port))
    threading.Thread(target=send, args=(client, server)).start()
    threading.Thread(target=send, args=(server, client)).start()


def main():
    proxy_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    proxy_server.bind((desc_host, desc_port))
    proxy_server.listen(5)

    print("Proxying from %s:%s to %s:%s ..." % (source_host, source_port, desc_host, desc_port))

    while 1:
        conn, addr = proxy_server.accept()
        print("received connect from %s:%s" % (addr[0], addr[1]))
        threading.Thread(target=proxy, args=(conn,)).start()


if __name__ == '__main__':
    main()

```

真的非常简单，手动监听端口，手动处理请求，手动读写数据。

使用 socketserver 提供的 server 和 handle 处理就是这样。

```python
# -*- coding: utf-8 -*-
import socket
import logging
import threading
from socketserver import StreamRequestHandler, BaseRequestHandler
from socketserver import ThreadingTCPServer as RawThreadingTCPServer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ThreadingTCPServer(RawThreadingTCPServer):
    allow_reuse_address = True


class ProxyHandler(BaseRequestHandler):
    def handle(self):
        # should be blocked until finish handle.
        target = socket.create_connection(('127.0.0.1', 5002))
        thread_list = []
        thread_list.append(threading.Thread(
            target=self.forward_reply, args=(self.request, target)
        ))
        thread_list.append(threading.Thread(
            target=self.forward_reply, args=(target, self.request)
        ))
        for t in thread_list:
            t.start()
        for t in thread_list:
            t.join()

    def forward_reply(self, local, target):
        try:
            while True:
                # target.write(local.read())
                data = local.recv(1024)
                if not data:
                    return
                target.send(data)
        except Exception as e:
            logger.info("forward error:%r", e)
            raise e


if __name__ == '__main__':
    server = ThreadingTCPServer(('127.0.0.1', 5003), ProxyHandler)
    server.serve_forever()

```

看起来确实少些两行代码，但是实际上还是非常的基础和简单。

## socks5 协议

socks5 属于正向代理的一种，像上面的反向代理和正向代理的区别在哪里呢？

那就是反向代理的目标地址是固定的，也就是说，请求转发的的终点已经固定了，但是如果我们想要自由的转发请求到任意地址呢？就需要正向代理服务了。

```python
# -*- coding: utf-8 -*-
import socket
import struct
import select
import gevent
import logging
import threading
from socketserver import StreamRequestHandler
from socketserver import ThreadingTCPServer as RawThreadingTCPServer
from gevent import monkey

monkey.patch_all()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
AUTH_USERNAME = "YOUR_PROXY_LOGIN"
AUTH_PASSWORD = "YOUR_PROXY_PASSWORD"


class ThreadingTCPServer(RawThreadingTCPServer):
    allow_reuse_address = True


class SocksException(Exception):
    pass


class Socks5Handler(StreamRequestHandler):
    def handle_forward(self, client, remote):
        # two threading to read and write
        # handle should be blocked
        thread_list = [threading.Thread(
            target=self.forward_reply, args=(client, remote)
        ), threading.Thread(
            target=self.forward_reply, args=(remote, client)
        )]
        for t in thread_list:
            t.start()
        for t in thread_list:
            t.join()

    def handle_forward_in_gevent(self, client, remote):
        spawns = [gevent.spawn(self.forward_reply, client, remote), gevent.spawn(self.forward_reply, remote, client)]
        gevent.joinall(spawns)

    def forward_reply(self, local, target):
        # type: (socket.socket, socket.socket) -> None
        try:
            while True:
                # target.write(local.read())
                data = local.recv(1024)
                if not data:
                    return
                target.send(data)
        except Exception as e:
            logger.info("forward error:%r", e)
            raise e

    def handle_forward_in_select(self, client, remote):
        # type: (socket.socket, socket.socket) -> None
        try:
            inputs = [client, remote]
            while inputs:
                readable, _, _ = select.select(inputs, [], [])
                if client in readable:
                    data = client.recv(4096)
                    if not data:
                        break
                    remote.sendall(data)

                if remote in readable:
                    data = remote.recv(4096)
                    if not data:
                        break
                    client.sendall(data)
        except Exception as e:
            logger.info("select error:%r", e)

    def socks_user_auth(self):
        buf = self.rfile.read(2)
        if buf[0] != chr(0x01):
            raise SocksException("invalid version")
        username_length = ord(buf[1])
        username = self.rfile.read(username_length)

        buf = self.rfile.read(1)
        password_length = ord(buf[0])
        password = self.rfile.read(password_length)
        logger.info("user auth: %s-%s", username, password)

        if username == AUTH_USERNAME and password == AUTH_PASSWORD:
            self.wfile.write(b'\x01\x00')
        else:
            self.wfile.write(b'\x01\x01')
            raise SocksException("socks user auth fail")

    def socks_auth(self):
        # self.rfile._sock.recv(2)
        buf = self.rfile.read(2)
        if buf[0] != chr(0x05):
            # python3 will get int
            # if buf[0] != chr(0x05):
            # if buf[0] != b'\x05':
            raise SocksException("invalid version")

        methods_length = ord(buf[1])
        methods = self.rfile.read(methods_length)
        logger.info("receive methods:%r", methods)
        if b'\x02' in methods:
            # socks user auth
            self.wfile.write(b'\x05\x02')
            self.socks_user_auth()
        else:
            self.wfile.write(b'\x05\x00')
        # maybe need one
        # self.wfile.flush()

    def socks_connect(self):
        ver, cmd, _, addr_type = self.rfile.read(4)
        if ver != chr(0x05) or cmd != chr(0x01):
            raise SocksException("invalid ver/cmd")

        if addr_type == chr(0x01):
            logger.info("client addr type:IPv4")
            packed_ip = self.rfile.read(4)
            remote_addr = socket.inet_ntoa(packed_ip)
        elif addr_type == chr(0x03):
            logger.info("client addr type:URL")
            addr_length = self.wfile.read(1)
            remote_addr = self.rfile.read(ord(addr_length))
        elif addr_type == chr(0x04):
            logger.info("client addr type:IPv6")
            packed_ip = self.rfile.read(16)
            remote_addr = socket.inet_ntop(socket.AF_INET6, packed_ip)
        else:
            raise SocksException("addr_type not supported.")

        addr_port = self.rfile.read(2)
        # 注意：这里是返回的tuple
        remote_port = struct.unpack('>H', addr_port)[0]

        reply = b'\x05\x00\x00\x01'
        reply += socket.inet_aton('0.0.0.0') + struct.pack('>H', 2222)
        self.wfile.write(reply)
        return remote_addr, remote_port

    def handle(self):
        try:
            logger.info("receive from:%r", self.request.getpeername())
            # step one: sock auth
            self.socks_auth()

            # step two: sock connect
            remote_addr, remote_port = self.socks_connect()
            logger.info("target addr:%r", (remote_addr, remote_port))

            # step three: sock forward
            remote = socket.create_connection((remote_addr, remote_port))
            self.handle_forward_in_select(self.connection, remote)
        except SocksException as e:
            logger.info("socks error:%r", e)
        except socket.error as e:
            logger.info("socket error:%r", e)
            raise


if __name__ == '__main__':
    server = ThreadingTCPServer(('127.0.0.1', 8572), Socks5Handler)
    server.serve_forever()

```

实现了 TCP 的 socks5 代理，同时支持 IPv6和用户认证，使用 curl 来测试下。

```shell
$ curl --socks5 socks5://127.0.0.1:9458 http://ipconfig.io
65.13.234.13
$ curl -4 --socks5 socks5://YOUR_PROXY_LOGIN:YOUR_PROXY_PASSWORD@127.0.0.1:9458 http://ipconfig.io
65.13.234.13
$ curl -6 --socks5 socks5://YOUR_PROXY_LOGIN:YOUR_PROXY_PASSWORD@127.0.0.1:9458 http://ipconfig.io
240e:b2:e401:4::7
$ curl --socks5 socks5://YOUR_PROXY_LOGIN:YOUR_PROXY_PASSWOR@127.0.0.1:9458 http://ipconfig.io
curl: (7) User was rejected by the SOCKS5 server (1 1).
```

## 具体实现

研究一下 socks5 的协议定义，socks5 protocol 在请求转发之前有两步交互，在请求认证，和获取目的地址之后，就和上文一下发起请求转发即可。
> 正向代理中，除了 socks5 还有 socks4 和 socks4a，都比 socks5 简单，就不详细介绍了。

1. sock auth
2. sock connect
3. sock forward

#### Auth

认证流程

##### client ---> server

客户端发送请求确认版本和请求方式，单位字节

```
+-------------------------+
| VER |	NMETHODS | METHODS|
+-------------------------+
| 1	  |    1     | 1-255  |
+-------------------------+
```

- VER: socks 的版本，这里应该是 `0x05`
- NMETHODS: METHODS 部分的长度，取值范围 1~255
- METHODS: 客户端支持的认证方式列表，每个方法占1字节，支持的认证方式有
    - `0x00`: 不需要认证
    - `0x01`: GSSAPI
    - `0x02`: 用户名，密码认证
    - `0x03`-`0x7F`: 保留，有 IANA 分配
    - `0x80`-`0xFE`: 自定义，私人方法
    - `0xFF`: 无可接受的的方法

###### server ---> client

服务器端返回支持的方法，单位字节

```
+--------------+
| VER |	METHOD |
+--------------+
| 1	  |    1   |
+--------------+
```

- VER: socks 的版本，这里应该是 `0x05`
- METHOD: 服务端选中的方法。如果返回 `0xFF` 表示没有选中任何方法，客户端需要关闭连接。

#### Connect

认证结束之后，客户端发送请求信息

##### client ---> server

```
+---------------------------------------------------+
| VER |	CMD  | RSV  | ATYP  |  DST.ADDR |  DST.PORT |
+---------------------------------------------------+
| 1	  |   1  |  1   |  1    | (dynamic) |    2      |
+---------------------------------------------------+
```

- VER: socks 的版本，这里应该是 `0x05`
- CMD: sock 的命令码
    - `0x01`: 表示 CONNECT 请求
    - `0x02`: 表示 BIND 请求
    - `0x03`: 表示 UDP 转发
- RSV: 保留，固定 `0x00`
- ATYP: DST.ADDR 的地址类型
    - `0x01`: IPv4 地址，DST.ADDR 部分4字节长度
    - `0x03`: DST.ADDR 部分第一个字节为域名长度，DST.ADDR 剩余部分内容为域名，没有`\0`的结束符
    - `0x04`: IPv6 地址，DST.ADDR 部分16字节长度
- DST.ADDR 目的地址
- DST.PORT 目的端口

##### server ---> client

```
+---------------------------------------------------+
| VER |	REP  | RSV  | ATYP  |  DST.ADDR |  DST.PORT |
+---------------------------------------------------+
| 1	  |   1  |  1   |  1    | (dynamic) |    2      |
+---------------------------------------------------+
```

- VER: socks 的版本，这里应该是 `0x05`
- REP: 应答字段，表示请求状态
    - `0x00`: 表示成功
    - `0x00`: 表示 SOCKS 服务器连接失败
    - `0x02`: 表示现有规则不允许连接
    - `0x03`: 表示网络不可达
    - `0x04`: 表示主机不可达
    - `0x05`: 表示连接被拒
    - `0x06`: 表示TTL超时
    - `0x07`: 表示不支持的命令
    - `0x08`: 表示不支持的地址类型
    - `0x09`-`0xFF`: 未定义
- RSV: 保留，固定 `0x00`
- ATYP: DST.ADDR 的地址类型
    - `0x01`: IPv4 地址，DST.ADDR 部分4字节长度
    - `0x03`: DST.ADDR 部分第一个字节为域名长度，DST.ADDR 剩余部分内容为域名，没有`\0`的结束符
    - `0x04`: IPv6 地址，DST.ADDR 部分16字节长度
- DST.ADDR 服务器绑定的地址
- DST.PORT 服务器绑定的端口

#### Forward

端口转发

#### UserAuth

使用用户名密码的方式进行用户认证

##### client ---> server

```
+--------------------------------------------------------------------+
| VER |	username length |  username  | password length |  password   |
+--------------------------------------------------------------------+
| 1	  |        1        | (dynamic)  |        1        |  (dynamic)  |
+--------------------------------------------------------------------+
```

- VER: 鉴定协议版本,目前为 `0x01`
- username length: 用户名长度
- username: 用户名 
- password length: 密码长度
- password: 密码

##### server ---> client

```
+--------------+
| VER |	STATUS |
+--------------+
| 1	  |    1   |
+--------------+
```

- VER: 鉴定协议版本,目前为 `0x01`
- STATUS: 鉴定状态
  - `0x00`: 表示成功
  - `0x01`: 表示失败


## 其他实现

用 Python 实现已经很简单了，但是我没想到的时候，使用 Golang 在网络操作上更底层更方便，也更加容易扩展。

```golang
package main

import (
	"bytes"
	"encoding/binary"
	"errors"
	"fmt"
	"io"
	"log"
	"net"
)

type Socks5UserAuthInfo struct {
	Username []byte
	Password []byte
}

var socks5UserAuthInfo = Socks5UserAuthInfo{
	Username: []byte("YOUR_PROXY_LOGIN"),
	Password: []byte("YOUR_PROXY_PASSWORD"),
}

func Socks5Connect(client net.Conn) (dstConn net.Conn, err error) {
	buf := make([]byte, 256)

	// 读取请求命令
	n, err := client.Read(buf[:4])
	if n != 4 || err != nil {
		return nil, errors.New("reading header: " + err.Error())
	}

	ver, cmd, _, atyp := buf[0], buf[1], buf[2], buf[3]
	if ver != 5 || cmd != 1 {
		return nil, errors.New("invalid ver/cmd")
	}

	// 读取请求地址
	addr := ""
	switch atyp {
	case 1:
		log.Printf("client addr type:IPv4\n")
		n, err = io.ReadFull(client, buf[:4])
		if n != 4 || err != nil {
			return nil, errors.New("reading IPv4 addr error:" + err.Error())
		}
		addr = net.IP(buf[:4]).String()
	case 3:
		log.Printf("client addr type:URL\n")
		n, err = io.ReadFull(client, buf[:1])
		if n != 1 || err != nil {
			return nil, errors.New("reading addr Len error:" + err.Error())
		}
		addrLen := int(buf[0])
		n, err = io.ReadFull(client, buf[:addrLen])
		if n != addrLen || err != nil {
			return nil, errors.New("reading addr URL error:" + err.Error())
		}
		addr = string(buf[:addrLen])
	case 4:
		log.Printf("client addr type:IPv6\n")
		n, err = io.ReadFull(client, buf[:16])
		if n != 16 || err != nil {
			return nil, errors.New("reading IPv4 addr error:" + err.Error())
		}
		addr = net.IP(buf[:16]).String()
	default:
		log.Printf("client addr type:Unknown\n")
		return nil, errors.New("invalid atyp")
	}

	n, err = io.ReadFull(client, buf[:2])
	if n != 2 || err != nil {
		return nil, errors.New("reading port error:" + err.Error())
	}
	port := binary.BigEndian.Uint16(buf[:2])

	network := ""
	dst := ""
	switch atyp {
	case 1:
		network = "tcp"
		dst = fmt.Sprintf("%s:%d", addr, port)
	case 3:
		network = "tcp"
		dst = fmt.Sprintf("%s:%d", addr, port)
	case 4:
		network = "tcp6"
		dst = fmt.Sprintf("[%s]:%d", addr, port)
	}

	log.Printf("client addr:%s\n", dst)
	dstConn, err = net.Dial(network, dst)
	if err != nil {
		return nil, errors.New("dial dst error:" + err.Error())
	}

	// 返回连接状态
	n, err = client.Write([]byte{0x05, 0x00, 0x00, 0x01, 0, 0, 0, 0, 0, 0})
	if err != nil {
		dstConn.Close()
		return nil, errors.New("writing error:" + err.Error())
	}

	return dstConn, nil
}

func Socks5Auth(client net.Conn) (err error) {
	buf := make([]byte, 256)

	// 读取 VER 和 NMETHODS
	//n, err := io.ReadFull(client, buf[:2])
	n, err := client.Read(buf[:2])
	if n != 2 || err != nil {
		return errors.New("reading header: " + err.Error())
	}

	ver, nMethods := int(buf[0]), int(buf[1])
	if ver != 5 {
		return errors.New("invalid version")
	}

	// 读取 METHODS 列表
	n, err = io.ReadFull(client, buf[:nMethods])
	if n != nMethods {
		return errors.New("reading methods:" + err.Error())
	}

	log.Printf("client accept methods:%+v\n", buf[:nMethods])

	if bytes.IndexByte(buf[:nMethods], 0x02) < 0 {
		// 如果没有用户名密码，则返回无需认证
		n, err = client.Write([]byte{0x05, 0x00})
		if n != 2 || err != nil {
			return errors.New("writing error:" + err.Error())
		}
	} else {
		// 返回用户名密码认证
		n, err = client.Write([]byte{0x05, 0x02})
		if n != 2 || err != nil {
			return errors.New("writing error:" + err.Error())
		}
		return Socks5UserAuth(client)
	}

	return nil
}

func Socks5UserAuth(client net.Conn) (err error) {
	buf := make([]byte, 256)
	var username, password []byte

	// 读取用户名
	n, err := client.Read(buf[:2])
	if n != 2 || err != nil {
		return errors.New("reading header: " + err.Error())
	}

	ver, nUsername := int(buf[0]), int(buf[1])
	if ver != 1 {
		return errors.New("invalid version")
	}

	n, err = client.Read(buf[:nUsername])
	if n != nUsername {
		return errors.New("reading username error:" + err.Error())
	}

	username = make([]byte, nUsername)
	copy(username, buf[:nUsername])

	// 读取密码
	n, err = client.Read(buf[:1])
	if n != 1 || err != nil {
		return errors.New("reading header: " + err.Error())
	}

	nPassword := int(buf[0])
	n, err = client.Read(buf[:nPassword])
	if n != nPassword {
		return errors.New("reading password error:" + err.Error())
	}

	password = make([]byte, nPassword)
	copy(password, buf[:nPassword])

	log.Printf("user auth username:%s, password:%s\n", username, password)

	if bytes.Equal(username, socks5UserAuthInfo.Username) && bytes.Equal(password, socks5UserAuthInfo.Password) {
		// 认证成功
		n, err = client.Write([]byte{0x01, 0x00})
		if n != 2 || err != nil {
			return errors.New("writing error:" + err.Error())
		}
	} else {
		// 认证失败
		n, err = client.Write([]byte{0x01, 0x01})
		if n != 2 || err != nil {
			return errors.New("writing error:" + err.Error())
		}
		return errors.New("user auth fail")
	}
	return nil
}

func Socks5Forward(client, target net.Conn) {
	forward := func(src, dst net.Conn) {
		defer src.Close()
		defer dst.Close()
		io.Copy(src, dst)
	}
	go forward(client, target)
	go forward(target, client)
}

func Socks5Process(client net.Conn) {
	log.Printf("start socks5 auth handle")

	if err := Socks5Auth(client); err != nil {
		log.Printf("auth error:%+v\n", err)
		client.Close()
		return
	}

	log.Printf("start socks5 connect handle")
	target, err := Socks5Connect(client)
	if err != nil {
		log.Printf("connect error:%+v\n", err)
		client.Close()
		return
	}

	log.Printf("start socks5 forward handle")
	Socks5Forward(client, target)
}

func main() {
	server, err := net.Listen("tcp", ":6543")
	if err != nil {
		log.Printf("Listen  failed: %v\n", err)
		return
	}

	for {
		client, err := server.Accept()
		if err != nil {
			log.Printf("Accept failed: %v\n", err)
			continue
		}
		remoteAddr := client.RemoteAddr().String()
		remoteNetwork := client.RemoteAddr().Network()
		log.Printf("Connection from: [%s]%s\n", remoteNetwork, remoteAddr)

		// 反向代理服务器
		//go ReverseProxyProcess(client)
		// 正向代理服务器-socks5
		go Socks5Process(client)
	}
}

func ReverseProxyProcess(client net.Conn) {
	dstConn, err := net.Dial("tcp", "127.0.0.1:5002")
	if err != nil {
		client.Close()
		log.Printf("Connect Internal failed: %v\n", err)
		return
	}

	Socks5Forward(client, dstConn)
}

```

## 参考链接

[实战：150行Go实现高性能socks5代理](https://mp.weixin.qq.com/s?__biz=MzU4NDA0OTgwOA==&mid=2247484209&idx=1&sn=2e9a2f2000d4430d4c0ccf31b25a1344&chksm=fd9ef6cecae97fd8b264700f10bae0c97557a2cc852180454757877d9c172161227a4fa2f733&scene=21#wechat_redirect)    
[实战：150行Go实现高性能加密隧道](https://mp.weixin.qq.com/s?__biz=MzU4NDA0OTgwOA==&mid=2247484246&idx=1&sn=be8a1e6f36c7b7da22da34854adb022e&chksm=fd9ef6a9cae97fbf983af32a4ff5b20853b716d24ef43edcfda71539ebe8e97ea1ae2ce92245&scene=21#wechat_redirect)    
[实战：+65行Go实现低延迟隧道](https://mp.weixin.qq.com/s/4r1I9-wCLcs2uf8uxXtVvQ)     
[SOCKS Protocol Version 5](https://tools.ietf.org/html/rfc1928)      
[SOCKS](https://zh.wikipedia.org/wiki/SOCKS)          
[socks4 protocol](https://www.openssh.com/txt/socks4.protocol)        

