#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tello import console #tello.py の console クラスを呼び出す。
import cv2 # open cv をインポート

def main(): # メイン関数
    drone = console() # console クラスを有効化
    while True:
        frame = drone.frame # このデータにドローンからのビデオデータがはいいている。
        if frame is None or frame.size == 0: # フレームデータがない、またはフレームのサイズが0の時は無視する
            continue
        cv2.imshow("TELLO CAMERA VIEW",frame) # ビデオを画面出力
        key = cv2.waitKey(1)
        if key & 0xFF == 27: # ESC キーが押されたら終了
            break
        elif key & 0xFF == ord("1"): # 下方カメラに切り替え
            print("down")
            drone.downvision(1)
        elif key & 0xFF == ord("2"): # メインカメラに切り替え
            print("up")
            drone.downvision(0)

    
    drone.cap.release # ドローンからのビデオデータ更新を停止
    cv2.destroyAllWindows() # cv2 によって生成されたウィンドウを殺す


if __name__ == "__main__": # このプログラムが外部から実行されないようにするおまじない
    main() # メインを実行
    del console # クラスのデストラクタを実行
