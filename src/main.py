import uasyncio as asyncio
from led import Led
from machine import Pin

l = Led(Pin(2,Pin.OUT))

async def main_loop():
    while True:
        l.toggle()
        await asyncio.sleep(0.2)




main_task = asyncio.create_task(main_loop())

asyncio.run_until_complete()