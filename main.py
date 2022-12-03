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
import traceback
from util import errorlogger
from config import Config
from pico_code import Pico
from ssd1306_oled import SSD1306
from mqtt_manager import MQTTManager
from esp32_wifi_coprocessor import Esp32WifiDevice

from adafruit_esp32spi import adafruit_esp32spi

from secrets import ssid,password,adafruit_io_username,adafruit_io_api_key
from pinout import oled_sda,oled_scl,oled_reset,wifi_esp32_sck,wifi_esp32_miso
from pinout import wifi_esp32_mosi, wifi_esp32_cs,wifi_esp32_ready,wifi_esp32_reset
###############################################################################
# MAIN LOOP
############################################################################### 

        
if __name__ == "__main__":
###############################################################################
# initialization step 1
# setup devices
###############################################################################


    #######################################
    # CONFIG
    #######################################
    try:
        # create config for setting auth and endpoints 
        new_config = Config(ssid,password,adafruit_io_username,adafruit_io_api_key)
    except Exception as e:
        errorlogger(e, "[-] Config init FAILED!")
    
    #######################################
    # PICO
    #######################################
    # create wrapper/reference for main board
    try:
        pico = Pico(new_config)
    except Exception as e:
        errorlogger(e, "[-] Pico module creation FAILED!")

    
    #######################################
    # PICO WIFI PINOUT
    #######################################
    # initialize the pins used for the wifi co-processor
    try:
        pico.set_wifi_coprocessor_pins(wifi_esp32_sck,wifi_esp32_miso,wifi_esp32_mosi,
                                      wifi_esp32_cs,wifi_esp32_ready,wifi_esp32_reset)
    except Exception as e:
        errorlogger(e, "[-] PICO WIFI PINOUT SETUP FAILED!")

    #######################################
    # PICO SPI BUS
    #######################################
    # initialize SPI bus and make reference to pass along to other things
    try:
        print("[+] Setting up SPI bus")
        esp_spi_bus = adafruit_esp32spi.ESP_SPIcontrol(pico.spi, 
                                                    pico.esp32_cs, 
                                                    pico.esp32_ready, 
                                                    pico.esp32_reset
                                                    )
    #esp_spi_bus = pico.esp_spi_bus
    except Exception as e:
        errorlogger(e, "[-] shit FAILED yo!")


    #######################################
    # WIFI (pretend its on the esp32)
    #######################################
    # create new wifi manager class, passing it the 
    # spi bus connection for bidirectional comms
    # and the config for configuration
    try:
        print("[+] Creating Esp32WifiDevice()")
        esp_device = Esp32WifiDevice(esp_spi_bus,new_config)
    except Exception as e:
        errorlogger(e, "[-] creation of ESP32 wifi module FAILED!")

    #######################################
    # authentication
    #######################################
    try:
        print("[+] Adding WLAN credentials to esp32 device")
        esp_device.wlan_authentication()
    except Exception as e:
        errorlogger(e, "[+] Failed to add WLAN credentials to device")
    #######################################
    # initialize wifi on esp32
    #######################################
    # init wifi ops on the esp32, feeding the data into the SPI
    # pipeline shared between pico and esp32
    try:
        print("[+] Initializing Wifi Operations")
        esp_device.init_wifi()
    except Exception as e:
        errorlogger(e, "[-] WIFI operation initialization FAILED!")
    
    #######################################
    # connect socket to SPI bus
    #######################################
    try:
        print("[+] connecting SPI bus to socket resource")
        esp_device.set_socket_to_SPI()
    except Exception as e:
        errorlogger(e, "[-] SPI to socket bus initialization FAILED!")


###############################################################################
# initialization step 2
# connect to network
###############################################################################

    #######################################
    # test adafruit connect()
    #######################################
    try:
        print("[+] connecting to AP")
        esp_device.wifi.connect()
    except Exception as e:
        print(traceback.format_exception(None, e, None))
        

    #######################################
    # connect to wlan
    #######################################
    try:
        print(f"[+] Connecting to Access Point with {esp_device.secrets}")
        esp_device.connect_to_AP(esp_device.secrets)
    except Exception as e:
        errorlogger(e, "[-] Connecting to Access Point FAILED!")

    #######################################
    # display IP addr
    ####################################### 
    try:
        print(f"[+] Device IP {esp_device.ip()}")
        #esp_device.ip()
    except Exception as e:
        errorlogger(e, "[-] Device IP FAILED!")

###############################################################################
# initialization step 3
# establish communications
###############################################################################

#######################################
# MQTT
#######################################
    
    # create mqtt manager class
    # pass it the config so it knows whats up
    #try:
    new_mqtt_manager = MQTTManager(new_config)
    #except Exception as e:
    #    errorlogger(e, "[-] mqtt manager init FAILED!")
    
    # init the internal mqtt connection
    new_mqtt_manager.init_mqtt(esp_spi_bus=esp_spi_bus)

    #######################################
    # create mqtt client
    #######################################
    try:
    # initialize an mqtt client
        new_mqtt_manager.init_mqtt_client()
    except Exception as e:
        errorlogger(e, "[-] mqtt client init FAILED!")


###############################################################################
# TESTING
###############################################################################
    #######################################
    # get text from interweb
    ####################################### 
    # test 1
    # retrieve text resource
    try:
        esp_device.get_text(esp_device.TEXT_URL)
    except Exception as e:
        errorlogger(e, "[-] FAILED!")
    
    #######################################
    # get JSON off interwebz
    ####################################### 
    # test 23
    # retrieve JSON resource
    try:
        esp_device.get_json(esp_device.JSON_URL)
    except Exception as e:
        print("[-] FAILED!")


    #######################################
    # FULL TEST
    ####################################### 
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
    except Exception as e:
        errorlogger(e, "[-] FAILED!")
