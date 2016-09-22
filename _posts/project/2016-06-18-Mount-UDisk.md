---
layout: post
title: 树莓派下挂载 u盘
category: project
description:  早期的 linux 都是不能自动挂载 U 盘的，但是现在好像一些常用的发行版本都可以自动挂载了，什么都可以在图形化界面下操作，都快不知道 U 盘是怎么挂载上的了。
---

树莓派二代 B ，比较老的版本了，准备做一个 samba 服务器，但是自身的 TF 卡只有 16 G 并不是很大，还准备把它做一个下载器，就需要大一点的空间，挂载一个 32 G 的 U 盘上去试试。

## 查看磁盘信息和已挂载分区

```
pi@raspberrypi ~ $ sudo fdisk -l

Disk /dev/mmcblk0: 15.5 GB, 15523119104 bytes
4 heads, 16 sectors/track, 473728 cylinders, total 30318592 sectors
Units = sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disk identifier: 0x0009bf4f

        Device Boot      Start         End      Blocks   Id  System
/dev/mmcblk0p1            8192      122879       57344    c  W95 FAT32 (LBA)
/dev/mmcblk0p2          122880    30318591    15097856   83  Linux

Disk /dev/sda: 32.2 GB, 32161923072 bytes
255 heads, 63 sectors/track, 3910 cylinders, total 62816256 sectors
Units = sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disk identifier: 0x0a9a1b1a

   Device Boot      Start         End      Blocks   Id  System
/dev/sda1            2048    62816255    31407104    7  HPFS/NTFS/exFAT
pi@raspberrypi ~ $ sudo df -lhT
Filesystem     Type      Size  Used Avail Use% Mounted on
/dev/root      ext4       15G  8.8G  4.8G  65% /
devtmpfs       devtmpfs  214M     0  214M   0% /dev
tmpfs          tmpfs      44M  720K   43M   2% /run
tmpfs          tmpfs     5.0M     0  5.0M   0% /run/lock
tmpfs          tmpfs      87M     0   87M   0% /run/shm
/dev/mmcblk0p1 vfat       56M   20M   37M  36% /boot

```

可以看到有两个磁盘，第一个磁盘为 `/dev/mmcblk0` 是我的 16 G 的 TF 卡，第二个 `/dev/sda` 是我 32 G 的 U 盘，已有一个分区 '/dev/sda1'，分区格式为 `NTFS` ， x现在我们需要将 U 盘中原有的分区删除然后进行重新分区，并将文件格式改为 Linux 下的 ext4 。

## 删除 U 盘上原有分区并创建新分区

```
pi@raspberrypi ~ $ sudo fdisk /dev/sda

Command (m for help): m         // 查看帮助
Command action
   a   toggle a bootable flag
   b   edit bsd disklabel
   c   toggle the dos compatibility flag
   d   delete a partition
   l   list known partition types
   m   print this menu
   n   add a new partition
   o   create a new empty DOS partition table
   p   print the partition table
   q   quit without saving changes
   s   create a new empty Sun disklabel
   t   change a partition's system id
   u   change display/entry units
   v   verify the partition table
   w   write table to disk and exit
   x   extra functionality (experts only)

Command (m for help): p         // 查看分区信息

Disk /dev/sda: 32.2 GB, 32161923072 bytes
255 heads, 63 sectors/track, 3910 cylinders, total 62816256 sectors
Units = sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disk identifier: 0x0a9a1b1a

   Device Boot      Start         End      Blocks   Id  System
/dev/sda1            2048    62816255    31407104    7  HPFS/NTFS/exFAT

Command (m for help): d         // 删除分区
Selected partition 1                    // 如果有多个分区，在此处会让你进行选择分区

Command (m for help): p         // 查看分区信息

Disk /dev/sda: 32.2 GB, 32161923072 bytes
255 heads, 63 sectors/track, 3910 cylinders, total 62816256 sectors
Units = sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disk identifier: 0x0a9a1b1a

   Device Boot      Start         End      Blocks   Id  System

Command (m for help): n         // 新建分区
Partition type:
   p   primary (0 primary, 0 extended, 4 free)
   e   extended
Select (default p):                         // 直接 Enter 选择默认
Using default response p
Partition number (1-4, default 1):      // 选择默认
Using default value 1
First sector (2048-62816255, default 2048):     //选择默认
Using default value 2048
Last sector, +sectors or +size{K,M,G} (2048-62816255, default 62816255):        //选择默认
Using default value 62816255

Command (m for help): p         // 查看分区信息

Disk /dev/sda: 32.2 GB, 32161923072 bytes
255 heads, 63 sectors/track, 3910 cylinders, total 62816256 sectors
Units = sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disk identifier: 0x0a9a1b1a

   Device Boot      Start         End      Blocks   Id  System
/dev/sda1            2048    62816255    31407104   83  Linux

Command (m for help): w         // 执行更改并保存退出
The partition table has been altered!

Calling ioctl() to re-read partition table.
Syncing disks.
pi@raspberrypi ~ $

```

## 格式化新分区
在上面可以看到树莓派原来使用的就是 ext4 格式的文件系统，我们就把 U 盘也格式化为这种格式的。

```
pi@raspberrypi ~ $ sudo mkfs.ext4 /dev/sda1
mke2fs 1.42.5 (29-Jul-2012)
Filesystem label=
OS type: Linux
Block size=4096 (log=2)
Fragment size=4096 (log=2)
Stride=0 blocks, Stripe width=0 blocks
1966080 inodes, 7851776 blocks
392588 blocks (5.00%) reserved for the super user
First data block=0
Maximum filesystem blocks=0
240 block groups
32768 blocks per group, 32768 fragments per group
8192 inodes per group
Superblock backups stored on blocks:
    32768, 98304, 163840, 229376, 294912, 819200, 884736, 1605632, 2654208,
    4096000

Allocating group tables: done
Writing inode tables: done
Creating journal (32768 blocks): done
Writing superblocks and filesystem accounting information: done

```

或者是格式化为其他格式的u盘

```
sudo mkfs.vfat /dev/sda1          //格式化为 VFAT 格式的 U 盘
sudo mkfs.ntfs /dev/sda1          //格式化为 NTFS 格式的 U 盘
sudo mkfs.ntfs -f /dev/sda1          //快速格式化
```

### 挂载 U 盘

```
pi@raspberrypi ~ $ mkdir media
pi@raspberrypi ~ $ cd media/
pi@raspberrypi ~/media $ mkdir Disk
pi@raspberrypi ~/media $ sudo mount /dev/sda1 ./Disk/
pi@raspberrypi ~/media $ sudo df -h
Filesystem      Size  Used Avail Use% Mounted on
/dev/root        15G  8.8G  4.8G  65% /
devtmpfs        214M     0  214M   0% /dev
tmpfs            44M  720K   43M   2% /run
tmpfs           5.0M     0  5.0M   0% /run/lock
tmpfs            87M     0   87M   0% /run/shm
/dev/mmcblk0p1   56M   20M   37M  36% /boot
/dev/sda1        30G   44M   28G   1% /home/pi/media/Disk

```

这样 U 盘就挂载到了 `～/media/Disk`  下，不过有一点问题，就是只能以 root 权限读写，pi 用户不能读写。

## 卸载 U 盘
我们先卸载了，然后再挂载上，让 pi 用户也能使用

```
pi@raspberrypi ~/media/Disk $ echo "test">test.txt
-bash: test.txt: Permission denied
pi@raspberrypi ~/media/Disk $ cd ../
pi@raspberrypi ~/media $ sudo umount /home/pi/media/Disk
pi@raspberrypi ~/media $ sudo mount /dev/sda1 ./Disk/
pi@raspberrypi ~/media $ sudo chmod -R 777 Disk/
pi@raspberrypi ~/media $ cd Disk/
pi@raspberrypi ~/media/Disk $ echo "test">test.txt
```

## 开机自动挂载

```
pi@raspberrypi /etc $ sudo vim fstab
```

将文件内容改成这样

```
proc            /proc           proc    defaults          0       0
/dev/mmcblk0p1  /boot           vfat    defaults          0       2
/dev/mmcblk0p2  /               ext4    defaults,noatime  0       1
/dev/sda1       /home/pi/media/Disk     ext4    defaults,noexec,umask=0000      0       0
# a swapfile is not a swap partition, so no using swapon|off from here on, use  dphys-swapfile swap[on|off]  for that
```

说明：
sda1是取决于你的实际情况，a 表示第一个硬盘，1 表示第一个分区。
umask=0000 0 0
前面四个 0 就是对所有人,可读可写可执行,
后面两个 0 ,第一个代表 dump , 0 是不备份,第二个代表 fsck 检查的顺序, 0 表示不检查

