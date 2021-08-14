from machine import PWM, Pin,ADC
from cfg import automation
import dht
import utime


def map_value( x , in_min,in_max,out_min,out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


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




class SoilProbe():
    def __init__(self,pin,drain_pin, in_min = 280 , in_max=760 , out_min = 95 , out_max = 5 ):
        self.pin = pin
        self.adc = ADC(self.pin)
        self.adc.width(ADC.WIDTH_10BIT)
        self.adc.atten(ADC.ATTN_11DB)
        self.in_min = in_min
        self.in_max = in_max
        self.out_min = out_min
        self.out_max = out_max
        self.drain = Pin(drain_pin,Pin.OPEN_DRAIN)


    def read(self):
        self.drain.off()
        utime.sleep_ms(20)
        self.drain.on()
        utime.sleep_ms(20)
        return int(map_value(self.adc.read() ,self.in_min,self.in_max,self.out_min,self.out_max ))
    



def get_status():
    try:
        humidity.measure()
        temp = humidity.temperature()
        hum = humidity.humidity()
    except Exception as e: 
        temp = "Error"
        hum="Error"
    return  {"ligth" : led.get_status() ,"pump" : pump.value() , "humidity" : hum , "soil_target" : 0 ,"soil_humidity" : soil.read() , "water_reserve" : 0 , "temp" : temp , "fans" : {"status" : 0, "duty" : 0} }


led = Led(Pin(2,Pin.OUT) , on= automation["ligth"]["time_on"] , off= automation["ligth"]["time_off"] , time= automation["ligth"]["time"]  )
pump = Pump(Pin(4 , Pin.OUT))
humidity = dht.DHT11(Pin(14))
soil = SoilProbe(Pin(32),33)
