from ...pkg.tello import console # console モジュールまでの相対パス

drone = console() # console モジュールを任意の変数に定義することでモジュールが使用可能になる
drone.takeoff() # 離陸
drone.cw(360) # 360°旋回
drone.land() # 着陸

