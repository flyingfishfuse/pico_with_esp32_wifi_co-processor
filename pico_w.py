# SPDX-FileCopyrightText: 2022 Liz Clark for Adafruit Industries
#
# SPDX-License-Identifier: MIT


import ssl
import machine
import network
import ubinascii
import os, gc
import adafruit_requests
from util import errorlogger
import ipaddress, wifi,socketpool


from pico_code import Pico

gc.collect()

print()
print("Connecting to WiFi")

class WifiBoard(Pico):
    def __init__(self,ssid:str,passphrase:str) -> None:
        """An implementation of the adafruit pico W

        init with ssid/passphrase explicitly in code, or init with no ssid/passphrase
        to draw that info from .env file
    
        """
        self.wlan_ssid = ssid
        self.wlan_pass = passphrase
        self.radio     = wifi.radio
    
    def connect(self,ssid:str,passphrase:str,use_env:bool=True):
        """connect to your SSID with given passphrase
        use_env defaults to true, taking the information from the environment
        variables specified in the .env file in the root of the project directory

        if use_env is given False as a parameter, you must supply an ssid/passphrase

        if WifiBoard class is instanced with ssid/pass, this function will ignore use_env
        Args:
            ssid (str): SSID to connect to
            passphrase (str): WPA passphrase to use for auth
            use_env (bool, optional): Takes ssid/passphrase from .env file in project root. Defaults to True.
        """
        try:
            if use_env:
                self.radio.connect(os.getenv('WIFI_SSID'), os.getenv('WIFI_PASSWORD'))
            #if ssid/pass supplied in function call
            elif use_env == False and ssid == None and passphrase == None:# and not self.wlan_pass and not self.wlan_ssid:
                print("[-] No SSID or PASSPHRASE given in WIFIBoard.connect(ssid,passphrase,use_env=False) function call")
                raise Exception
            # if class instanced with ssid/pass
            # will ignore ssid/pass given in function call even if use_env == False
            elif self.wlan_ssid and self.wlan_pass:
                self.radio.connect(self.wlan_ssid,self.wlan_pass)
            #everything went well
            # yes I am missing some cases, I will maybe add them later if I remember
            print("Connected to WiFi")
        except Exception as e:
            errorlogger(e, "[-] Failed to connect to wireless network with  WIFIBoard.connect()")
    
    def create_pool(self)-> socketpool.SocketPool:
        """
        creates a socket pool to tx/rx data with
        """
        self.pool = socketpool.SocketPool(self.radio)
        return self.pool

    def session(self):
        """returns a "session object" you can treat like a "requests" lib object
        e.g requests.get(url)/requests.post(url) will GET/POST
        """
        # they can skip some setup if its not a good flow for them
        if not self.pool:
            errorlogger("[-] Socket pool not yet established, creating (this will be removed in the future... maybe)...")
            self.pool = socketpool.SocketPool(self.radio)
        else:
            self.requests = adafruit_requests.Session(self.pool, ssl.create_default_context())

    def show_stats(self):
        """
        prints information about the connection and device
        """
        print("My MAC addr:", [hex(i) for i in self.radio.mac_address])
        print("My IP address is", self.radio.ipv4_address)

    def ping(self,ipaddress:ipaddress.IPv4Address)
        """Pings a server by IP
        Returns:
            IPv4Address: string representing an IPV4 address (e.g. 192.168.0.1)
        """ 
        self.radio.ping(ipv4)*1000


ssid = os.getenv("WLAN_ssid")
password = os.getenv("WLAN_password")

WifiBoard()

while True:
    try:
        #  pings openweather
        response = requests.get(url)
        #  packs the response into a JSON
        response_as_json = response.json()
        print()
        #  prints the entire JSON
        print(response_as_json)
        #  gets location name
        place = response_as_json['name']
        #  gets weather type (clouds, sun, etc)
        weather = response_as_json['weather'][0]['main']
        #  gets humidity %
        humidity = response_as_json['main']['humidity']
        #  gets air pressure in hPa
        pressure = response_as_json['main']['pressure']
        #  gets temp in kelvin
        temperature = response_as_json['main']['temp']
        #  converts temp from kelvin to F
        converted_temp = (temperature - 273.15) * 9/5 + 32
        #  converts temp from kelvin to C
        #  converted_temp = temperature - 273.15

        #  prints out weather data formatted nicely as pulled from JSON
        print()
        print("The current weather in %s is:" % place)
        print(weather)
        print("%s°F" % converted_temp)
        print("%s%% Humidity" % humidity)
        print("%s hPa" % pressure)
        #  delay for 5 minutes
        time.sleep(300)
    # pylint: disable=broad-except
    except Exception as e:
        print("Error:\n", str(e))
        print("Resetting microcontroller in 10 seconds")
        time.sleep(10)
        microcontroller.reset()
#  pings Google
ipv4 = ipaddress.ip_address("8.8.4.4")
print("Ping google.com: %f ms" % ())

# this is the raspberry pi pico
mqtt_server = os.getenv("mqtt_server")


client_id = ubinascii.hexlify(machine.unique_id())

topic_pub_temp = b'esp/dht/temperature'
topic_pub_hum = b'esp/dht/humidity'

last_message = 0
message_interval = 5

station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
  pass

print('Connection successful')
