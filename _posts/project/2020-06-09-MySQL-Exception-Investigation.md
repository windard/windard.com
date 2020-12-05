---
layout: post
title: MySQL 异常排查
description:  线上一些常见的 MySQL 问题分析总结
category: project
keywords: MySQL 事务
---

## 引入

首先介绍一下 MySQL 的事务，和事务的四大特性。一般 MySQL 正常使用，也不会出现什么问题，主要基本上都在 事务 造成的问题。

### 事务

事务，是指单个逻辑单元的一系列操作，需要符合 ACID 四大特性。
- A(Atomic)       原子性，事务中的一系列操作必须符合原子性，要么全部成功，要么全部失败，不能一样一半。
- C(Consist)      一致性，数据库在事务执行前是一致的，在事务执行后也必须是一致的，不能对账不平。
- I(Isoland)      隔离性，多个事务之间，不会互相影响。
- D(Duration)     持久性，事务完成后，如果服务器宕机，不会影响事务结果。

其中隔离性是考的最多的，隔离性的几个等级
- RU(Read Uncommited)     未提交读
- RC(Read Commited)       已提交读
- RR(Read Repeated)       可重复读
- S(Serializable)         可串行化

使用 MCVV(Multiply Version Concurrent Control) 多版本并发控制来实现不同的隔离等级。

## 索引

每次都要问候选人事务和索引，结果自己连索引是怎么建的都搞不清楚，这就是拎不清吖。

## 获取锁超时

### 异常现场

```
ERROR 1205 (HY000): Lock wait timeout exceeded; try restarting transaction
```

一般出现这个问题的原因是因为有另一个事务获取锁，当前事务在获取锁的时候，等待超时，抛出异常，在 MySQL 中获取锁的超时时间是 50 秒。

复现一下也很简单。

首先在一个 MySQL 连接中，开启事务，然后锁定全表。

```
mysql> BEGIN;
mysql> select * from note for update;
```

然后在另一个 链接中，更新字段，就会等待直到超时最终报错。

```
mysql> update note set content="改一下-确实很简朴" where id = 9;
ERROR 1205 (HY000): Lock wait timeout exceeded; try restarting transaction
```

在事务中 `rollback` 回滚，`commit` 提交，都可以结束当前事务。

### 如何解决

##### 查进程

找到获取锁的进程 `show full processlist;`

```
mysql> show full processlist;
+----+-----------------+-----------+----------+---------+--------+------------------------+-----------------------+
| Id | User            | Host      | db       | Command | Time   | State                  | Info                  |
+----+-----------------+-----------+----------+---------+--------+------------------------+-----------------------+
|  4 | event_scheduler | localhost | NULL     | Daemon  | 102717 | Waiting on empty queue | NULL                  |
| 11 | root            | localhost | nodetodo | Query   |      0 | starting               | show full processlist |
| 12 | root            | localhost | nodetodo | Sleep   |    200 |                        | NULL                  |
+----+-----------------+-----------+----------+---------+--------+------------------------+-----------------------+
3 rows in set (0.00 sec)
```

可以看到 12 号进程也是在 nodetodo 表上占用，而且占用时间过长 `kill 12` 就好了。

##### 查事务

查看当前活动事务，找到长期持有未释放锁的事务 `select * from information_schema.innodb_trx;`

```
mysql> select * from information_schema.innodb_trx;
+-----------------+-----------+---------------------+-----------------------+------------------+------------+---------------------+---------------------------------------------+---------------------+-------------------+-------------------+------------------+-----------------------+-----------------+-------------------+-------------------------+---------------------+-------------------+------------------------+----------------------------+---------------------------+---------------------------+------------------+----------------------------+
| trx_id          | trx_state | trx_started         | trx_requested_lock_id | trx_wait_started | trx_weight | trx_mysql_thread_id | trx_query                                   | trx_operation_state | trx_tables_in_use | trx_tables_locked | trx_lock_structs | trx_lock_memory_bytes | trx_rows_locked | trx_rows_modified | trx_concurrency_tickets | trx_isolation_level | trx_unique_checks | trx_foreign_key_checks | trx_last_foreign_key_error | trx_adaptive_hash_latched | trx_adaptive_hash_timeout | trx_is_read_only | trx_autocommit_non_locking |
+-----------------+-----------+---------------------+-----------------------+------------------+------------+---------------------+---------------------------------------------+---------------------+-------------------+-------------------+------------------+-----------------------+-----------------+-------------------+-------------------------+---------------------+-------------------+------------------------+----------------------------+---------------------------+---------------------------+------------------+----------------------------+
| 5647            | RUNNING   | 2020-06-09 20:13:22 | NULL                  | NULL             |          2 |                  12 | NULL                                        | NULL                |                 0 |                 1 |                2 |                  1136 |               1 |                 0 |                       0 | REPEATABLE READ     |                 1 |                      1 | NULL                       |                         0 |                         0 |                0 |                          0 |
| 281479655995944 | RUNNING   | 2020-06-09 20:22:37 | NULL                  | NULL             |          0 |                  11 | select * from information_schema.innodb_trx | NULL                |                 0 |                 0 |                0 |                  1136 |               0 |                 0 |                       0 | REPEATABLE READ     |                 1 |                      1 | NULL                       |                         0 |                         0 |                0 |                          0 |
+-----------------+-----------+---------------------+-----------------------+------------------+------------+---------------------+---------------------------------------------+---------------------+-------------------+-------------------+------------------+-----------------------+-----------------+-------------------+-------------------------+---------------------+-------------------+------------------------+----------------------------+---------------------------+---------------------------+------------------+----------------------------+
2 rows in set (0.04 sec)
```

或者换一个展示方式 和上面👆是同样的数据

```
mysql> select * from information_schema.innodb_trx\G
*************************** 1. row ***************************
                    trx_id: 5647
                 trx_state: RUNNING
               trx_started: 2020-06-09 20:13:22
     trx_requested_lock_id: NULL
          trx_wait_started: NULL
                trx_weight: 2
       trx_mysql_thread_id: 12
                 trx_query: NULL
       trx_operation_state: NULL
         trx_tables_in_use: 0
         trx_tables_locked: 1
          trx_lock_structs: 2
     trx_lock_memory_bytes: 1136
           trx_rows_locked: 1
         trx_rows_modified: 0
   trx_concurrency_tickets: 0
       trx_isolation_level: REPEATABLE READ
         trx_unique_checks: 1
    trx_foreign_key_checks: 1
trx_last_foreign_key_error: NULL
 trx_adaptive_hash_latched: 0
 trx_adaptive_hash_timeout: 0
          trx_is_read_only: 0
trx_autocommit_non_locking: 0
*************************** 2. row ***************************
                    trx_id: 281479655995944
                 trx_state: RUNNING
               trx_started: 2020-06-09 20:22:37
     trx_requested_lock_id: NULL
          trx_wait_started: NULL
                trx_weight: 0
       trx_mysql_thread_id: 11
                 trx_query: select * from information_schema.innodb_trx
       trx_operation_state: NULL
         trx_tables_in_use: 0
         trx_tables_locked: 0
          trx_lock_structs: 0
     trx_lock_memory_bytes: 1136
           trx_rows_locked: 0
         trx_rows_modified: 0
   trx_concurrency_tickets: 0
       trx_isolation_level: REPEATABLE READ
         trx_unique_checks: 1
    trx_foreign_key_checks: 1
trx_last_foreign_key_error: NULL
 trx_adaptive_hash_latched: 0
 trx_adaptive_hash_timeout: 0
          trx_is_read_only: 0
trx_autocommit_non_locking: 0
2 rows in set (0.00 sec)
```

字段详解

1. trx_id: 唯一事务id号，只读事务和非锁事务是不会创建id的。
2. TRX_WEIGHT: 事务的高度，代表修改的行数（不一定准确）和被事务锁住的行数。为了解决死锁，innodb会选择一个高度最小的事务来当做牺牲品进行回滚。已经被更改的非交易型表的事务权重比其他事务高，即使改变的行和锁住的行比其他事务低。
3. TRX_STATE: 事务的执行状态，值一般分为: RUNNING, LOCK WAIT, ROLLING BACK, and COMMITTING.
4. TRX_STARTED: 事务的开始时间
5. TRX_REQUESTED_LOCK_ID: 如果trx_state是lockwait,显示事务当前等待锁的id，不是则为空。想要获取锁的信息，根据该lock_id，以innodb_locks表中lock_id列匹配条件进行查询，获取相关信息。
6. TRX_WAIT_STARTED: 如果trx_state是lockwait,该值代表事务开始等待锁的时间；否则为空。
7. TRX_MYSQL_THREAD_ID: mysql线程id。想要获取该线程的信息，根据该thread_id，以INFORMATION_SCHEMA.PROCESSLIST表的id列为匹配条件进行查询。
8. TRX_QUERY: 事务正在执行的sql语句。
9. TRX_OPERATION_STATE: 事务当前的操作状态，没有则为空。
10. TRX_TABLES_IN_USE: 事务在处理当前sql语句使用innodb引擎表的数量。
11. **TRX_TABLES_LOCKED**: 当前sql语句有行锁的innodb表的数量。（因为只是行锁，不是表锁，表仍然可以被多个事务读和写）
12. TRX_LOCK_STRUCTS: 事务保留锁的数量。
13. TRX_LOCK_MEMORY_BYTES: 在内存中事务索结构占得空间大小。
14. TRX_ROWS_LOCKED: 事务行锁最准确的数量。这个值可能包括对于事务在物理上存在，实际不可见的删除标记的行。
15. TRX_ROWS_MODIFIED: 事务修改和插入的行数
16. TRX_CONCURRENCY_TICKETS: 该值代表当前事务在被清掉之前可以多少工作，由 innodb_concurrency_tickets系统变量值指定。
17. TRX_ISOLATION_LEVEL: 事务隔离等级。
18. TRX_UNIQUE_CHECKS: 当前事务唯一性检查启用还是禁用。当批量数据导入时，这个参数是关闭的。
19. TRX_FOREIGN_KEY_CHECKS: 当前事务的外键坚持是启用还是禁用。当批量数据导入时，这个参数是关闭的。
20. TRX_LAST_FOREIGN_KEY_ERROR: 最新一个外键错误信息，没有则为空。
21. TRX_ADAPTIVE_HASH_LATCHED: 自适应哈希索引是否被当前事务阻塞。当自适应哈希索引查找系统分区，一个单独的事务不会阻塞全部的自适应hash索引。自适应hash索引分区通过 innodb_adaptive_hash_index_parts参数控制，默认值为8。
22. TRX_ADAPTIVE_HASH_TIMEOUT: 是否为了自适应hash索引立即放弃查询锁，或者通过调用mysql函数保留它。当没有自适应hash索引冲突，该值为0并且语句保持锁直到结束。在冲突过程中，该值被计数为0，每句查询完之后立即释放门闩。当自适应hash索引查询系统被分区（由 innodb_adaptive_hash_index_parts参数控制），值保持为0。
23. TRX_IS_READ_ONLY: 值为1表示事务是read only。
24. TRX_AUTOCOMMIT_NON_LOCKING: 值为1表示事务是一个select语句，该语句没有使用for update或者shared mode锁，并且执行开启了autocommit，因此事务只包含一个语句。当TRX_AUTOCOMMIT_NON_LOCKING和TRX_IS_READ_ONLY同时为1，innodb通过降低事务开销和改变表数据库来优化事务。

#### 根本原因

还是有事务开启长期占用锁未提交，开启 autocommit 或者在每个事务中都要求必须手动 commit 

查看是否开启 autocommit 

```
mysql> select @@autocommit;
+--------------+
| @@autocommit |
+--------------+
|            1 |
+--------------+
1 row in set (0.00 sec)
```

如果为 0 的话需要开启 `set global autocommit=1;`

## MySQL 字段长度

以 int 为例，tinyint 是 1个字节，smallint 是 2个字节，int 是 4个字段，bigint 是 8个字节。所以其存储的数据大小是根据其存储空间决定的。


|Type    |  Storage (Bytes) |Minimum Value Signed | Minimum Value Unsigned | Maximum Value Signed | Maximum Value Unsigned |
|------------| -----------------|------------------| --------------------------| -------------------| ---------------- |
|TINYINT   |1         |-128     |0                |127        |255      |
|SMALLINT  |2         |-32768     |0                |32767        |65535      |
|MEDIUMINT   |3         |-8388608   |0                |8388607      |16777215   |
|INT       |4         |-2147483648  |0                |2147483647     |4294967295   |
|BIGINT    |8         |-2^63     |0                |2^63-1       |2^64-1      |

以 smallint 为例，如果你在创建表的时候，未指定是 unsigned 字段，那么如果存入 65535 的值，就会报错。

```
> UPDATE xxxx_table_name t SET t.yyyy_cloum_name = 65535 WHERE t.id = 1
Data truncation: Out of range value for column 'yyyy_cloum_name' at row 1
```

如果需要更大的字段范围，需要创建时指定

```
alter table xxxx_table_name 
add column yyyy_cloum_name smallint unsigned NOT NULL DEFAULT 0 ;
```

以 text 为例，我都不知道原来 text 有这么长，TEXT数据类型的最大长度。

|Type| Storage | Size|
|----|---------|-----|
|TINYTEXT | 256 bytes |  |
|TEXT | 65,535 bytes | ~64kb |
|MEDIUMTEXT | 16,777,215 bytes | ~16MB |
|LONGTEXT  |4,294,967,295 bytes| ~4GB |

## 乐观锁和悲观锁


## 参考链接

[MySQL事务锁等待超时 Lock wait timeout exceeded; try restarting transaction](https://juejin.im/post/5e5b7935518825492d4de463) <br>
[MySql Lock wait timeout exceeded该如何处理？](https://ningyu1.github.io/site/post/75-mysql-lock-wait-timeout-exceeded/) <br>
[[Mysql] mysql innodb_trx参数详解 2018-09-10](https://zeven0707.github.io/2018/09/10/mysql%20innodb_trx%E5%8F%82%E6%95%B0%E8%AF%A6%E8%A7%A3/) <br>
[MySql 死锁时的一种解决办法](https://www.cnblogs.com/farb/p/MySqlDeadLockOneOfSolutions.html) <br>
