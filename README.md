# overview
    This is a more robust implementation of the wifi coprocessor setup using 
    a circuitpython enabled microprocessor in combination with an esp32 for WLAN
    functionality using SPI bridging between devices

    This also contains code for interacting with the system via a 4x4 keypad and oled

    I am building this for the monitoring of lizard and bug farm enclosures, with expansion 
    into game bird hatching chambers and garden monitoring systems for the enabling of self sufficient
    suburban farming


    The usual thing I have seen in circuitpython code is having the file be representation of the
    modules, everything is mashed together.

    This is not pythonic

    This library allows you to treat each class as the module it purports to be, the Pico() class represents an rp2040 device
    same with the esp/ssd1306/etc.

    This requires you are using an ESP32 flashed with adafruit's NINA firmware!!!
    https://github.com/adafruit/nina-fw
        
    the IOxx numbers indicate which pin you use on the ESP32 module but ONLY if it is NOT an "airlift" module from adafruit
        
    You can find the corresponding pins by looking at the schematic of the esp32 module itself to figure out what IOxx pin on your 
    chosen esp32 module to use

    This code was written with a raspberry pi pico as the main controller so this code uses the Pico class defined above. You can replace that 
    with your own class, defining its own pins
    
# unrelated notes on security as public service announcement for the masses
    
    Don't just use code people wrote without reading it, look for syscals, network calls, URI's leading to random places owned by china or iran or russia, obfuscated code, muckery with your OS internals... the list goes on and on.
    Hackers like skids, they are useful idiots, dont be a skid, learn to read the code you use and dont just run any script you find because it sounds like it's what you need.
    Attacks have been focused more and more frequently on the tooling and background workings of softwares, it's always been a vector but now its almost ubiquitous.



# components
    
    Config()
        stores global configuration variables, for most people this is all you need to change around

    Pico()
        representation of a pico main board

    ESP32WifiDevice()
        ditto

    SSD1306()
        ditto

    MQTTManagment()
        put mqtt interactions here
 

# >`secrets.py`
create a file named "secrets.py" and put the following code in it, dont forget to put your information into that file

```python
adafruit_io_username    = ""
adafruit_io_api_key     = ""
ssid                    = ""
password                = ''
```
        
# how to use

    main.py has an example of the most basic implementation


# MQTT OVERVIEW

```yaml
subscriber  : retrieves messages
broker      : relays messages
publisher   : sends messages
---  
raspberry pi pico:
    Broker:
        of:
            - sensor temperature
            - sensor humidity
        from:
            - sensor_esp32 (1 through n)
        to:
            - internet -> phone
            - WLAN -> phone
            - display_esp32 (planned)
    Publisher:
        of: 
            - diagnostics
        from:
            - raspberry pi pico (this)
        to:
            - WLAN -> phone
            - internet -> phone
    Subscriber:
        of:
            -
        from:
            -
---
ESP32 with attached sensors:
    Publisher:
        of:
            - sensor temperature
            - sensor humidity
        from:
            - attached sensors (1 through n)
        to:
            - internet -> phone
            - WLAN -> phone
            - display_esp32 (planned)
```
