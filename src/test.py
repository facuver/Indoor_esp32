

from machine import Pin,TouchPad
import utime
pad = TouchPad(Pin(32))

p = Pin(2,Pin.PULL_UP)
t = Pin(4,Pin.PULL_UP)

for _ in range(1):
    p.on()
    utime.sleep(0.5)
    p.off()
    utime.sleep(0.5)

while True:
    if pad.read() > 500:
        t.off()
        
    else:
        t.on()
    utime.sleep_ms(100)
    
    
    
    