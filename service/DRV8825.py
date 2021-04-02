import RPi.GPIO as GPIO
import time

MOTOR_UP = "up"
MOTOR_DOWN = "down"

class DRV8825():
    '''
    Default step distance is set by hardware at full steps (all switches to 0).  

    1.8 degree: nema23, nema14
    200 steps = 1 revolution
    '''
    def __init__(self, dir_pin, step_pin, enable_pin, mode_pins):
        self.dir_pin = dir_pin
        self.step_pin = step_pin        
        self.enable_pin = enable_pin
        self.mode_pins = mode_pins
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.dir_pin, GPIO.OUT)
        GPIO.setup(self.step_pin, GPIO.OUT)
        GPIO.setup(self.enable_pin, GPIO.OUT)
        GPIO.setup(self.mode_pins, GPIO.OUT)
        
    def digital_write(self, pin, value):
        '''
        Set the pin's value
        '''
        GPIO.output(pin, value)
        
    def Start(self):
        '''
        Switch on the motor
        '''
        self.digital_write(self.enable_pin, 1)

    def Stop(self):
        '''
        Switch off the motor
        '''
        self.digital_write(self.enable_pin, 0)
            
    def TurnStep(self, direction, steps, stepDelay=0.003):
        '''
        Set direction and turn the motor the prescribed number of steps
        '''
        # Validate inputs
        if direction not in (MOTOR_UP, MOTOR_DOWN):
            raise TypeError(f"The direction must be: '{MOTOR_UP}' or '{MOTOR_DOWN}'")

        if steps <= 0:
            raise TypeError("Steps must be greater than 0")

        # Set direction
        if direction == MOTOR_UP:
            self.digital_write(self.dir_pin, 0)
        elif direction == MOTOR_DOWN:
            self.digital_write(self.dir_pin, 1)

        # Turn the motor  
        # print (f"DRV8825: {direction} - {steps} steps")
        self.Start()
        for i in range(steps):
            self.digital_write(self.step_pin, 1)
            time.sleep(stepDelay)
            self.digital_write(self.step_pin, 0)
            time.sleep(stepDelay)
        self.Stop()

    def SetMicroStep(self, mode, stepFormat):
        """
        (1) mode
            'hardware' :    Use the switch on the module to control the microstep
            'software' :    Use software to control microstep pin levels
                Need to put the All switch to 0
        (2) stepFormat
            ('fullstep', 'halfstep', '1/4step', '1/8step', '1/16step', '1/32step')
        """
        microstep = {'fullstep': (0, 0, 0),
                     'halfstep': (1, 0, 0),
                     '1/4step': (0, 1, 0),
                     '1/8step': (1, 1, 0),
                     '1/16step': (0, 0, 1),
                     '1/32step': (1, 0, 1)}

        print (f"Control mode: {mode}")
        if (mode == 'software'):
            print ("Setting pins")
            self.digital_write(self.mode_pins, microstep[stepFormat])

