
################################
# Internal
################################
from config import Config

################################
# communications
################################
# spi
from adafruit_esp32spi import adafruit_esp32spi
from adafruit_esp32spi import adafruit_esp32spi_wifimanager
# http / sockets
from adafruit_requests import adafruit_requests as requests
import adafruit_esp32spi.adafruit_esp32spi_socket as socket
###############################################################################
# REPRESENTATION OF ESP32 WIFI CO-PROCESSOR
#
#   This is a class representing an esp32 module
#   TODO: type up background and specs
#
#
###############################################################################   
class Esp32WifiDevice:
    def __init__(self,
                 spi_bus,
                 config:Config,
                 ):#spi_pin_set:dict):#, controller:Pico):
        '''
        pass this class the spi bus created on the pico
        pico.esp_spi_bus
        '''

        # pass the pins from the pico that you are using for spi
        # get these pins with Pico.get_spi_pins
        #self.spi_pin_set = spi_pin_set
        #self.pico = controller
        self.config = config
        # spi bus connection from pico
        self.spi_bus = spi_bus
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
# WIFI OPERATIONS
###############################################################################   
    def init_wifi(self):
        '''
        Initializes esp32 wifi managment
        '''
        self.wifi     = adafruit_esp32spi_wifimanager.ESPSPI_WiFiManager(self.spi_bus, self.secrets)

        # establishes a socket resource to be made available for the esp32 data
        requests.set_socket(socket, self.spi_bus)

        self.TEXT_URL = "http://wifitest.adafruit.com/testwifi/index.html"
        self.JSON_URL = "http://api.coindesk.com/v1/bpi/currentprice/USD.json"

    def __ip__(self):
        '''
        Returns ip address 
        '''
        try:
            self.ip = print("[+] IPv4 addr: ", self.spi_bus.pretty_ip(self.spi_bus.ip_address))
        except:
            self.ip = "[-] IPv4 addr: N/A - not connected to any network"

    def check_idle(self) -> bool:
        '''
        checks if esp32 is in idle state
        '''
        if self.spi_bus.status == adafruit_esp32spi.WL_IDLE_STATUS:
            print("[+] ESP32 found and in idle mode")
        else:
            print("[+] ESP32 Active")

    def show_esp32_hardware_info(self):
        '''
        displays data about firmware and hardware address
        '''
        print("Firmware vers.", self.spi_bus.firmware_version)
        print("MAC addr:", [hex(i) for i in self.spi_bus.MAC_address])

    def display_scan_results(self):
        '''
        prints data about local APs
        '''
        for ap in self.spi_bus.scan_networks():
            print("\t%s\t\tRSSI: %d" % (str(ap["ssid"], "utf-8"), ap["rssi"]))

    def check_wifi_reset_if_bad(self):#esp32thing(self):
        try:
            s = self.spi_bus.status
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
        while not self.spi_bus.is_connected:
            try:
                # ssid and password are in config, config is given to the pico
                self.spi_bus.connect_AP(
                                    self.config.ssid,
                                    self.config.password
                                    )#secrets["ssid"], secrets["password"])
            except OSError as e:
                print("[-] Could not connect to AP, retrying: ", e)
                continue
        
        print("[+] Connected to", str(self.spi_bus.ssid, "utf-8"), "\tRSSI:", self.spi_bus.rssi)
        print("[+] My IP address is", self.spi_bus.pretty_ip(self.spi_bus.ip_address))

    def http_request(self,uri="adafruit.com"):
        '''
        Requests a resource via an http request
        stores return data in 
            self.http_request_result
        '''
        print(f"[+ requesting http resource {uri}]")
        self.http_request_result = self.spi_bus.get_host_by_name(uri)
 
    def get_IP_by_hostname(self,uri="adafruit.com"):
        '''
        obtains IP of given hostname
        stores return data in 
            self.host_lookup_return
        '''
        host_lookpup = self.spi_bus.get_host_by_name(uri)
        self.host_lookup_return = host_lookpup
        print(
            "[+] IP lookup adafruit.com: %s" % self.spi_bus.pretty_ip(self.host_lookup_return)
        )

    def ping(self, uri="google.com"):
        '''
        issues ICMP ping to given resource
        '''
        ping_result = self.spi_bus.ping(uri)
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
