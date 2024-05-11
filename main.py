from time import sleep_ms, time, sleep
from machine import RTC, Pin
import machine
import neopixel
import network
import socket
import ntptime

COLOR_OF_ALPHAS = (255, 255, 255)  # green, red, blue format
COLOR_OF_SECONDS = (63, 123, 0)
COLOR_OF_CORNERS = (0, 0, 255)
COLOR_OF_ALPHAS_TIMER = (0, 255, 0)
COLOR_OF_BORDER_TIMER = (0, 255, 0)


WIFI_LOGINS = [["GMH", "covidgmh"], ["ESP", "espgmhco2"], ["twojnar", "kvorechu"]]

RTC = RTC()
NEOLED = Pin(23, Pin.OUT)
NEOLED_SECONDS = Pin(22, Pin.OUT)
BUTTON = machine.Pin(4, machine.Pin.IN, machine.Pin.PULL_UP)

NEOPIXEL_MAIN = neopixel.NeoPixel(NEOLED, 110)
NEOPIXEL_SECONDS = neopixel.NeoPixel(NEOLED_SECONDS, 60)

DICTIONARY = [
    {
        0: [26, 27, 28, 29, 30, 31, 32],
        1: [6, 7, 8, 9, 10],
        2: [19, 20, 21],
        3: [37, 38, 39],
        4: [55, 56, 57, 58, 59],
        5: [16, 17, 18],
        6: [40, 41, 42, 43],
        7: [22, 23, 24, 25],
        8: [44, 45, 46],
        9: [11, 12, 13, 14, 15],
        10: [33, 34, 35, 36, 37],
        11: [47, 48, 49, 50, 51, 52, 53],
        12: [26, 27, 28, 29, 30, 31, 32],
        13: [6, 7, 8, 9, 10],
        14: [19, 20, 21],
        15: [37, 38, 39],
        16: [55, 56, 57, 58, 59],
        17: [16, 17, 18],
        18: [40, 41, 42, 43],
        19: [22, 23, 24, 25],
        20: [44, 45, 46],
        21: [11, 12, 13, 14, 15],
        22: [33, 34, 35, 36, 37],
        23: [47, 48, 49, 50, 51, 52, 53],
        24: [26, 27, 28, 29, 30, 31, 32],
    },
    {
        0: [],
        5: [84, 85, 86, 87, 107, 108, 109],
        10: [61, 62, 63, 64, 65],
        15: [77, 78, 79, 80, 81, 82, 83],
        20: [66, 67, 68, 69, 70, 71],
        25: [66, 67, 68, 69, 70, 71, 107, 108, 109],
        30: [71, 72, 73, 74, 75, 76],
        35: [71, 72, 73, 74, 75, 76, 107, 108, 109, 110],
        40: [91, 92, 93, 94, 95, 96, 97],
        45: [91, 92, 93, 94, 95, 96, 97, 107, 108, 109],
        50: [99, 100, 101, 102, 103, 104, 105],
        55: [99, 100, 101, 102, 103, 104, 105, 107, 108, 109],
    },
]

FIVE = (
    (14, 15, 16),
    (61, 62, 63, 64, 65),
    (37, 38, 39),
    (11, 12, 13),
    (6, 7, 8, 9, 10),
)
TEN = (
    (39, 40, 41, 42, 43),
    (17, 18, 19, 20, 21),
    (44, 45, 46),
    (11, 12, 13),
    (33, 34, 35, 36),
)
FIFTEEN = (
    (81, 82, 83, 84, 85, 86, 87),
    (55, 56, 58, 80, 81, 82, 83),
    (37, 38, 39, 80, 81, 82, 83),
    (26, 27, 28, 29, 30, 31, 32),
    (47, 48, 49, 50, 51, 52, 53, 54),
)

network.phy_mode(network.MODE_11G)
ap = network.WLAN(network.AP_IF)
ap.active(False)
station = network.WLAN(network.STA_IF)
station.active(True)


def isconnected():
    "function to check if we are connected to wifi"
    return station.isconnected()


def getmac():
    "function to get mac address"
    return station.config("mac")


def wifi_connect(id, pswd):
    "function to connect to wifi"
    sta_if = network.WLAN(network.STA_IF)
    ssid = id
    password = pswd
    if sta_if.isconnected():
        return True
    print(sta_if.status())
    sta_if.active(False)
    sleep_ms(1000)
    sta_if.active(True)
    sta_if.connect(ssid, password)
    time_out = 0
    time_out_max = 50
    while (not sta_if.isconnected()) and time_out < time_out_max:
        sleep_ms(100)
        time_out = time_out + 1
    if sta_if.isconnected():
        return True
    print("Connection attempt failed")
    return False


def disconnect():
    "function to disconnect from wifi"
    station.active(False)
    if station.isconnected() is False:
        print("Disconnected")


def connect():
    "function to connect to wifi"
    for wifi_essid, wifi_pwd in WIFI_LOGINS:
        print("connecting to wifi: " + wifi_essid + "," + wifi_pwd)
        if not isconnected():
            wifi_connect(wifi_essid, wifi_pwd)
        if isconnected():
            break


def hour_offset(current_time):
    "function to get hour offset from winter to summer time"
    summer_time = False
    if current_time[1] in [4, 5, 6, 7, 8, 9]:
        summer_time = True
    elif current_time[1] in [11, 12, 1, 2]:
        pass
    elif current_time[1] == 3 and current_time[2] >= 25:
        if 7 - current_time[3] + current_time[2] >= 31:
            summer_time = True
        else:
            pass
    elif current_time[1] == 10 and current_time[2] >= 25:
        if 7 - current_time[3] + current_time[2] >= 31:
            pass
        else:
            summer_time = True
    if summer_time:
        current_time[4] += 2
    else:
        current_time[4] += 1


def count_down(list_of_word_for_countdown):
    "function to count down"
    light_alphas_timer(list_of_word_for_countdown[0])
    for k in range(5):
        NEOPIXEL_SECONDS.fill(COLOR_OF_BORDER_TIMER)
        j = 0
        for j in range(60):
            NEOPIXEL_SECONDS[59 - j] = (0, 0, 0)
            j += 1
            sleep(1)
            NEOPIXEL_SECONDS.write()
        for j in range(4):
            if 4 - k == 4 - j:
                light_alphas_timer(list_of_word_for_countdown[j + 1])
        if 4 - k == 0:
            if list_of_word_for_countdown[0][0] == 14:
                NEOPIXEL_MAIN.fill((0, 0, 0))
            elif list_of_word_for_countdown[0][0] == 39:
                count_down(FIVE)
            elif list_of_word_for_countdown[0][0] == 81:
                count_down(TEN)
        NEOPIXEL_MAIN.write()


def light_alphas_timer(area):
    "function to light alphas"
    NEOPIXEL_MAIN.fill((0, 0, 0))
    for j in area:
        NEOPIXEL_MAIN[j] = COLOR_OF_ALPHAS_TIMER
    NEOPIXEL_MAIN.write()


def count_down_mode():
    "function to count down mode"
    mode = 0
    for neo in (NEOPIXEL_MAIN, NEOPIXEL_SECONDS):
        neo.fill((0, 0, 0))
        neo.write()
    light_alphas_timer((14, 15, 16))
    for _ in range(10):
        sleep(0.5)
        if BUTTON.value() == 0:
            sleep(0.5)
            mode += 1
            if mode == 1:
                light_alphas_timer((39, 40, 41, 42, 43))
            else:
                light_alphas_timer((81, 82, 83, 84, 85, 86, 87))
        sleep(0.5)

    if mode == 0:
        count_down(FIVE)
    elif mode == 1:
        count_down(TEN)
    else:
        count_down(FIFTEEN)


def clock_mode():
    "function to clock mode"
    current_time = list(RTC.datetime())
    hour_offset(current_time)
    hours = current_time[4]
    minutes = current_time[5]
    clock_text = [0] * 110
    clock_dots = [False] * 4
    for j in range(1, 5):
        if minutes in [
            0 + j,
            5 + j,
            10 + j,
            15 + j,
            20 + j,
            25 + j,
            30 + j,
            35 + j,
            40 + j,
            45 + j,
            50 + j,
            55 + j,
        ]:
            for k in range(j):
                clock_dots[k] = True
    minutes = (minutes // 5) * 5
    filtered_clock_text = set(
        DICTIONARY[0].get(hours, []) + DICTIONARY[1].get(minutes, [])
    )
    result_list = [index in filtered_clock_text for index in range(len(clock_text))]
    if hours in [0, 1, 5, 6, 7, 8, 9, 10, 11, 12, 13, 17, 18, 19, 20, 21, 22, 23, 24]:
        for j in range(2):
            result_list[j] = True
    else:
        for j in range(2, 6):
            result_list[j] = True
    lists = [result_list[i : i + 11] for i in range(0, len(result_list), 11)]
    for j, sublist in enumerate(lists):
        if j % 2 == 1:
            lists[j] = sublist[::-1]

    NEOPIXEL_MAIN.fill((0, 0, 0))
    NEOPIXEL_SECONDS.fill((0, 0, 0))
    row = 0
    for sublist in lists:
        for b, value in enumerate(sublist):
            if value is True:
                index = b + 11 * row
                if index < len(NEOPIXEL_MAIN):
                    NEOPIXEL_MAIN[index] = COLOR_OF_ALPHAS
        row += 1
    for index, content in enumerate(clock_dots):
        if content is True:
            index = (15 * (1 + index)) - 1
            NEOPIXEL_SECONDS[index] = COLOR_OF_CORNERS
        else:
            pass
    NEOPIXEL_SECONDS.write()
    NEOPIXEL_MAIN.write()
    return clock_dots, current_time


print("System starting...")
while not isconnected():
    connect()
print("Connected")
ntptime.settime()

print("Displaying time...")
while True:
    clock_mode()
    dots = clock_mode()[0]
    current_time_list = clock_mode()[1]
    for i in range(60 - current_time_list[6]):
        sleep(0.5)
        if BUTTON.value() == 0:
            print("This is countdown")
            count_down_mode()
            NEOPIXEL_SECONDS.fill((0, 0, 0))
            light_alphas_timer((35, 51, 70))
            while True:
                for i in ((0, 0, 0), (COLOR_OF_BORDER_TIMER)):
                    NEOPIXEL_SECONDS.fill(i)
                    NEOPIXEL_SECONDS.write()
                    sleep(0.5)
                if BUTTON.value() == 0:
                    sleep(0.1)
                    break
            break
        if (i in [14, 29, 44, 59]) and any(
            i == (14 + 15 * j) for j, dot in enumerate(dots) if dot
        ):
            NEOPIXEL_SECONDS[i] = COLOR_OF_CORNERS
        else:
            NEOPIXEL_SECONDS[i] = COLOR_OF_SECONDS
        NEOPIXEL_SECONDS.write()
        sleep(0.5)
