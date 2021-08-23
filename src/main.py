import uasyncio as asyncio
from periferics import led, soil, pump, dht11, fan, get_status
import gc
from web import app
from cfg import automation, log


def soil_update():
    if soil.read() < automation["soil_target"]:
        pump.on()
    else:
        pump.off()


def fan_update():
    if dht11.read()[1] > automation["humidity_target"]:
        fan.on()
    else:
        fan.off()


async def main_loop() -> None:
    while True:
        led.update()
        soil_update()
        fan_update()
        print(get_status())
        await asyncio.sleep(5)


async def gc_run():
    while True:
        gc.collect()
        await asyncio.sleep(0.5)


if __name__ == "__main__":
    log("Starting Server")
    main_task = asyncio.create_task(main_loop())

    app.run(host="0.0.0.0", port=80, debug=True)
