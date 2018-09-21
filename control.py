#!/usr/bin/env python
# coding:utf-8

import resource
import run as r
rsrc = resource.RLIMIT_AS
soft, hard = resource.getrlimit(rsrc)
## Memory sizeの制限
## 現在の設定を取得
## softはユーザーで設定、hardはスーパーユーザーで設定できる。

soft = 1024
resource.setrlimit(rsrc,(soft,hard))
## 1024バイト、-1はシステムで許されている上限を設定。

rsrc = resource.RLIMIT_CPU
## CPU使用時間の制限:単位(秒)
resource.setrlimit(rsrc,(0.01,hard))


## このプロセスのリソースの使用状態を把握する
# print getattr(resource.getrusage(resource.RUSAGE_SELF),'ru_utime')
## ユーザモードの実行時間
# print(resource.getrusage(resource.RUSAGE_SELF),'ru_ixrss')
## 共有メモリのサイズ