from config import ConfigHandler
import web
from gun import shoot, ammo_count


app = web.App(host="0.0.0.0", port=80)
ch = ConfigHandler()


def landing_page():
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
               <form id="config-form" action="/save" method="POST">
                    <label for="field1">Delay Piston:</label>
                    <input type="number" id="DELAY_PISTON" name="DELAY_PISTON" value=%s required>

                    <label for="field2">Delay Valve:</label>
                    <input type="number" id="DELAY_VALVE" name="DELAY_VALVE" value=%s required>

                    <label for="field2">Delay Between:</label>
                    <input type="number" id="DELAY_BETWEEN" name="DELAY_BETWEEN" value=%s required>

                    <label for="field3">Delay Trigger:</label>
                    <input type="number" id="DELAY_TRIGGER" name="DELAY_TRIGGER" value=%s required>

                    <label for="field3">Delay Fire:</label>
                    <input type="number" id="DELAY_FIRE" name="DELAY_FIRE" value=%s required>

                    <button type="submit">Save</button>
               </form>

               <script>
                    let count = 0;

                    // Fire function to handle the counter and API call
                    function fire() {
                         count++;
                         document.getElementById("counter").textContent = count;

                         fetch('/fire', {
                              method: 'GET',
                         })
                         .then(response => {
                              if (!response.ok) {
                                   console.error("API call failed:", response.statusText);
                              } else {
                                   console.log("API call successful!");
                              }
                         })
                         .catch(error => {
                              console.error("Error during API call:", error);
                         });
                    }

                    // Toggle form visibility
                    function toggleForm() {
                         const form = document.getElementById("config-form");
                         if (form.style.display === "none" || form.style.display === "") {
                              form.style.display = "flex"; // Show form
                         } else {
                              form.style.display = "none"; // Hide form
                         }
                    }

                    // Save function to submit form data
                    function save(event) {
                         event.preventDefault(); // Prevent default form submission

                         const form = document.getElementById("config-form");
                         const formData = new FormData(form);

                         // Log FormData as key-value pairs for debugging
                         console.log(formData)

                         fetch('/save', {
                              method: 'POST',
                              body: formData,
                         })
                         .then(response => {
                              if (!response.ok) {
                                   console.error("API call failed:", response.statusText);
                              } else {
                                   console.log("Configuration saved successfully!");
                              }
                         })
                         .catch(error => {
                              console.error("Error during API call:", error);
                         });
                    }
               </script>

          </body>
          </html>
     """ % (
        ammo_count,
        ch.config.get("DELAY_PISTON"),
        ch.config.get("DELAY_VALVE"),
        ch.config.get("DELAY_BETWEEN"),
        ch.config.get("DELAY_TRIGGER"),
        ch.config.get("DELAY_FIRE"),
    )

    return html


@app.route("/")
async def home(r, w):
    # write http headers
    w.write(b"HTTP/1.0 200 OK\r\n")
    w.write(b"Content-Type: text/html; charset=utf-8\r\n")
    w.write(b"\r\n")

    lp = landing_page()
    w.write(lp)

    await w.drain()


@app.route("/fire")
async def fire(r, w):
    shoot()

    w.write(b"HTTP/1.0 200 OK\r\n")
    w.write(b"Content-Type: text/html; charset=utf-8\r\n")
    w.write(b"\r\n")
    await w.drain()


@app.route("/save", methods=["POST"])
async def save_config(r, w):
    body = await r.read(1024)
    form = web.parse_qs(body.decode())

    for k, v in form.items():
        ch.config[k] = int(v)

    print("Save New Config")
    print(ch.config)

    ch.write()
    w.write(b"HTTP/1.0 302 Found\r\n")
    w.write(b"Location: /\r\n")  # Redirect to "/"
    w.write(b"\r\n")
    await w.drain()
