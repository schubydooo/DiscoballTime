import sys
from DRV8825 import DRV8825
import threading

lock = threading.Lock()

def lower_discoball():
    Motor1.TurnStep(direction='up', steps=1775)
    Motor3.TurnStep(direction='up', steps=1175)
    Motor1.TurnStep(direction='down', steps=3800)

def raise_discoball():
    Motor1.TurnStep(direction='up', steps=3800)
    Motor3.TurnStep(direction='down', steps=1175)
    Motor1.TurnStep(direction='down', steps=1775)

# Spin up resources
Motor1 = DRV8825(dir_pin=13, step_pin=19, enable_pin=12, mode_pins=(0, 1, 2))
Motor3 = DRV8825(dir_pin=24, step_pin=18, enable_pin=4, mode_pins=(3, 4, 5))

desired_action = sys.argv[1]

Motor1.Start()
Motor3.Start()

if desired_action == 'raise':
    raise_discoball()
elif desired_action == 'lower':
    lower_discoball()
else: 
    print(f"Invalid action: {desired_action}")

Motor1.Stop()
Motor3.Stop()

