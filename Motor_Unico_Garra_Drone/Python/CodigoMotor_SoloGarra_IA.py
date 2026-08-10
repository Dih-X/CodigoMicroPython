# Controle de um motor de passo único em Python
# Exemplo para motor de passo unipolar (4 fios) usando Raspberry Pi ou MicroPython

try:
    from machine import Pin
    from time import sleep_ms
    GPIO_TYPE = "micropython"
    
except ImportError:
    import RPi.GPIO as GPIO
    from time import sleep
    GPIO_TYPE = "raspberry"

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
        if GPIO_TYPE == "raspberry":
            GPIO.setmode(GPIO.BCM)
            for pin in self.pins:
                GPIO.setup(pin, GPIO.OUT)
                GPIO.output(pin, GPIO.LOW)
        else:
            self.pins = [Pin(pin, Pin.OUT) for pin in self.pins]

    def move_steps(self, steps, delay=5):
        direction = 1 if steps >= 0 else -1
        steps = abs(steps)
        for _ in range(steps):
            self.step_index = (self.step_index + direction) % len(self.sequence)
            self._write_step(self.sequence[self.step_index])
            if GPIO_TYPE == "raspberry":
                sleep(delay / 1000.0)
            else:
                sleep_ms(delay)

    def _write_step(self, coils):
        for pin, value in zip(self.pins, coils):
            if GPIO_TYPE == "raspberry":
                GPIO.output(pin, GPIO.HIGH if value else GPIO.LOW)
            else:
                pin.value(value)

    def release(self):
        for pin in self.pins:
            if GPIO_TYPE == "raspberry":
                GPIO.output(pin, GPIO.LOW)
            else:
                pin.value(0)

    def cleanup(self):
        self.release()
        if GPIO_TYPE == "raspberry":
            GPIO.cleanup()

if __name__ == "__main__":
    motor_pins = [17, 18, 27, 22]
    motor = StepperMotor(motor_pins)
    try:
        print("Girando no sentido horário")
        motor.move_steps(4096, delay=3)
        if GPIO_TYPE == "raspberry":
            sleep(1)
        else:
            sleep_ms(1000)
        print("Girando no sentido anti-horário")
        motor.move_steps(-4096, delay=3)
    finally:
        motor.cleanup()
