import RPi.GPIO as GPIO
import time
from DRV8825 import DRV8825

MOTOR_UP = "up"
MOTOR_DOWN = "down"

REVOLUTION = 200
try:
    Motor1 = DRV8825(dir_pin=13, step_pin=19, enable_pin=12, mode_pins=(0, 1, 2))
    Motor2 = DRV8825(dir_pin=24, step_pin=18, enable_pin=4, mode_pins=(3, 4, 5))

    Motor1.TurnStep(direction=MOTOR_UP, steps=REVOLUTION, stepDelay = 0.005)
    Motor1.TurnStep(direction=MOTOR_DOWN, steps=200, stepDelay = 0.005)
    
    Motor2.TurnStep(direction=MOTOR_UP, steps=2*REVOLUTION, stepDelay=0.002)
    Motor2.TurnStep(direction=MOTOR_DOWN, steps=400, stepDelay=0.002)
    
except TypeError as e:
    print(f"Error: {e}")

finally:
    print ("Stopping motors & resetting GPIO")
    Motor1.Stop()
    Motor2.Stop()
    GPIO.cleanup()
    exit()