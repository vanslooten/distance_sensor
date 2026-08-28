import time
from machine import Pin, PWM

buzzer = PWM(Pin(15))
buzzer.freq(660)
buzzer.duty_u16(0)

def beep():
    buzzer.duty_u16(2 ** 15)
    time.sleep(0.5)
    buzzer.duty_u16(0)
    time.sleep(0.5)

while True:
    beep()
