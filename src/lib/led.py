class Led():
    def __init__(self, pin, on=12, off=12):
        self.pin = pin
        self.on_time = on
        self.off_time = off

    def on(self):
        self.pin.on()

    def off(self):
        self.pin.off()

    def toggle(self):
        self.pin.value(not self.pin.value())

    def set_on_time(self, time):
        self.on_time = time
        return self.on_time

    def set_off_time(self, time):
        self.off_time = time
        return self.off_time

    def value(self):
        return self.pin.value()