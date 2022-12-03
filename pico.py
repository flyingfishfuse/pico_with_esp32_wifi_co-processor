# SPDX-FileCopyrightText: 2019 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

################################
# Internal
################################
import busio
from digitalio import DigitalInOut

################################
# communications
################################
# spi
from adafruit_esp32spi import adafruit_esp32spi
#from adafruit_esp32spi import adafruit_esp32spi_wifimanager
# http / sockets
#import adafruit_requests as requests
#import adafruit_esp32spi.adafruit_esp32spi_socket as socket


################################
# Project imports
# e.g. module/sensor definitions
################################
from config import Config
from ssd1306_oled import SSD1306
from mqtt_manager import MQTTManager


###############################################################################
# REPRESENTATION OF PICO MODULE
###############################################################################   
class Pico:
    def __init__(self,
                 config:Config,
                 #mqtt_manager:MQTTManager,
                 #screen:SSD1306
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
        print("[+] Creating Pico() class")
        self.config             = config
        #self.mqtt_manager       = mqtt_manager
        # uncomment if using an OLED screen
        #self.screen             = screen

        #self.spi_pin_set        = {}

###############################################################################
# PINOUT
###############################################################################   
    def set_wifi_coprocessor_pins(self,
                                  wifi_esp32_sck,
                                  wifi_esp32_miso,
                                  wifi_esp32_mosi,
                                  wifi_esp32_cs,
                                  wifi_esp32_ready,
                                  wifi_esp32_reset
                                  ):
        """This pinout requires you are using an ESP32 flashed with adafruit's

            NINA firmware!!!
        
        the IOxx numbers indicate which pin you use on the ESP32 module
        but ONLY if it is NOT an "airlift" module frfom adafruit

        You can find the corresponding pins by looking at the schematic
        of the esp32 module itself to figure out what IOxx pin on your 
        chosen esp32 module to use but in general IOxx directly translates
        to GPIOxx

        ergo, IO05 maps directly to GPIO5 and so on

        The ESP32spi has 12 connections. 

        This code was written with a raspberry pi pico as the main controller
        so this code uses the Pico class defined above. You can replace that 
        with your own class, defining its own pins

        This is done so that I can meta my way out of having the file represent
        the board. Treat this class as a pico, kind of. All operations in
        main.py/code.py are going to be running on the pico which will function
        as an "orchestrator"


        Args:
            wifi_esp32_sck (board.GPIO): _description_
            wifi_esp32_miso (_type_): _description_
            wifi_esp32_mosi (_type_): _description_
            wifi_esp32_cs (_type_): _description_
            wifi_esp32_ready (_type_): _description_
            wifi_esp32_reset (_type_): _description_
        """
        print("[+] Setting wifi co-processor pins ")
        self.wifi_esp32_sck    = wifi_esp32_sck
        self.wifi_esp32_miso   = wifi_esp32_miso
        self.wifi_esp32_mosi   = wifi_esp32_mosi
        self.wifi_esp32_cs     = wifi_esp32_cs
        self.wifi_esp32_ready  = wifi_esp32_ready
        self.wifi_esp32_reset  = wifi_esp32_reset

        # this represents the SPI bus connections between esp32 and pico
        self.spi            = busio.SPI(self.wifi_esp32_sck, 
                                        self.wifi_esp32_mosi,
                                        self.wifi_esp32_miso
                                        )

        self.esp32_cs           = DigitalInOut(self.wifi_esp32_cs)

        self.esp32_ready    = DigitalInOut(self.wifi_esp32_ready)

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

###############################################################################
# UART
###############################################################################
    def init_uart(self,tx,rx,baudrate=9600):
        """Initializes UART bus on the pico

        Args:
            tx (board.TX): Transmit
            rx (board.RX): Receive
            baudrate (int, optional): baudrate of UART line. Defaults to 9600.
        """
        self.uart = busio.UART(tx, rx, baudrate=baudrate)

    def set_mqtt_manager(self,new_manager):
        """_summary_

        Args:
            new_manager (MQTTManager): an instance of MQTTManager class
        """
        self.mqtt_manager = new_manager

    def set_screen(self,new_oled):
        """sets screen to use for pico as display

        Args:
            new_oled (SSD1306): Instance of SSD1306 class
        """
        self.screen = new_oled
