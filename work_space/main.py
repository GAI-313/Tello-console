from tello import console

try:
    drone = console()
    drone.takeoff()
    drone.speed(100)
    drone.up(100)
    drone.land()

except KeyboardInterrupt:
    drone.stop()
    drone.land()