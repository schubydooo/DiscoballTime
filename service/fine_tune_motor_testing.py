import sys
from DRV8825 import DRV8825


# Spin up resources
Motor1 = DRV8825(dir_pin=13, step_pin=19, enable_pin=12, mode_pins=(0, 1, 2))
Motor3 = DRV8825(dir_pin=24, step_pin=18, enable_pin=4, mode_pins=(3, 4, 5))

Motor1.Start()
Motor3.Start()

desired_action = sys.argv[1]
desired_motor_num = sys.argv[2]
desired_direction = sys.argv[3]
desired_steps = sys.argv[4]

if desired_action == "off":  
    print('stopping motors')
    # Motor1.Stop()
    Motor3.Stop()

else: 
    if desired_motor_num == '1':
        Motor = Motor1
    elif desired_motor_num == '3':
        Motor = Motor3
    else:
        raise TypeError(f"Motor Num {desired_motor_num} is invalid") 

    if desired_direction not in ('up', 'down'):
        raise TypeError(f"Direction is invalid for {desired_direction}")
    Motor.TurnStep(direction=desired_direction, steps=int(desired_steps))

    Motor1.Start()
    Motor3.Start()
