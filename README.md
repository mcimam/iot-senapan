# IOT SENAPAN

This code contains python software to control home-made airgun. This software is design to be deployed to esp-32 with device 

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

