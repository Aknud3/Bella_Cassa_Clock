# Vyrobil Eduard Wojnar

#import všech knihoven
from time import sleep_ms, time, sleep
from machine import RTC, Pin, WDT
import machine
import neopixel
import network
import socket
import ntptime
import gc

# tisknutí volné paměti v čipu
print(gc.mem_free())

# Nastavení všech barev ledek
#GRB
COLOR_OF_ALPHAS = (184*5, 255*5, 0) # barvy písmen
COLOR_OF_ALPHAS_TIMER = (0, 500, 0) # barvy písmen v timeru

# RGB
COLOR_OF_SECONDS = (2, 2, 2) # barvy sekund
COLOR_OF_CORNERS = (0, 0, 64) # barvy rohů
COLOR_OF_BORDER_TIMER = (128, 0, 0) # barva sekund v timeru
COLOR_OF_AMBIENT = (0, 0, 0) # barvy ambientního osvětlení

COLOR_OF_SUPPORT_ALPHAS = (51, 30, 0) # Barvy pomocných písmen (poslední řada písmenek
COLOR_OF_SUPPORT_ALPHAS_TIMER = (100, 0, 0) # barvy pomocných písmen v timeru

FIRST_CORNER_INDEX = 1 # index prvního rohu
SECOND_CORNER_INDEX = 33 # index druhého rohu
THIRD_CORNER_INDEX = 65 # index třetího rohu
FOURTH_CORNER_INDEX = 97 # index čtvrtého rohu

BUTTON_PRESS = 2 # tlačítko, je vypnuto můžete ignorovat

WIFI_LOGINS = [["GMH", "covidgmh"], ["ESP", "espgmhco2"]] # hesla na wifi
wdt = WDT(timeout=100000000) # vypnutý timeout, protože bez toho to padá
wdt.feed() # bez tohohle to padá kvůli timeoutu
RTC_MODULE = RTC() # deklarace RTC modulu

# Určení na jakém pinu jsou věci
NEOLED = Pin(15, Pin.OUT)  # na pinu 15 jsou písmenka
NEOLED_SUPPORT = Pin(16, Pin.OUT) # na pinu 16 jsou pomocná písmenka
NEOLED_SECONDS = Pin(13, Pin.OUT) # na pinu 13 jsou sekundy
BUTTON = Pin(27, Pin.IN) # na pinu 27 je tlačítko


NEOPIXEL_MAIN = neopixel.NeoPixel(NEOLED, 110) # písmenka
NEOPIXEL_SECONDS = neopixel.NeoPixel(NEOLED_SECONDS, 140) # sekundy
NEOPIXEL_MAIN_SUPPORT = neopixel.NeoPixel(NEOLED_SUPPORT, 11) # pomocná písmenka

# Toto je slovník demon, který určuje jaká ledka se rozsvítí v sekundách 

DEMON = {
    0: FIRST_CORNER_INDEX,
    1: 3,
    2: 5,
    3: 7,
    4: 9,
    5: 11,
    6: 13,
    7: 15,
    8: 17,
    9: 19,
    10: 21,
    11: 23,
    12: 25,
    13: 27,
    14: 29, 
    15: SECOND_CORNER_INDEX,
    16: 35,
    17: 37,
    18: 39,
    19: 41,
    20: 43,
    21: 45,
    22: 47,
    23: 49,
    24: 51,
    25: 53,
    26: 55,
    27: 57,
    28: 59,
    29: 61,
    30: THIRD_CORNER_INDEX,
    31: 67,
    32: 69,
    33: 71,
    34: 73,
    35: 75,
    36: 77,
    37: 79,
    38: 81,
    39: 83,
    40: 85,
    41: 87,
    42: 89,
    43: 91,
    44: 93,
    45: FOURTH_CORNER_INDEX,
    46: 99,
    47: 101,
    48: 103,
    49: 105,
    50: 107, 
    51: 109,
    52: 111,
    53: 113,
    54: 115,
    55: 117,
    56: 119,
    57: 121,
    58: 123,
    59: 125,
}

# Tady jsou zbylé slovníky, které určují jaké ledky písmenkách se rozsvěcujou. 3, 37 - T, 38 - Ř, 39 - I etc.
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
    # Tady jsou na sekundy 10, 61 - D, 62 - E... 
    {
        0: [],
        5: [84, 85, 86, 87, 107, 108, 109],
        10: [61, 62, 63, 64, 65],
        15: [77, 78, 79, 80, 81, 82, 83],
        20: [66, 67, 68, 69, 70, 71],
        25: [66, 67, 68, 69, 70, 71, 107, 108, 109],
        30: [71, 72, 73, 74, 75, 76],
        35: [71, 72, 73, 74, 75, 76, 107, 108, 109, 110],
        40: [90, 91, 92, 93, 94, 95, 96, 97],
        45: [90, 91, 92, 93, 94, 95, 96, 97, 107, 108, 109],
        50: [99, 100, 101, 102, 103, 104, 105],
        55: [99, 100, 101, 102, 103, 104, 105, 107, 108, 109],
    },
]

# toto se používá pro timer
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

# Nastavení sítě (Tento kód je Pana Jelínka, který programoval k čidlu vzduchu
network.phy_mode(network.MODE_11G)
ap = network.WLAN(network.AP_IF)
ap.active(False)
station = network.WLAN(network.STA_IF)
station.active(True)

# Funkce Pana Jelínka, co zjišťuje jestli jsme připojení k internetu
def isconnected():
    "function to check if we are connected to wifi"
    return station.isconnected()

# Funkce Pana Jelínka, co nám získá mac adresu
def getmac():
    "function to get mac address"
    return station.config("mac")

# FUnkce Pana Jelínka, co řídí připojení k internetu
def wifi_connect(ssid, pswd):
    "function to connect to wifi"
    sta_if = network.WLAN(network.STA_IF)
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

# Funkce Pana Jelínka, pro odpojení od Wifi
def disconnect():
    "function to disconnect from wifi"
    station.active(False)
    if station.isconnected() is False:
        print("Disconnected")

# Funkce Pana Jelínka, pro připojení k wifi
def connect():
    "function to connect to wifi"
    for wifi_essid, wifi_pwd in WIFI_LOGINS:
        print("connecting to wifi: " + wifi_essid + "," + wifi_pwd)
        if not isconnected():
            wifi_connect(wifi_essid, wifi_pwd)
        if isconnected():
            break

# Funkce, co řídí letní a zimní čas
def hour_offset(current_time):
    "function to get hour offset from winter to summer time"

    # funguje na principu dopočítávání dnů v měsící 
    summer_time = False # defaultně je nastaven na zimní čas
    
    if current_time[1] in [4, 5, 6, 7, 8, 9]: # Jestli jsou tyto měsíce tak je automaticky letní čas
        summer_time = True
    elif current_time[1] in [11, 12, 1, 2]: # Jestli jsou tyto měsíce tak je automaticky, tak se nic nestane a je zimní čas
        pass
        
    elif current_time[1] == 3 and current_time[2] >= 25: # Jestli je tento měsíc a jsou tyto dny
        if 7 - current_time[3] + current_time[2] >= 31: # funguje tam nějaká logika, co už si nepamatuju jak jsem vymýšlel, ale je to nějak spojené s nedělemi
            summer_time = True 
        else:
            pass
            
    elif current_time[1] == 10 and current_time[2] <= 25: # Stejná logika jako o řádky nahoře, akorát pro jiný měsíc
        if 7 - current_time[3] + current_time[2] >= 31:
            pass
        else:
            summer_time = True

    if summer_time: # Protože bereme Anglický čas, ak letní je 2+ a zimní 1+
        current_time[4] += 2
    else:
        current_time[4] += 1

# Funkce timeru, kterou jsem tady nechal, zapíná se tlačítkem
def count_down(list_of_word_for_countdown):
    "function to count down"
    # tady je hodně velkej demon (koment pro mě, co mám opravi)

    # Tohle funguje na principu, že tam hodím list a podle toho se mi rozsvítí nějaké písmenka
    light_alphas_timer(list_of_word_for_countdown[0])
    for k in range(5): # Vše funguje v 5 minutovém formátu
        NEOPIXEL_SECONDS.fill(COLOR_OF_BORDER_TIMER) # vše se zbarvní do barvy a potom každou sekundu se jedna ledka vypne, jakoby odpočítává
        NEOPIXEL_SECONDS.write()
        for j in range(60):
            NEOPIXEL_SECONDS[DEMON[59 - j]] = (0, 0, 0)
            sleep(1) 
            NEOPIXEL_SECONDS.write() # odpočítává
        if k < 4:
            light_alphas_timer(list_of_word_for_countdown[k + 1]) # dostaneme se na další písmenka 

        if k == 4: # Jestli jsme u posledního indexu, tak se podíváme, jaký timer jsme si vybrali, jestli 5 tak se funkce ukončí, jestli 10, tak jede timer pro 5 minut, jestli 15 tak jede timer pro 10 minut, proto to je v 5 minutovém formátu, abych tuto funkci mohl použít víckrát
            if list_of_word_for_countdown == FIVE:
                NEOPIXEL_MAIN.fill((0, 0, 0))
            elif list_of_word_for_countdown == TEN:
                count_down(FIVE)
            elif list_of_word_for_countdown == FIFTEEN:
                count_down(TEN)
        NEOPIXEL_MAIN.write() #vše se zapíše do ledek

# pouze pomocná funkce, co mi pomáhá rozsvítit ledky, používá se hodně v kodu
def light_alphas_timer(area):
    "function to light alphas"
    NEOPIXEL_MAIN.fill((0, 0, 0)) # vše nastaví na bezbarvy
    for j in area: # podle toho, co do funkce vložíme, to se rozsvítí na tu barvu, co chceme
        NEOPIXEL_MAIN[j] = COLOR_OF_ALPHAS_TIMER
    NEOPIXEL_MAIN.write() # zase zapíšeme

# Funkce, co nám řídí jak moc velký countdown chceme
def count_down_mode():
    "function to count down mode"
    mode = 0 # defaultní mod je 0
    for neo in (NEOPIXEL_MAIN, NEOPIXEL_SECONDS, NEOPIXEL_MAIN_SUPPORT): # Vše zhasne
        neo.fill((0, 0, 0))
        neo.write()
    light_alphas_timer((14, 15, 16)) # rozsvítíme pět protože to je defaultní 
    for _ in range(10): # 5 sekund čekáme a jestli během toho někdo znova zmáčkne tlačítko, tak se mod dá + 1 a rozsvítí se deset nebo patnáct
        sleep(0.5)
        if BUTTON.value() == BUTTON_PRESS:
            sleep(0.5)
            mode += 1
            if mode == 1:
                light_alphas_timer((39, 40, 41, 42, 43))
            else:
                light_alphas_timer((81, 82, 83, 84, 85, 86, 87))
        sleep(0.5)

    if mode == 0: # Jestli je mode stále 0, tak je pět minut timer
        count_down(FIVE)
    elif mode == 1: # Jestli je mode 1 tak je timer na 10 minut
        count_down(TEN)
    else: # Jestli to je cokoliv jiného tak je timer na 15 minut
        count_down(FIFTEEN)
        
    # Tato funkce tady stále je, ale protože je tlačítko vypnuté, tak se nepoužívá

# Toto je hlavní funkce hodin
def clock_mode():
    "function to clock mode" 
    current_time = list(RTC_MODULE.datetime()) #Vememe si čas z knihovny
    hour_offset(current_time) # Hodíme ho do funkce hour_offset aby nám to dalo víc hodin
    hours = current_time[4] # Vememe si z času hodiny 
    minutes =  current_time[5] # Vememe si z času minuty
    clock_text = [0] * 110 # Uděláme si pole
    clock_dots = [False] * 4 # Uděláme si pole pro minuty 

    # Tady tenhle loop z minut normálních dělá rohy (nevím už jak to funuje, je to nějaká demonovina)
    for j in range(1, 5):
        if minutes in [5 * x + j for x in range(0, 12)]:
            for k in range(j):
                clock_dots[k] = True
                
    minutes = (minutes // 5) * 5 # zaokrouhlíme si minuty bez pětek

    # Toto je demon 
    # Tohle mi funguje s těma minutama a slovníkama to převede 
    filtered_clock_text = set(
        DICTIONARY[0].get(hours, []) + DICTIONARY[1].get(minutes, [])
    )
    result_list = [index in filtered_clock_text for index in range(len(clock_text))]
    if hours in [0, 1, 5, 6, 7, 8, 9, 10, 11, 12, 13, 17, 18, 19, 20, 21, 22, 23, 24]: # Jestli jsou tyhle hodiny, tak se rozsvítí JE
        for j in range(2):
            result_list[j] = True
    else:
        for j in range(2, 6): # Jinak se rozsvítí JSOU
            result_list[j] = True
            
    # Tohle mi rozdělí ten velkej list na menší listy        
    lists = [result_list[i : i + 11] for i in range(0, len(result_list), 11)]
    for j, sublist in enumerate(lists): # Protože podle toho jak tam jsou ledky nalepené, tak se to tam lepí do hada a proto vždy sudé se musí obrátit zrcadlově
        if j % 2 == 1:
            lists[j] = sublist[::-1]

    # Tohle mi vše resetuje
    NEOPIXEL_MAIN.fill((0, 0, 0))
    NEOPIXEL_SECONDS.fill((0, 0, 0))
    NEOPIXEL_MAIN_SUPPORT.fill((0, 0, 0))

    # Nastaví ambientního osvětlení
    for j in range(140):
        if j % 2 != 1:
            NEOPIXEL_SECONDS[j] = COLOR_OF_AMBIENT

    # Tohle je další demon
    row = 0 # řada je první
    for sublist in lists: # pro sublist v listech
        for b, value in enumerate(sublist): # podívám se na idex i co v tom je 
            if value is True: # jestli value je pravdivá
                index = b + 11 * row # Nastaví index podle řady
                if index < 99: # Jestli to je menší jak 99, tak je to normální led pásek
                    NEOPIXEL_MAIN[index] = COLOR_OF_ALPHAS
                elif 110 >= index and index >= 99: # jestli to je mezi tímto tak to je pro podporný pásek
                    NEOPIXEL_MAIN_SUPPORT[(index - 99)] = COLOR_OF_SUPPORT_ALPHAS # ta matika tam je aby se odečetl ten index a normálně to fungovalo
        row += 1 # přičte se čada v tom listu

    # tady bude ultra demonek (tady byl ultra demonek, ale tohle už je opravený)
    
    #tady s tím jsem se moc neprděl, je to extrémně jednoduchej kod 
    corners = 0 # podle toho jaký jsou minuty v rozích tak, to se rozsvítí
    for content in clock_dots:
        if content is True:
            corners += 1
        else:
            pass

    if corners == 1: # jestli jedna, tak jenom jedna ledka
        NEOPIXEL_SECONDS[FIRST_CORNER_INDEX] = COLOR_OF_CORNERS
    elif corners == 2: #Jestli dvě, tak dvě se rozsvítí etc.
        for i in (FIRST_CORNER_INDEX, SECOND_CORNER_INDEX):
            NEOPIXEL_SECONDS[i] = COLOR_OF_CORNERS
    elif corners == 3:
        for i in (FIRST_CORNER_INDEX, SECOND_CORNER_INDEX, THIRD_CORNER_INDEX):
            NEOPIXEL_SECONDS[i] = COLOR_OF_CORNERS
    elif corners == 4:
        for i in (FIRST_CORNER_INDEX, SECOND_CORNER_INDEX, THIRD_CORNER_INDEX, FOURTH_CORNER_INDEX):
            NEOPIXEL_SECONDS[i] = COLOR_OF_CORNERS
            
    NEOPIXEL_SECONDS.write() # vše zapíšu

    NEOPIXEL_MAIN.write() # 
    NEOPIXEL_MAIN_SUPPORT.write()
    return current_time, corners # tahle funkce mi do main loopu vrací current_time a rohy minut


wdt.feed() # vyčistím pamět, protože jinak to padá
print("System starting...") # print na start systému
while not isconnected(): # funkce na connect k internetu
    connect()
print("Connected")
ntptime.settime() # vememe si čas

print("Displaying time...") # print, že hodiny fungujou

while True: # Hlavní loop 
    wdt.feed() # zase pamět
    current_time_list, cornerss = clock_mode() # spustíme logiku
    if current_time_list[6] == 1: # Protože čas někdy z internetu buguje a nezačíná na 0 ale 1, tak tohle ho upraví aby sekudny jeli dokonce
        current_time_list[6] -= 1
    for i in range(60 - current_time_list[6]): # tohle nám synchronizuje sekundy
        
        NEOPIXEL_SECONDS[DEMON[i]] = COLOR_OF_SECONDS # podívá se do démona
        
        if cornerss >= 1  and i != 0: # nastavuje sekundy aby to tam probliklo
            NEOPIXEL_SECONDS[FIRST_CORNER_INDEX] = COLOR_OF_CORNERS
                
        if cornerss >= 2 and i != 15: # Nastavuje sekundy aby to probliklo
            NEOPIXEL_SECONDS[SECOND_CORNER_INDEX] = COLOR_OF_CORNERS
        if cornerss >= 3 and i != 30:
            NEOPIXEL_SECONDS[THIRD_CORNER_INDEX] = COLOR_OF_CORNERS
        if cornerss == 4 and i != 45:
            NEOPIXEL_SECONDS[FOURTH_CORNER_INDEX] = COLOR_OF_CORNERS
            
        # Tohle je aby se rozsvítila poslední ledka kdyby to bugovalo
        if i == 59:
            NEOPIXEL_SECONDS[125] = COLOR_OF_SECONDS
        NEOPIXEL_SECONDS.write()
        sleep(1) # sleep 1 sekunda aby to čekalo 



# Tohle jsem vypnul proto to je odkomentované je to pro tlačítko

  #if BUTTON.value() == BUTTON_PRESS:
           # print("This is countdown")
            #count_down_mode()
            #NEOPIXEL_SECONDS.fill((0, 0, 0))
            #light_alphas_timer((35, 51, 70))


            #while True:
             #   for color in ((0, 0, 0), COLOR_OF_BORDER_TIMER):
              #      NEOPIXEL_SECONDS.fill(color)
               #     NEOPIXEL_SECONDS.write()
                #    sleep(0.5)

                #if BUTTON.value() == BUTTON_PRESS:
                 #   sleep(0.1)
                  #  break
           # break

# Jestli to někdo dočetl až sem tak klobouk dolů
