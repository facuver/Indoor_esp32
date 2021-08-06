import uasyncio as asyncio
from periferics import led
import gc
from web import app



async def main_loop():
    while True:     
        led.update()

        await asyncio.sleep(5)

async def gc_run():
    while True:
        gc.collect()
        await asyncio.sleep(0.5)

if __name__ == "__main__":
    main_task = asyncio.create_task(main_loop())
    app.run(host="0.0.0.0",port=80,debug=True)