# Tello.py解説
## 01 Modules
Tello.pyは、以下のモジュールを使用して機能しています。
|モジュール名|使用内容|
|----|----|
|socket|ドローンとの通信に使用|
|threading|プログラムを並列稼働させるのに使用|
|cv2|ドローンからのカメラデータを取得するのに使用|
|numpy|ドローンからの2次元配列データを処理するのに使用|
|time|時間管理のために使用|
|sys|プログラム停止用に使用|
  
モジュールのインポートについてはこのようになっています。
```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re # これはなくてもいい
import socket
import threading
import numpy as np
import time
import cv2
import sys
```
## 02 SetClass
```python
class console():
```
ここでクラスが定義されています。
## 03 Init
```python
  def __init__(self,cmd_timeout=3, tello_ip='192.168.10.1', tello_port=8889):
```
この関数は、クラスが実行された際の初期値を定義する関数です。クラス内に記述されるこの関数はメゾットと呼ばれます。メゾットには、必ず第1引数に self を定義します。
## 04 Del
## 05 Recver
## 06 Video Recver
## 07 Timeout
## 08 Send cmd
## 09 Sset aboutFrag
