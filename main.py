# SPDX-FileCopyrightText: 2019 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# main project license is GPLv3

# if you steal my code and sell things built with it without providing
# the modified source bad things will happen

# frilled lizards and leopard geckos will ride ninja cats into battle
# also laweyers , lots of lawyers, actually... mostly lawyers

################################
# Project imports
# e.g. module/sensor definitions
################################
from config import Config
from pico_code import Pico
from ssd1306_oled import SSD1306
from mqtt_manager import MQTTManager
from esp32_wifi_coprocessor import Esp32WifiDevice

from secrets import ssid,password,adafruit_io_username,adafruit_io_api_key
from pinout import oled_sda,oled_scl,oled_reset,wifi_esp32_sck,wifi_esp32_miso
from pinout import wifi_esp32_mosi, wifi_esp32_cs,wifi_esp32_ready,wifi_esp32_reset
###############################################################################
# MAIN LOOP
###############################################################################   
if __name__ == "__main__":

# initialization step 1
# setup devices
    try:
    #create config for setting auth and endpoints
        print("[+] Creating new Config")
        new_config = Config(
                            ssid,
                            password,
                            adafruit_io_username,
                            adafruit_io_api_key
                            )
        print(new_config)
    except:
        print("[-] FAILED!")
    

    # create new screen manager
    # pass configuration for configuration
    try:
        print("[+] Creating new screen")
        new_screen = SSD1306(new_config)
    except:
        print("[-] FAILED!")

    # and set the pinout
    try:
        print("[+] Setting OLED pins")
        new_screen.setpins(oled_sda,oled_scl,oled_reset)
    except:
        print("[-] FAILED!")

    # AFTER setting the pinout, init I2C
    try:
        print("[+] Initializing OLED i2c")
        new_screen.init_I2C()
    except:
        print("[-] FAILED!")
    
    # initialize display
    # TODO: move this to internal function
    try:
        print("[+] Setting OLED display")
        new_screen.set_display()
    except:
        print("[-] FAILED!")

    # show the REPL
    try:
        print("[+] Dropping to REPL")
        new_screen.show_terminal()
    except:
        print("[-] FAILED!")

    # create mqtt manager class
    # pass it the config so it knows whats up
    try:
        print("[+] Creating new MQTT manager")
        new_mqtt_manager = MQTTManager(new_config)
    except:
        print("[-] FAILED!")

    # create wrapper/reference for main board
    # with configuration, mqtt, and screen managers
    try:
        print("[+] Creating Pico() class with mqtt and screen")
        pico = Pico(new_config,
                    new_mqtt_manager,
                    new_screen,
                    )
    except:
        print("[-] FAILED!")

    # initialize the pins used for the wifi co-processor
    try:
        print("[+] Setting wifi co-processor pins ")
        pico.set_wifi_coprocessor_pins(
                                      wifi_esp32_sck,
                                      wifi_esp32_miso,
                                      wifi_esp32_mosi,
                                      wifi_esp32_cs,
                                      wifi_esp32_ready,
                                      wifi_esp32_reset
                                      )
    except:
        print("[-] FAILED!")

    # make reference to esp spi bus
    esp_spi_bus = pico.esp_spi_bus

    # create new wifi manager class, passing it the 
    # spi bus connection for bidirectional comms
    # and the config for configuration
    try:
        print("[+] Creating Esp32WifiDevice()")
        esp_device = Esp32WifiDevice(esp_spi_bus,new_config)
    except:
        print("[-] FAILED!")

    # establish communications between pico and esp32
    try:
        print("[+] Initializing wifi co-processor spi")
        esp_device.init_spi()
    except:
        print("[-] FAILED!")

    try:
        print("[+] Initializing Wifi Operations")
        esp_device.init_wifi()
    except:
        print("[-] FAILED!")

# initialization step 2
# connect to network
    # connect
    try:
        print(f"[+] Connecting to Access Point with {esp_device.secrets}")
        esp_device.connect_to_AP(esp_device.secrets)
    except:
        print("[-] FAILED!")
    
    ## display IP addr
    try:
        print(f"[+] Device IP {esp_device.ip()}")
        #esp_device.ip()
    except:
        print("[-] FAILED!")


# initialization step 3
# establish communications
    
    #init_mqtt(pico)

    # test 1
    # retrieve text resource
    try:
        print("[+] ")
        esp_device.get_text(esp_device.TEXT_URL)
    except:
        print("[-] FAILED!")
    
    # test 23
    # retrieve JSON resource
    try:
        print("[+] ")
        esp_device.get_json(esp_device.JSON_URL)
    except:
        print("[-] FAILED!")


    # loop the main operations
        # all you have to do is:
        # config.debug = False
    try:
        if new_config.debug == True:
            while True:
                esp_device.check_wifi_reset_if_bad()
                esp_device.display_scan_results()
                esp_device.http_request()
                print(esp_device.http_request_result)
                esp_device.get_text()
                esp_device.get_json()
                esp_device.get_IP_by_hostname()

    # not debugging, everything is setup properly
        elif new_config.debug == False:
            while True:
                print("[+] ")
                esp_device.check_wifi_reset_if_bad()
    except:
        print("[-] FAILED!")
