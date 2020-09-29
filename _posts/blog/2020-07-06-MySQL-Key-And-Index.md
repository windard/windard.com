---
layout: post
title: MySQL 中的键和索引
description: 他们生来不同，却被处处混用。
category: blog
---

MySQL 中的键和索引并不是同一个东西，但是却很类似，概念不易区分。

键是 MySQL 表上的一个约束条件，约束规范表中的列行为，比如主键或者唯一键，然后在约束之后，会自动为其生成索引。

索引其实是 MySQL 是表中的一个附加存储结构，用来加速数据查询性能。

键和索引都可以对于单列或者多列。

## 键

MySQL 中一般常见的就是主键，外键，唯一键,联合键

MySQL 有且仅有一个主键，但是可以有多个唯一键。创建键即自动创建索引。

查看表中有哪些键。

```
show keys from name;
```

### primary key
主键可以在建表的时候指定，也可以在建表之后再添加。

```
alter table table_name add primary key(name);
```

主键也是唯一键即不能重复，且不能为空。

### unique key 

唯一键允许为空，在一张表里只能有一个主键，但是可以有多个唯一键。

唯一键的意思是改列中每一行没有重复，不能有两行有相同的值。

```
alter table table_name add unique key(name);
```

### foreign key

外键即一张表中的字段和另一张表中的字段相互关联。

使用外键会对表中的数据操作造成限制来保证数据一致性，对性能有影响，一般不推荐使用外键。

### multi key 

普通键，就是普通索引，一般用来创建索引。数据可以重复。

```
alter table table_name add key(user);
```

### 删除键

```
alter table table_name drop key id;
```

## 索引

键和索引基本上就是同义词，大部分情况下可以混用或者互换。

查看全部索引

```
show index from name;
```

### 普通索引

创建索引和创建键的命令一模一样。

```
alter table table_name add index(id);
```

或者指定索引名

```
alter table user add index idx_user (user);
```

### 全文索引

全文索引是 MySQL 5.6 之后支持的新功能。

```
alter table table_name add fulltext (user);
```

或者叫 

```
alter table table_name add fulltext index name_full_index(name);
```

### 删除索引

```
alter table table_name drop index user;
```

同时，还可以直接删除

```
drop index index_name on table_name;
```

## 总结

感觉讲了个寂寞，上文中大部分的 `index` 都可以用 `key` 替换，反之亦然。

key 主要是用来约束，主要是 主键，唯一键和普通键。

index 主要是加速查询，主要是普通索引和全文索引。

## 引用

[MySQL 中 KEY vs PRIMARY KEY vs UNIQUE KEY vs INDEX 的区别](http://einverne.github.io/post/2017/07/mysql-key-vs-primary-key-vs-unique-key-vs-index.html)  
[mysql联合索引](https://www.cnblogs.com/softidea/p/5977860.html)
