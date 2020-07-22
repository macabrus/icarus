# GLAVNI PROGRAM

drone = Drone()

# potprogram za kalibraciju
drone.calibrate()


drone.initialize_flight()
# postavljanje referentnih vrijednosti


while 1:
    drone.get_coordinates()

