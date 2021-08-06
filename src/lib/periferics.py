from machine import PWM, Pin,ADC
from cfg import automation
from dht import DHT11

class Led():
    def __init__(self, pin, on=4, off=4 , time=0):
        self.pin = pin
        self.on_time = on
        self.off_time = off
        self.time = time

    def on(self):
        self.time = 0
        self.pin.on()

    def off(self):
        self.time = 0
        self.pin.off()

    def toggle(self):
        self.time = 0
        self.pin.value(not self.pin.value())

    def set_on_time(self, time):
        self.on_time = time
        return self.on_time

    def set_off_time(self, time):
        self.off_time = time
        return self.off_time

    def value(self):
        return self.pin.value()

    def update(self):
        self.on_time = automation["ligth"]["time_on"]
        self.off_time = automation["ligth"]["time_off"]
        if self.value():
            if self.time >= self.on_time:
                self.off()
                self.time = 0
        else:
            if self.time >= self.off_time:
                self.on()
                self.time = 0
        self.time += 1

   

    def get_status(self):
        return {"status" : self.value() , "time_on" : self.on_time , "time_off": self.off_time , "time" : self.time}


class Pump():
    def __init__(self, pin):
        self.pin = pin

    def on(self):
        self.pin.on()

    def off(self):
        self.pin.off()

    def value(self):
        return self.pin.value()


class Fan():

    def __init__(self, pin, duty=10):
        self.pin = pin
        self.duty = duty
        self.pwm = PWM(self.pin)

    def set_duty(self, duty):
        self.duty = duty
        self.pwm.duty(self.duty)
        return duty

    def full(self):
        self.pwm.duty(1024)



def get_status():
    return  {"ligth" : led.get_status() ,"pump" : pump.value() , "humidity" : 0 , "soil_humidity" : 0 , "water_reserve" : 0 , "temp" : 0 , "fans" : {"status" : 0, "duty" : 0} }


led = Led(Pin(2,Pin.OUT) , on= automation["ligth"]["time_on"] , off= automation["ligth"]["time_off"] , time= automation["ligth"]["time"]  )
pump = Pump(Pin(4 , Pin.OUT))
dht = DHT11(Pin(6))
soil = ADC(Pin(36)).atten(ADC.ATTN_11DB)
