#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tello import console #tello.py の console クラスを呼び出す。

def main(): # メイン関数
    try: # 例外処理　except と一緒に記述する
        drone = console() # console クラスを有効化
        
        drone.takeoff() # 離陸
        drone.cw(360) # 360°旋回
        drone.land() # 着陸
    
    except KeyboardInterrupt: # Cntrol + C が押されたら以下の処理を実行
        drone.emergency() # モーター停止
    
    del drone

if __name__ == "__main__": # このプログラムが外部から実行されないようにするおまじない
    main() # メインを実行
