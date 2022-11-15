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
# OLED display
################################
import adafruit_displayio_ssd1306


################################
# project imports
################################
from config import Config



###############################################################################
# REPRESENTATION OF PICO MODULE
###############################################################################   
class Pico:
    def __init__(self,config:Config,mqtt_manager:MQTTManager):
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
###############################################################################
# PINOUT
###############################################################################   
    def set_wifi_coprocessor_pins(self):
        self.wifi_esp32_sck    = board.GP10
        self.wifi_esp32_miso   = board.GP12
        self.wifi_esp32_mosi   = board.GP11
        self.wifi_esp32_cs     = board.GP13
        self.wifi_esp32_ready  = board.GP14
        self.wifi_esp32_reset  = board.GP15
###############################################################################
# SPI
###############################################################################   
    def set_spi(self):
        '''
        UNFINISHED
        sets spi pinout on the pico
        '''
        set_of_things = {
            "sck"   :self.wifi_esp32_sck,
            "miso"  :self.wifi_esp32_miso,
            "mosi"  :self.wifi_esp32_mosi,
            "cs"    :self.wifi_esp32_cs,
            "ready" :self.wifi_esp32_ready,
        }
        

    def get_spi(self):
        '''
        UNFINISHED
        Describes SPI pinout on the pico
        '''
        # Initialize MQTT interface with the esp interface

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


###############################################################################
# REPRESENTATION OF ss1306 OLED display
#   Attached to pico
###############################################################################   
class SS1306:
    def __init__(self):
        '''
        This class represents an OLED module I have had for years 
        now but never really used

        The SS1306, looks neat in low light. Visible in sunlight also.
        '''
###############################################################################
# pinout
###############################################################################   

    def setpins(self):
        '''
        pinout for module to pico via i2c
        '''
        #---------------- SDA ----------------*
        # ss1306 OLED           = SDA 
        # pico                  = GP18, <I2C1 SDA> , physical pin 24
        self.i2c_sda = board.GP18
        #
        #----------------SCL -----------------*
        # ss1306 OLED           = SCL 
        # pico                  = GP19, <I2C1 SCL> , physical pin 25
        self.i2c_sda = board.GP19

    def init_I2C(self):
        '''
        initializes I2C communications between pico and OLED module
        '''
        self.i2c = busio.I2C(scl=board.GP5, sda=board.GP4) # This RPi Pico way to call I2C<br>

    def test_print(self):
        """
        prints a message in a outline for testing
        """
###############################################################################
# REPRESENTATION OF ESP32 WIFI CO-PROCESSOR
###############################################################################   
class Esp32WifiDevice:
    def __init__(self, controller:Pico):
        '''
        '''
        self.pico = controller
        # slot to store html from a webrequest
        self.requestedpage = {}
        self.ip = self.__ip__()
        #self.init_spi()
        #self.init_wifi()

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
###############################################################################
# PINOUT
###############################################################################   
    def set_pins(self):
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
        self.spi            = busio.SPI(self.pico.wifi_esp32_sck, 
                                        self.pico.wifi_esp32_mosi,
                                        self.pico.wifi_esp32_miso
                                        )
        #
        #
        #------- CS (clock select) ------------*
        # esp32-S_NINA_firmware = IO5 (hiletgo esp32d GPIO5)
        # pico                  = GP13
        self.esp32_cs           = DigitalInOut(self.pico.wifi_esp32_cs)
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
        self.esp32_ready    = DigitalInOut(self.pico.wifi_esp32_ready)

        #------- RST ------------ = GP9
        # esp32-S_NINA_firmware = label:  RESET  | MODULE pin 2
        #                         IC pin: chp_pu | PHYSICAL pin 3
        self.esp32_reset        = DigitalInOut(self.pico.wifi_esp32_reset)

        # GP0               = Not needed - used for Bootloading and Blutooth
        # RXI               = Not needed for Wifi - Used for Blutooth 
        # TXO               = Not needed for Wifi - Used for Blutooth

###############################################################################
# SPI OPERATIONS
###############################################################################   
    def init_spi(self):
        '''
        Initializes SPI bus operations
        '''
        #ESP32 Setup on Pico:
        self.esp      = adafruit_esp32spi.ESP_SPIcontrol(self.spi, 
                                                    self.esp32_cs, 
                                                    self.esp32_ready, 
                                                    self.esp32_reset
                                                    )

###############################################################################
# WIFI OPERATIONS
###############################################################################   
    def init_wifi(self):
        '''
        Initializes esp32 wifi managment
        '''
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

    def check_wifi_reset_if_bad(self):#esp32thing(self):
        try:
            s = self.esp.status
            if s == 0:
                self.wifi.connect()
        except RuntimeError:
            self.wifi.reset()    

    def connect_to_AP(self, secrets):
        '''
        Connects to  AP with given credentials

        format of credentials as parameter is as follows:
        
        secrets = {
            'ssid' : 'Untrusted Network',
            'password' : 'Whatapassword1!'
            }
        '''
        print("[+] Connecting to AP...")
        while not self.esp.is_connected:
            try:
                # ssid and password are in config, config is given to the pico
                self.esp.connect_AP(
                                    self.pico.config.ssid,
                                    self.pico.config.password
                                    )#secrets["ssid"], secrets["password"])
            except OSError as e:
                print("[-] Could not connect to AP, retrying: ", e)
                continue
        
        print("[+] Connected to", str(self.esp.ssid, "utf-8"), "\tRSSI:", self.esp.rssi)
        print("[+] My IP address is", self.esp.pretty_ip(self.esp.ip_address))

    def http_request(self,uri="adafruit.com"):
        '''
        Requests a resource via an http request
        stores return data in 
            self.http_request_result
        '''
        print(f"[+ requesting http resource {uri}]")
        self.http_request_result = self.esp.get_host_by_name(uri)
 
    def get_IP_by_hostname(self,uri="adafruit.com"):
        '''
        obtains IP of given hostname
        stores return data in 
            self.host_lookup_return
        '''
        host_lookpup = self.esp.get_host_by_name(uri)
        self.host_lookup_return = host_lookpup
        print(
            "[+] IP lookup adafruit.com: %s" % self.esp.pretty_ip(self.host_lookup_return)
        )

    def ping(self, uri="google.com"):
        '''
        issues ICMP ping to given resource
        '''
        ping_result = self.esp.ping(uri)
        print(f"[+] Ping {uri} {ping_result} ms")

    def get_text(self, uri):
        '''

        '''
        print(f"[+] retreiving text from {uri}")
        result = requests.get(uri)
        print("-" * 40)
        print(result.text)
        print("-" * 40)
        result.close()

    def get_json(self,uri):
        '''

        '''
        print(f"[+] retreiving json from {uri}")
        result = requests.get(uri)
        print("-" * 40)
        print(result.json())
        print("-" * 40)
        result.close()

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

    # create mqtt manager class
    new_mqtt_manager = MQTTManager()
    # create wrapper/reference for main board
    # with configuration
    pico = Pico(new_config,new_mqtt_manager)
    # initialize the pins used for the wifi co-processor
    pico.set_wifi_coprocessor_pins()

    # create new wifi manager class
    esp_device = Esp32WifiDevice(pico)

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
