import network
import asyncio
from config import ConfigHandler
from gun import shoot, ammo_count


class WebServer:
    def __init__(self, ssid, password):
        self.ssid = ssid
        self.password = password
        self.ch = ConfigHandler()
        self.ch.read()
        self.value = self.ch.config
        self.server = None

    def setup_ap(self):
        global ap
        ap = network.WLAN(network.AP_IF)
        ap.config(essid=self.ssid, password=self.password)
        ap.active(True)
        print("Connection successful")
        print(ap.ifconfig())

    def start_web(self):
        self.server = asyncio.start_server(self.handle_client, "0.0.0.0", 80)

    #     global web_s
    #     web_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #     web_s.bind(("", 80))
    #     web_s.listen(5)

    def web_page(self):
        html = """
            <html lang="en">
            <head>
                <title>SENAPAN</title>
                <style>
                    body {
                        display: flex;
                        flex-direction: column;
                        align-items: center;
                        justify-content: center;
                        min-height: 100vh;
                        margin: 0;
                        font-family: Arial, sans-serif;
                        background-color: #f4f4f4;
                        padding: 20px;
                        box-sizing: border-box;
                    }

                    h1 {
                        margin-bottom: 20px;
                        font-size: 2rem;
                        text-align: center;
                        color: #333;
                    }

                    button {
                        padding: 0.75rem 1.5rem;
                        font-size: 1rem;
                        border: none;
                        border-radius: 5px;
                        cursor: pointer;
                        transition: background-color 0.3s ease;
                    }

                    #counter-button {
                        background-color: #007BFF;
                        color: #fff;
                    }

                    #counter-button:hover {
                        background-color: #0056b3;
                    }

                    #config-button {
                        font-size: 0.875rem;
                        background-color: #6c757d;
                        color: #fff;
                        margin-bottom: 20px;
                    }

                    #config-button:hover {
                        background-color: #5a6268;
                    }

                    /* Counter display */
                    p {
                        font-size: 1.25rem;
                        margin: 10px 0;
                        color: #333;
                    }

                    /* Form Styling */
                    form {
                        display: none;
                        flex-direction: column;
                        align-items: center;
                        max-width: 400px;
                        background-color: #fff;
                        padding: 20px;
                        border-radius: 8px;
                        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                    }

                    label {
                        font-size: 1rem;
                        margin-bottom: 5px;
                        color: #333;
                    }

                    input {
                        padding: 0.5rem;
                        margin-bottom: 15px;
                        border: 1px solid #ccc;
                        border-radius: 5px;
                        font-size: 1rem;
                    }

                    button[type="submit"] {
                        background-color: #28a745;
                        color: #fff;
                    }

                    button[type="submit"]:hover {
                        background-color: #218838;
                    }

                    @media (max-width: 600px) {
                        h1 {
                            font-size: 1.5rem;
                        }

                        button {
                            font-size: 0.875rem;
                        }

                        p {
                            font-size: 1rem;
                        }
                    }
                </style>
            </head>
            <body>
                <h1>SENAPAN</h1>

                <!-- Counter Section -->
                <button id="counter-button" onclick="fire()">Fire</button>
                <p>Counter: <span id="counter">%s</span></p>

                <!-- Form Section -->
                <button id="config-button" onclick="toggleForm()">⚙️ Configure</button>
                <form id="config-form" action="/save" method="GET">
                    <label for="field1">Delay Piston:</label>
                    <input type="number" id="DELAY_PISTON" name="DELAY_PISTON" value=%s required>

                    <label for="field2">Delay Valve:</label>
                    <input type="number" id="DELAY_VALVE" name="DELAY_VALVE" value=%s required>

                    <label for="field2">Delay Between:</label>
                    <input type="number" id="DELAY_BETWEEN" name="DELAY_BETWEEN" value=%s required>

                    <label for="field3">Delay Trigger:</label>
                    <input type="number" id="DELAY_TRIGGER" name="DELAY_TRIGGER" value=%s required>

                    <button type="submit">Save</button>
                </form>

                <script>
                    let count = 0;

                    function fire() {
                        count++;
                        document.getElementById("counter").textContent = count;

                        fetch('/fire', {
                            method: 'GET',
                        }).then(response => {
                            if (!response.ok) {
                                console.error("API call failed:", response.statusText);
                            } else {
                                console.log("API call successful!");
                            }
                        }).catch(error => {
                            console.error("Error during API call:", error);
                        });
                    }

                    function toggleForm() {
                        const form = document.getElementById("config-form");
                        form.style.display = form.style.display === "none" ? "flex" : "none";
                    }
                </script>
            </body>
            </html>
        """ % (
            ammo_count,
            self.value.get("DELAY_PISTON"),
            self.value.get("DELAY_VALVE"),
            self.value.get("DELAY_BETWEEN"),
            self.value.get("DELAY_TRIGGER"),
        )

        return html

    def save_config(self, values):
        for v, k in values:
            self.ch.update(v, k)
        self.ch.write()

    async def handle_client(reader, writer):
        print("Client connected")
        request_line = await reader.readline()
        print("Request:", request_line)

        # Skip HTTP request headers
        while await reader.readline() != b"\r\n":
            pass

        request = str(request_line, "utf-8").split()[1]
        print("Request:", request)

    def recieve_conn(self):
        global web_s
        conn, addr = web_s.accept()
        # print("---------")
        # print(addr)

        req = conn.recv(1024).decode("utf-8")
        # print('Request:', req)

        # We Get REQUEST PART
        request = req.split("\n")[0]
        if "/save" in request:
            try:
                params = request.split("?")[1].split(" ")[0].split("&")
                for param in params:
                    key, value = param.split("=")
                    # print("%s : %s" % (key, value))
                    self.ch.update(key, value)
            except Exception:
                print("Error")

        elif ("/fire") in request:
            shoot()

        response = self.web_page()
        conn.send(response)
        conn.close()
