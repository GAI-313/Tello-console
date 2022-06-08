from tello import console

drone = console()
drone.takeoff()
drone.flip("f")
drone.land()