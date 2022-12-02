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
import traceback,sys
def errorlogger(e, exception:Exception, message:str):
    """
    prints line number and traceback
    TODO: save stack trace to error log
            only print linenumber and function failure
    """
    #exc_type, exc_value, exc_tb = sys.exc_info()
    #trace = traceback.TracebackException(exc_type, exc_value, exc_tb)
    print(message)
    traceback.format_exception(None, exception, None)
    #lineno = 'LINE NUMBER : ' + str(exc_tb.tb_lineno)
    #print(
    #    message+"\n [-] "+lineno+"\n [-] "+''.join(trace.format_exception_only()) +"\n"
    #    )
        
if __name__ == "__main__":

# initialization step 1
# setup devices
    #try:
    #create config for setting auth and endpoints
    new_config = Config(ssid,password,adafruit_io_username,adafruit_io_api_key)
    #except Exception as e:
    #    errorlogger(e, "[-] FAILED!")
    

    # create new screen manager
    # pass configuration for configuration
    try:
        new_screen = SSD1306(new_config,oled_sda,oled_scl,oled_reset)
    except Exception as e:
        errorlogger(e, "[-] OLED init FAILED!")

    # and set the pinout
    ## DEPRECATED
    #try:
        #new_screen.setpins(oled_sda,oled_scl,oled_reset)
    #except Exception as e:
    #    errorlogger(e, "[-] OLED setpins FAILED!")

    # AFTER setting the pinout, init I2C
    #try:
    #    new_screen.init_I2C()
    #except Exception as e:
    #    errorlogger(e, "[-] OLED init i2c FAILED!")
    
    # initialize display
    # TODO: move this to internal function
    #try:
    #    new_screen.set_display()
    #except Exception as e:
    #    errorlogger(e, "[-] set_display FAILED!")

    # show the REPL
    try:
        new_screen.show_terminal()
    except Exception as e:
        errorlogger(e, "[-] show terminal FAILED!")

    # create wrapper/reference for main board
    # with configuration, mqtt, and screen managers
    try:
        pico = Pico(new_config)#,new_screen)
    except Exception as e:
        errorlogger(e, "[-] Pico module creation FAILED!")

    # initialize the pins used for the wifi co-processor
    try:
        pico.set_wifi_coprocessor_pins(wifi_esp32_sck,wifi_esp32_miso,wifi_esp32_mosi,
                                      wifi_esp32_cs,wifi_esp32_ready,wifi_esp32_reset)
    except Exception as e:
        errorlogger(e, "[-] set_wifi_coprocessor_pins FAILED!")

    # initialize SPI bus and make reference to pass along to other things
    pico.init_spi()
    esp_spi_bus = pico.esp_spi_bus

    # create mqtt manager class
    # pass it the config so it knows whats up
    #try:
    new_mqtt_manager = MQTTManager(new_config)
    #except Exception as e:
    #    errorlogger(e, "[-] mqtt manager init FAILED!")
    
    # init the internal mqtt connection
    new_mqtt_manager.init_mqtt(esp_spi_bus=esp_spi_bus)
    
    try:
    # initialize an mqtt client
        new_mqtt_manager.init_mqtt_client()
    except Exception as e:
        errorlogger(e, "[-] mqtt client init FAILED!")


    # create new wifi manager class, passing it the 
    # spi bus connection for bidirectional comms
    # and the config for configuration
    try:
        print("[+] Creating Esp32WifiDevice()")
        esp_device = Esp32WifiDevice(esp_spi_bus,new_config)
    except Exception as e:
        errorlogger(e, "[-] creation of ESP32 wifi module FAILED!")

    # establish communications between pico and esp32
    #try:
    #    print("[+] Initializing wifi co-processor spi")
    #    esp_device.init_spi()
    #except Exception as e:
    #    errorlogger(e, "[-] FAILED!")

    # init wifi ops on the esp32, feeding the data into the SPI
    # pipeline shared between pico and esp32
    try:
        print("[+] Initializing Wifi Operations")
        esp_device.init_wifi()
    except Exception as e:
        errorlogger(e, "[-] WIFI operation initialization FAILED!")

# initialization step 2
# connect to network
    # connect
    try:
        print(f"[+] Connecting to Access Point with {esp_device.secrets}")
        esp_device.connect_to_AP(esp_device.secrets)
    except Exception as e:
        errorlogger(e, "[-] Connecting to Access Point FAILED!")
    
    ## display IP addr
    try:
        print(f"[+] Device IP {esp_device.ip()}")
        #esp_device.ip()
    except Exception as e:
        print("[-] Device IP FAILED!")


# initialization step 3
# establish communications
    
    #init_mqtt(pico)

    # test 1
    # retrieve text resource
    try:
        esp_device.get_text(esp_device.TEXT_URL)
    except Exception as e:
        errorlogger(e, "[-] FAILED!")
    
    # test 23
    # retrieve JSON resource
    try:
        esp_device.get_json(esp_device.JSON_URL)
    except Exception as e:
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
    except Exception as e:
        print("[-] FAILED!")
