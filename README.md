# IOT SENAPAN

This project provides Python-based software for controlling a custom-built airgun. The software is designed for deployment on an ESP32 microcontroller and utilizes MicroPython for embedded execution. 

**DISCLAIMER**: This project involves the control of potentially dangerous devices.  Use with extreme caution.  The authors are not responsible for any injury, damage, or legal issues resulting from the use or misuse of this software or hardware.  This project is for educational and experimental purposes only.

## Config
Config can be set through rpl or website or directly modified throu config file. 

List of available config.
| Name          | Description                       | Default Value |
| ------------- | --------------------------------- | ------------- |
| ENABLE_WEB    | Enable web interface              | 1             |
| DELAY_PISTON  | Time pushback piston open         | 30            |
| DELAY_VALVE   | Time firing piston open           | 40            |
| DELAY_BETWEEN | Delay between firing and pushback | 30            |
| DELAY_TRIGGER | \-                                | 20            |
| DELAY_FIRE    | Delay between shoot               | 10            |
| DELAY_WEB     | Time to pend web startup          | 100           |


## Deployment
1. Install micropython firmare to ESP-32 device.
2. Copy everything inside `src` into `/` file in esp32.
3. Restart ESP-32 device.


## Credits
- Yusuf Hidayat <>
- Choirul Imam <imam123.ci@gmail.com>

## License
This Code is license under AGPL-3

