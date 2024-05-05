import machine
from machine import RTC, Pin
import neopixel
import network
import socket
from time import sleep_ms, time, sleep
import ntptime

COLOR_OF_ALPHAS = (255, 255, 255)  #green, red, blue format 
COLOR_OF_SECONDS = (63, 123, 0)
COLOR_OF_CORNERS =  (0, 0, 255)
COLOR_OF_ALPHAS_TIMER = (0, 255, 0)
COLOR_OF_BORDER_TIMER = (0, 255, 0)

wifi_loginy=[["GMH","covidgmh"],["ESP","espgmhco2"]]

rtc = RTC()
neoled = Pin(23, Pin.OUT)
neoled_seconds = Pin(22, Pin.OUT)
button = machine.Pin(4, machine.Pin.IN, machine.Pin.PULL_UP)

neopixel_main = neopixel.NeoPixel(neoled, 110)
neopixel_seconds = neopixel.NeoPixel(neoled_seconds, 60)

network.phy_mode(network.MODE_11G)
ap = network.WLAN(network.AP_IF)
ap.active(False)

station = network.WLAN(network.STA_IF)
station.active(True)

dic_first_part = {
    0: [26, 27, 28, 29, 30, 31, 32], 1: [6, 7, 8, 9, 10], 2: [19, 20, 21], 3: [37, 38, 39],
    4: [55, 56, 57, 58, 59], 5: [16, 17, 18], 6: [40, 41, 42, 43], 7: [22, 23, 24, 25],
    8: [44, 45, 46], 9: [11, 12, 13, 14, 15], 10: [33, 34, 35, 36, 37], 11: [47, 48, 49, 50, 51, 52, 53],
    12: [26, 27, 28, 29, 30, 31, 32], 13: [6, 7, 8, 9, 10], 14: [19, 20, 21], 15: [37, 38, 39],
    16: [55, 56, 57, 58, 59], 17: [16, 17, 18], 18: [40, 41, 42, 43], 19: [22, 23, 24, 25],
    20: [44, 45, 46], 21: [11, 12, 13, 14, 15], 22: [33, 34, 35, 36, 37], 23: [47, 48, 49, 50, 51, 52, 53],
    24: [26, 27, 28, 29, 30, 31, 32]
}

dic_second_part = {
    0: [], 5: [84, 85, 86, 87, 107, 108, 109], 10: [61, 62, 63, 64, 65], 15: [77, 78, 79, 80, 81, 82, 83],
    20: [66, 67, 68, 69, 70, 71], 25: [66, 67, 68, 69, 70, 71, 107, 108, 109], 30: [71, 72, 73, 74, 75, 76],
    35: [71, 72, 73, 74, 75, 76, 107, 108, 109, 110], 40: [91, 92, 93, 94, 95, 96, 97],
    45: [91, 92, 93, 94, 95, 96, 97, 107, 108, 109], 50: [99, 100, 101, 102, 103, 104, 105],
    55: [99, 100, 101, 102, 103, 104, 105, 107, 108, 109],
}

def isconnected():
    global station
    return station.isconnected()

def getmac():
    return station.config('mac')

def wifi_connect(id, pswd):
    global station
    ssid = id
    password = pswd
    if  station.isconnected():   
        return
    print(station.status())
    station.active(False)
    sleep_ms(1000)
    
    station.active(True)
    station.connect(ssid, password)
    
    timeOut=0 
    timeOutMax=50
    while ((not station.isconnected()) and timeOut<timeOutMax):
      sleep_ms(100)
      timeOut=timeOut+1
    if station.isconnected():
        return True
    print("Connection attempt failed")
    return False

def disconnect():
    station.active(False)
    if station.isconnected() == False:
         print("Disconnected")
          
def connect():
  for wifi_essid, wifi_pwd in wifi_loginy:
      print("connecting to wifi: "+wifi_essid+","+wifi_pwd)
      if not isconnected():
          wifi_connect(wifi_essid, wifi_pwd)
      if isconnected():
          break

def hour_offset(current_time):
    summer_time = False
    
    if current_time[1]  in [4, 5, 6, 7, 8, 9]:
        summer_time = True
    elif current_time[1]  in [11, 12, 1, 2]:
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

def count_down(list):
    light_alphas_timer(list[0])
    for i in range(5):
            neopixel_seconds.fill(COLOR_OF_BORDER_TIMER)
            j = 0
            for j in range(60):
                neopixel_seconds[59 - j] = (0, 0, 0)
                j += 1
                sleep(1)
                neopixel_seconds.write()
            
            for l in range(4):
                if 4 - i == 4 - l:
                    light_alphas_timer(list[l + 1])
                    
            if 4 - i == 0:
                if list[0][0] == 14:
                    neopixel_main.fill((0,0,0))
                elif list[0][0] == 39:
                    count_down((14,15,16), (61, 62, 63, 64, 65), (37, 38, 39), (11, 12, 13), (6, 7, 8, 9, 10))
                elif list[0][0] == 81:
                   count_down((39, 40, 41, 42, 43), (17, 18, 19, 20, 21), (44, 45, 46), (11, 12, 13), (33, 34, 35, 36))
                    
            neopixel_main.write()
            
def light_alphas_timer(area):
    neopixel_main.fill((0,0,0))
    for k in (area):
        neopixel_main[k] = COLOR_OF_ALPHAS_TIMER
    neopixel_main.write()
                        
def count_down_mode():
    mode = 0
    for neo in (neopixel_main, neopixel_seconds):
        neo.fill((0, 0, 0))
        neo.write()
    
    light_alphas_timer((14, 15, 16))
    
    for i in range(10):
        sleep(0.5)
        if button.value() == 0:
            i  = 10
            sleep(0.5)
            mode += 1
            if mode == 1:
                light_alphas_timer((39, 40, 41, 42, 43))
            else:
               light_alphas_timer((81, 82, 83, 84, 85, 86, 87))
        sleep(0.5)

    if mode == 0:
        count_down((14,15,16), (61, 62, 63, 64, 65), (37, 38, 39), (11, 12, 13), (6, 7, 8, 9, 10))
    elif mode == 1:
        count_down((39, 40, 41, 42, 43), (17, 18, 19, 20, 21), (44, 45, 46), (11, 12, 13), (33, 34, 35, 36))
    else:
        count_down((81, 82, 83, 84, 85, 86, 87), (55, 56, 58, 80, 81, 82, 83), (37, 38, 39, 80, 81, 82, 83), (26, 27, 28, 29, 30, 31, 32), (47, 48, 49, 50, 51, 52, 53, 54))

def clock_mode():
    current_time_list = list(rtc.datetime())
    hour_offset(current_time_list)
    
    hours = current_time_list[4]
    minutes = current_time_list[5]
    
    clock_text = [0] * 110
    dots = [False] * 4
    
    for i in range(1,5):
        if minutes in [0+i,5+i, 10+i, 15+i, 20+i, 25+i, 30+i, 35+i, 40+i, 45+i, 50+i, 55+i]:
            for j in range(i):
                dots[j] = True
    
    minutes = (minutes//5)*5
    filtered_clock_text_indices = set(dic_first_part.get(hours, []) + dic_second_part.get(minutes, []))
    result_list = [index in filtered_clock_text_indices for index in range(len(clock_text))]
    
    if hours in [0, 1, 5, 6, 7, 8, 9, 10, 11, 12, 13, 17, 18, 19, 20, 21, 22, 23, 24]:
        for i in range(2):
            result_list[i] = True
    else:
        for i in range(2, 6):
            result_list[i] = True
          
    sublists = [result_list[i:i+11] for i in range(0, len(result_list), 11)]
    
    for i, sublist in enumerate(sublists):
        if i % 2 == 1:
            sublists[i] = sublist[::-1]

    neopixel_main.fill((0,0,0))
    neopixel_seconds.fill((0,0,0))
       
    row = 0
    for sublist in sublists:
        for i, value in enumerate(sublist):
            if value == True:
                index = i + 11 * row
                if index < len(neopixel_main):
                    neopixel_main[index] = COLOR_OF_ALPHAS
        row += 1
    
    for index, content in enumerate(dots):
        if content == True:
            index = (15 * (1 + index)) - 1
            neopixel_seconds[index] = COLOR_OF_CORNERS
        else:
            pass
        
    neopixel_seconds.write()  
    neopixel_main.write()    
    return dots, current_time_list

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
        if button.value() == 0:
            print("This is countdown")
            count_down_mode()
            neopixel_seconds.fill((0,0,0))
            light_alphas_timer((35, 51, 70))
            while True:
                for i in ((0,0,0), (COLOR_OF_BORDER_TIMER)):
                    neopixel_seconds.fill(i)
                    neopixel_seconds.write()
                    sleep(0.5)
                if button.value() == 0:
                    sleep(0.1)
                    break
            break
        else:
            pass
        
        if (i == 14 and dots[0]) or (i == 29 and dots[1]) or (i == 44 and dots[2]) or (i == 59 and dots[3]):
            neopixel_seconds[i] = COLOR_OF_CORNERS
        else:
            neopixel_seconds[i] = COLOR_OF_SECONDS
            
        neopixel_seconds.write()
        sleep(0.5)
            
