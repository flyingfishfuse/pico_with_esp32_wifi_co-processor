# SPDX-FileCopyrightText: 2019 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

################################
# Internal
################################
import board
import busio
from time import sleep
from machine import Pin
from digitalio import DigitalInOut

################################
# MQTT
################################
from mqtt_manager import MQTTManager
from adafruit_io.adafruit_io import IO_MQTT
import adafruit_minimqtt.adafruit_minimqtt as MQTT

################################
# communications
################################
# spi
from adafruit_esp32spi import adafruit_esp32spi
from adafruit_esp32spi import adafruit_esp32spi_wifimanager
# http / sockets
from adafruit_requests import adafruit_requests as requests
import adafruit_esp32spi.adafruit_esp32spi_socket as socket


################################
# Project imports
# e.g. module/sensor definitions
################################
from config import Config
from ssd1306_oled import SSD1306


###############################################################################
# REPRESENTATION OF PICO MODULE
###############################################################################   
class Pico:
    def __init__(self,
                 config:Config,
                 mqtt_manager:MQTTManager,
                 screen:SSD1306
                 ):
        '''
        UNFINISHED
        metaclass to keep pico in scope
            pretty much a tiny wrapper for "board"

        Defines all pin connections to other modules
        These modules are to be given descriptive names for readability

            wifi module prefix : wifi_esp32_
        
            sensor controller  : sensor_esp32_
        '''
        self.config             = config
        self.mqtt_manager       = mqtt_manager
        # uncomment if using an OLED screen
        self.screen             = screen

        #self.spi_pin_set        = {}
###############################################################################
# PINOUT
###############################################################################   
    def set_wifi_coprocessor_pins(self):
        '''
        This pinout requires you are using an ESP32 flashed with adafruit's

            NINA firmware!!!
        
        the IOxx numbers indicate which pin you use on the ESP32 module
        but ONLY if it is NOT an "airlift" module frfom adafruit

        You can find the corresponding pins by looking at the schematic
        of the esp32 module itself to figure out what IOxx pin on your 
        chosen esp32 module to use

        The ESP32spi has 12 connections. 

        This code was written with a raspberry pi pico as the main controller
        so this code uses the Pico class defined above. You can replace that 
        with your own class, defining its own pins

        This is done so that I can meta my way out of having the file represent
        the board. Treat the class as a pico kind of
        '''
        self.wifi_esp32_sck    = board.GP10
        self.wifi_esp32_miso   = board.GP12
        self.wifi_esp32_mosi   = board.GP11
        self.wifi_esp32_cs     = board.GP13
        self.wifi_esp32_ready  = board.GP14
        self.wifi_esp32_reset  = board.GP15

        #----------------------------------------------------------------------
        # POWER             |
        # Vin 3.3v-5v / 250ma required for WiFi use. (Pin Position 40)
        # 3v Out - upto 50ma for other devices (not used)
        # GND               | Ground (Pin Position 13)
        #          
        ###-----------------------------------------------------###
        #       SPI PINOUT
        ###-----------------------------------------------------###

        # (there has been a movement to change miso/mosi naming)
        # MISO                  = Peripheral Out Controller In (PoCi)
        # MOSI                  = Peripheral In Controller Out (PiCo)
        #-------------------------------------------------------###
        #
        #------- SCK -------------*
        # esp32-S_NINA_firmware = IO18 (hiletgo esp32d gpio18)
        # pico                  = GP10
        #
        #------- MOSI (PICO) (TX) ------------*
        # esp32-S_NINA_firmware = IO23 (hiletgo esp32d gpio23)
        # pico                  = GP11
        #
        #------- MISO (POCI) (RX) ------------*
        # esp32-S_NINA_firmware = IO14 (hiletgo esp32d gpio14)
        # pico                  = GP12
        #
        # this represents the SPI bus connections between esp32 and pico
        self.spi            = busio.SPI(self.wifi_esp32_sck, 
                                        self.wifi_esp32_mosi,
                                        self.wifi_esp32_miso
                                        )
        #
        #
        #------- CS (clock select) ------------*
        # esp32-S_NINA_firmware = IO5 (hiletgo esp32d GPIO5)
        # pico                  = GP13
        self.esp32_cs           = DigitalInOut(self.wifi_esp32_cs)
        #
        #================================
        #   NOTE: in the airlift, BUSY is attached to pin 9 (IO33/A1_5/X32N)
        #   This means that in other modules, if flashed with NINA firmware
        #   BUSY will be on IO33
        #       on hiletgo wroom-esp32S (mislabeled as esp-wroom-32-d)
        #       this is pin33 in the pinout given by hiletgo, meaning GPIO33
        # on other boards, you will need to look at the schematic
        #   
        #------- BUSY ------------
        # esp32-S_NINA_firmware = IO33 
        # pico                  = GP14
        self.esp32_ready    = DigitalInOut(self.wifi_esp32_ready)

        #------- RST ------------ = GP9
        # esp32-S_NINA_firmware = label:  RESET  | MODULE pin 2
        #                         IC pin: chp_pu | PHYSICAL pin 3
        self.esp32_reset        = DigitalInOut(self.wifi_esp32_reset)

        # GP0               = Not needed - used for Bootloading and Blutooth
        # RXI               = Not needed for Wifi - Used for Blutooth 
        # TXO               = Not needed for Wifi - Used for Blutooth

###############################################################################
# SPI
###############################################################################
    def init_spi(self):
        '''
        Initializes SPI bus operations
        '''
        #ESP32 Setup on Pico:
        self.esp_spi_bus      = adafruit_esp32spi.ESP_SPIcontrol(self.spi, 
                                                    self.esp32_cs, 
                                                    self.esp32_ready, 
                                                    self.esp32_reset
                                                    )

    def get_spi_pins(self)->dict :
        '''
        UNFINISHED, possibly unneeded
        returns dict of spi pinout on the pico

        be sure to label these properly, dont get confused like me
        '''
        set_of_things = {
            "wifi_esp32_sck"   :self.wifi_esp32_sck,
            "wifi_esp32_miso"  :self.wifi_esp32_miso,
            "wifi_esp32_mosi"  :self.wifi_esp32_mosi,
            "wifi_esp32_cs"    :self.wifi_esp32_cs,
            "wifi_esp32_ready" :self.wifi_esp32_ready,
        }
        return set_of_things

###############################################################################
# MQTT operations
###############################################################################
    def init_mqtt(self):
        '''
        initializes an mqtt client
        '''
        MQTT.set_socket(socket, self.esp)

    def set_mqtt_secret(self,mqtt_secret:dict):
        '''
        Performs auth setup by getting secrets from either
        supplied parameter or config class

        If mqtt_secret is not supplied as parameter, will use config
                
        defaults to my test network credentials if no parameter given
        '''
        # must try to validate auth creds a little more
        if mqtt_secret is not None and len(mqtt_secret) == 2:
            for each in mqtt_secret:
                setattr(self,each,mqtt_secret.get(each))
            #self.mqtt_secret = mqtt_secret
        # defaults to my test network credentials
        else:
            self.mqtt_secret = {
                'mqtt_username' : self.config.mqtt_username,
                'mqtt_key' : self.config.mqtt_key
                }

    def init_mqtt_client(self):#,mqtt_secret):
        '''
        Initialize a new MQTT Client object
        must provide authentication credentials as dict
        e.g :
        {
            'username' : '"mqtt_service_username"',
            'key' : 'mqtt_service_key'
        }
        '''
        # old code, refactoring out
        #self.set_mqtt_secret(mqtt_secret)
        self.mqtt_client = MQTT.MQTT(
            broker=self.mqtt_manager.broker,
            port=self.mqtt_manager.port,
            
            username=self.mqtt_username,
            password=self.mqtt_key

            # old code, refactoring out
            #username=self.mqtt_secret["username"],
            #password=self.mqtt_secret["key"],
        )
        # Initialize an Adafruit IO MQTT Client
        io = IO_MQTT(self.mqtt_client)

        # Connect the callback methods defined above to Adafruit IO
        io.on_connect = self.mqtt_manager.connected
        io.on_disconnect = self.mqtt_manager.disconnected
        io.on_subscribe = self.mqtt_manager.subscribe
