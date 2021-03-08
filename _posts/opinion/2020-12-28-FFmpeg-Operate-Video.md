---
layout: post
title: FFmpeg 使用简介
category: opinion
description: 使用 FFmpeg 操作视频的一些常用方法。
---

FFmpeg 是一个很常见的视频操作剪辑工具，简单记录一下一些常用的操作。

## 安装 FFmpeg

这个就不多说了，一般常见的系统发行软件源上都有，可以用 CentOS 的 yum 安装或则 MacOS 的 brew 安装。

## 视频截图

截取一段时间内的截图，按时间段截取，比如 24帧的视频，那截取 1秒就会生成 24张照片，一般人眼不能区分的视频是最少是每秒 24帧。

```
ffmpeg -ss 0 -t 1 -i 3499394.ts %3d.png
```

- `-ss 00:00:00` 截取片段的开始时间
- `-to 00:57:00` 截取片段的结束时间
- `-t 00:00:30` 指定截取的时间，比如30秒
- `-i xx-yy-zz.mp4` 源视频
- `%3d.png` 生成图片命令格式，3位数字依次递增
- `-f image2` 指定生成 JPG 格式图片，实际上保存的后缀名为 `jpg` 会默认确定格式
- `-f gif` 指定生成 GIF 格式图片,实际上保存的后缀名为 `gif` 会默认确定格式
- `-frames:v 1` 如果想截取某秒内单张截图，指定帧数为1

其他截图命令

```
# 截图某秒内的一张截图
ffmpeg -ss 0 -t 1 -i 3499394.ts -frames:v 1 -f image2 -y test1.jpg
# 将视频第一帧截取为图片
ffmpeg -i 3499543.ts -vframes  1 test2.png
# 将截取的图片合成为视频
ffmpeg -i %3d.png output.mp4
# 从三十秒开始截取十秒作为 GIF
ffmpeg -i 6544387.mp4 -ss 0:0:30 -t 10  -f gif output.gif
# 从开头截取 30帧 作为 GIF
ffmpeg -i 7697387.mp4 -vframes 30 -f gif output.gif
# 每秒一张并截图保存为 PNG 图片
ffmpeg  -i input.mp4 -vf fps=1  output%d.png
# 十秒一张并截图保存为 JPG 图片
ffmpeg  -i input.mp4 -vf fps=0.1  output%d.jpg
# 每秒十张并截图保存为 BMP 图片
ffmpeg  -i input.mp4 -vf fps=10  output%d.bmp
```

## 视频分割

对于视频分割取样就比较简单了。常见的命令就是

```
ffmpeg -ss 00:00:00 -to 00:57:00 -i xx-yy-zz.mp4 -codec copy output.mp4
```

- `-ss 00:00:00` 截取片段的开始时间
- `-to 00:57:00` 截取片段的结束时间
- `-t 00:00:30` 指定截取的时间，比如30秒
- `-i xx-yy-zz.mp4` 源视频
- `-vcodec copy` 使用源视频编解码方式
- `-acodec copy` 使用源音频编解码方式
- `-codec copy` 或者 `-c copy` 可以直接采用这种方式，表示视频音频编解码方式一致，取代上面的两条指令
- `output.mp4` 输出视频
- `-accurate_see` 如果需要更精确的剪裁，可以加入这个指令在`-i`前面
- `-avoid_negative_ts 1` 还有这个指令在 `-i` 后面可以更精确

但是一般常见的场景下直接剪切还是足够精确的。	

## 视频提取

从视频中提取纯视频或者纯音频，可以去除音轨或者提取音轨。

提取音频

```
ffmpeg -i input.mp4 -acodec copy -vn output.aac
```

提取视频

```
ffmpeg -i input.mp4 -vcodec copy -an output.mp4
```

- `-an`: 去掉音频
- `-vcodec`: 视频选项，一般后面加copy表示拷贝
- `-vn`: 去掉视频
- `-acodec`: 音频选项， 一般后面加copy表示拷贝

将音视频合成

```
ffmpeg -y –i input.mp4 –i input.aac –vcodec copy –acodec copy output.mp4
```

## 视频转码

一般简单的视频转码就直接转就可以了

```
ffmpeg -i 3499289.ts 3499289.avi
ffmpeg -i 3499289.ts 3499289.mp4
```

复杂点的就需要了解下深入了解了。

常见的视频格式有 mp4,avi 等，但是具体视频编解码方式和视频文件格式的关系又有几人能分清呢？
> <a href="https://www.bgteach.com/article/134" target="_blank" class="external">视频文件格式知多少 | avi、mpeg、mp4、mov、ProRes、DNxHR、mfx、mkv、wmv、flv、rmvb、webm...</a>

简单的介绍一下 TS,TS代表`Transport Stream(传输流)`，其全名是`MPEG2-TS`，是一种视频媒体文件格式，TS的文件扩展名是`.ts`，`.tsv`，`.tsa`。 它是日本高清摄像机拍摄下进行的封装格式，是用于音效、图像与数据的通信协定，最早应用于DVD的实时传送节目。

> `MPEG2-TS` 格式的特点就是要求从视频流的任一片段开始都是可以独立解码的。所以实际上你得到的任意一个 ts 片段都是可以独立播放的，如果不能，那就是播放器的问题，直接将 ts 文件顺序合并也可以认为得到一个完整可播放的视频。

现在很多播放器不支持TS格式的视频，或者有的播放器支持，但是在播放时拖动进度条会卡顿，这时我们就需要将TS格式转换成常见的MP4等视频格式了。

此外，除了将TS转换为MP4之外，打开TS视频的另一个选项是将其重命名为MPEG。 大多数多媒体播放器已支持MPEG视频。 这是因为TS文件是MPEG文件，因此如果将文件扩展名从TS重命名为MPEG，则媒体播放器或媒体设备可能会识别并播放TS文件。

直接转化的命令,可以将 ts 文件转码为 MP4 文件。

```
ffmpeg -i xxx.ts -c copy -map 0 -bsf:a aac_adtstoasc yyy.mp4
```

> 如果音轨不是AAC_ADTS可以不加`-bsf:a aac_adtstoasc`

这里的 ts 源文件可以是单个的 ts 片段，也可以是 ts 片段顺序组合后的数据。

## 视频合并

常规的 TS 分片除了先合并再转码之外，也可以通过 FFmpeg 直接进行合并转码。

音视频合并编码可以合并 mp3,mp4,ts 等格式文件，在合并 ts 文件的时候可以将其转码成 mp4 格式。

```
ffmpeg -i "concat:input1.mpg|input2.mpg|input3.mpg" -c copy output.mpg
```

> 保存 QuickTime/MP4 格式容器的时候，建议加上 `-movflags +faststart`。这样分享文件给别人的时候可以边下边看。

实际上上面的命令也可以改为直接将文件合并再转码

```
cat intermediate1.mpg intermediate2.mpg |\
ffmpeg -f mpeg -i - -c:v mpeg4 -c:a libmp3lame output.avi
```

这样虽然也可以，但是一般 ts 文件数量都是比较多的，可以将 ts 文件名写入列表中，然后统一合并。

```
# filelist.txt：

file 'input1.ts'
file 'input2.ts'
file 'input3.ts'
```

**注意**
1. 如果文件名有奇怪的字符，要在 filelist.txt 中转义。     
2. ts 文件的位置是与 filelist.txt 的相对路径。

使用 FFmpeg concat 合并

```
ffmpeg -f concat -i filelist.txt -bsf:a aac_adtstoasc -c copy output.mp4
```

在文件列表中，除了 ts 文件的相对位置之外，也可以存储 ts 的网络位置，即 URI 。

比如 `v.qq.list` 文件列表中存储一部小短片中的 ts 片段地址

```
file https://apd-12dd18229b77409b7819cadf55b2b04d.v.smtcdns.com/omts.tc.qq.com/Ag9l8P9QAURHfwC8cEllr5PZsRbJO49sGyU0AFBANCb8/uwMROfz2r57BIaQXGdGnC2dXOm8P0YjZ7A3O5v3O_MjSfoLv/svp_50069/qAN57HVHcwmmYdxw7PBj8MjXIdcTdb-gRirCgnCWmYL1tG9of38ePitSgPwVlZVSIJMnqSK7KmjtvhCX6fhRTsyORPratFaOJ-iNcdgylmFonoMWzdDpYqmr7By8e2J9ISkqfbOi3i9oCl1Isf3dksVrbvhKuzvrVDx7xhVCOWU/00_gzc_1000035_0bc3kqa5waabi4ae3ohi2vpzivgd3nkadw2a.f306110.1.ts?index=0&start=0&end=10240&brs=0&bre=493499&ver=4&token=09810316cdc2e79b6fc86276629ed7f2
file https://apd-12dd18229b77409b7819cadf55b2b04d.v.smtcdns.com/omts.tc.qq.com/Ag9l8P9QAURHfwC8cEllr5PZsRbJO49sGyU0AFBANCb8/uwMROfz2r57BIaQXGdGnC2dXOm8P0YjZ7A3O5v3O_MjSfoLv/svp_50069/qAN57HVHcwmmYdxw7PBj8MjXIdcTdb-gRirCgnCWmYL1tG9of38ePitSgPwVlZVSIJMnqSK7KmjtvhCX6fhRTsyORPratFaOJ-iNcdgylmFonoMWzdDpYqmr7By8e2J9ISkqfbOi3i9oCl1Isf3dksVrbvhKuzvrVDx7xhVCOWU/01_gzc_1000035_0bc3kqa5waabi4ae3ohi2vpzivgd3nkadw2a.f306110.1.ts?index=1&start=10240&end=19440&brs=493500&bre=1068215&ver=4&token=2029595cf348093dd774b100df412e3c
file https://apd-12dd18229b77409b7819cadf55b2b04d.v.smtcdns.com/omts.tc.qq.com/Ag9l8P9QAURHfwC8cEllr5PZsRbJO49sGyU0AFBANCb8/uwMROfz2r57BIaQXGdGnC2dXOm8P0YjZ7A3O5v3O_MjSfoLv/svp_50069/qAN57HVHcwmmYdxw7PBj8MjXIdcTdb-gRirCgnCWmYL1tG9of38ePitSgPwVlZVSIJMnqSK7KmjtvhCX6fhRTsyORPratFaOJ-iNcdgylmFonoMWzdDpYqmr7By8e2J9ISkqfbOi3i9oCl1Isf3dksVrbvhKuzvrVDx7xhVCOWU/02_gzc_1000035_0bc3kqa5waabi4ae3ohi2vpzivgd3nkadw2a.f306110.1.ts?index=2&start=19440&end=29880&brs=1068216&bre=1595555&ver=4&token=09c318b29f4f911259d8e7642a9e5a0a
file https://apd-12dd18229b77409b7819cadf55b2b04d.v.smtcdns.com/omts.tc.qq.com/Ag9l8P9QAURHfwC8cEllr5PZsRbJO49sGyU0AFBANCb8/uwMROfz2r57BIaQXGdGnC2dXOm8P0YjZ7A3O5v3O_MjSfoLv/svp_50069/qAN57HVHcwmmYdxw7PBj8MjXIdcTdb-gRirCgnCWmYL1tG9of38ePitSgPwVlZVSIJMnqSK7KmjtvhCX6fhRTsyORPratFaOJ-iNcdgylmFonoMWzdDpYqmr7By8e2J9ISkqfbOi3i9oCl1Isf3dksVrbvhKuzvrVDx7xhVCOWU/03_gzc_1000035_0bc3kqa5waabi4ae3ohi2vpzivgd3nkadw2a.f306110.1.ts?index=3&start=29880&end=39080&brs=1595556&bre=2051831&ver=4&token=f288c265c3ab71852103fdfb22ef7543
file https://apd-12dd18229b77409b7819cadf55b2b04d.v.smtcdns.com/omts.tc.qq.com/Ag9l8P9QAURHfwC8cEllr5PZsRbJO49sGyU0AFBANCb8/uwMROfz2r57BIaQXGdGnC2dXOm8P0YjZ7A3O5v3O_MjSfoLv/svp_50069/qAN57HVHcwmmYdxw7PBj8MjXIdcTdb-gRirCgnCWmYL1tG9of38ePitSgPwVlZVSIJMnqSK7KmjtvhCX6fhRTsyORPratFaOJ-iNcdgylmFonoMWzdDpYqmr7By8e2J9ISkqfbOi3i9oCl1Isf3dksVrbvhKuzvrVDx7xhVCOWU/04_gzc_1000035_0bc3kqa5waabi4ae3ohi2vpzivgd3nkadw2a.f306110.1.ts?index=4&start=39080&end=50920&brs=2051832&bre=3229651&ver=4&token=a33c99faf630d2faa76b8c04881d1c9c
file https://apd-12dd18229b77409b7819cadf55b2b04d.v.smtcdns.com/omts.tc.qq.com/Ag9l8P9QAURHfwC8cEllr5PZsRbJO49sGyU0AFBANCb8/uwMROfz2r57BIaQXGdGnC2dXOm8P0YjZ7A3O5v3O_MjSfoLv/svp_50069/qAN57HVHcwmmYdxw7PBj8MjXIdcTdb-gRirCgnCWmYL1tG9of38ePitSgPwVlZVSIJMnqSK7KmjtvhCX6fhRTsyORPratFaOJ-iNcdgylmFonoMWzdDpYqmr7By8e2J9ISkqfbOi3i9oCl1Isf3dksVrbvhKuzvrVDx7xhVCOWU/05_gzc_1000035_0bc3kqa5waabi4ae3ohi2vpzivgd3nkadw2a.f306110.1.ts?index=5&start=50920&end=61800&brs=3229652&bre=5154395&ver=4&token=e10affbcdff184b96c55e0d0ab284f01
file https://apd-12dd18229b77409b7819cadf55b2b04d.v.smtcdns.com/omts.tc.qq.com/Ag9l8P9QAURHfwC8cEllr5PZsRbJO49sGyU0AFBANCb8/uwMROfz2r57BIaQXGdGnC2dXOm8P0YjZ7A3O5v3O_MjSfoLv/svp_50069/qAN57HVHcwmmYdxw7PBj8MjXIdcTdb-gRirCgnCWmYL1tG9of38ePitSgPwVlZVSIJMnqSK7KmjtvhCX6fhRTsyORPratFaOJ-iNcdgylmFonoMWzdDpYqmr7By8e2J9ISkqfbOi3i9oCl1Isf3dksVrbvhKuzvrVDx7xhVCOWU/06_gzc_1000035_0bc3kqa5waabi4ae3ohi2vpzivgd3nkadw2a.f306110.1.ts?index=6&start=61800&end=73800&brs=5154396&bre=5942115&ver=4&token=c1baf2b3cf5fa22447e9cf7774d0d806
file https://apd-12dd18229b77409b7819cadf55b2b04d.v.smtcdns.com/omts.tc.qq.com/Ag9l8P9QAURHfwC8cEllr5PZsRbJO49sGyU0AFBANCb8/uwMROfz2r57BIaQXGdGnC2dXOm8P0YjZ7A3O5v3O_MjSfoLv/svp_50069/qAN57HVHcwmmYdxw7PBj8MjXIdcTdb-gRirCgnCWmYL1tG9of38ePitSgPwVlZVSIJMnqSK7KmjtvhCX6fhRTsyORPratFaOJ-iNcdgylmFonoMWzdDpYqmr7By8e2J9ISkqfbOi3i9oCl1Isf3dksVrbvhKuzvrVDx7xhVCOWU/07_gzc_1000035_0bc3kqa5waabi4ae3ohi2vpzivgd3nkadw2a.f306110.1.ts?index=7&start=73800&end=84080&brs=5942116&bre=6880799&ver=4&token=906cbc7365901e534de6848d0bd746bc
file https://apd-12dd18229b77409b7819cadf55b2b04d.v.smtcdns.com/omts.tc.qq.com/Ag9l8P9QAURHfwC8cEllr5PZsRbJO49sGyU0AFBANCb8/uwMROfz2r57BIaQXGdGnC2dXOm8P0YjZ7A3O5v3O_MjSfoLv/svp_50069/qAN57HVHcwmmYdxw7PBj8MjXIdcTdb-gRirCgnCWmYL1tG9of38ePitSgPwVlZVSIJMnqSK7KmjtvhCX6fhRTsyORPratFaOJ-iNcdgylmFonoMWzdDpYqmr7By8e2J9ISkqfbOi3i9oCl1Isf3dksVrbvhKuzvrVDx7xhVCOWU/08_gzc_1000035_0bc3kqa5waabi4ae3ohi2vpzivgd3nkadw2a.f306110.1.ts?index=8&start=84080&end=93720&brs=6880800&bre=7359823&ver=4&token=62acb592784f0fc1ae520091d870eeac
file https://apd-12dd18229b77409b7819cadf55b2b04d.v.smtcdns.com/omts.tc.qq.com/Ag9l8P9QAURHfwC8cEllr5PZsRbJO49sGyU0AFBANCb8/uwMROfz2r57BIaQXGdGnC2dXOm8P0YjZ7A3O5v3O_MjSfoLv/svp_50069/qAN57HVHcwmmYdxw7PBj8MjXIdcTdb-gRirCgnCWmYL1tG9of38ePitSgPwVlZVSIJMnqSK7KmjtvhCX6fhRTsyORPratFaOJ-iNcdgylmFonoMWzdDpYqmr7By8e2J9ISkqfbOi3i9oCl1Isf3dksVrbvhKuzvrVDx7xhVCOWU/09_gzc_1000035_0bc3kqa5waabi4ae3ohi2vpzivgd3nkadw2a.f306110.1.ts?index=9&start=93720&end=103680&brs=7359824&bre=7877011&ver=4&token=3790a39e7125bddf058815f2eb10261d
file https://apd-12dd18229b77409b7819cadf55b2b04d.v.smtcdns.com/omts.tc.qq.com/Ag9l8P9QAURHfwC8cEllr5PZsRbJO49sGyU0AFBANCb8/uwMROfz2r57BIaQXGdGnC2dXOm8P0YjZ7A3O5v3O_MjSfoLv/svp_50069/qAN57HVHcwmmYdxw7PBj8MjXIdcTdb-gRirCgnCWmYL1tG9of38ePitSgPwVlZVSIJMnqSK7KmjtvhCX6fhRTsyORPratFaOJ-iNcdgylmFonoMWzdDpYqmr7By8e2J9ISkqfbOi3i9oCl1Isf3dksVrbvhKuzvrVDx7xhVCOWU/010_gzc_1000035_0bc3kqa5waabi4ae3ohi2vpzivgd3nkadw2a.f306110.1.ts?index=10&start=103680&end=114520&brs=7877012&bre=8324639&ver=4&token=826bd56d8542b868670d0b3de8382494
file https://apd-12dd18229b77409b7819cadf55b2b04d.v.smtcdns.com/omts.tc.qq.com/Ag9l8P9QAURHfwC8cEllr5PZsRbJO49sGyU0AFBANCb8/uwMROfz2r57BIaQXGdGnC2dXOm8P0YjZ7A3O5v3O_MjSfoLv/svp_50069/qAN57HVHcwmmYdxw7PBj8MjXIdcTdb-gRirCgnCWmYL1tG9of38ePitSgPwVlZVSIJMnqSK7KmjtvhCX6fhRTsyORPratFaOJ-iNcdgylmFonoMWzdDpYqmr7By8e2J9ISkqfbOi3i9oCl1Isf3dksVrbvhKuzvrVDx7xhVCOWU/011_gzc_1000035_0bc3kqa5waabi4ae3ohi2vpzivgd3nkadw2a.f306110.1.ts?index=11&start=114520&end=126360&brs=8324640&bre=8725831&ver=4&token=3ddfa99a0e2f6de30c103097fb56b7fb
file https://apd-12dd18229b77409b7819cadf55b2b04d.v.smtcdns.com/omts.tc.qq.com/Ag9l8P9QAURHfwC8cEllr5PZsRbJO49sGyU0AFBANCb8/uwMROfz2r57BIaQXGdGnC2dXOm8P0YjZ7A3O5v3O_MjSfoLv/svp_50069/qAN57HVHcwmmYdxw7PBj8MjXIdcTdb-gRirCgnCWmYL1tG9of38ePitSgPwVlZVSIJMnqSK7KmjtvhCX6fhRTsyORPratFaOJ-iNcdgylmFonoMWzdDpYqmr7By8e2J9ISkqfbOi3i9oCl1Isf3dksVrbvhKuzvrVDx7xhVCOWU/012_gzc_1000035_0bc3kqa5waabi4ae3ohi2vpzivgd3nkadw2a.f306110.1.ts?index=12&start=126360&end=135480&brs=8725832&bre=10149367&ver=4&token=e849bc33a9fbc279aa193865a8d4c936
file https://apd-12dd18229b77409b7819cadf55b2b04d.v.smtcdns.com/omts.tc.qq.com/Ag9l8P9QAURHfwC8cEllr5PZsRbJO49sGyU0AFBANCb8/uwMROfz2r57BIaQXGdGnC2dXOm8P0YjZ7A3O5v3O_MjSfoLv/svp_50069/qAN57HVHcwmmYdxw7PBj8MjXIdcTdb-gRirCgnCWmYL1tG9of38ePitSgPwVlZVSIJMnqSK7KmjtvhCX6fhRTsyORPratFaOJ-iNcdgylmFonoMWzdDpYqmr7By8e2J9ISkqfbOi3i9oCl1Isf3dksVrbvhKuzvrVDx7xhVCOWU/013_gzc_1000035_0bc3kqa5waabi4ae3ohi2vpzivgd3nkadw2a.f306110.1.ts?index=13&start=135480&end=144520&brs=10149368&bre=11845127&ver=4&token=8dc85e04c56d1d9fe6d8231b2bd6b6f6
file https://apd-12dd18229b77409b7819cadf55b2b04d.v.smtcdns.com/omts.tc.qq.com/Ag9l8P9QAURHfwC8cEllr5PZsRbJO49sGyU0AFBANCb8/uwMROfz2r57BIaQXGdGnC2dXOm8P0YjZ7A3O5v3O_MjSfoLv/svp_50069/qAN57HVHcwmmYdxw7PBj8MjXIdcTdb-gRirCgnCWmYL1tG9of38ePitSgPwVlZVSIJMnqSK7KmjtvhCX6fhRTsyORPratFaOJ-iNcdgylmFonoMWzdDpYqmr7By8e2J9ISkqfbOi3i9oCl1Isf3dksVrbvhKuzvrVDx7xhVCOWU/014_gzc_1000035_0bc3kqa5waabi4ae3ohi2vpzivgd3nkadw2a.f306110.1.ts?index=14&start=144520&end=152520&brs=11845128&bre=13365859&ver=4&token=1567c93b03efdaca0c544f2f623ce0ab
file https://apd-12dd18229b77409b7819cadf55b2b04d.v.smtcdns.com/omts.tc.qq.com/Ag9l8P9QAURHfwC8cEllr5PZsRbJO49sGyU0AFBANCb8/uwMROfz2r57BIaQXGdGnC2dXOm8P0YjZ7A3O5v3O_MjSfoLv/svp_50069/qAN57HVHcwmmYdxw7PBj8MjXIdcTdb-gRirCgnCWmYL1tG9of38ePitSgPwVlZVSIJMnqSK7KmjtvhCX6fhRTsyORPratFaOJ-iNcdgylmFonoMWzdDpYqmr7By8e2J9ISkqfbOi3i9oCl1Isf3dksVrbvhKuzvrVDx7xhVCOWU/015_gzc_1000035_0bc3kqa5waabi4ae3ohi2vpzivgd3nkadw2a.f306110.1.ts?index=15&start=152520&end=162480&brs=13365860&bre=14478819&ver=4&token=d0fc525bd16055ff28c15da6c07ef4d6
file https://apd-12dd18229b77409b7819cadf55b2b04d.v.smtcdns.com/omts.tc.qq.com/Ag9l8P9QAURHfwC8cEllr5PZsRbJO49sGyU0AFBANCb8/uwMROfz2r57BIaQXGdGnC2dXOm8P0YjZ7A3O5v3O_MjSfoLv/svp_50069/qAN57HVHcwmmYdxw7PBj8MjXIdcTdb-gRirCgnCWmYL1tG9of38ePitSgPwVlZVSIJMnqSK7KmjtvhCX6fhRTsyORPratFaOJ-iNcdgylmFonoMWzdDpYqmr7By8e2J9ISkqfbOi3i9oCl1Isf3dksVrbvhKuzvrVDx7xhVCOWU/016_gzc_1000035_0bc3kqa5waabi4ae3ohi2vpzivgd3nkadw2a.f306110.1.ts?index=16&start=162480&end=170520&brs=14478820&bre=15986767&ver=4&token=28de2b57f1497d841b5dddf8e8d5d709
file https://apd-12dd18229b77409b7819cadf55b2b04d.v.smtcdns.com/omts.tc.qq.com/Ag9l8P9QAURHfwC8cEllr5PZsRbJO49sGyU0AFBANCb8/uwMROfz2r57BIaQXGdGnC2dXOm8P0YjZ7A3O5v3O_MjSfoLv/svp_50069/qAN57HVHcwmmYdxw7PBj8MjXIdcTdb-gRirCgnCWmYL1tG9of38ePitSgPwVlZVSIJMnqSK7KmjtvhCX6fhRTsyORPratFaOJ-iNcdgylmFonoMWzdDpYqmr7By8e2J9ISkqfbOi3i9oCl1Isf3dksVrbvhKuzvrVDx7xhVCOWU/017_gzc_1000035_0bc3kqa5waabi4ae3ohi2vpzivgd3nkadw2a.f306110.1.ts?index=17&start=170520&end=182520&brs=15986768&bre=16818291&ver=4&token=03c4d12ccdbd0b0080f0c9841b9b86de
file https://apd-12dd18229b77409b7819cadf55b2b04d.v.smtcdns.com/omts.tc.qq.com/Ag9l8P9QAURHfwC8cEllr5PZsRbJO49sGyU0AFBANCb8/uwMROfz2r57BIaQXGdGnC2dXOm8P0YjZ7A3O5v3O_MjSfoLv/svp_50069/qAN57HVHcwmmYdxw7PBj8MjXIdcTdb-gRirCgnCWmYL1tG9of38ePitSgPwVlZVSIJMnqSK7KmjtvhCX6fhRTsyORPratFaOJ-iNcdgylmFonoMWzdDpYqmr7By8e2J9ISkqfbOi3i9oCl1Isf3dksVrbvhKuzvrVDx7xhVCOWU/018_gzc_1000035_0bc3kqa5waabi4ae3ohi2vpzivgd3nkadw2a.f306110.1.ts?index=18&start=182520&end=193680&brs=16818292&bre=17303143&ver=4&token=531fb8197047df958483b5d8201b8710
file https://apd-12dd18229b77409b7819cadf55b2b04d.v.smtcdns.com/omts.tc.qq.com/Ag9l8P9QAURHfwC8cEllr5PZsRbJO49sGyU0AFBANCb8/uwMROfz2r57BIaQXGdGnC2dXOm8P0YjZ7A3O5v3O_MjSfoLv/svp_50069/qAN57HVHcwmmYdxw7PBj8MjXIdcTdb-gRirCgnCWmYL1tG9of38ePitSgPwVlZVSIJMnqSK7KmjtvhCX6fhRTsyORPratFaOJ-iNcdgylmFonoMWzdDpYqmr7By8e2J9ISkqfbOi3i9oCl1Isf3dksVrbvhKuzvrVDx7xhVCOWU/019_gzc_1000035_0bc3kqa5waabi4ae3ohi2vpzivgd3nkadw2a.f306110.1.ts?index=19&start=193680&end=204640&brs=17303144&bre=17984079&ver=4&token=9175c42709446c8dbe28dd5024a1185f
file https://apd-12dd18229b77409b7819cadf55b2b04d.v.smtcdns.com/omts.tc.qq.com/Ag9l8P9QAURHfwC8cEllr5PZsRbJO49sGyU0AFBANCb8/uwMROfz2r57BIaQXGdGnC2dXOm8P0YjZ7A3O5v3O_MjSfoLv/svp_50069/qAN57HVHcwmmYdxw7PBj8MjXIdcTdb-gRirCgnCWmYL1tG9of38ePitSgPwVlZVSIJMnqSK7KmjtvhCX6fhRTsyORPratFaOJ-iNcdgylmFonoMWzdDpYqmr7By8e2J9ISkqfbOi3i9oCl1Isf3dksVrbvhKuzvrVDx7xhVCOWU/020_gzc_1000035_0bc3kqa5waabi4ae3ohi2vpzivgd3nkadw2a.f306110.1.ts?index=20&start=204640&end=213320&brs=17984080&bre=19072787&ver=4&token=62c7a1b48dfab955d694f83f56d1b40f
file https://apd-12dd18229b77409b7819cadf55b2b04d.v.smtcdns.com/omts.tc.qq.com/Ag9l8P9QAURHfwC8cEllr5PZsRbJO49sGyU0AFBANCb8/uwMROfz2r57BIaQXGdGnC2dXOm8P0YjZ7A3O5v3O_MjSfoLv/svp_50069/qAN57HVHcwmmYdxw7PBj8MjXIdcTdb-gRirCgnCWmYL1tG9of38ePitSgPwVlZVSIJMnqSK7KmjtvhCX6fhRTsyORPratFaOJ-iNcdgylmFonoMWzdDpYqmr7By8e2J9ISkqfbOi3i9oCl1Isf3dksVrbvhKuzvrVDx7xhVCOWU/021_gzc_1000035_0bc3kqa5waabi4ae3ohi2vpzivgd3nkadw2a.f306110.1.ts?index=21&start=213320&end=222800&brs=19072788&bre=20576787&ver=4&token=3d67d7868da9a7f66cff2556f747fd71
file https://apd-12dd18229b77409b7819cadf55b2b04d.v.smtcdns.com/omts.tc.qq.com/Ag9l8P9QAURHfwC8cEllr5PZsRbJO49sGyU0AFBANCb8/uwMROfz2r57BIaQXGdGnC2dXOm8P0YjZ7A3O5v3O_MjSfoLv/svp_50069/qAN57HVHcwmmYdxw7PBj8MjXIdcTdb-gRirCgnCWmYL1tG9of38ePitSgPwVlZVSIJMnqSK7KmjtvhCX6fhRTsyORPratFaOJ-iNcdgylmFonoMWzdDpYqmr7By8e2J9ISkqfbOi3i9oCl1Isf3dksVrbvhKuzvrVDx7xhVCOWU/022_gzc_1000035_0bc3kqa5waabi4ae3ohi2vpzivgd3nkadw2a.f306110.1.ts?index=22&start=222800&end=232840&brs=20576788&bre=22316727&ver=4&token=9026b6254017b1c3790ff555e8802dd4
file https://apd-12dd18229b77409b7819cadf55b2b04d.v.smtcdns.com/omts.tc.qq.com/Ag9l8P9QAURHfwC8cEllr5PZsRbJO49sGyU0AFBANCb8/uwMROfz2r57BIaQXGdGnC2dXOm8P0YjZ7A3O5v3O_MjSfoLv/svp_50069/qAN57HVHcwmmYdxw7PBj8MjXIdcTdb-gRirCgnCWmYL1tG9of38ePitSgPwVlZVSIJMnqSK7KmjtvhCX6fhRTsyORPratFaOJ-iNcdgylmFonoMWzdDpYqmr7By8e2J9ISkqfbOi3i9oCl1Isf3dksVrbvhKuzvrVDx7xhVCOWU/023_gzc_1000035_0bc3kqa5waabi4ae3ohi2vpzivgd3nkadw2a.f306110.1.ts?index=23&start=232840&end=243320&brs=22316728&bre=23733119&ver=4&token=f1ce588e41918c60e7ebaa92798e38d2
file https://apd-12dd18229b77409b7819cadf55b2b04d.v.smtcdns.com/omts.tc.qq.com/Ag9l8P9QAURHfwC8cEllr5PZsRbJO49sGyU0AFBANCb8/uwMROfz2r57BIaQXGdGnC2dXOm8P0YjZ7A3O5v3O_MjSfoLv/svp_50069/qAN57HVHcwmmYdxw7PBj8MjXIdcTdb-gRirCgnCWmYL1tG9of38ePitSgPwVlZVSIJMnqSK7KmjtvhCX6fhRTsyORPratFaOJ-iNcdgylmFonoMWzdDpYqmr7By8e2J9ISkqfbOi3i9oCl1Isf3dksVrbvhKuzvrVDx7xhVCOWU/024_gzc_1000035_0bc3kqa5waabi4ae3ohi2vpzivgd3nkadw2a.f306110.1.ts?index=24&start=243320&end=251960&brs=23733120&bre=24250119&ver=4&token=4f6396f3e58bcdbdb952b80500e5e392
file https://apd-12dd18229b77409b7819cadf55b2b04d.v.smtcdns.com/omts.tc.qq.com/Ag9l8P9QAURHfwC8cEllr5PZsRbJO49sGyU0AFBANCb8/uwMROfz2r57BIaQXGdGnC2dXOm8P0YjZ7A3O5v3O_MjSfoLv/svp_50069/qAN57HVHcwmmYdxw7PBj8MjXIdcTdb-gRirCgnCWmYL1tG9of38ePitSgPwVlZVSIJMnqSK7KmjtvhCX6fhRTsyORPratFaOJ-iNcdgylmFonoMWzdDpYqmr7By8e2J9ISkqfbOi3i9oCl1Isf3dksVrbvhKuzvrVDx7xhVCOWU/025_gzc_1000035_0bc3kqa5waabi4ae3ohi2vpzivgd3nkadw2a.f306110.1.ts?index=25&start=251960&end=261040&brs=24250120&bre=24824083&ver=4&token=df58735bf779e2bb46ad225f8d438d84
file https://apd-12dd18229b77409b7819cadf55b2b04d.v.smtcdns.com/omts.tc.qq.com/Ag9l8P9QAURHfwC8cEllr5PZsRbJO49sGyU0AFBANCb8/uwMROfz2r57BIaQXGdGnC2dXOm8P0YjZ7A3O5v3O_MjSfoLv/svp_50069/qAN57HVHcwmmYdxw7PBj8MjXIdcTdb-gRirCgnCWmYL1tG9of38ePitSgPwVlZVSIJMnqSK7KmjtvhCX6fhRTsyORPratFaOJ-iNcdgylmFonoMWzdDpYqmr7By8e2J9ISkqfbOi3i9oCl1Isf3dksVrbvhKuzvrVDx7xhVCOWU/026_gzc_1000035_0bc3kqa5waabi4ae3ohi2vpzivgd3nkadw2a.f306110.1.ts?index=26&start=261040&end=268560&brs=24824084&bre=25233359&ver=4&token=70682b6c2610af160bc11326b72e460d
file https://apd-12dd18229b77409b7819cadf55b2b04d.v.smtcdns.com/omts.tc.qq.com/Ag9l8P9QAURHfwC8cEllr5PZsRbJO49sGyU0AFBANCb8/uwMROfz2r57BIaQXGdGnC2dXOm8P0YjZ7A3O5v3O_MjSfoLv/svp_50069/qAN57HVHcwmmYdxw7PBj8MjXIdcTdb-gRirCgnCWmYL1tG9of38ePitSgPwVlZVSIJMnqSK7KmjtvhCX6fhRTsyORPratFaOJ-iNcdgylmFonoMWzdDpYqmr7By8e2J9ISkqfbOi3i9oCl1Isf3dksVrbvhKuzvrVDx7xhVCOWU/027_gzc_1000035_0bc3kqa5waabi4ae3ohi2vpzivgd3nkadw2a.f306110.1.ts?index=27&start=268560&end=280560&brs=25233360&bre=25918431&ver=4&token=0d96dd047c8a9e53d0a1166300db16b6
file https://apd-12dd18229b77409b7819cadf55b2b04d.v.smtcdns.com/omts.tc.qq.com/Ag9l8P9QAURHfwC8cEllr5PZsRbJO49sGyU0AFBANCb8/uwMROfz2r57BIaQXGdGnC2dXOm8P0YjZ7A3O5v3O_MjSfoLv/svp_50069/qAN57HVHcwmmYdxw7PBj8MjXIdcTdb-gRirCgnCWmYL1tG9of38ePitSgPwVlZVSIJMnqSK7KmjtvhCX6fhRTsyORPratFaOJ-iNcdgylmFonoMWzdDpYqmr7By8e2J9ISkqfbOi3i9oCl1Isf3dksVrbvhKuzvrVDx7xhVCOWU/028_gzc_1000035_0bc3kqa5waabi4ae3ohi2vpzivgd3nkadw2a.f306110.1.ts?index=28&start=280560&end=292120&brs=25918432&bre=26845083&ver=4&token=73e8f867e71f387727f65db763143859
file https://apd-12dd18229b77409b7819cadf55b2b04d.v.smtcdns.com/omts.tc.qq.com/Ag9l8P9QAURHfwC8cEllr5PZsRbJO49sGyU0AFBANCb8/uwMROfz2r57BIaQXGdGnC2dXOm8P0YjZ7A3O5v3O_MjSfoLv/svp_50069/qAN57HVHcwmmYdxw7PBj8MjXIdcTdb-gRirCgnCWmYL1tG9of38ePitSgPwVlZVSIJMnqSK7KmjtvhCX6fhRTsyORPratFaOJ-iNcdgylmFonoMWzdDpYqmr7By8e2J9ISkqfbOi3i9oCl1Isf3dksVrbvhKuzvrVDx7xhVCOWU/029_gzc_1000035_0bc3kqa5waabi4ae3ohi2vpzivgd3nkadw2a.f306110.1.ts?index=29&start=292120&end=302480&brs=26845084&bre=27415851&ver=4&token=f8d0c68f34afa1391b18d6fb919733e4
file https://apd-12dd18229b77409b7819cadf55b2b04d.v.smtcdns.com/omts.tc.qq.com/Ag9l8P9QAURHfwC8cEllr5PZsRbJO49sGyU0AFBANCb8/uwMROfz2r57BIaQXGdGnC2dXOm8P0YjZ7A3O5v3O_MjSfoLv/svp_50069/qAN57HVHcwmmYdxw7PBj8MjXIdcTdb-gRirCgnCWmYL1tG9of38ePitSgPwVlZVSIJMnqSK7KmjtvhCX6fhRTsyORPratFaOJ-iNcdgylmFonoMWzdDpYqmr7By8e2J9ISkqfbOi3i9oCl1Isf3dksVrbvhKuzvrVDx7xhVCOWU/030_gzc_1000035_0bc3kqa5waabi4ae3ohi2vpzivgd3nkadw2a.f306110.2.ts?index=30&start=302480&end=310800&brs=0&bre=561555&ver=4&token=379bd72a50d56128a736606043bfdad1
file https://apd-12dd18229b77409b7819cadf55b2b04d.v.smtcdns.com/omts.tc.qq.com/Ag9l8P9QAURHfwC8cEllr5PZsRbJO49sGyU0AFBANCb8/uwMROfz2r57BIaQXGdGnC2dXOm8P0YjZ7A3O5v3O_MjSfoLv/svp_50069/qAN57HVHcwmmYdxw7PBj8MjXIdcTdb-gRirCgnCWmYL1tG9of38ePitSgPwVlZVSIJMnqSK7KmjtvhCX6fhRTsyORPratFaOJ-iNcdgylmFonoMWzdDpYqmr7By8e2J9ISkqfbOi3i9oCl1Isf3dksVrbvhKuzvrVDx7xhVCOWU/031_gzc_1000035_0bc3kqa5waabi4ae3ohi2vpzivgd3nkadw2a.f306110.2.ts?index=31&start=310800&end=320040&brs=561556&bre=876831&ver=4&token=6c47a645e9938087ad2f247ed7babaec
file https://apd-12dd18229b77409b7819cadf55b2b04d.v.smtcdns.com/omts.tc.qq.com/Ag9l8P9QAURHfwC8cEllr5PZsRbJO49sGyU0AFBANCb8/uwMROfz2r57BIaQXGdGnC2dXOm8P0YjZ7A3O5v3O_MjSfoLv/svp_50069/qAN57HVHcwmmYdxw7PBj8MjXIdcTdb-gRirCgnCWmYL1tG9of38ePitSgPwVlZVSIJMnqSK7KmjtvhCX6fhRTsyORPratFaOJ-iNcdgylmFonoMWzdDpYqmr7By8e2J9ISkqfbOi3i9oCl1Isf3dksVrbvhKuzvrVDx7xhVCOWU/032_gzc_1000035_0bc3kqa5waabi4ae3ohi2vpzivgd3nkadw2a.f306110.2.ts?index=32&start=320040&end=329080&brs=876832&bre=1475047&ver=4&token=4e489a5ef2d3c08461344f9ffce1ef5d
file https://apd-12dd18229b77409b7819cadf55b2b04d.v.smtcdns.com/omts.tc.qq.com/Ag9l8P9QAURHfwC8cEllr5PZsRbJO49sGyU0AFBANCb8/uwMROfz2r57BIaQXGdGnC2dXOm8P0YjZ7A3O5v3O_MjSfoLv/svp_50069/qAN57HVHcwmmYdxw7PBj8MjXIdcTdb-gRirCgnCWmYL1tG9of38ePitSgPwVlZVSIJMnqSK7KmjtvhCX6fhRTsyORPratFaOJ-iNcdgylmFonoMWzdDpYqmr7By8e2J9ISkqfbOi3i9oCl1Isf3dksVrbvhKuzvrVDx7xhVCOWU/033_gzc_1000035_0bc3kqa5waabi4ae3ohi2vpzivgd3nkadw2a.f306110.2.ts?index=33&start=329080&end=340320&brs=1475048&bre=1977947&ver=4&token=da94e9c74eec78b80e3faeb0dd8f80dc
file https://apd-12dd18229b77409b7819cadf55b2b04d.v.smtcdns.com/omts.tc.qq.com/Ag9l8P9QAURHfwC8cEllr5PZsRbJO49sGyU0AFBANCb8/uwMROfz2r57BIaQXGdGnC2dXOm8P0YjZ7A3O5v3O_MjSfoLv/svp_50069/qAN57HVHcwmmYdxw7PBj8MjXIdcTdb-gRirCgnCWmYL1tG9of38ePitSgPwVlZVSIJMnqSK7KmjtvhCX6fhRTsyORPratFaOJ-iNcdgylmFonoMWzdDpYqmr7By8e2J9ISkqfbOi3i9oCl1Isf3dksVrbvhKuzvrVDx7xhVCOWU/034_gzc_1000035_0bc3kqa5waabi4ae3ohi2vpzivgd3nkadw2a.f306110.2.ts?index=34&start=340320&end=347400&brs=1977948&bre=2322363&ver=4&token=aa840beef0043a9896ca44fb77318ffd
file https://apd-12dd18229b77409b7819cadf55b2b04d.v.smtcdns.com/omts.tc.qq.com/Ag9l8P9QAURHfwC8cEllr5PZsRbJO49sGyU0AFBANCb8/uwMROfz2r57BIaQXGdGnC2dXOm8P0YjZ7A3O5v3O_MjSfoLv/svp_50069/qAN57HVHcwmmYdxw7PBj8MjXIdcTdb-gRirCgnCWmYL1tG9of38ePitSgPwVlZVSIJMnqSK7KmjtvhCX6fhRTsyORPratFaOJ-iNcdgylmFonoMWzdDpYqmr7By8e2J9ISkqfbOi3i9oCl1Isf3dksVrbvhKuzvrVDx7xhVCOWU/035_gzc_1000035_0bc3kqa5waabi4ae3ohi2vpzivgd3nkadw2a.f306110.2.ts?index=35&start=347400&end=359400&brs=2322364&bre=2801199&ver=4&token=f11d605fef9d6d267a4a2abfed71f4dd
file https://apd-12dd18229b77409b7819cadf55b2b04d.v.smtcdns.com/omts.tc.qq.com/Ag9l8P9QAURHfwC8cEllr5PZsRbJO49sGyU0AFBANCb8/uwMROfz2r57BIaQXGdGnC2dXOm8P0YjZ7A3O5v3O_MjSfoLv/svp_50069/qAN57HVHcwmmYdxw7PBj8MjXIdcTdb-gRirCgnCWmYL1tG9of38ePitSgPwVlZVSIJMnqSK7KmjtvhCX6fhRTsyORPratFaOJ-iNcdgylmFonoMWzdDpYqmr7By8e2J9ISkqfbOi3i9oCl1Isf3dksVrbvhKuzvrVDx7xhVCOWU/036_gzc_1000035_0bc3kqa5waabi4ae3ohi2vpzivgd3nkadw2a.f306110.2.ts?index=36&start=359400&end=375680&brs=2801200&bre=3572751&ver=4&token=1b237cb0507349b7ccec30d116705602
```

使用 FFmpeg 直接下载并合并

```
ffmpeg -f concat -safe 0  -protocol_whitelist file,http,https,tcp,tls,crypto   -i v.qq.list  -c copy v.qq.mp4
```

> 可以使用 `-headers 'Referer: https://v.qq.com'`增加请求 headers 信息

## ffprobe

在 FFmpeg 套件中，除了 ffmpeg 命令之外，还有两个工具命令，ffprobe 可以用来查看使用信息。

```
ffprobe video-1589278522.29.mp4
```

## ffplay

ffplay 播放视频，除了可以播放本地视频，还能播放网络视频。

```
ffplay video-1589278522.29.mp4
```

播放网络视频

```
ffplay -window_title "播放测试" rtmp://up.v.test.com/live/stream
```

## 参考

[FFMPEG 视频分割和合并](https://www.jianshu.com/p/cf1e61eb6fc8)  
[使用FFMPEG将ts无损转换为mp4](https://www.simaek.com/archives/6/)    
[使用ffmpeg合并视频文件的三种方法](https://blog.csdn.net/spark_csdn/article/details/57080034)      
[用ffmpeg拼接音视频、字幕：concat方案的三种用法及优缺点](https://www.bilibili.com/read/cv4830499/)         
[ffmpeg拼接视频方法concat详解](https://www.cnblogs.com/huojinfeng/articles/13167730.html)        
[3.14 How can I concatenate video files?](https://ffmpeg.org/faq.html#How-can-I-concatenate-video-files_003f)    
[使用ffmpeg简单裁剪素材，-ss、-t、-to参数的学习](https://www.bilibili.com/read/cv4497290?from=articleDetail)     
[ffmpeg 视频截图](https://blog.csdn.net/ternence_hsu/article/details/92980451)        
[FFmpeg 视频处理入门教程](http://www.ruanyifeng.com/blog/2020/01/ffmpeg.html)     
[视频格式那么多，MP4/RMVB/MKV/AVI 等，这些视频格式与编码压缩标准 mpeg4，H.264.H.265 等有什么关系？](https://www.zhihu.com/question/20997688)           
[FFmpeg工具使用及参数说明](https://blog.csdn.net/DaveBobo/article/details/80685328)       
[ffmpeg常用命令](https://blog.csdn.net/newchenxf/article/details/51384360)             
 
