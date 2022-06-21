from modules.tello import console
import threading
import time
import cv2

class height_detect:
    def __init__(self,height):
        self.drone = console()
        self.tof = None
        self.height = height
        self.throttle = 0
        self.th = threading.Thread(target=self.tof_recver)
        self.th.daemon = True
        #self.main()
        self.test()
    
    def tof_recver(self):
        """
        get_tof エラーの修正
        line 23, in tof_recver
        ValueError: invalid literal for int() with base 10: ''
        """
        self.drone.rc(-100,-100,-100,100)
        time.sleep(15)
        while True:
            tof = self.drone.get_tof()
            if tof == "None resp" or tof is None:
                continue
            self.tof = int(tof)
            self.throttle = self.height - self.tof
            self.move()
            time.sleep(0.1)

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
                #self.move()
                    
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

height_detect(1500)