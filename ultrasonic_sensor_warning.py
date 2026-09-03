# see:
# https://randomnerdtutorials.com/raspberry-pi-pico-hc-sr04-micropython/
#
# if you want to re-create this project at your own computer,
# make sure to have the files main.py, ssd1306.py and hcsr04.py in your folder.
# drivers are from:
# https://github.com/micropython/micropython-lib/tree/master/micropython/drivers/display/ssd1306
# https://github.com/rsc1975/micropython-hcsr04
#
from machine import Pin, I2C, PWM
import ssd1306
import time
from hcsr04 import HCSR04

time.sleep(0.1) # Wait for USB to become ready

# I2C setup: using I2C1 with GP2 (SDA) and GP3 (SCL)
i2c = I2C(1, scl=Pin(3), sda=Pin(2), freq=400000)

# Scan for devices
devices = i2c.scan()
if devices:
    print("I2C devices found:", [hex(dev) for dev in devices])
else:
    print("No I2C devices found")

# Initialize display (most SSD1306 are 128x64, some are 128x32)
oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

# Initialize the HC-SR04 sensor with trigger on GPIO 27 and echo on GPIO 28
sensor = HCSR04(trigger_pin=17, echo_pin=16, echo_timeout_us=30000)

# Clear the display
oled.fill(0)

# Show some text
oled.text('Distance:', 0, 0)

# Update the display
oled.show()

# initialize the buzzer on GPIO 15
buzzer = PWM(Pin(15))
buzzer.freq(660)
buzzer.duty_u16(0)

def beep():
    buzzer.duty_u16(2 ** 15)
    time.sleep(0.5)
    buzzer.duty_u16(0)
    time.sleep(0.5)

# beep two times:
for x in range(2):
    beep()

while True:
    try:
        # Measure distance in centimeters
        distance_cm = sensor.distance_cm()

        oled.fill(0)
        
        # something nearby?
            # sound alarm

        # display the distance
        oled.text("Distance:", 0, 10)
        oled.text("{:.1f} cm".format(distance_cm), 0, 30)
        oled.show()

    except OSError as e:
        print('Error:', e)
    
    # catch an KeyboardInterrupt:
    except KeyboardInterrupt:
        print("Keyboard Interrupt received")
        break # exit the loop

    # Wait 1 second before the next measurement
    try:
        time.sleep(1)
    # catch an KeyboardInterrupt:
    except KeyboardInterrupt:
        print("Keyboard Interrupt received")
        break # exit the loop

# after finished, clear the screen
oled.fill(0)
oled.show()

