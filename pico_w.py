## SPDX-FileCopyrightText: 2022 Liz Clark for Adafruit Industries
#
# SPDX-License-Identifier: MIT

# extra license, GPLv3, under ME. I wrote this.
from secrets import adafruit_io_username, adafruit_io_api_key, ssid, password
import traceback
import ssl, os, time
import microcontroller
import adafruit_requests
import ipaddress, wifi,socketpool
from adafruit_io.adafruit_io import IO_HTTP, AdafruitIO_RequestError

def errorlogger(exception:Exception, message:str):
    """
    prints line number and traceback
    TODO: save stack trace to error log
            only print linenumber and function failure
    """
    #exc_type, exc_value, exc_tb = sys.exc_info()
    #trace = traceback.TracebackException(exc_type, exc_value, exc_tb)
    print(message)
    print(traceback.format_exception(None, exception, None))
    #lineno = 'LINE NUMBER : ' + str(exc_tb.tb_lineno)
    #print(
    #    message+"\n [-] "+lineno+"\n [-] "+''.join(trace.format_exception_only()) +"\n"
    #    )



class WifiBoard():
    def __init__(self,ssid:str,passphrase:str) -> None:
        """An implementation of the adafruit pico W

        init with ssid/passphrase explicitly in code, or init with no ssid/passphrase
        to draw that info from .env file
    
        """
        print("[+] Creating WifiBoard() class")
        self.wlan_ssid = ssid
        self.wlan_pass = passphrase
        #self.headers = {'Authorization': 'Bearer ' + os.getenv('bearer_token')}
        self.radio     = wifi.radio
        
    def reset(self):
        """resets pico board
        """
        print("Resetting microcontroller in 10 seconds")
        time.sleep(10)
        microcontroller.reset()


    #def connect(self,ssid:str,passphrase:str,use_env:bool=True):
    def connect(self,use_env:bool=False):
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
        print("Connecting to WiFi") 

        try:
            if use_env:
                print("[+] Using environment Variables")
                self.radio.connect(os.getenv('WIFI_SSID'), os.getenv('WIFI_PASSWORD'))
            #if ssid/pass supplied in function call
            elif use_env == False:# and ssid == None and passphrase == None:# and not self.wlan_pass and not self.wlan_ssid:
                # if class instanced with ssid/pass
                print("[+] Using loaded credentials")
                if self.wlan_ssid and self.wlan_pass:
                    print("[+] Attempting connection")
                    self.radio.connect(self.wlan_ssid,self.wlan_pass)
                else:
                    print("[-] No SSID or PASSPHRASE given in WIFIBoard.connect(ssid,passphrase,use_env=False) function call")
                    raise Exception
            else:
                print("major TODO here, finish catching cases")
            #everything went well
            # yes I am missing some cases, I will maybe add them later if I remember
            print("Connected to WiFi")
        except Exception as e:
            errorlogger(e, "[-] Failed to connect to wireless network with  WIFIBoard.connect()")
    
    def create_pool(self)-> socketpool.SocketPool:
        """
        creates a socket pool to tx/rx data with
        """
        try:
            self.pool = socketpool.SocketPool(self.radio)
            return self.pool
        except Exception as e:
            errorlogger(e, f"[-] Failed to create socket pool")

    def create_session(self):
        """returns a "session object" you can treat like a "requests" lib object
        e.g requests.get(url)/requests.post(url) will GET/POST
        """
        # they can skip some setup if its not a good flow for them
        if not self.pool:
            errorlogger("[-] Socket pool not yet established, creating (this will be removed in the future... maybe)...")
            self.create_pool()
        else:
            try:
                self.session = adafruit_requests.Session(self.pool, ssl.create_default_context())
            except Exception as e:
                errorlogger(e, f"[-] Failed to create TCP session")

    def get(self, uri:str):
        """uses self.session for GET to specified URI
        if WifiBoard.create_session() has not been called yet, this function
        will create a session  for later usage.

        if this behavior is undesired, use WIFIBoard.uget() for a sessionless GET

        Args:
            URI (str): URI to request via GET
        """
        # if session has not been created yet
        # create one so user can define flow control as they see fit
        try:
            if not self.session:
                print("[+] Session has not been created yet .. creating (this behavior may be removed or changed in the future)")
                self.create_session()
            response =self.session.get(uri)
            return response
        except Exception as e:
            errorlogger(e, f"[-] Failed to perform GET request for {uri}")
    
    def uget(self,uri:str):
        """performs a regular GET with no session 

        Args:
            uri (str): URI to request via GET
        """
        try:
            response =adafruit_requests.get(uri)
            return response
        except Exception as e:
            errorlogger(e, f"[-] Failed to Perform GET request to {uri}")
    
    def scan(self,start_chan:int,stop_chan:int):
        """scans for AP's in range

        Args:
            start_chan (int): channel to begin scanning on
            stop_chan (int): channel to end scanning on
        """
        print("[+] Beginning Scanning")
        counter = 1
        self.scan_results = {}
        for network in self.radio.start_scanning_networks():
            print(network.ssid)
            self.scan_results.update(
                {
                    counter:{
                    "ssid" : network.ssid,
                    "bssid": network.bssid,
                    "rssi" : network.rssi,
                    "chan" : network.ssid
                    }
                }
            )
            counter + 1
    
    def show_scan_results(self):
        """prints results from scan()"""
        for network in self.scan_results:
            print(network)

    def connect_AIO(self):
        """connects to adafruit IO servers
        """
        try:
            self.aio = IO_HTTP(self.aio_username, self.aio_key, self.session)
            print("connected to io")
        except Exception as e:
            errorlogger(e, "[-] Failed to connect to Adafruit IO")

    def show_stats(self):
        """
        prints information about the connection and device
        """
        try:
            print("My MAC addr:", [hex(i) for i in self.radio.mac_address])
            print("My IP address is", self.radio.ipv4_address)
        except Exception as e:
            errorlogger(e, "[-] Failed to show information about device")

    def ping(self,ipaddress:str="8.8.4.4"):#:ipaddress.IPv4Address):
        """Pings a server by IP
        Args:
            ipaddress (str): String of IPV4 octets, e.g. 192.168.0.1
        """
        try:
            #ipaddress.ip_address("8.8.4.4")
            ip = ipaddress.ip_address(ipaddress)
            self.radio.ping(ip)*1000
        except Exception as e:
            errorlogger(e, "[-] Failed to Ping")


if __name__ == "__main__":
###############################################################################
# initialization step 1
# setup devices
###############################################################################
    # pull env vars for operation
    #ssid = os.getenv("WIFI_SSID")
    #print("[+] SSID: " + ssid)
    #password = os.getenv("WIFI_PASSWORD")
    #print("[+] PASS: " + password)


    
    #######################################
    # PICO
    #######################################
    # create wrapper/reference for main board
    try:
        #pico = WifiBoard()
        pico = WifiBoard(ssid=ssid, passphrase=password)
        #print(pico.wlan_ssid)
        #print(pico.wlan_pass)
        #pico.connect(use_env=False)

    except Exception as e:
        errorlogger(e, "[-] Pico module creation FAILED!")
        #errorlogger(e, "\n[-] Pico module creation FAILED!")


    #######################################
    # WIFI
    #######################################
    try:
        print("[+] Connecting to WLAN")
        pico.connect(use_env=False)
    except Exception as e:
        errorlogger(e, "[-] Wlan connection FAILED!")

    #######################################
    # Session
    #######################################
    try:
        print("[+] Creating a session object without URI")
        pico.create_session()
    except Exception as e:
        errorlogger(e, "[+] Failed to create TCP session object")

    #######################################
    # Scanning
    #######################################
    try:
        print("[+] Scanning for networks")
        pico.scan() 
        pico.show_scan_results()
    except Exception as e:
        errorlogger(e, "[-] Network scanning failed!")
