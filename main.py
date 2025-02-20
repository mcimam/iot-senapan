import network
import uasyncio as asyncio

from config import ConfigHandler
from gun import handle_shooting
from webpage import app

print("Booting", end =" ")

ch = ConfigHandler()
loop = asyncio.get_event_loop()

enable_web = ch.config.get("ENABLE_WEB", 1)

print(".", end =" ")

# GUN 
async def main_shoot():
    while True:
        handle_shooting()
        if enable_web:
            await asyncio.sleep_ms(ch.config.get("DELAY_WEB", 200))        
loop.create_task(main_shoot())
print(".", end =" ")

# SERVER
if enable_web:
    print(".", end =" ")
    ap = network.WLAN(network.AP_IF)
    ap.config(essid="SENAPAN", pm=network.WLAN.PM_POWERSAVE)
    ap.active(True)
        
    loop.create_task(app.serve())
    print(".")
    print("Server Started")

try:
    # Run the event loop indefinitely
    print("Booting Finish")
    loop.run_forever()
except Exception as e:
    print('Error occured: ', e)
except KeyboardInterrupt:
    print('Program Interrupted by the user')