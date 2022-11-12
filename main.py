# SPDX-FileCopyrightText: 2019 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import board
import busio
from time import sleep
from machine import Pin
from digitalio import DigitalInOut
import adafruit_requests as requests
from adafruit_esp32spi import adafruit_esp32spi
from adafruit_esp32spi import adafruit_esp32spi_wifimanager
import adafruit_esp32spi.adafruit_esp32spi_socket as socket

class Pico:
    def __init__(self):
        '''
        sets up board info for pico
        '''

class Esp32WifiDevice:
    def __init__(self):
        '''
        '''
        # slot to store html from a webrequest
        self.requestedpage
        self.ip = self.__ip__()

    def authentication(self,secrets:dict):
        '''
        WLAN authentication credentials, in most cases you want this in a different
        file so you can exclude any credential leakages when uploading code to a 
        repository. In this case, I have an isolated WLAN specifically for non 
        internet connected wireless devices.

        defaults to my test network credentials if no parameter given
        '''
        # must try to validate auth creds
        if secrets is not None and len(secrets) == 2:
            self.secrets = secrets
        # defaults to my test network credentials
        else:
            self.secrets = {
                'ssid' : 'Untrusted Network',
                'password' : 'Whatapassword1!'
                }

    def set_pins(self):
        '''
        it is necessary to set pins to connections made to other devices
        and parts of the circuit

        This code was written with a raspberry pi pico as the main controller
        so this code uses the Pico class defined above. You can replace that 
        with your own class, defininf its own pins

        This is done so that I can meta my way out of having the file represent
        the board. Treat the class as a pico kind of
        '''
        # PINOUT FROM PICO TO ESP32
        #   The ESP32spi has 12 connections. 
        #   
        #   This pinout guide requires looking at the module schematics
        #   to figure out what IOxx pin on your chosen esp32 module to use
        #----------------------------------------------------------------------
        # POWER             |
        # Vin 3.3v-5v / 250ma required for WiFi use. (Pin Position 40)
        # 3v Out - upto 50ma for other devices (not used)
        # GND               | Ground (Pin Position 13)
        #          
        ###-----------------------------------------------------###
        #       SPI PINOUT
        ###-----------------------------------------------------###

        # (there has been a movment to change miso/mosi naming)
        # MISO              = Peripheral Out Controller In (PoCi)
        # MOSI              = Peripheral In Controller Out (PiCo)
        #-------------------------------------------------------###
        #------- SCK -------------
        # esp32-s_NINA      = IO18 (hiletgo esp32d gpio23)
        # SCK               = GP10 (pico)
        #------- MISO ------------
        # esp32-S_NINA      = IO14 (hiletgo esp32d gpio23)
        # MISO (POCI) (RX)  = GP12 (pico)
        #------- MOSI ------------
        # esp32-S_NINA      = IO23 (hiletgo esp32d gpio23)
        # MOSI (PICO) (TX)  = GP11 (pico)

        self.spi            = busio.SPI(board.GP10, board.GP11, board.GP12)
        #
        #
        # CS                = GP13
        #esp32_cs           = DigitalInOut(board.GP13)
        self.esp32_cs       = DigitalInOut(board.GP13)

        #================================
        #   NOTE: in the airlift, BUSY is attached to pin 9 (IO33/A1_5/X32N)
        #   This means that in other modules, if flashed with NINA firmware
        #   BUSY will be on IO33
        #       on hiletgo wroom-esp32S (mislabeled as esp-wroom-32-d)
        #       this is pin33 in the pinout given by hiletgo, meaning GPIO33
        # on other boards, you will need to look at the schematic
        #   
        # BUSY              = esp32-S IO33 gpio33
        # esp32-S_NINA      = IO33 
        # esp32_ready       = DigitalInOut(board.GP8)
        self.esp32_ready    = DigitalInOut(board.GP14)

        # RST               = GP9
        #esp32_reset        = DigitalInOut(board.GP9)
        self.esp32_reset         = DigitalInOut(board.GP15)

        # GP0               = Not needed - used for Bootloading and Blutooth
        # RXI               = Not needed for Wifi - Used for Blutooth 
        # TXO               = Not needed for Wifi - Used for Blutooth

        #ESP32 Setup on Pico:
        self.esp      = adafruit_esp32spi.ESP_SPIcontrol(self.spi, 
                                                    self.esp32_cs, 
                                                    self.esp32_ready, 
                                                    self.esp32_reset
                                                    )
        self.spi      = busio.SPI(board.GP10, 
                                  board.GP11, 
                                  board.GP12
                                )

        self.wifi     = adafruit_esp32spi_wifimanager.ESPSPI_WiFiManager(self.esp, self.secrets)

        # establishes a socket resource to be made available for the esp32 data
        requests.set_socket(socket, self.esp)

        self.TEXT_URL = "http://wifitest.adafruit.com/testwifi/index.html"
        self.JSON_URL = "http://api.coindesk.com/v1/bpi/currentprice/USD.json"

    def __ip__(self):
        '''
        Returns ip address 
        '''
        try:
            self.ip = print("[+] IPv4 addr: ", self.esp.pretty_ip(self.esp.ip_address))
        except:
            self.ip = "[-] IPv4 addr: N/A - not connected to any network"

    def check_idle(self) -> bool:
        '''
        checks if esp32 is in idle state
        '''
        if self.esp.status == adafruit_esp32spi.WL_IDLE_STATUS:
            print("[+] ESP32 found and in idle mode")
        else:
            print("[+] ESP32 Active")

    def show_esp32_hardware_info(self):
        '''
        displays data about firmware and hardware address
        '''
        print("Firmware vers.", self.esp.firmware_version)
        print("MAC addr:", [hex(i) for i in self.esp.MAC_address])

    def display_scan_results(self):
        '''
        prints data about local APs
        '''
        for ap in self.esp.scan_networks():
            print("\t%s\t\tRSSI: %d" % (str(ap["ssid"], "utf-8"), ap["rssi"]))

    def esp32thing(self):
        try:
            s = self.esp.status
            if s == 0:
                self.wifi.connect()
        except RuntimeError:
            self.wifi.reset()    

    def connect_to_AP(self, secrets):
        '''
        Connects to  AP with given credentials

        format of credentials pass as parameter is as follows:
        
        secrets = {
            'ssid' : 'Untrusted Network',
            'password' : 'Whatapassword1!'
            }
        '''
        print("Connecting to AP...")
        while not self.esp.is_connected:
            try:
                self.esp.connect_AP(secrets["ssid"], secrets["password"])
            except OSError as e:
                print("could not connect to AP, retrying: ", e)
                continue
        print("Connected to", str(self.esp.ssid, "utf-8"), "\tRSSI:", self.esp.rssi)
        print("My IP address is", self.esp.pretty_ip(self.esp.ip_address))

    def http_request(self,uri="adafruit.com"):
        '''
        Requests a resource via an http request
        '''
        self.requestedpage = self.esp.get_host_by_name(uri)
 
    def get_IP_by_hostname(self,uri="adafruit.com"):
        '''
        obtains IP of given hostname
        '''
        print(
            "IP lookup adafruit.com: %s" % self.esp.pretty_ip(self.esp.get_host_by_name(uri))
        )

    def ping(self, uri="google.com"):
        '''
        issues ICMP ping to given resource
        '''
        print("Ping google.com: %d ms" % self.esp.ping(uri))

    def get_text(self, uri):
        '''

        '''
    # self.esp._debug = True
        print("Fetching text from", uri)
        r = requests.get(uri)
        print("-" * 40)
        print(r.text)
        print("-" * 40)
        r.close()

    def get_json(self,uri):
        '''

        '''
        print("Fetching json from", uri)
        r = requests.get(uri)
        print("-" * 40)
        print(r.json())
        print("-" * 40)
        r.close()



if __name__ == "__main__":
    esp_device = Esp32WifiDevice()
    # connect
    esp_device.connect_to_AP(esp_device.secrets)
    ## display IP addr
    esp_device.ip()
    # retrieve text resource
    esp_device.get_text(esp_device.TEXT_URL)
    # retrieve JSON resource
    esp_device.get_json(esp_device.JSON_URL)
