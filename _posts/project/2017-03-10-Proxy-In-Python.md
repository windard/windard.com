---
layout: post
title: 使用 Python socket 完成端口转发
category: project
description: Nginx ，iptables 都能实现端口转发，实现反向代理，现在使用 Python socket 来试一下。
---

## 端口转发

端口转发，也被称为端口映射，可以用来正向代理，反向代理。它的应用很广泛，最主要的就是当你无法直接访问某个网址时，可以使用通过转发，或者代理访问。

本文使用 Python socket 实现的 端口转发，只能实现简单的流量转发，并不能对底层数据进行处理，也没有对任何代理数据进行任何的截取分析，不能实现多通道协议（如 FTP）的转发。

### 最简单的实现

```
# coding=utf-8

import time
import socket
import urllib
import urlparse

desc_host = '127.0.0.1'
desc_port = 8080

source_url = "http://127.0.0.1:5002/"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((desc_host, desc_port))

print "Proxying to %s:%s ..."%(desc_host, desc_port)

while 1:
    server.listen(5)
    conn, addr = server.accept()
    request = conn.recv(1024).split(" ")[1]
    page = urllib.urlopen(urlparse.urljoin(source_url + request)).read()
    print time.strftime('%Y-%m-%d %H:%M:%S')," [%s:%s] %s"%(addr[0], addr[1], request)
    conn.sendall(page)
    conn.close()
```

能够实现最基础的 HTTP GET 请求转发，虽然没有 headers ，也没有 cookies 保持登陆，但是起码完成了一小步。

### 使用 socket 实现

```
# coding=utf-8

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
            break
            print "recv error"

        try:
            recver.sendall(data)
        except:
            break
            print "send error"
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
    proxy_server.listen(50)

    print "Proxying from %s:%s to %s:%s ..."%(source_host, source_port, desc_host, desc_port)

    while 1:
        conn, addr = proxy_server.accept()
        print "received connect from %s:%s"%(addr[0], addr[1])
        threading.Thread(target=proxy, args=(conn, )).start()

if __name__ == '__main__':
    main()
```

这是都纯使用 socket 实现的转发，功能完成。

### TCP 协议转发

```
# -*- coding: utf-8 -*-
# tcp mapping created by hutaow(hutaow.com) at 2014-08-31

import sys
import socket
import logging
import threading


# 端口映射配置信息
CFG_REMOTE_IP = '192.168.137.128'
CFG_REMOTE_PORT = 21
CFG_LOCAL_IP = '0.0.0.0'
CFG_LOCAL_PORT = 10086

# 接收数据缓存大小
PKT_BUFF_SIZE = 2048

logger = logging.getLogger("Proxy Logging")
formatter = logging.Formatter('%(name)-12s %(asctime)s %(levelname)-8s %(lineno)-4d %(message)s', '%Y %b %d %a %H:%M:%S',)

stream_handler = logging.StreamHandler(sys.stderr)
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

logger.setLevel(logging.DEBUG)

# 单向流数据传递
def tcp_mapping_worker(conn_receiver, conn_sender):
    while True:
        try:
            data = conn_receiver.recv(PKT_BUFF_SIZE)
        except Exception:
            logger.debug('Connection closed.')
            break

        if not data:
            logger.info('No more data is received.')
            break

        try:
            conn_sender.sendall(data)
        except Exception:
            logger.error('Failed sending data.')
            break

        # logger.info('Mapping data > %s ' % repr(data))
        logger.info('Mapping > %s -> %s > %d bytes.' % (conn_receiver.getpeername(), conn_sender.getpeername(), len(data)))

    conn_receiver.close()
    conn_sender.close()

    return

# 端口映射请求处理
def tcp_mapping_request(local_conn, remote_ip, remote_port):
    remote_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        remote_conn.connect((remote_ip, remote_port))
    except Exception:
        local_conn.close()
        logger.error('Unable to connect to the remote server.')
        return

    threading.Thread(target=tcp_mapping_worker, args=(local_conn, remote_conn)).start()
    threading.Thread(target=tcp_mapping_worker, args=(remote_conn, local_conn)).start()

    return

# 端口映射函数
def tcp_mapping(remote_ip, remote_port, local_ip, local_port):
    local_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    local_server.bind((local_ip, local_port))
    local_server.listen(5)

    logger.debug('Starting mapping service on ' + local_ip + ':' + str(local_port) + ' ...')

    while True:
        try:
            (local_conn, local_addr) = local_server.accept()
        except KeyboardInterrupt, Exception:
            local_server.close()
            logger.debug('Stop mapping service.')
            break

        threading.Thread(target=tcp_mapping_request, args=(local_conn, remote_ip, remote_port)).start()

        logger.debug('Receive mapping request from %s:%d.' % local_addr)

    return

# 主函数
if __name__ == '__main__':
    tcp_mapping(CFG_REMOTE_IP, CFG_REMOTE_PORT, CFG_LOCAL_IP, CFG_LOCAL_PORT)
```

测试对 HTTP，SSH 协议都能实现完美转发。

### 既能转发 TCP，还能转发 UDP

```
#-* -coding: UTF-8 -* -

'''

Created on 2012-5-8

@author: qh

'''
import time
import socket
import threading

def log(strLog):
    strs = time.strftime("%Y-%m-%d %H:%M:%S")
    print strs  +" -> "+strLog

class pipethread(threading.Thread):
    '''
    classdocs
    '''
    def __init__(self,source,sink):
        '''
        Constructor
        '''
        threading.Thread.__init__(self)
        self.source = source
        self.sink = sink
        log("New Pipe create:%s->%s" % (self.source.getpeername(),self.sink.getpeername()))

    def run(self):
        while True:
            try:
                data = self.source.recv(1024)
                if not data: break
                self.sink.send(data)
            except Exception ,ex:
                log("redirect error:"+str(ex))
                break

        self.source.close()
        self.sink.close()

class portmap(threading.Thread):
    def __init__(self, port, newhost, newport, local_ip = ''):
        threading.Thread.__init__(self)
        self.newhost = newhost
        self.newport = newport
        self.port = port
        self.local_ip = local_ip
        self.protocol = 'tcp'
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.sock.bind((self.local_ip, port))
        self.sock.listen(5)
        log("start listen protocol:%s,port:%d " % (self.protocol, port))

    def run(self):
        while True:
            newsock, address = self.sock.accept()
            log("new connection->protocol:%s,local port:%d,remote address:%s" % (self.protocol, self.port,address[0]))
            fwd = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            try:
                fwd.connect((self.newhost,self.newport))
            except Exception ,ex:
                log("connet newhost error:"+str(ex))
                break
            p1 = pipethread(newsock, fwd)
            p1.start()
            p2 = pipethread(fwd, newsock)
            p2.start()

class pipethreadUDP(threading.Thread):
    def __init__(self, connection, connectionTable, table_lock):
        threading.Thread.__init__(self)
        self.connection = connection
        self.connectionTable = connectionTable
        self.table_lock = table_lock
        log('new thread for new connction')

    def run(self):
        while True:
            try:
                data,addr = self.connection['socket'].recvfrom(4096)
                #log('recv from addr"%s' % str(addr))
            except Exception, ex:
                log("recvfrom error:"+str(ex))
                break
            try:
                self.connection['lock'].acquire()
                self.connection['Serversocket'].sendto(data,self.connection['address'])
                #log('sendto address:%s' % str(self.connection['address']))
            except Exception ,ex:
                log("sendto error:"+str(ex))
                break
            finally:self.connection['lock'].release()
            self.connection['time'] = time.time()
        self.connection['socket'].close()
        log("thread exit for: %s" % str(self.connection['address']))
        self.table_lock.acquire()
        self.connectionTable.pop(self.connection['address'])
        self.table_lock.release()
        log('Release udp connection for timeout:%s' % str(self.connection['address']))

class portmapUDP(threading.Thread):
    def __init__(self, port, newhost, newport, local_ip = ''):
        threading.Thread.__init__(self)
        self.newhost = newhost
        self.newport = newport
        self.port = port
        self.local_ip = local_ip
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.sock.bind((self.local_ip,port))
        self.connetcTable = {}
        self.port_lock = threading.Lock()
        self.table_lock = threading.Lock()
        self.timeout = 300
        #ScanUDP(self.connetcTable,self.table_lock).start()
        log('udp port redirect run->local_ip:%s,local_port:%d,remote_ip:%s,remote_port:%d' % (local_ip,port,newhost,newport))

    def run(self):
        while True:
            data,addr = self.sock.recvfrom(4096)
            connection = None
            newsock = None
            self.table_lock.acquire()
            connection = self.connetcTable.get(addr)
            newconn = False
            if connection is None:
                connection = {}
                connection['address'] = addr
                newsock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
                newsock.settimeout(self.timeout)
                connection['socket'] = newsock
                connection['lock'] = self.port_lock
                connection['Serversocket'] = self.sock
                connection['time'] = time.time()
                newconn = True

                log('new connection:%s' % str(addr))
            self.table_lock.release()
            try:
                connection['socket'].sendto(data,(self.newhost,self.newport))
            except Exception ,ex:
                log("sendto error:"+str(ex))
                #break
            if newconn:
                self.connetcTable[addr] = connection
                t1=pipethreadUDP(connection,self.connetcTable,self.table_lock)
                t1.start()
        log('main thread exit')
        for key in self.connetcTable.keys():
            self.connetcTable[key]['socket'].close()

if __name__=='__main__':

    myp = portmap(12345, '127.0.0.1', 5002)
    myp.start()

```

TCP 亲测可用，UDP 未曾测试。

### 最后一个

```
# -*- coding: utf-8 -*-

'''
#!/usr/bin/env python
# coding=utf-8

"""
filename: rtcp.py
@desc:
利用 Python 的 socket 端口转发，用于远程维护
如果连接不到远程，会 sleep 36s，最多尝试 200（即两小时）

@usage:
./rtcp.py stream1 stream2
stream 为：l:port 或 c:host:port
l:port 表示监听指定的本地端口
c:host:port 表示监听远程指定的端口

@author: watercloud, zd, knownsec team
@web: www.knownsec.com, blog.knownsec.com
@date: 2009-7
"""

import socket
import sys
import threading
import time


streams = [None, None]  # 存放需要进行数据转发的两个数据流（都是 SocketObj 对象）
debug = 1  # 调试状态 0 or 1


def _usage():
    print('Usage: ./rtcp.py stream1 stream2\nstream: l:port  or c:host:port')


def _get_another_stream(num):
    """
    从streams获取另外一个流对象，如果当前为空，则等待
    """
    if num == 0:
        num = 1
    elif num == 1:
        num = 0
    else:
        raise 'ERROR'

    while True:
        if streams[num] == 'quit':
            print('can not connect to the target, quit now!')
            sys.exit(1)

        if streams[num] is not None:
            return streams[num]
        else:
            time.sleep(1)


def _xstream(num, s1, s2):
    """
    交换两个流的数据
    num为当前流编号,主要用于调试目的，区分两个回路状态用。
    """
    try:
        while True:
            # 注意，recv 函数会阻塞，直到对端完全关闭（close 后还需要一定时间才能关闭，最快关闭方法是 shutdow）
            buff = s1.recv(1024)
            if debug > 0:
                print('%d recv' % num)
            if len(buff) == 0:  # 对端关闭连接，读不到数据
                print('%d one closed' % num)
                break
            s2.sendall(buff)
            if debug > 0:
                print('%d sendall' % num)
    except:
        print('%d one connect closed.' % num)

    try:
        s1.shutdown(socket.SHUT_RDWR)
        s1.close()
    except:
        pass

    try:
        s2.shutdown(socket.SHUT_RDWR)
        s2.close()
    except:
        pass

    streams[0] = None
    streams[1] = None
    print('%d CLOSED' % num)


def _server(port, num):
    """
    处理服务情况，num 为流编号（第 0 号还是第 1 号）
    """
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind(('0.0.0.0', port))
    srv.listen(1)
    while True:
        conn, addr = srv.accept()
        print('connected from: %s' % str(addr))
        streams[num] = conn  # 放入本端流对象
        s2 = _get_another_stream(num)  # 获取另一端流对象
        _xstream(num, conn, s2)


def _connect(host, port, num):
    """处理连接，num 为流编号（第 0 号还是第 1 号）

    @note: 如果连接不到远程，会 sleep 36s，最多尝试 200（即两小时）
    """
    not_connet_time = 0
    wait_time = 36
    try_cnt = 199
    while True:
        if not_connet_time > try_cnt:
            streams[num] = 'quit'
            print('not connected')
            return None

        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            conn.connect((host, port))
        except Exception:
            print('can not connect %s:%s!' % (host, port))
            not_connet_time += 1
            time.sleep(wait_time)
            continue

        print('connected to %s:%i' % (host, port))
        streams[num] = conn  # 放入本端流对象
        s2 = _get_another_stream(num)  # 获取另一端流对象
        _xstream(num, conn, s2)


def main():
    if len(sys.argv) != 3:
        _usage()
        sys.exit(1)
    tlist = []  # 线程列表，最终存放两个线程对象
    targv = [sys.argv[1], sys.argv[2]]
    for i in [0, 1]:
        s = targv[i]  # stream 描述 c:ip:port 或 l:port
        sl = s.split(':')
        if len(sl) == 2 and (sl[0] == 'l' or sl[0] == 'L'):  # l:port
            t = threading.Thread(target=_server, args=(int(sl[1]), i))
            tlist.append(t)
        elif len(sl) == 3 and (sl[0] == 'c' or sl[0] == 'C'):  # c:host:port
            t = threading.Thread(target=_connect, args=(sl[1], int(sl[2]), i))
            tlist.append(t)
        else:
            _usage()
            sys.exit(1)

    for t in tlist:
        t.start()
    for t in tlist:
        t.join()
    sys.exit(0)


if __name__ == '__main__':
    main()
```

知道创宇出品，[Github 项目地址](https://github.com/knownsec/rtcp)

使用 asyncore 实现的端口转发

```
# -*- coding: utf-8 -*-

import socket
import asyncore


class Receiver(asyncore.dispatcher):
    def __init__(self, conn):
        asyncore.dispatcher.__init__(self, conn)
        self.from_remote_buffer = b''
        self.to_remote_buffer = b''
        self.sender = None

    def handle_connect(self):
        pass

    def handle_read(self):
        read = self.recv(4096)
        # print '%04i -->'%len(read)
        self.from_remote_buffer += read

    def writable(self):
        return len(self.to_remote_buffer) > 0

    def handle_write(self):
        sent = self.send(self.to_remote_buffer)
        # print '%04i <--'%sent
        self.to_remote_buffer = self.to_remote_buffer[sent:]

    def handle_close(self):
        self.close()
        if self.sender:
            self.sender.close()


class Sender(asyncore.dispatcher):
    def __init__(self, receiver, remoteaddr, remoteport):
        asyncore.dispatcher.__init__(self)
        self.receiver = receiver
        receiver.sender = self
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((remoteaddr, remoteport))

    def handle_connect(self):
        pass

    def handle_read(self):
        read = self.recv(4096)
        # print '<-- %04i'%len(read)
        self.receiver.to_remote_buffer += read

    def writable(self):
        return len(self.receiver.from_remote_buffer) > 0

    def handle_write(self):
        sent = self.send(self.receiver.from_remote_buffer)
        # print '--> %04i'%sent
        self.receiver.from_remote_buffer = self.receiver.from_remote_buffer[sent:]

    def handle_close(self):
        self.close()
        self.receiver.close()


class Forwarder(asyncore.dispatcher):
    def __init__(self, ip, port, remoteip, remoteport, backlog=5):
        asyncore.dispatcher.__init__(self)
        self.remoteip = remoteip
        self.remoteport = remoteport
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((ip, port))
        self.listen(backlog)

    def handle_accept(self):
        conn, addr = self.accept()
        # print '--- Connect --- '
        self.log_info('Connected from %s:%s to %s:%s' % (addr[0], addr[1], self.remoteip, self.remoteport))
        Sender(Receiver(conn), self.remoteip, self.remoteport)

if __name__ == '__main__':
    f = Forwarder('127.0.0.1', 5089, '127.0.0.1', 5002)
    asyncore.loop()

```

整篇博客，只有前面两个是本人写的，后面都是转载。。。实在惭愧。

