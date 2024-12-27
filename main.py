from config import ConfigHandler
from web import WebServer
from gun import handle_shooting

import asyncio

CH = ConfigHandler()
CH.read()


# setup_gun()

# Starting Hotspot and webserver
if CH.config["ENABLE_WEB"]  == 1:
    SSID = "SENAPAN"
    PASSWORD = "1234"
    WS = WebServer(SSID, PASSWORD)

    WS.setup_ap()


async def main_shoot():
    while True:
        handle_shooting()

# Create an Event Loop
async def handle_client(reader, writer):
    print("Client connected")
    request_line = await reader.readline()
    print("Request:", request_line)

    # Skip HTTP request headers
    while await reader.readline() != b"\r\n":
        pass

    request = str(request_line, "utf-8").split()[1]
    print("Request:", request)

async def main_server():
    print("TRYING SERVER ")
    server = await asyncio.start_server(handle_client, "0.0.0.0", 80)
    print("SERVER STARTED")
    print(server)

    while True:
        await asyncio.sleep(5)
        print("Print every 5 s")

# loop = asyncio.get_event_loop()
# loop.create_task(main_server())
# loop.create_task(main_shoot())

async def main():
    # Run both the server and `main_shoot` concurrently
    await asyncio.gather(main_server(), main_shoot())

try:
    # Run the event loop indefinitely
    asyncio.run(main())
except Exception as e:
    print('Error occured: ', e)
except KeyboardInterrupt:
    print('Program Interrupted by the user')