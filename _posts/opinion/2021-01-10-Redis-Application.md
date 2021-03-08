---
layout: post
title: redis 的一些典型应用 （二）
description: Redis 的典型应用的续集，使用 Redis 的 bitmap 统计日活和月活
category: opinion
---

## 位图

位图(bitmap), 很常见，常用于布隆过滤器等场景，在 Redis 中的一种基本数据类型，可以更加方便的应用。

常用命令有
- `SETBIT key offset value` 在 key 的 offset 偏移量上设置 bit 位，可以是`1`或`0` ，offset 必须大于等于0，小于 2^32 (42亿)，即 512M 大小
- `GETBIT key offset` 获取 key 的 offset 偏移量上获取 bit 位, offset 从 0 开始，中间缺失自动补 0.
- `BITCOUNT key [start] [end]` 计算 key 中设定为1 的比特位数，可以指定计算的起始位置。
- `BITPOS key bit [start] [end]` 返回 key 中第一个比特位为 bit 的位置，可以是`1`或`0`。
- `BITOP operation destkey key [key …]` 对多个 key 的值做位计算，operation 可以是 `AND`, `OR`, `NOT`, `XOR` 四种中的一种，将结果保存在 `destkey` 中。
- `BITFIELD key [GET type offset] [SET type offset value] [INCRBY type offset increment] [OVERFLOW WRAP|SAT|FAIL]` 对 key 上取片段的值进行整体操作，比如整体加1，溢出丢失。

感觉使用上缺少了一个功能，就是获取全部输出，以及获取全部输出组成的整数值。
> 可以通过 `bitfield` 计算得出

需要注意点的是，`bitcount` 和 `bitpos` 的区间范围，单位是 byte 而不是 bit ，也就是说是字节级别的区间查找，而不是比特位的范围内。

## 使用

设置 `twenty` 为整数20的位图 `00010100`, 即20的无符号32位二进制表示 `00010100`, 注意 offset 从 0 开始数。

```
127.0.0.1:6379> exists twenty
(integer) 0
127.0.0.1:6379> setbit twenty 3 1
(integer) 0
127.0.0.1:6379> setbit twenty 5 1
(integer) 0
127.0.0.1:6379> getbit twenty 0
(integer) 0
127.0.0.1:6379> getbit twenty 1
(integer) 0
127.0.0.1:6379> getbit twenty 2
(integer) 0
127.0.0.1:6379> getbit twenty 3
(integer) 1
127.0.0.1:6379> getbit twenty 4
(integer) 0
127.0.0.1:6379> getbit twenty 5
(integer) 1
127.0.0.1:6379> bitcount twenty
(integer) 2
127.0.0.1:6379> bitpos twenty 1
(integer) 3
127.0.0.1:6379> bitpos twenty 0
(integer) 0
```

其实可以通过 `bitfield` 获取到，根据 8bit读取就是 `20(00010100)`，根据 16bit 读取就是 `5120(0001010000000000)`

```
127.0.0.1:6379> bitfield twenty get i8 0
1) (integer) 20
127.0.0.1:6379> bitfield twenty get i16 0
1) (integer) 5120
```

或者将 20的位图 `00010100` 和 15的位图 `00001111` 进行位运算，异或结果为27 `00011011`
> python 中使用 `'{:08b}'.format(20)` 和 `'{:08b}'.format(15)` 快速查看二进制表示

```
127.0.0.1:6379> bitfield twenty get i8 0
1) (integer) 20
127.0.0.1:6379> bitfield fif get i8 0
1) (integer) 15
127.0.0.1:6379> bitop XOR res twenty fif
(integer) 1
127.0.0.1:6379> bitfield res get i8 0
1) (integer) 27
```

有了以上的基础知识之后，我们可以运用 bitmap 进行一些实际的使用。

## 内存挑战

在 Redis 中使用位图是不会自动压缩的，也就是说如果你真的在高位上设置了一个值的话，地位上会全部设置为0，并实际占用这么大的内存空间。

比如在第一亿位上设置为1，可以计算内存占用应该是会有 `11.9M` 的内存，在第十亿位上设置为1，会占用内存 `119M` 

```
127.0.0.1:6379> info
# Server
redis_version:5.0.7
...
# Memory
used_memory:9305952
used_memory_human:8.87M
used_memory_rss:561152
used_memory_rss_human:548.00K
127.0.0.1:6379> setbit sobig 100000000 1
(integer) 0
127.0.0.1:6379> info
# Server
redis_version:5.0.7
...
# Memory
used_memory:21807344
used_memory_human:20.80M
used_memory_rss:13377536
used_memory_rss_human:12.76M
```

在设置一亿的位图之后，内存占用增加了12M，确实和预期一致。

```
127.0.0.1:6379> setbit sosobig 1000000000 1
(integer) 0
127.0.0.1:6379> info memory
# Memory
used_memory:146808480
used_memory_human:140.01M
used_memory_rss:138424320
used_memory_rss_human:132.01M
```

在设置十亿的位图之后，内存占用增加了120M，再次尝试设计百亿位图。

```
127.0.0.1:6379> setbit sososobig 10000000000 1
(error) ERR bit offset is not an integer or out of range
127.0.0.1:6379> setbit sososobig 4294967296 1
(error) ERR bit offset is not an integer or out of range
127.0.0.1:6379> setbit sososobig 4294967295 1
(integer) 0
```

偏移量超限，上限应该是 `2^32-1` 即`4294967295`，32位无符号数最大值, 42亿多, 内存占用 512M。

此时在系统中查看 Redis 内存占用，已经达到 653M

```
$ top -l 1|grep redis
64439  redis-cli        0.0  00:00.03 1     0   14     524K  0B    148K  64439 51260 sleeping *0[1]       0.00000 0.00000    501 479      86     37        14        1709      79        428       36      0        0.0   0      0      bytedance              N/A    N/A   N/A   N/A   N/A   N/A
1061   redis-server     0.0  00:43.15 4     0   17     653M  0B    139M  1061  1     sleeping *0[1]       0.00000 0.00000    501 170413   256    1073925   536938    1075342   1074019   823812    378     146378   0.0   0      0      bytedance              N/A    N/A   N/A   N/A   N/A   N/A
```

## 统计活跃天数

统计某个用户一年内的活跃天数

```
# -*- coding: utf-8 -*-

import random
import redis
import datetime
import calendar


redis_client = redis.Redis(password="Redispassword")


def get_day_of_year(datetime_day):
    return datetime_day.timetuple().tm_yday


def parse_day_of_year(year_and_day):
    return datetime.datetime.strptime(year_and_day, "%Y-%j")


def random_data(user_key):
    # 2020 年有366天
    for count in range(random.randrange(366)):
        day = random.randint(1, 366)
        redis_client.setbit(user_key, day, 1)


def show_data(user_key):
    # 按月展示
    for month in range(1, 13):
        days = calendar.monthrange(2020, month)[1]
        month_active_days = []
        for day in range(1, days + 1):
            offset = get_day_of_year(datetime.datetime.strptime("2020-{}-{}".format(month, day), "%Y-%m-%d"))
            month_active_days.append(redis_client.getbit(user_key, offset))

        datetime_month = datetime.datetime.strptime("2020-{}".format(month), "%Y-%m")
        print(
            "{}(Active Days:{:3d}):{}".format(
                datetime_month.strftime("%Y-%b"),
                sum(month_active_days),
                "".join(map(lambda x: "*" if x else "_", month_active_days)),
            )
        )


def check_active(user_key, datetime_day):
    active = redis_client.getbit(user_key, get_day_of_year(datetime_day))
    print(
        "{}: user is active!".format(datetime_day.strftime("%Y-%m-%d"))
        if active
        else "{}: user is not active~".format(datetime_day.strftime("%Y-%m-%d"))
    )


def first_login(user_key):
    day = redis_client.bitpos(user_key, 1)
    datetime_day = parse_day_of_year("2020-{}".format(day))
    print("First Login Time:{}".format(datetime_day.strftime("%Y-%m-%d")))


def total_login(user_key):
    print("Total Active Days:{}".format(redis_client.bitcount(user_key)))


if __name__ == '__main__':
    user_id = int(random.random() * 100000000)
    key = "user_id:{}".format(user_id)
    random_data(key)

    first_login(key)
    total_login(key)
    show_data(key)
    for i in range(10):
        random_day = random.randint(1, 366)
        random_day = parse_day_of_year("2020-{}".format(random_day))
        check_active(key, random_day)

```

查看效果

```
First Login Time:2020-01-02
Total Active Days:190
2020-Jan(Active Days: 15):_*_____*__***_***_****_**_____*
2020-Feb(Active Days: 14):**_*___*_____**_**_***_***___
2020-Mar(Active Days: 17):*____***__*_**_**_***_*___*_***
2020-Apr(Active Days: 16):___*__**___*****_****__**___**
2020-May(Active Days: 14):*_***_**___________**__***_***_
2020-Jun(Active Days: 16):**_***_____*_*_*****_**__*___*
2020-Jul(Active Days: 16):**___*____***_**_*******______*
2020-Aug(Active Days: 20):****_*_*_*___*_***_***_*_****_*
2020-Sep(Active Days: 14):___*_***_**____**__*_____*****
2020-Oct(Active Days: 17):*_***__*_*_***_**__**_*_**_*___
2020-Nov(Active Days: 15):_*_*_*_****__**__**__**_*____*
2020-Dec(Active Days: 16):_*_****__*_____*****__**_**_*__
2020-09-23: user is not active~
2020-09-07: user is active!
2020-07-17: user is not active~
2020-04-30: user is active!
2020-04-28: user is not active~
2020-01-15: user is active!
2020-01-02: user is active!
2020-12-26: user is active!
2020-06-18: user is active!
2020-06-03: user is not active~
```

使用 bitmap 统计单用户的活跃天数，一年也只需要 45个字节，是不是非常节省。

但是如果用户量大的情况下，百万用户，数据占用就比较多了，而且使用也不太方便。


## 统计日活和月活

统计百万日活下的千万月活用户，计算月登陆天数最多的用户。

在随机生成数据的时候，对 Redis 的 QPS 达到几千甚至上万，实际使用内存不多，但是会不停的内存增长达到上G，在停下之后恢复正常占用的几十M，可能是Redis buffer 缓冲区？

```python
# -*- coding: utf-8 -*-

import redis
import random
import datetime


redis_client = redis.Redis(password="Redispassword")
day_key_pattern = "daily_key:{}"
month_key_pattern = "monthly_key:{}"
year_key_pattern = "yearly:{}"


def get_day_of_year(datetime_day):
    return datetime_day.timetuple().tm_yday


def parse_day_of_year(year_and_day):
    return datetime.datetime.strptime(year_and_day, "%Y-%j")


def random_data():
    for day in range(22, 32):
        # 日活在百万
        datetime_day = parse_day_of_year("2020-{}".format(day))
        day_key = day_key_pattern.format(datetime_day.strftime("%Y-%m-%d"))
        month_key = month_key_pattern.format(datetime_day.strftime("%Y-%m"))
        # year_key = year_key_pattern.format(datetime_day.strftime("%Y"))
        for _ in range(random.randrange(2000000)):
            user_id = random.randrange(10000000)
            redis_client.setbit(day_key, user_id, 1)
            redis_client.setbit(month_key, user_id, 1)
            # redis_client.setbit(year_key, user_id, 1)


def show_data():
    daily_user_count = []
    for day in range(1, 32):
        datetime_day = parse_day_of_year("2020-{}".format(day))
        day_str = datetime_day.strftime("%Y-%m-%d")
        dau = redis_client.bitcount(day_key_pattern.format(day_str))

        daily_user_count.append(dau)
        print("{}({:8d}):{}".format(day_str, dau, '*' * int(dau / 100000)))

    # print("Daily user:{}".format(daily_user_count))
    print("Average user({:8d}):{}".format(sum(daily_user_count) / 31, '*' * int(sum(daily_user_count) / 31 / 100000)))
    monthly_key = month_key_pattern.format(datetime_day.strftime("%Y-%m"))
    print(
        "Monthly user({:8d}):{}".format(
            redis_client.bitcount(monthly_key), '*' * (redis_client.bitcount(monthly_key) / 100000)
        )
    )


def count_monthly_user():
    monthly_user_key = "monthly_user_key"
    daily_user_key = []

    for day in range(1, 32):
        datetime_day = parse_day_of_year("2020-{}".format(day))
        day_str = datetime_day.strftime("%Y-%m-%d")
        daily_user_key.append(day_key_pattern.format(day_str))

    redis_client.bitop("OR", monthly_user_key, *daily_user_key)
    print(
        "Monthly user({:8d}):{}".format(
            redis_client.bitcount(monthly_user_key), '*' * (redis_client.bitcount(monthly_user_key) / 100000)
        )
    )


def continuous_active_user():
    continuous_active_user = "continuous_active_user"
    daily_user_key = []

    for day in range(1, 32):
        datetime_day = parse_day_of_year("2020-{}".format(day))
        day_str = datetime_day.strftime("%Y-%m-%d")
        daily_user_key.append(day_key_pattern.format(day_str))

    redis_client.bitop("AND", continuous_active_user, *daily_user_key)
    print(
        "Continuous user({:8d}):{}".format(
            redis_client.bitcount(continuous_active_user),
            '*' * (redis_client.bitcount(continuous_active_user) / 100000),
        )
    )


if __name__ == '__main__':
    # random_data()
    show_data()
    count_monthly_user()
    continuous_active_user()

```

查看效果

```
2020-01-01( 1628322):****************
2020-01-02(  744877):*******
2020-01-03( 1563564):***************
2020-01-04( 1311508):*************
2020-01-05( 1730680):*****************
2020-01-06(   52108):
2020-01-07(  320483):***
2020-01-08( 1072159):**********
2020-01-09( 1385716):*************
2020-01-10(  776542):*******
2020-01-11(  778230):*******
2020-01-12( 1420932):**************
2020-01-13( 1450910):**************
2020-01-14(  644336):******
2020-01-15(  723175):*******
2020-01-16( 1407733):**************
2020-01-17(  679196):******
2020-01-18(  394180):***
2020-01-19( 1664516):****************
2020-01-20( 1117985):***********
2020-01-21(  221111):**
2020-01-22( 1434690):**************
2020-01-23(   60968):
2020-01-24(  202462):**
2020-01-25( 1131955):***********
2020-01-26( 1749595):*****************
2020-01-27(  865355):********
2020-01-28(   57406):
2020-01-29( 1066695):**********
2020-01-30( 1781939):*****************
2020-01-31(  442681):****
Average user(  963935):*********
Monthly user( 9591795):***********************************************************************************************
Monthly user( 9591795):***********************************************************************************************
Continuous user(       0):
```

## 监控

不得不吐槽一下网上的几个 Redis 监控工具，都太老了吧，虽然已经开源，但是无人维护，年久失修。
- redis-stat: 只有实时统计，数据不够详细，不过也有一个命令行的监控，但是挺炫酷的。
- RedisLive: 几个 pr 也不和，前端依赖缺失，Google chat css 404 了，实时命令执行数无数据。
- redmon: 功能也比较少，不够 modern，不够 fashion 。
- Redis-faina: 对 Redis monitor 的分析，没有 web 页面，不能实时统计 QPS 。
- redis_exporter: 只提供 grafana 打点，需要配合其他工具使用。
- redis-monitor: 我只能说，求求你们了，前端发展太快了，css 和 js 依赖还是放在本地吧，不然资源随时可能失效，比如 Google 的一些公共依赖。
- RedisPAPA: 网上那些乱七八糟的 cdn 还是不要用了，这不就完了嘛，又挂了一个。好不容易找到之后，版本又对不上。幸好 docker 镜像里的还是干净能用的，同样数据比较少，而且感觉数据有些不对。
- Redis Manager: Java 开发，配置有点复杂


## 参考链接

[聊聊redis的监控工具](https://juejin.cn/post/6844903683390439438)     
[位图](http://redisdoc.com/bitmap/index.html)    
[一看就懂系列之 详解redis的bitmap在亿级项目中的应用](https://blog.csdn.net/u011957758/article/details/74783347)      
[利用 Redis 位运算快速实现签到统计功能](https://gist.github.com/lifeblood/75287f739ddf9a0b9b5e345bd87518eb)      
[redis-bitmap在签到和统计状态项目中的妙用](https://segmentfault.com/a/1190000023966711)          
[Redis：Bitmaps使用场景-用户签到、统计活跃用户、用户在线状态](https://blog.csdn.net/fly910905/article/details/82629687)     
[利用redis的bitmap实现用户签到功能](https://zhuanlan.zhihu.com/p/83604814)        
[Redis中bitmap的妙用](https://segmentfault.com/a/1190000008188655)        
 
