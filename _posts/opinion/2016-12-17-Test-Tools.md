---
layout: post
title: 一些 web 性能测试工具
category: opinion
description: 主要是 Apache Benchmark 和 Siege 两款压力测试工具 
---

## Siege

```
[root@iZ2ze83hhomw2zcf15c3qcZ ~]# siege -h
SIEGE 4.0.2
Usage: siege [options]
       siege [options] URL
       siege -g URL
Options:
  -V, --version             VERSION, prints the version number.
  -h, --help                HELP, prints this section.
  -C, --config              CONFIGURATION, show the current config.
  -v, --verbose             VERBOSE, prints notification to screen.
  -q, --quiet               QUIET turns verbose off and suppresses output.
  -g, --get                 GET, pull down HTTP headers and display the
                            transaction. Great for application debugging.
  -c, --concurrent=NUM      CONCURRENT users, default is 10
  -r, --reps=NUM            REPS, number of times to run the test.
  -t, --time=NUMm           TIMED testing where "m" is modifier S, M, or H
                            ex: --time=1H, one hour test.
  -d, --delay=NUM           Time DELAY, random delay before each requst
  -b, --benchmark           BENCHMARK: no delays between requests.
  -i, --internet            INTERNET user simulation, hits URLs randomly.
  -f, --file=FILE           FILE, select a specific URLS FILE.
  -R, --rc=FILE             RC, specify an siegerc file
  -l, --log[=FILE]          LOG to FILE. If FILE is not specified, the
                            default is used: PREFIX/var/siege.log
  -m, --mark="text"         MARK, mark the log file with a string.
                            between .001 and NUM. (NOT COUNTED IN STATS)
  -H, --header="text"       Add a header to request (can be many)
  -A, --user-agent="text"   Sets User-Agent in request
  -T, --content-type="text" Sets Content-Type in request
```

最常用法

```
siege -c 1000 -r 100 -b http://127.0.0.1:8090
```

```
Transactions:                  25416 hits
Availability:                  99.67 %
Elapsed time:                  42.07 secs
Data transferred:               0.29 MB
Response time:                  0.29 secs
Transaction rate:             604.14 trans/sec
Throughput:                     0.01 MB/sec
Concurrency:                  177.53
Successful transactions:       25416
Failed transactions:              84
Longest transaction:           31.62
Shortest transaction:           0.00
```

主要查看参数 `Transaction rate`

## Apache Benchmark

```
[root@iZ2ze83hhomw2zcf15c3qcZ /]# ab -h
Usage: ab [options] [http[s]://]hostname[:port]/path
Options are:
    -n requests     Number of requests to perform
    -c concurrency  Number of multiple requests to make at a time
    -t timelimit    Seconds to max. to spend on benchmarking
                    This implies -n 50000
    -s timeout      Seconds to max. wait for each response
                    Default is 30 seconds
    -b windowsize   Size of TCP send/receive buffer, in bytes
    -B address      Address to bind to when making outgoing connections
    -p postfile     File containing data to POST. Remember also to set -T
    -u putfile      File containing data to PUT. Remember also to set -T
    -T content-type Content-type header to use for POST/PUT data, eg.
                    'application/x-www-form-urlencoded'
                    Default is 'text/plain'
    -v verbosity    How much troubleshooting info to print
    -w              Print out results in HTML tables
    -i              Use HEAD instead of GET
    -x attributes   String to insert as table attributes
    -y attributes   String to insert as tr attributes
    -z attributes   String to insert as td or th attributes
    -C attribute    Add cookie, eg. 'Apache=1234'. (repeatable)
    -H attribute    Add Arbitrary header line, eg. 'Accept-Encoding: gzip'
                    Inserted after all normal header lines. (repeatable)
    -A attribute    Add Basic WWW Authentication, the attributes
                    are a colon separated username and password.
    -P attribute    Add Basic Proxy Authentication, the attributes
                    are a colon separated username and password.
    -X proxy:port   Proxyserver and port number to use
    -V              Print version number and exit
    -k              Use HTTP KeepAlive feature
    -d              Do not show percentiles served table.
    -S              Do not show confidence estimators and warnings.
    -q              Do not show progress when doing more than 150 requests
    -g filename     Output collected data to gnuplot format file.
    -e filename     Output CSV file with percentages served
    -r              Don't exit on socket receive errors.
    -h              Display usage information (this message)
    -Z ciphersuite  Specify SSL/TLS cipher suite (See openssl ciphers)
    -f protocol     Specify SSL/TLS protocol
                    (SSL2, SSL3, TLS1, TLS1.1, TLS1.2 or ALL)
```

最常用法

```
ab -n 255 -c 100 http://127.0.0.1:8090/
```

结果

```
[root@iZ2ze83hhomw2zcf15c3qcZ ~]# ab -n 255 -c 100 http://127.0.0.1:8090/
This is ApacheBench, Version 2.3 <$Revision: 1430300 $>
Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
Licensed to The Apache Software Foundation, http://www.apache.org/

Benchmarking 127.0.0.1 (be patient)
Completed 100 requests
Completed 200 requests
Finished 255 requests


Server Software:        Werkzeug/0.11.11
Server Hostname:        127.0.0.1
Server Port:            8090

Document Path:          /
Document Length:        12 bytes

Concurrency Level:      100
Time taken for tests:   0.265 seconds
Complete requests:      255
Failed requests:        0
Write errors:           0
Total transferred:      42585 bytes
HTML transferred:       3060 bytes
Requests per second:    960.67 [#/sec] (mean)
Time per request:       104.095 [ms] (mean)
Time per request:       1.041 [ms] (mean, across all concurrent requests)
Transfer rate:          156.67 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    2   2.6      0       6
Processing:     3   82  31.3     99     106
Waiting:        0   81  31.4     99     106
Total:          5   84  29.4    100     107

Percentage of the requests served within a certain time (ms)
  50%    100
  66%    102
  75%    103
  80%    104
  90%    105
  95%    106
  98%    106
  99%    106
 100%    107 (longest request)
```

主要参看参数 `Requests per second`
