from machine import Pin, Timer
from time import sleep_ms
from config import ConfigHandler

# CONSTANT
SELENOID1 = Pin(22, Pin.OUT)
SELENOID2 = Pin(23, Pin.OUT)

BF = Pin(15, Pin.IN, Pin.PULL_DOWN)
BFS = Pin(33, Pin.IN)

# LOAD SERVICE
CH = ConfigHandler()

# variable
timer = Timer(1)  # for debouncer
ammo_count = 0

fire_state = 0  # 0:single;1:burst;2:brmmm
shoot_state = False  # Indicate if it's still firing

# SENAPAN METHOD
def blowback():
    SELENOID2.on()
    sleep_ms(CH.config["DELAY_PISTON"])
    SELENOID2.off()


def valve():
    SELENOID1.on()
    sleep_ms(CH.config["DELAY_VALVE"])
    SELENOID1.off()


def fire():
    valve()
    sleep_ms(CH.config["DELAY_BETWEEN"])
    blowback()
    global ammo_count
    ammo_count += 1


def shoot():
    if BFS.value() == 0:
        fire()
        sleep_ms(CH.config["DELAY_FIRE"])
    # elif fire_state == 1:
    #     for i in range(1, 3):
    #         fire()
    #         sleep_ms(CH.config["DELAY_FIRE"])
    elif BFS.value() == 1:
        while BF.value() == 1:
            fire()
            sleep_ms(CH.config["DELAY_FIRE"])



# INTERUPT
def handle_shooting():
    global shoot_state
    # print("---")
    # print(BF.value())
    if BF.value() == 1 and shoot_state is False:
        shoot_state = True
        shoot()
    elif BF.value() == 0:
        shoot_state = False
        return

# def handle_interupt_timer(p):
#     # debouncing
#     print("ITERUPT TR 1")
#     timer.init(mode=Timer.ONE_SHOT, period=CH.config["DELAY_TRIGGER"], callback=handle_interupt_rising)


# def setup_gun():
#     global BF
#     BF.irq(trigger=Pin.IRQ_RISING, handler=handle_interupt_rising)
