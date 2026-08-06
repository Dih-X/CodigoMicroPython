# Controle de um motor de passo único em Python
# Exemplo para motor de passo unipolar (4 fios) usando Raspberry Pi ou MicroPython


import RPi.GPIO as GPIO
from time import sleep
#GPIO_TYPE = "raspberry"

class StepperMotor:
    def __init__(self, pins):
        self.pins = pins
        self.step_index = 0
        self.sequence = [
            [1, 0, 0, 0],
            [1, 1, 0, 0],
            [0, 1, 0, 0],
            [0, 1, 1, 0],
            [0, 0, 1, 0],
            [0, 0, 1, 1],
            [0, 0, 0, 1],
            [1, 0, 0, 1],
        ]
        
        GPIO.setmode(GPIO.BCM)
        for pin in self.pins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.LOW)
        
    def move_steps(self, steps, delay=5):
        direction = 1 if steps >= 0 else -1
        steps = abs(steps)
        for _ in range(steps):
            self.step_index = (self.step_index + direction) % len(self.sequence)
            self._write_step(self.sequence[self.step_index])
            
            sleep(delay / 1000.0)

    def _write_step(self, coils):
        for pin, value in zip(self.pins, coils):
            GPIO.output(pin, GPIO.HIGH if value else GPIO.LOW)
            
    def release(self):
        for pin in self.pins:
            GPIO.output(pin, GPIO.LOW)

    def cleanup(self):
        self.release()
        GPIO.cleanup()

if __name__ == "__main__":
    motor_pins = [17, 18, 27, 22]
    motor = StepperMotor(motor_pins)
    try:
        print("Girando no sentido horário")
        motor.move_steps(4096, delay=3)
        sleep(1)
        
        print("Girando no sentido anti-horário")
        motor.move_steps(-4096, delay=3)
    finally:
        motor.cleanup()
