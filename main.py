from machine import Pin, I2C
import time
import neopixel
from ssd1306 import SSD1306_I2C

# -------------------------------------------------------------
# OLED SETUP (SSD1306 on GP0 SDA, GP1 SCL)
# -------------------------------------------------------------
i2c = I2C(0, scl=Pin(1), sda=Pin(0))
oled = SSD1306_I2C(128, 64, i2c)

def show_time(h, m, s):
    oled.fill(0)
    oled.text("CLOCK", 0, 0)
    oled.text("{:02d}:{:02d}:{:02d}".format(h, m, s), 0, 20)
    oled.show()

# -------------------------------------------------------------
# SK6812 LED SETUP
# -------------------------------------------------------------
NUM_LEDS = 1

led_pins = [26, 27, 28, 22]
leds = [neopixel.NeoPixel(Pin(pin, Pin.OUT), NUM_LEDS) for pin in led_pins]

def set_seconds_led(second):
    # Determine which LED should be ON
    index = second // 15  # 0..3

    for i, strip in enumerate(leds):
        if i == index:
            strip[0] = (0, 150, 255)  # cyan, ON
        else:
            strip[0] = (0, 0, 0)      # OFF
        strip.write()

# -------------------------------------------------------------
# MANUAL TIME SET (CHANGE THIS BEFORE UPLOADING)
# -------------------------------------------------------------
h = 12   # starting hour
m = 0    # starting minute
s = 0    # starting second

# -------------------------------------------------------------
# MAIN LOOP
# -------------------------------------------------------------
last_tick = time.ticks_ms()

while True:
    now = time.ticks_ms()
    if time.ticks_diff(now, last_tick) >= 1000:
        last_tick = now
        s += 1
        if s >= 60:
            s = 0
            m += 1
        if m >= 60:
            m = 0
            h += 1
        if h >= 24:
            h = 0

        # Update OLED
        show_time(h, m, s)

        # Update LED seconds indicator
        set_seconds_led(s)
