from modules.tello import console
import threading
import time
import cv2

class height_detect:
    """
    引数: height 単位 = mm : データ = int
    height に与えられた高度へ tof センサーからの差分を求めて上昇下降を行う。
    例: 1000 が入力されると 機体が 地表から1000mm の高度になるよう調整する。
    
    Introduction
        Tello EDU 下部には VPS (Vision Positioning System) と呼ばれるビジョンセンサーと ToF (赤外線測距センサー)からなるセンサー群が搭載されている。
        このクラスは VPS からのカメラデータを表示し、Tof センサーからの高度測定を行う。加えてユーザーから任意の高度を指定することで指定された高度まで飛行することができる。
    
    Use
        height_detect は height int 引数をとる。これは指定高度であり、引数に与えられた高度へ飛行することができる。
        現在は Tof センサーからの値と入力された値の差分からスロットル出力を求めているが、将来的にはこれを PID による制御で実現したいと考えている。
    """
    def __init__(self,height):
        self.drone = console()
        self.tof = None
        self.height = height
        self.throttle = 0
        self.th = threading.Thread(target=self.tof_recver)
        self.th.daemon = True
        self.main() # tof からの任意高度を飛行する場合はこれを使う。
        #self.test() # これはテストメゾット
        #self.tof_recver()
    
    def tof_recver(self):
        """
        get_tof エラーの修正
        line 23, in tof_recver
        ValueError: invalid literal for int() with base 10: ''
        """
        self.drone.start_mortor()
        time.sleep(20)
        while True:
            try:
                tof = self.drone.get_tof()
                if tof == "None resp" or tof is None:
                    continue
                self.tof = int(tof)
                self.throttle = self.height - self.tof
                self.move()
                time.sleep(0.1)
            except Exception as e:
                print(e)
                self.drone.emergency()

    def main(self):
        self.drone.downvision(1)
        self.th.start()

        while True:
            try:
                frame = self.drone.frame
                if frame is None or frame.size == 0:
                    continue

                cv2.putText(frame,"VPS:"+str(self.tof)+"mm",(0,20),cv2.FONT_HERSHEY_PLAIN,1.0,(0,255,0))
                cv2.imshow("VPS",frame)
                self.move()
                    
                key = cv2.waitKey(1) & 0xFF
                if key == 27:
                    break
            except KeyboardInterrupt:
                self.drone.emergency()
                break
        
        self.drone.stop()
        self.drone.land()
        self.drone.cap.release()
        cv2.destroyAllWindows()
    
    def move(self):
        throttle = int(self.throttle/10)
        if throttle <= -100:
            throttle = -100
        elif throttle >= 50:
            throttle = 50
        
        self.drone.rc(0,0,throttle,50)

    def test(self):
        self.drone.start_mortor()
        time.sleep(5)
        self.drone.start_mortor()

height_detect(2000)