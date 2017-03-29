---
layout: post
title: 使用 Celery 和 redis 完成任务队列 
description: 消息队列和任务队列在实际生产中应用的非常广泛，主要学习一下 Python 实现的 Celery。
category: opinion
---

任务队列与消息队列都是由队列实现的异步协议，只是消息队列(Message Queue) 用来做异步通信，而任务队列(Task Queue) 更强调异步执行的任务。实际上发送消息也是一个任务，也就是说任务队列是在消息队列之上的管理工作，任务队列的很多典型应用就是发送消息，如发送邮件，发送短信，发送消息推送等。

作为队列，也就具有一个先进先出模型，任务的生产者发送任务到队列中，消费者则接收任务并处理它，这样就实现了一个基本的应用解耦合和异步通信，任务或者消息是平台和语言无关的。

任务队列的主要应用场景在 

1. 不用实现响应，性能占用较大，任务处理时间较长的任务，如占用网络性能的发送邮件，占用IO性能的视频处理。
2. 按时发布的定时任务，如定期对服务器的检查，对当天网站的监测分析。

一般的任务就是消息，消息中的有效载荷包含执行任务需要的全部数据。消息中间件或者称为消息代理，就是用来接收生产者发送过来的任务消息，存进队列再按序发送给任务消费方。

常见的消息队列有 rabbitmq，zeromq，以及 redis(rq) 等，而 Celery 则强调自己是一个任务队列，按其[官网](http://www.celeryproject.org/)上的定义.

```
Celery is an asynchronous task queue/job queue based on distributed message passing.	It is focused on real-time operation, but supports scheduling as well.
```

Celery 是一个异步的分布式任务队列，主要用于实时处理和任务调度。不过它的消息中间件是默认选择使用 rabbitmq ，也可以使用 redis ，它还支持其他的消息队列或者是数据库，本文即使用 redis 作为其 broker 。

Celery 包含的组件：
1. Celery Beat: 任务调度器，用来调度周期任务。
2. Producer: 任务生产者，调用 Celery 产生任务。
3. Broker: 消息中间件，任务消息存进队列，再按序发送给消费者。
4. Celery Worker: 执行任务的消费者，通常可以进行在多台服务器上运行多个消费者。
5. Result Backend: 任务处理完成之后保存状态信息和结果，一般是数据库。

Celery 产生任务的方式有两种
1. 发布者发布任务
2. 任务调度按时发布定时任务

Celery 的架构
![Celery.png](/images/Celery.png)


## Celery 入门

使用 redis 作为消息代理和存储位置，首先我们来定义一个任务队列的 server 端。(tasks.app)

```
# coding=utf-8

import time
from celery import Celery

app = Celery('tasks', backend='redis://127.0.0.1:6379/0', broker='redis://127.0.0.1:6379/1')

@app.task
def sendmail(mail):
    print 'sending mail to %s ...'%mail['to']
    time.sleep(2)
    print 'mail send.'
    return 'Send Successful!'


@app.task
def add(x, y):
    return x + y

```

我们定义了一个发送邮件的任务，在发送邮件的过程中会停止等待两秒才完成。

接下来定义客户端。(client.py)

```
# coding=utf-8

import time
from tasks import sendmail, add

print sendmail.delay(dict(to='celery@python.org'))

answer = sendmail.delay(dict(to='windard@windard.com'))

while 1:
    print 'wait for ready'
    if answer.ready():
        break
    time.sleep(0.5)

print answer.get()

```

启动 redis-server 服务器，启动 celery 服务器。

```
redis-server
celery -A tasks worker --loglevel=info
```

看到如下输出即启动成功。

```
[2017-03-19 00:51:21,893: WARNING/MainProcess] /usr/lib/python2.7/site-packages/celery/apps/worker.py:162: CDeprecationWarning:
Starting from version 3.2 Celery will refuse to accept pickle by default.

The pickle serializer is a security concern as it may give attackers
the ability to execute any command.  It's important to secure
your broker from unauthorized access when using pickle, so we think
that enabling pickle should require a deliberate action and not be
the default choice.

If you depend on pickle then you should set a setting to disable this
warning and to be sure that everything will continue working
when you upgrade to Celery 3.2::

    CELERY_ACCEPT_CONTENT = ['pickle', 'json', 'msgpack', 'yaml']

You must only enable the serializers that you will actually use.


  warnings.warn(CDeprecationWarning(W_PICKLE_DEPRECATED))

 -------------- celery@localhost.localdomain v3.1.20 (Cipater)
---- **** -----
--- * ***  * -- Linux-3.10.0-229.el7.x86_64-x86_64-with-centos-7.1.1503-Core
-- * - **** ---
- ** ---------- [config]
- ** ---------- .> app:         tasks:0x31a6cd0
- ** ---------- .> transport:   redis://127.0.0.1:6379/1
- ** ---------- .> results:     redis://127.0.0.1:6379/0
- *** --- * --- .> concurrency: 1 (prefork)
-- ******* ----
--- ***** ----- [queues]
 -------------- .> celery           exchange=celery(direct) key=celery


[tasks]
  . tasks.add
  . tasks.sendmail

[2017-03-19 00:51:22,437: INFO/MainProcess] Connected to redis://127.0.0.1:6379/1
[2017-03-19 00:51:22,742: INFO/MainProcess] mingle: searching for neighbors
[2017-03-19 00:51:24,623: INFO/MainProcess] mingle: all alone
[2017-03-19 00:51:25,009: WARNING/MainProcess] celery@localhost.localdomain ready.
```

现在我们打开另一个终端运行客户端执行任务。

```
[windard@localhost asynchronous]$ python client.py
Sun Mar 19 00:53:59 2017
a9326a8e-2ee4-40b6-be30-46a9231fcbd6
Sun Mar 19 00:54:00 2017
wait for ready
wait for ready
wait for ready
wait for ready
wait for ready
wait for ready
wait for ready
wait for ready
wait for ready
wait for ready
Send Successful!
Sun Mar 19 00:54:04 2017
```

同时查看 celery 日志

```
[2017-03-19 00:54:00,319: INFO/MainProcess] Received task: tasks.sendmail[a9326a8e-2ee4-40b6-be30-46a9231fcbd6]
[2017-03-19 00:54:00,403: WARNING/Worker-1] sending mail to celery@python.org ...
[2017-03-19 00:54:00,404: INFO/MainProcess] Received task: tasks.sendmail[d8e2e4af-d010-42b2-988c-367739f78e85]
[2017-03-19 00:54:02,406: WARNING/Worker-1] mail send.
[2017-03-19 00:54:02,541: INFO/MainProcess] Task tasks.sendmail[a9326a8e-2ee4-40b6-be30-46a9231fcbd6] succeeded in 2.19810597599s: 'Send Successful!'
[2017-03-19 00:54:02,551: WARNING/Worker-1] sending mail to windard@windard.com ...
[2017-03-19 00:54:04,555: WARNING/Worker-1] mail send.
[2017-03-19 00:54:04,558: INFO/MainProcess] Task tasks.sendmail[d8e2e4af-d010-42b2-988c-367739f78e85] succeeded in 2.0068878379s: 'Send Successful!'
```

可以看到我们的两个任务是在几乎同时发送到队列中，说明生产者发布任务的过程是异步的，在生成任务之后并推送给队列之后即可处理其他的事务。

因为我们只使用了一个消费者处理任务，所以我们的任务只能顺序进行，如果任务已经完成，则 `answer.ready()` 函数返回 `True` ，即可使用 `answer.get()` 获得任务的返回值。

判断是否完成的函数也是异步非阻塞的，获得返回值的函数是同步阻塞的(可以设置 timeout 等待时间)。

我们可以在 redis 中查看存储的结果，你会发现结果的辨认度很低，因为默认采用 pickle 序列化存储，但是从 Celery 3.2 开始将不在支持 pickle 存储方式。

其实若是认真查看前面的日志，即可得到这一信息，日志中也提醒我们设置一个其他的序列化方式。

现在我们将 配置 写入配置文件，然后从配置文件中读取。(config.py)

```
# coding=utf-8

BROKER_URL = 'redis://127.0.0.1:6379/1'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'
CELERY_TASK_SERIALIZER = 'msgpack'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_RESULT_EXPIRES = 60 * 60 * 24
CELERY_ACCEPT_CONTENT = ['json', 'msgpack']
```

在任务调度中使用 msgpack 序列化，在任务结果中使用 json 序列化。

将主函数也可以分离。(app.py)

```
# coding=utf-8

from celery import Celery

app = Celery('app', include=['tasks'])
app.config_from_object('config')

```

任务函数单独作为一个文件。(tasks.py)

```
# coding=utf-8

import time
from app import app

@app.task
def sendmail(mail):
    print 'sending mail to %s ...'%mail['to']
    time.sleep(2)
    print 'mail send.'
    return 'Send Successful!'

```

客户端仍是之前客户端，启动 Celery 服务器。

```
celery -A app worker --loglevel=info
```

在执行完任务之后，在 redis 中即可查看任务结果，以 json 格式显示，索引是 task_id，而当我们想要再次找到之前任务的结果时，也可以使用 task_id 找到它，`sendmail.AsyncResult(task_id)` 。

我们也可以在 ipython 中调用任务

```
In [1]: from tasks import sendmail
In [2]: r = sendmail.delay({'to':"foo@bar.com"})
In [3]: r.status
Out[3]: u'SUCCESS'
In [4]: r.ready()
Out[4]: True
In [5]: r
Out[5]: <AsyncResult: 00e310f9-986c-41e6-b8cc-fff12b299358>
In [6]: r.get()
Out[6]: u'Send Successful!'
In [7]: r.backend
Out[7]: <celery.backends.redis.RedisBackend at 0x2b93a90>
In [8]: r.task_id
Out[8]: '00e310f9-986c-41e6-b8cc-fff12b299358'
In [9]: r.task_name
Out[9]: 'tasks.sendmail'
```


## 使用任务调度

任务调度的一种常见需求是每隔一段时间执行一遍任务，我们在配置文件中补充一些调度配置。(config.py)

```
CELERY_TIMEZONE = 'Asia/Shanghai'

from datetime import timedelta

CELERYBEAT_SCHEDULE = {
    'send-every-30-seconds': {
        'task': 'tasks.sendmail',
        'schedule': timedelta(seconds=30),
        'args': (dict(to='windard@windard.com'), )
    }
}
```

在配置文件中加上如上的配置，注意，任务的参数需为 元祖 (tuple) 格式。

启动 Celery ，因使用了调度配置，所以需加上 `-B` 参数。

```
celery -A app worker -B -l info
```

即可用在日志中看到每  30 秒执行一遍任务。

在配置文件中指定 Celery 时区，虽然在本例中用不到，但是如果需要调度任务在指定时刻执行，即需要当地时间。

可以使用 crontab 制定一个指定时间执行的调度任务。

```
CELERY_TIMEZONE = 'Asia/Shanghai'

from celery.schedules import crontab

CELERYBEAT_SCHEDULE = {
    'send-every-30-seconds': {
        'task': 'tasks.sendmail',
        'schedule': crontab(hour=16, minute=30),
        'args': (dict(to='windard@windard.com'), )
    }
}

```

crontab 还可以做更细致的时间规划，也可以在任务定义时，即制定时间规划。

在任务制定的文件中，我们增加一个指定时间执行的任务。(tasks.py)

```
from celery.schedules import crontab
from celery.task import periodic_task

@periodic_task(run_every=crontab(hour='16', minute='58'))
def schedule_sendmail():
    print 'sending mail task'
    time.sleep(2)
    print 'mail send.'
    return 'Send Successful!'
```

在配置文件增加时区，然后同样的运行 Celery。

```
celery -A app worker -B -l info
```

这个任务仍然能够被生产者调用，也会在指定时间被任务调度执行，只不过不能有参数传递。

crontab 调度的几种常见用法

|写法                     |含义                |
|------                   |---------           |
|crontab()                |每分钟              |
|crontab(minute='10', hour='6')                |每天 6 点 10 分           |
|crontab(hour='0, 3, 6, 9', day_of_week='0, 1, 2')    |每周天，周一，周二的 0,3,6,9 点        |
|crontab(minute='*/15')                |每十五分钟              |
|crontab(minute='0', hour='*/2')                |每两个小时的 0 分              |
|crontab(day_of_month='1-7,15-21')                |每个月的 1-7, 15-21 号              |


## 使用多条队列

在上文中我们的任务虽然是异步执行的，但是在任务执行的过程中，因为只有一条队列，所以任务执行是同步的。

在 Celery 中，默认只有一条 `celery` 的队列，用于消息队列。

在队列里任务一个一个的完成，这样的效率很低，我们可以创建多个队列，让多条队列同步进行。

在配置文件中添加如下配置创建多个队列。(config.py)

```
from kombu import Queue

CELERY_QUEUES = (
    Queue('default', routing_key='task.#'),
    Queue('web_tasks', routing_key='web.#'),
)

```

默认队列是 `default`。

接下来对任务指定队列。

```
@app.task
def add(x, y, queue='default'):
    return x + y
```

然后在调用的时候也需要指定队列，这时的队列可以不一定是任务指定的队列。

```
result = add.apply_async((1, 2), routing_key='task.add')
```

```
result = add.apply_async(args=(1, 2), queue='default')
```

仅开启单个路由

```
celery -A tasks worker -Q default -l info
```

## 其他功能

### 记录日志和重试

同样的修改我们的任务文件。(tasks.py)

```
# coding=utf-8

from app import app
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

@app.task(bind=True)
def div(self, x, y):
    logger.info('Executing task id {0.id}, args: {0.args!r}'
                'kwargs: {0.kwargs!r}'.format(self.request))

    try:
        result = x / y
    except ZeroDivisionError as e:
        raise self.retry(exc=e, countdown=5, max_retries=3)
    return result
```

在 ipython 中调用任务

```
In [3]: from tasks import  div
In [4]: div.delay(2, 1)
Out[4]: <AsyncResult: 3bca5f7c-31ab-4f35-b262-1cdd9d1d467b>
In [5]: div.delay(2, 0)
Out[5]: <AsyncResult: df5d7387-39ca-493d-8850-1ff91aad173c>
```

即可在日志中看到输出的日志，造成异常的函数也会被执行三次，每五秒重试一次，最后抛出异常结束。

### 工作流

1. 关联任务

调用任务函数 `add.delay(1,2)` 的效果与 `add.apply_async(args=(1,2))` 相同。使用 link 将第一个任务的结果作为第二个任务的参数。

```
add.apply_async(args=(1,2), link=add.s(4))
```

结果为 7
2. 过期时间

expires 单位为 秒，超过过期时间还未开始执行的任务会被回收。

```
add.apply_async((1,2), expires=10)
```

3. 并行调度

group , 一次调度多个任务，将任务结果以列表形式返回。

```
In [16]: from celery import group
In [17]: res = group(add.s(i, i) for i in xrange(10))()
In [18]: res.get()
Out[18]: [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]
```

4. 串行调度

chain , 一次调度多个任务，将前一个任务的结果作为参数传入下一个任务

```
In [19]: from celery import chain
In [20]: res = chain(add.s(2, 2), add.s(4), add.s(8))()
In [21]: res.get(timeout=1)
Out[21]: 16
```

效果同

```
c2 = (add.s(4, 16) | mul.s(2) | (add.s(4) | mul.s(8)))()
```

5. chord
6. map
7. starmap
8. chunks
