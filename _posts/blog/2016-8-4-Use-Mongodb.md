---
layout: post
title: Ubuntu 下安装和使用 Mongodb
description:  nodejs 连接使用 mongodb
category: blog
---

## Mongodb

Mongodb 分布式文件存储型的数据库，属于 NoSQL 的一种，不同于传统的关系型数据库，Mongodb 支持的数据类型非常的松散，且是以一种类似 json 的数据格式存储的。

在 Mongodb 中，传统数据库的表单 `table` 被称为集合 `collection` 。

## 安装 Mongodb

目前最新的 Mongodb 的版本是 3.2 ,但是 Ubuntu 的官方源才更新到 2.4.9 ，Ubuntu 的很多软件的官方支持版本都比较低，比如说 nodejs ， 最新版都已经到了 4.X 了，但是官方的版本还是非常原始，推荐使用 NVM 来安装 nodejs 。

好吧，nodejs 因为发展比较迅速，版本差距太大恐怕不太好，而且不同版本之间还不太兼容，全是 Python 带起的不良风气，所以安装最新版本，但是 Mongodb 就可以随意一点，可以按照 Mongodb 的[官方说明安装](https://docs.mongodb.com/master/tutorial/install-mongodb-on-ubuntu/) 来安装最新版本，或者是索性就像我一样，2.4的版本也能用。

```
sudo apt-get install mongodb
```

## 简单使用

Mongodb 安装好了之后，它是默认开启的。

在 Ubuntu 中被注册为服务，可以通过 `sudo service mongodb status` 来查看运行状态。开启 `sudo service mongodb start` ，关闭 `sudo service mongodb stop` .

或者是通过 自带的服务器端 `mongod` 来开启 。

mongodb 的默认服务端口是 27017 ， 浏览器访问 `http://127.0.0.1:27017/` ,会出现

```
You are trying to access MongoDB on the native driver port. For http diagnostic access, add 1000 to the port number
```

访问 `http://127.0.0.1:28017/` ,才是 mongodb 的服务页面。

mongodb 的配置文件是 `/etc/mongodb.conf` 数据库默认存储位置是 `dbpath=/var/lib/mongodb` 日志的默认存储位置是 `logpath=/var/log/mongodb/mongodb.log`

可以通过 `mongod --dbpath dbdata --logpath dblog/mongod.log` 来设定存储位置。

在安装好 mongodb 之后，就可以通过 自带的客户端 `mongo` 来操作数据库，若未指定数据库，则使用默认数据库 `test` 。

mongodb 的插入和查找都是以 json 格式进行的。

mongodb 的创建数据库时，实际数据库并没有被创建，只有当数据库被插入数据时数据库才被创建出来。

mongodb 的集合并不需要被显示的创建，只要插入数据就会被自动创建。

mongodb 的集合中并不需要规定数据类型，是完全松散的，即使每次插入的数据格式不一致，只要是 json 格式就可以。

mongodb 插入的每一条数据，都会被自动的加上一个唯一的 `_id` 。

```
windard@windard:~$ mongo
MongoDB shell version: 2.4.9
connecting to: test                                                                                                                                                 // 使用数据库 test
Server has startup warnings:
Wed Aug  3 23:16:58.054 [initandlisten]
Wed Aug  3 23:16:58.054 [initandlisten] ** NOTE: This is a 32 bit MongoDB binary.
Wed Aug  3 23:16:58.054 [initandlisten] **       32 bit builds are limited to less than 2GB of data (or less with --journal).
Wed Aug  3 23:16:58.054 [initandlisten] **       See http://dochub.mongodb.org/core/32bit
Wed Aug  3 23:16:58.054 [initandlisten]
> show dbs                                                                                                                                                          // 查看数据库
local   0.03125GB
microblog   0.0625GB
> use newcreate                                                                                                                                                    // 创建并使用数据库 newcreate
switched to db newcreate
> show dbs                                                                                                                                                             // 查看数据库，可以看到此时数据库并没有被创建
local   0.03125GB
microblog   0.0625GB
> db.user.insert({"name":"windard","email":"1106911190"})                                                                           // 创建集合 user 并插入数据
> show dbs                                                                                                                                                              // 查看数据库，此时数据库已被创建
local   0.03125GB
microblog   0.0625GB
newcreate   0.0625GB
> db.user.find()                                                                                                                                                            // 查看数据集合 user 内容
{ "_id" : ObjectId("57a30232691d6fdaaea65f5f"), "name" : "windard", "email" : "1106911190" }
> db.user.insert({"name":"admin","email":"admin@admin.com"})                                                                           // 再次插入数据
> db.user.find()
{ "_id" : ObjectId("57a30232691d6fdaaea65f5f"), "name" : "windard", "email" : "1106911190" }
{ "_id" : ObjectId("57a30262691d6fdaaea65f60"), "name" : "admin", "email" : "admin@admin.com" }
> db.user.find({"user":"admin"})                                                                                                                                    // 查找数据
> db.user.find({"name":"admin"})
{ "_id" : ObjectId("57a30262691d6fdaaea65f60"), "name" : "admin", "email" : "admin@admin.com" }
> db.user.insert({"username":"foo","password":"123456"})                                                                                            // 插入不同数据格式的数据
> db.user.find()                                                                                                                                                                    // 查看数据集合内容
{ "_id" : ObjectId("57a30232691d6fdaaea65f5f"), "name" : "windard", "email" : "1106911190" }
{ "_id" : ObjectId("57a30262691d6fdaaea65f60"), "name" : "admin", "email" : "admin@admin.com" }
{ "_id" : ObjectId("57a303c2691d6fdaaea65f61"), "username" : "foo", "password" : "123456" }
> db.user.find().pretty()                                                                                                                                                           // 格式话打印出来
{
    "_id" : ObjectId("57a30232691d6fdaaea65f5f"),
    "name" : "windard",
    "email" : "1106911190"
}
{
    "_id" : ObjectId("57a30262691d6fdaaea65f60"),
    "name" : "admin",
    "email" : "admin@admin.com"
}
{
    "_id" : ObjectId("57a303c2691d6fdaaea65f61"),
    "username" : "foo",
    "password" : "123456"
}
> show collections                                                                                                                                                                      // 查看集合
system.indexes
user
> db.adress.insert({"name":"windard","addr":"china"})                                                                                                           // 创建集合 address 并插入数据
> show collections                                                                                                                                                                      // 查看集合
adress
system.indexes
user
> db.address.remove()                                                                                                                                                                   // 删除数据
> db.address.find()
> db.user.update({"username":"foo"},{"name":"foo","email":"foo@bar.com"})                                                                       // 更新数据
> db.user.find()
{ "_id" : ObjectId("57a30232691d6fdaaea65f5f"), "name" : "windard", "email" : "1106911190" }
{ "_id" : ObjectId("57a30262691d6fdaaea65f60"), "name" : "admin", "email" : "admin@admin.com" }
{ "_id" : ObjectId("57a303c2691d6fdaaea65f61"), "name" : "foo", "email" : "foo@bar.com" }
> db.dropDatabase()                                                                                                                                                                         // 删除数据库
{ "dropped" : "newcreate", "ok" : 1 }
> show dbs
local   0.03125GB
microblog   0.0625GB

```

## nodejs 与 mongodb

nodejs 关于 mongodb 的库有 mongoose ， mongodb ， 和 monk 等，一般用 mongodb 比较多。

先安装 mongodb 库， `npm install mongodb`

```
var  mongodb = require('mongodb');
var  server  = new mongodb.Server('127.0.0.1', 27017, {auto_reconnect:true});
var  mongodb = new mongodb.Db('newcreate', server, {safe:true});

// 连接数据库
mongodb.open(function(err, db){
    if(!err){
        console.log('connect db');
         // 连接Collection
         db.collection('user',{safe:true}, function(err, collection){
             if(err){
                 console.log("ERROR:")
                 console.log(err);
             }else{
                // 插入数据
                collection.insert({"name":"windard","email":"1106911190@qq.com"},{safe:true},function(err,result){
                  console.log(result);
                });
                collection.insert({"username":"foo","password":"123456"},{safe:true},function(err,result){
                    if(err){
                        console.log("ERROR:")
                        console.log(err);
                    }else{
                        console.log(result);
                    }
                });
                // 查询数据
                collection.find({"name":"windard"}).toArray(function(err,result){
                    if(err){
                        console.log("ERROR:")
                        console.log(err);
                    }else{
                        result.forEach(function(item){
                            console.log(result);
                        });
                    };
                });
                collection.findOne({},function(err,result){
                    if(err){
                        console.log("ERROR:")
                        console.log(err);
                    }else{
                        console.log(result);
                    };
                });
                // 更新数据
                collection.update({"username":"foo"},{"name":"foo"},{safe:true},function(err,result){
                    if(err){
                        console.log("ERROR:")
                        console.log(err);
                    }else{
                        console.log(result);
                    }
                });

                collection.find({}).toArray(function(err,result){
                    if(err){
                        console.log("ERROR:")
                        console.log(err);
                    }else{
                        result.forEach(function(item){
                            console.log(item);
                        });
                    };
                });
                // 删除数据
                collection.remove({},function(err,result){
                    if(err){
                        console.log("ERROR:")
                        console.log(err);
                    }else{
                        console.log(result);
                    }
                });
            };
        });
    }else{
        console.log(err);
    };
    mongodb.close();
});

```

在连接 collection 时有两种方案：

1. `db.collection('collection',function(err,coll){});` 此时第二个可选参数{safe:true},如果加上了这个参数，那么当collection不存在的时候则报错。
2. `db.createCollection('collection',function(err,coll){});` 此时第二个可选参数{safe:true},如果加上了这个参数，那么当collection存在的时候则报错。
