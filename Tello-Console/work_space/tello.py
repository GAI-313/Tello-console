#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import socket
import threading
import numpy as np
import time
import cv2
import sys

class console():
    def __init__(self,cmd_timeout=3, tello_ip='192.168.10.1', tello_port=8889):
        self.about_frag = False #中断フラグ
        self.cmd_timeout = cmd_timeout #タイムアウト時間
        self.response = None #応答データ
        self.frame = None #ドローンカメラの映像データ
        self.cap = None # ドローンキャプチャデータ
        self.flight_speed = 100 # ドローンの水平飛行速度のデフォルト値
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #ソケット送受信ようソケット
        self.tello_address = (tello_ip, tello_port) # 通信用ipアドレス
        self.local_video_port = 11111 # ビデオ受信ポート番号
        self.video_address = 'udp://@0.0.0.0:11111'
        self.last_height = 0 # 飛行高度初期値
        self.sock.bind(("", 8889))
        #コマンド応答受信スレッド
        self.recv_thread = threading.Thread(target=self._recver)
        self.recv_thread.daemon = True
        self.recv_thread.start()
        # ビデオ受信の開始
        response = self.send_cmd("command")
        if response == "None response":
            print('\033[31m'+"接続エラー：ドローンに接続されていません。"+'\033[0m')
            sys.exit()
        self.send_cmd("streamon")
        response = self.get_battery()
        response = int(response)
        if response <= 10:
            print('\033[31m'+"バッテリー残量が少ないため、プログラムは中止されました。：残り {}% "+'\033[0m'.format(response))
            sys.exit()
        # ビデオ受信スレッド
        self.video_recv_thread = threading.Thread(target=self._video_recver)
        self.video_recv_thread.daemon = True
        self.video_recv_thread.start()
        # タイムアウトカウンタースレッドの構築
        self.timeout_frag = False
        self.timeout_skipper_frag = False
        self.timeout_thread = threading.Thread(target=self._timeout)
        self.timeout_thread.daemon = True
        self.timeout_thread.start()

    def __del__(self):
        """ローカル通信を閉じる"""
        self.sock.close()
        print("Done")
    
    def _recver(self):
        """
        ドローンからの応答を監視するスレッド
        """
        while True:
            try:
                self.response, ip = self.sock.recvfrom(3000)  
            except socket.error as se:
                print ('\033[31m'+"予期せぬソケットエラー : %s"+'\033[0m' % se)
            except Exception as e:
                print('\033[31m'+"レシーバーラー: %s"+'\033[0m' % e)
    
    def _video_recver(self):
        """
        カメラデータを監視するスレッド
        """
        if self.cap is None:
            self.cap = cv2.VideoCapture(self.video_address)
        if not self.cap.isOpened():
            self.cap.open(self.video_address)
        while True:
            try:
                ret, frame = self.cap.read()
                self.frame = frame
            except Exception as e:
                print('\033[31m'+"カメラレシーバーエラー: %s"+'\033[0m' % e)
    
    def _timeout(self):
        """
        タイムアウトする前にコマンドを常時送信する。frag が上がったらスレッドがスタートする。
        """
        print('\033[32m'+"SYSTEM IS ACTIVATED"+'\033[32m')
        current_time = time.time()
        pre_time = current_time
        while True:
            try:
                current_time = time.time()
                if self.timeout_skipper_frag is True:
                    self.timeout_skipper_frag = False
                    continue
                if self.timeout_frag is False:
                    break
                else:
                    if current_time - pre_time == 10:
                        print('\033[33m'+"timeout. send command"+'\033[33m')
                        self.send_cmd("command")
            except:
                break

# 使用可能ライブラリ群
    def send_cmd(self, cmd):
        """
        コマンドを送信するメゾット
        """
        self.about_frag = False # 中断フラグを倒す
        timer = threading.Timer(self.cmd_timeout, self.set_about_frag) # タイムアウトしたらフラグを立てるタイマースレッドを起動
        self.sock.sendto(cmd.encode('utf-8'), self.tello_address)  
        timer.start() # タイマースレッド
        while self.response is None:
            if self.about_frag is True:
                break
        timer.cancel() #タイマー停止
        if self.response is None:
            response = "None response"
        else:
            response = self.response.decode("utf-8")
        self.response = None
        print('\033[37m'+"send command >>> {}: response >>> {}"+'\033[0m'.format(cmd,response))
        return response

    def set_about_frag(self):
        """
        about_frag を立てるメゾット
        この関数が呼ばれるということは、応答が来なくてタイムアウトしたということ。
        """
        self.about_frag = True
        print('\033[33m'+"タイムアウト"+'\033[33m')
    
    def takeoff(self):
        """
        離陸
        """
        response = self.send_cmd("takeoff")
        print("安定化のため10秒ホバリング")
        time.sleep(10)
        self.send_cmd("command")
        self.timeout_frag = True
        return response
    def land(self):
        """
        着陸：全てのフローを中止して、着陸する。
        """
        self.timeout_frag = False
        return self.send_cmd("land")
    def emergency(self):
        """
        モーター停止：全てのフローを中止して、モーターを停止する。墜落するので要注意
        """
        self.timeout_frag = False
        self.timeout_thread.join()
        return self.send_cmd("emergency")
    def stop(self):
        """
        停止：全てのフローを中止して、その場にホバリング
        """
        self.timeout_skipper_frag = True
        return self.send_cmd("stop")
    
    def speed(self, cm):
        """
        スピード設定：ドローンの水平飛行速度を設定。
        引数: cm (50 ~ 500 : int)
        """
        self.timeout_skipper_frag = True
        self.flight_speed = cm
        response = self.send_cmd("speed {}".format(cm))
        return response
    
    def up(self, cm):
        """
        上昇
        引数: cm (50 ~ 500 : int)
        """
        self.timeout_skipper_frag = True
        response = self.send_cmd("up {}".format(cm))
        sec = cm//100 + 2.6
        time.sleep(sec) 
        return response
    
    def down(self, cm):
        """
        下降
        引数: cm (50 ~ 500 : int)
        """
        self.timeout_skipper_frag = True
        response = self.send_cmd("down {}".format(cm))
        sec = cm//100 + 2.6
        time.sleep(sec) 
        return response
    
    def forward(self, cm):
        """
        前進
        引数: cm (50 ~ 500 : int)
        """
        self.timeout_skipper_frag = True
        sec = cm / self.flight_speed + 2 + self.flight_speed/125
        response = self.send_cmd("forward {}".format(cm))
        time.sleep(sec) 
        return response

    def back(self, cm):
        """
        後進
        引数: cm (50 ~ 500 : int)
        """
        self.timeout_skipper_frag = True
        sec = cm / self.flight_speed + 2 + self.flight_speed/125
        response = self.send_cmd("back {}".format(cm))
        time.sleep(sec) 
        return response
    
    def left(self, cm):
        """
        左
        引数: cm (50 ~ 500 : int)
        """
        self.timeout_skipper_frag = True
        sec = cm / self.flight_speed + 2 + self.flight_speed/125
        response = self.send_cmd("left {}".format(cm))
        time.sleep(sec) 
        return response

    def right(self, cm):
        """
        右
        引数: cm (50 ~ 500 : int)
        """
        self.timeout_skipper_frag = True
        sec = cm / self.flight_speed + 2 + self.flight_speed/125
        response = self.send_cmd("right {}".format(cm))
        time.sleep(sec) 
        return response
    
    def cw(self, dig):
        """
        時計回り
        引数: dig (1~360 : int)
        """
        self.timeout_skipper_frag = True
        response = self.send_cmd("cw {}".format(dig))
        sec = dig / 50 + 1
        time.sleep(sec) 
        return response 
    
    def ccw(self, dig):
        """
        反時計回り
        引数: dig (1~360 : int)
        """
        self.timeout_skipper_frag = True
        response = self.send_cmd("ccw {}".format(dig))
        sec = dig / 50 + 1
        time.sleep(sec) 
        return response

    def flip(self, dir):
        """
        フリップ:任意の方向に宙返りをする。バッテリー残量が 50% 以下だと実行できない
        引数: dir (f,b,l,f : str)
        """
        self.timeout_skipper_frag = True
        response = self.send_cmd("flip {}".format(dir))
        time.sleep(2.5)
        return response
    
    def go(self, x,y,z,speed):
        """
        任意の方向へ任意の速度で飛行
        引数： 
        x,y,z (20 ~ 500 : int) 
        speed (50 ~ 500 : int)
        """
        self.timeout_skipper_frag = True
        sec = ((x + y + z) / 3) / self.flight_speed + 2 + self.flight_speed/125
        response = self.send_cmd("go {} {} {} {}".format(x,y,z,speed))
        time.sleep(sec) 
        return response
    
    def rc(self, elron, elevator, srotol, lador):
        """
        RCコントロール値をドローンhw出力
        引数：
        elron：左右移動の出力値 -で左
        elevator：前進後進の出力値 -で後進
        srotol：上昇下降の出力値 -で下降
        lador：旋回の出力値 -で反時計回り
        sec：実行時間を設定
        """
        self.timeout_skipper_frag = True
        response = self.send_cmd("rc %s %s %s %s"%(int(elron), int(elevator), int(srotol), int(lador)))
        return response
    
    def smart_rc(self, elron, elevator, srotol, lador, sec):
        """
        RCコントロール値をドローンhw出力
        引数：
        elron：左右移動の出力値 -で左
        elevator：前進後進の出力値 -で後進
        srotol：上昇下降の出力値 -で下降
        lador：旋回の出力値 -で反時計回り
        sec：実行時間を設定
        """
        self.timeout_skipper_frag = True
        response = self.send_cmd("rc %s %s %s %s"%(int(elron), int(elevator), int(srotol), int(lador)))
        time.sleep(sec)
        response = self.send_cmd("rc 0 0 0 0")
        time.sleep(0.5)
        return response
    
    def wait(self,sec):
        """
        ドローンを待機させる returnなし
        引数：sec 秒
        """
        time.sleep(sec)
    
    def get_response(self):
        """
        ドローンからの応答を取得
        return : response
        """
        response = self.response
        return response
    
    def get_battery(self):
        """
        ドローンからの応答を取得
        return : response
        """
        self.timeout_skipper_frag = True
        response = self.send_cmd("battery?")
        return response
    
    def downvision(self, dir):
        """
        下方カメラ情報を取得：
        引数：dir(1,0 : int)
        1
        下方ビジョンセンサーのデータを流す
        0
        メインカメラのデータ流す

        self.frame にデータが受け取られる。
        """
        self.timeout_skipper_frag = True
        return self.send_cmd("downvision {}".format(dir))
