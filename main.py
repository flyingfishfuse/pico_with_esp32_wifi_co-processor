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
import adafruit_minimqtt.adafruit_minimqtt as MQTT
from adafruit_io.adafruit_io import IO_MQTT


# MQTT OVERVIEW

#    bidirectional pipeline
#        subscriber  : retrieves messages
#        broker      : relays messages
#        publisher   : sends messages
#    
#    raspberry pi pico:
#        Broker:
#            of:
#                - sensor temperature
#                - sensor humidity
#            from:
#                - sensor_esp32 (1 through n)
#            to:
#                - internet -> phone
#                - WLAN -> phone
#                - display_esp32 (planned)
#        Publisher:
#            of: 
#                - diagnostics
#            from:
#                - raspberry pi pico (this)
#            to:
#                - WLAN -> phone
#                - internet -> phone
#        Subscriber:
#            of:
#                -
#            from:
#                -
#            to:
#                -
#    ----------------------------------------
#    ESP32 with attached sensors:
#        Publisher:
#            of:
#                - sensor temperature
#                - sensor humidity
#            from:
#                - attached sensors (1 through n)
#            to:
#                - internet -> phone
#                - WLAN -> phone
#                - display_esp32 (planned)
class Config:
    '''
    Config class for holding all your secrets and endpoints
    '''
    def __init__(self):
        '''
        waaat
        '''
        self.ssid           = "Untrusted Network"
        self.password       = 'Whatapassword1!'
        self.aio_username   = 'your_adafruit_io_username_'
        self.aio_key        = 'your_big_huge_super_long_aio_key_'
        self.broker         = 'io.adafruit.com',
        self.port           = '1883'

class Sensors:
    '''
    Possibly unnecessary metaclass for representing the sensors on the esp32
    '''
    
class MQTTManager:
    def __init__(self,config:Config):
        '''
        This class is the handler for all mqtt activities

        It holds the callbacks and the init as well as dial out, dial in
        '''
        # do nothing, user must call init themself
        self.aio_username   = config.aio_username
        self.aio_passkey    = config.aio_key
        self.broker         = config.broker


    def init_mqtt(self):
        '''
        Dials out to adafruit broker
        '''
        # Set your Adafruit IO Username and Key in secrets.py
        # (visit io.adafruit.com if you need to create an account,
        # or if you need your Adafruit IO key.)
        aio_username = self.aio_username
        aio_key = self.aio_passkey

        # original adafruit code stub
        #print("Connecting to %s" % secrets["ssid"])
        #wifi.radio.connect(secrets["ssid"], secrets["password"])
        #print("Connected to %s!" % secrets["ssid"])
        
        ### Feeds ###

        # Setup a feed named 'photocell' for publishing to a feed
        #photocell_feed = self.aio_username + "/feeds/photocell"

        # Setup a feed named 'onoff' for subscribing to changes
        #onoff_feed = self.aio_username + "/feeds/onoff"

    def create_feeds(self,new_feeds:dict):
        '''
        Creates endpoints for publishing and subscribing
        input:
            list_of_feeds = [new_endpoint_name_1','new_endpoint_name_2']
        
        This will be added as class member via setattr()
        output:
            self.new_endpoint_name_1 = "aio_username/feeds/new_endpoint_name_1
        '''
        for each in new_feeds:
            setattr(self,each ,f"{self.aio_username}/feeds/{each}")

    # Define callback methods which are called when events occur
    # pylint: disable=unused-argument, redefined-outer-name
    def connected(client, userdata, flags, rc):
        # This function will be called when the client is connected
        # successfully to the broker.
        print("Connected to Adafruit IO! Listening for topic changes on %s" % onoff_feed)
        # Subscribe to all changes on the onoff_feed.
        client.subscribe(onoff_feed)


    def disconnected(client, userdata, rc):
        # This method is called when the client is disconnected
        print("Disconnected from Adafruit IO!")


    def message(client, topic, message):
        # This method is called when a topic the client is subscribed to
        # has a new message.
        print("New message on topic {0}: {1}".format(topic, message))


class Pico:
    def __init__(self,config:Config):
        '''
        UNFINISHED
        metaclass to keep pico in scope
            pretty much a tiny wrapper for "board"

        Defines all pin connections to other modules
        These modules are to be given descriptive names for readability

            wifi module prefix : wifi_esp32_
        
            sensor controller  : sensor_esp32_
        '''
        self.wifi_esp32_sck    = board.GP10
        self.wifi_esp32_miso   = board.GP12
        self.wifi_esp32_mosi   = board.GP11
        self.wifi_esp32_cs     = board.GP13
        self.wifi_esp32_ready  = board.GP14
        self.wifi_esp32_reset  = board.GP15
    
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
   
    def set_mqtt_secret(self,mqtt_secret:dict):
        '''
        Performs auth setup by getting secrets from either
        supplied parameters or local file
                defaults to my test network credentials if no parameter given
        '''
        # must try to validate auth creds
        if mqtt_secret is not None and len(mqtt_secret) == 2:
            self.mqtt_secret = mqtt_secret
        # defaults to my test network credentials
        else:
            self.mqtt_secret = {
                'username' : '"mqtt_service_username"',
                'key' : 'mqtt_service_key'
                }

    def init_mqtt(self):
        '''
        initializes an mqtt client
        '''
        MQTT.set_socket(socket, self.esp)

    def init_mqtt_client(self,mqtt_secret):
        '''
        Initialize a new MQTT Client object
        must provide authentication credentials as dict
        e.g :
        {
            'username' : '"mqtt_service_username"',
            'key' : 'mqtt_service_key'
        }
        '''
        self.set_mqtt_secret(mqtt_secret)
        self.mqtt_client = MQTT.MQTT(
            broker="io.adafruit.com",
            port=1883,
            username=self.mqtt_secret["username"],
            password=self.mqtt_secret["key"],
        )
        # Initialize an Adafruit IO MQTT Client
        io = IO_MQTT(mqtt_client)

        # Connect the callback methods defined above to Adafruit IO
        io.on_connect = connected
        io.on_disconnect = disconnected
        io.on_subscribe = subscribe

class Esp32WifiDevice:
    def __init__(self, controller:Pico):
        '''
        '''
        self.pico = controller
        # slot to store html from a webrequest
        self.requestedpage
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
        self.spi            = busio.SPI(pico.wifi_esp32_sck, pico.wifi_esp32_mosi, pico.wifi_esp32_miso)
        #
        #
        #------- CS (clock select) ------------*
        # esp32-S_NINA_firmware = IO5 (hiletgo esp32d GPIO5)
        # pico                  = GP13
        self.esp32_cs           = DigitalInOut(pico.wifi_esp32_cs)
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
        self.esp32_ready    = DigitalInOut(pico.wifi_esp32_ready)

        #------- RST ------------ = GP9
        # esp32-S_NINA_firmware = label:  RESET  | MODULE pin 2
        #                         IC pin: chp_pu | PHYSICAL pin 3
        self.esp32_reset        = DigitalInOut(pico.wifi_esp32_reset)

        # GP0               = Not needed - used for Bootloading and Blutooth
        # RXI               = Not needed for Wifi - Used for Blutooth 
        # TXO               = Not needed for Wifi - Used for Blutooth

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

        format of credentials as parameter is as follows:
        
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
            "[+] IP lookup adafruit.com: %s" % self.esp.pretty_ip(host_lookup)
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



if __name__ == "__main__":

# initialization step 1
# setup devices

    #create config for setting auth and endpoints
    config = Config()
    # if your WLAN SSID differs from my test network setup, you might want to change your
    # ssid and password here
    # same with adafruit creds
    config.ssid = "Other Network"
    # but that was just an example, this is going to run on my network so I am going to change the name back!
    config.ssid = "Untrusted Network"
    # create wrapper/reference for main board
    # with configuration
    pico = Pico(config)

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

    # establish an MQTT connection on the pico
    pico.init_mqtt()
    # initialize an mqtt client
    pico.init_mqtt_client({
        "username":"username",
        "key":"abc123password321cba"
    })

    # test 1
    # retrieve text resource
    esp_device.get_text(esp_device.TEXT_URL)
    
    # test 23
    # retrieve JSON resource
    esp_device.get_json(esp_device.JSON_URL)
