from machine import PWM, Pin, ADC
import dht
from cfg import automation, log
from utime import ticks_ms, ticks_diff


def map_value(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


class Led:
    def __init__(self, pin, on=4, off=4, time=0):
        self.pin = pin
        self.on_time = on
        self.off_time = off
        self.time = time

    def on(self):
        log("Led ON")
        self.time = 0
        self.pin.on()

    def off(self):
        log("Led OFF")
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
        return {
            "status": self.value(),
            "time_on": self.on_time,
            "time_off": self.off_time,
            "time": self.time,
        }


class Pump:
    def __init__(self, pin):
        self.pin = pin

    def on(self):
        if not self.value():
            log("Pump ON")
        self.pin.on()

    def off(self):
        if self.value():
            log("Pump OFF")
        self.pin.off()

    def value(self):
        return self.pin.value()


class Fan:
    def __init__(self, pin):
        self.pin = pin

    def on(self):
        if not self.value():
            log("Fan ON")
        self.pin.on()

    def off(self):
        if self.value():
            log("Fan OFF")
        self.pin.off()

    def value(self):
        return self.pin.value()


class SoilProbe:
    def __init__(self, pin, in_min=350, in_max=900, out_min=95, out_max=5):
        self.pin = pin
        self.adc = ADC(self.pin)
        self.adc.width(ADC.WIDTH_10BIT)
        self.adc.atten(ADC.ATTN_11DB)
        self.in_min = in_min
        self.in_max = in_max
        self.out_min = out_min
        self.out_max = out_max

    def read(self):
        return int(
            map_value(
                self.adc.read(), self.in_min, self.in_max, self.out_min, self.out_max
            )
        )

    def read_raw(self):
        return self.adc.read()


class AirSensor:
    def __init__(self, pin):
        self.dht11 = dht.DHT11(pin)
        self.temp = 0
        self.hum = 0
        self.last_read = 0

    def read(self):
        if ticks_diff(ticks_ms(), self.last_read) > 2000:
            self.last_read = ticks_ms()
            try:
                self.dht11.measure()
                self.temp = self.dht11.temperature()
                self.hum = self.dht11.humidity()
            except Exception as e:
                print(e)
                self.temp = 0
                self.hum = 0

        return (self.temp, self.hum)


def get_status():

    return {
        "ligth": led.get_status(),
        "pump": pump.value(),
        "humidity": dht11.hum,
        "humidity_target": 20,
        "soil_target": automation["soil_target"],
        "soil_humidity": soil.read(),
        "water_reserve": 0,
        "temp": dht11.temp,
        "fans": fan.value(),
    }


led = Led(
    Pin(19, Pin.OUT),
    on=automation["ligth"]["time_on"],
    off=automation["ligth"]["time_off"],
    time=automation["ligth"]["time"],
)
pump = Pump(Pin(4, Pin.OUT))
dht11 = AirSensor(Pin(14))
soil = SoilProbe(Pin(33), 13)
fan = Fan(Pin(18, Pin.OUT))
