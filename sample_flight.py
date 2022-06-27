from src.modules.tello import console # console モジュールまでの相対パス

drone = console() # consple をこのプログラムで使用できるようにする
drone.takeoff # 離陸
drone.cw(360) # 360°時計回りに旋回
drone.land() # 着陸
