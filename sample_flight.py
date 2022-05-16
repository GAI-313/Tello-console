#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tello import console #tello.py の console クラスを呼び出す。

def main(): # メイン関数
    drone = console() # console クラスを有効化
    drone.takeoff() # 離陸
    drone.cw(360) # 時計回りに 360°旋回
    drone.down(50) # 50 cm 下降
    drone.up(100) # 100 cm 上昇
    drone.forward(100)  # 100 cm 前進
    drone.back(100) # 100 cm 後進
    drone.cw(90) # 時計回りに 90°旋回
    drone.left(100)  # 100 cm 左
    drone.right(100) # 100 cm 右
    drone.land() # 着陸

if __name__ == "__main__": # このプログラムが外部から実行されないようにするおまじない
    main() # メインを実行
