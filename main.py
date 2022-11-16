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


###############################################################################
# operations functions
###############################################################################
def init_communications(pico:Pico):
    # establish an MQTT connection on the pico
    pico.init_mqtt()
    
    # setup the authorization credentials for mqtt
    pico.set_mqtt_secret({
        pico.mqtt_manager.mqtt_username, #"username":"username",
        pico.mqtt_manager.mqtt_passkey   #"key":"abc123password321cba"
    })
    
    # initialize an mqtt client
    pico.init_mqtt_client()#{
    #    pico.mqtt_manager.mqtt_username, #"username":"username",
    #    pico.mqtt_manager.mqtt_passkey   #"key":"abc123password321cba"
    #})
###############################################################################
# MAIN LOOP
###############################################################################   
if __name__ == "__main__":

# initialization step 1
# setup devices

    #create config for setting auth and endpoints
    new_config = Config()
    # if your WLAN SSID differs from my test network setup, you might want to change your
    # ssid and password here
    # same with adafruit creds
    new_config.ssid = "Other Network"
    # but that was just an example, this is going to run on my network so I am going to change the name back!
    new_config.ssid = "Untrusted Network"

    # create new screen manager
    # TODO: add config params to SSD1306().__init__
    new_screen = SSD1306()

    # create new wifi manager
    #new_wifi_manager = Esp32WifiDevice()
    # create mqtt manager class
    # pass it the config so it knows whats up
    new_mqtt_manager = MQTTManager(new_config)
    # create wrapper/reference for main board
    # with configuration, mqtt, and screen managers
    pico = Pico(new_config,
                new_mqtt_manager,
                new_screen,
                )
    # initialize the pins used for the wifi co-processor
    pico.set_wifi_coprocessor_pins()

    # create new wifi manager class, passing it the 
    # spi bus connection for bidirectional comms
    # and the config for configuration
    esp_device = Esp32WifiDevice(pico.esp_spi_bus,new_config)

    # establish communications between pico and esp32
    esp_device.init_spi()
    esp_device.init_wifi()

# initialization step 2
# connect to network
    # connect
    esp_device.connect_to_AP(esp_device.secrets)
    
    ## display IP addr
    esp_device.ip()


# initialization step 3
# establish communications
    
    init_communications(pico)

    # test 1
    # retrieve text resource
    esp_device.get_text(esp_device.TEXT_URL)
    
    # test 23
    # retrieve JSON resource
    esp_device.get_json(esp_device.JSON_URL)


    # loop the main operations
        # all you have to do is:
        # config.debug = False
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
            esp_device.check_wifi_reset_if_bad()
