import RPi.GPIO as GPIO
import time
from DRV8825 import DRV8825

MOTOR_UP = "up"
MOTOR_DOWN = "down"

def revolutions_to_steps(revolution_count, steps_per_revolution=200):
    '''
    Returns the # of steps necessary for that revolutions, based on the hardware set cycle of 200 steps/revolution
    '''
    return revolution_count * steps_per_revolution

try:
    stepDelay = 0.001

    Motor1 = DRV8825(dir_pin=13, step_pin=19, enable_pin=12, mode_pins=(0, 1, 2))
    Motor2 = DRV8825(dir_pin=24, step_pin=18, enable_pin=4, mode_pins=(3, 4, 5))

    Motor1.TurnStep(direction=MOTOR_UP, steps=revolutions_to_steps(1), stepDelay=stepDelay)
    Motor1.TurnStep(direction=MOTOR_DOWN, steps=revolutions_to_steps(2), stepDelay=stepDelay)
    
    Motor2.TurnStep(direction=MOTOR_UP, steps=revolutions_to_steps(1), stepDelay=stepDelay)
    Motor2.TurnStep(direction=MOTOR_DOWN, steps=revolutions_to_steps(2), stepDelay=stepDelay)
    
except TypeError as e:
    print(f"Error: {e}")

finally:
    print ("Stopping motors & resetting GPIO")
    Motor1.Stop()
    Motor2.Stop()
    GPIO.cleanup()
    exit()