import machine
from machine import RTC, Pin
import neopixel
import network
import socket
from time import sleep_ms, time, sleep
import ntptime

color_of_alphas = (0, 255, 0)  #green, red, blue format 
color_of_seconds = (0, 0, 255)
color_of_corners =  (255, 0, 0)
color_of_alphas_timer = (255, 255, 0)
color_of_border_timer = (0, 255, 255)

wifi_loginy=[["GMH","covidgmh"],["ESP","espgmhco2"]]

rtc = RTC()
neoled = Pin(23, Pin.OUT)
neoled_seconds = Pin(22, Pin.OUT)
button = machine.Pin(4, machine.Pin.IN, machine.Pin.PULL_UP)

np = neopixel.NeoPixel(neoled, 110)
np_seconds = neopixel.NeoPixel(neoled_seconds, 60)

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

def count_down_5_min():
    light_alphas_timer((14,15,16))
    for i in range(5):
            np_seconds.fill(color_of_border_timer)
            j = 0
            for j in range(60):
                np_seconds[59 - j] = (0, 0, 0)
                j += 1
                sleep(1)
                np_seconds.write()
            
            if 4 - i == 4:
                light_alphas_timer((61, 62, 63, 64, 65))
           
            elif 4 - i == 3:
                light_alphas_timer((37, 38, 39))
                    
            elif 4 - i == 2:
                light_alphas_timer((11, 12, 13))
                    
            elif 4 - i == 1:
                light_alphas_timer((6, 7, 8, 9, 10))

            elif 4 - i == 0:
                np.fill((0,0,0))
                    
            np.write()

def count_down_10_min():
    light_alphas_timer((39, 40, 41, 42, 43))
    for i in range(5):
                np_seconds.fill((color_of_border_timer))
                j = 0
                for j in range(60):
                    np_seconds[59 - j] = (0, 0, 0)
                    j += 1
                    sleep(1)
                    np_seconds.write()
                
                if 4 - i == 4:
                    light_alphas_timer((17, 18, 19, 20, 21))

                elif 4 - i == 3:
                    light_alphas_timer((44, 45, 46))
                        
                elif 4 - i == 2:
                    light_alphas_timer((11, 12, 13))
                        
                elif 4 - i == 1:
                    light_alphas_timer((33, 34, 35, 36))
                        
                elif 4 - i == 0:
                    count_down_5_min()
                        
def count_down_15_min():
    light_alphas_timer((81, 82, 83, 84, 85, 86, 87))
    for i in range(5):
                np_seconds.fill((color_of_border_timer))
                j = 0
                for j in range(60):
                    np_seconds[59 - j] = (0, 0, 0)
                    j += 1
                    sleep(1)
                    np_seconds.write()
                
                if 4 - i == 4:
                    light_alphas_timer((55, 56, 58, 80, 81, 82, 83))
            
                elif 4 - i == 3:
                    light_alphas_timer((37, 38, 39, 80, 81, 82, 83))
                        
                elif 4 - i == 2:
                    light_alphas_timer((26, 27, 28, 29, 30, 31, 32))   
                        
                elif 4 - i == 1:
                    light_alphas_timer((47, 48, 49, 50, 51, 52, 53, 54))
                        
                elif 4 - i == 0:
                    count_down_10_min()

def light_alphas_timer(list):
    np.fill((0,0,0))
    for k in (list):
        np[k] = (color_of_alphas_timer)
    np.write()
                        
def count_down_mode():
    mode = 0
    for neo in (np, np_seconds):
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
        count_down_5_min()
    elif mode == 1:
        count_down_10_min()
    else:
        count_down_15_min()

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

    np.fill((0,0,0))
    np_seconds.fill((0,0,0))
       
    row = 0
    for sublist in sublists:
        for i, value in enumerate(sublist):
            if value == True:
                index = i + 11 * row
                if index < len(np):
                    np[index] = color_of_alphas
        row += 1
    
    for index, content in enumerate(dots):
        if content == True:
            index = (15 * (1 + index)) - 1
            np_seconds[index] = color_of_corners
        else:
            pass
        
    np_seconds.write()  
    np.write()    

    return dots
print("System starting...")
while not isconnected():
    connect()
    
print("Connected")
ntptime.settime()


while True:
    print("Displaying time...")
    clock_mode()
    dots = clock_mode()
    
    for i in range(60):
        sleep(0.5)
        if button.value() == 0:
            print("This is countdown")
            count_down_mode()
            np_seconds.fill((0,0,0))
            light_alphas_timer((35, 51, 70))
            while True:
                for i in ((0,0,0), (color_of_border_timer)):
                    np_seconds.fill(i)
                    np_seconds.write()
                    sleep(0.5)
                if button.value() == 0:
                    break
            break
        else:
            pass
        
        if (i == 14 and dots[0]) or (i == 29 and dots[1]) or (i == 44 and dots[2]) or (i == 59 and dots[3]):
            np_seconds[i] = color_of_corners
        else:
            np_seconds[i] = color_of_seconds
            
        np_seconds.write()
        sleep(0.5)
            
