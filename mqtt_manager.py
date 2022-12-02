################################
# MQTT
################################
#from mqtt_manager import MQTTManager
import adafruit_requests as requests
from adafruit_io.adafruit_io import IO_MQTT
import adafruit_minimqtt.adafruit_minimqtt as MQTT

import adafruit_esp32spi.adafruit_esp32spi_socket as socket

from config import Config


class MQTTManager:
    def __init__(self,
                 config:Config,
                 #i2c_bus
                 #mqtt_secret:dict
                 ):
        '''
        This class is the handler for all mqtt activities

        It holds the callbacks and the init as well as dial out, dial in
        '''
        print("[+] Creating new MQTT manager")
        # do nothing, user must call init themself
        self.mqtt_username   = config.mqtt_username
        self.mqtt_passkey    = config.mqtt_key
        self.broker          = config.broker
        self.port            = config.port
        self.feed_list = {}

        #self.mqtt_secret = config.mqtt_secret
        self.set_mqtt_secret(config.mqtt_auth_creds)

        # establish an MQTT connection on the pico
        #self.init_mqtt()
    
        # initialize an mqtt client
        #self.init_mqtt_client()
###############################################################################
# MQTT operations
###############################################################################
    def init_mqtt(self,esp_spi_bus):
        '''
        initializes an mqtt socket, give it the spi_bus from the pico()
        '''
        print(f"[+] MQTTManager.init_mqtt")
        MQTT.set_socket(socket, esp_spi_bus)

    def set_mqtt_secret(self,mqtt_secret:dict):
        '''
        just for testing currently, dont try to reset the creds via any method or it will fail
        Performs auth setup by getting secrets from either
        supplied parameter or config class

        If mqtt_secret is not supplied as parameter, will use config
                
        defaults to my test network credentials if no parameter given

        BIG TODO: refactor this function, I got brainulated and skipped 
        doing the thing to the thing for the things with the thingamabooble
        '''
        print(f"[+] MQTTManager.set_mqtt_secret({mqtt_secret})")
        # must try to validate auth creds a little more
        if len(mqtt_secret) == 2 and isinstance(mqtt_secret, dict):
            for each in mqtt_secret:
                setattr(self,each,mqtt_secret.get(each))
            self.mqtt_secret = {
                                'username': self.mqtt_username,
                                'key'     : self.mqtt_passkey
                                }

            #self.mqtt_secret = mqtt_secret
        # defaults to my test network credentials
        else:
            print("[-] Bad data given, falling back to original from config")

            self.mqtt_secret = {
                                'username': self.mqtt_username,
                                'key'     : self.mqtt_passkey
                                }

    def init_mqtt_client(self):#,mqtt_secret):
        '''
        Initialize a new MQTT Client object
        '''
        print(f"[+] MQTTManager.init_mqtt_client()")
        self.mqtt_client = MQTT.MQTT(
                                     broker=self.broker,
                                     port=self.port,
                                     username=self.mqtt_username,
                                     password=self.mqtt_passkey
                                    )
        # Initialize an Adafruit IO MQTT Client
        io = IO_MQTT(self.mqtt_client)

        # Connect the callback methods defined above to Adafruit IO
        io.on_connect = self.connected
        io.on_disconnect = self.disconnected
        io.on_subscribe = self.subscribe

    def send_sensor_data_to_api(self,dict_of_data:dict):
        """
        Sends sensor data to adafruit api with HTTP requests
         This is a fallback method and should be transitioned from when moving from 
         dev to production
        """
        print(f"[+] MQTTManager.send_sensor_data_to_api({dict_of_data}) ")
        #TODO: build this out
        #crafted_request = dict_of_data
        #requests.post(crafted_request)

    def create_feeds(self,new_feeds:dict):
        '''
        Creates endpoints for publishing and subscribing
        input:
            list_of_feeds = [new_endpoint_name_1','new_endpoint_name_2']
        
        This will be added as class member via setattr()
        output:
            self.new_endpoint_name_1 = "mqtt_username/feeds/new_endpoint_name_1
        '''
        print(f"[+] MQTTManager.create_feeds")
        for each in new_feeds:
            # add class member named after feed
            setattr(self,each ,f"{self.mqtt_username}/feeds/{each}")
            # put it in a list for tracking and later operations
            self.feed_list[each] = f"{self.mqtt_username}/feeds/{each}"

    def list_feeds(self):
        '''
        returns an itterable for programmatically operating with 
        individual feeds as one operation
        '''
        for feed_item in self.feed_list:
            print(f"[+] Feed entry: {self.feed_list.get(feed_item)}")

    #def init_mqtt(self):
    #    '''
    #    Dials out to adafruit broker
    #    '''
        # Set your Adafruit IO Username and Key in secrets.py (not anymore!)
        # (visit io.adafruit.com if you need to create an account,
        # or if you need your Adafruit IO key.)

        # original adafruit code stub
        #print("Connecting to %s" % secrets["ssid"])
        #wifi.radio.connect(secrets["ssid"], secrets["password"])
        #print("Connected to %s!" % secrets["ssid"])
        
        ### Feeds ###

        # Setup a feed named 'photocell' for publishing to a feed
        #photocell_feed = self.mqtt_username + "/feeds/photocell"

        # Setup a feed named 'onoff' for subscribing to changes
        #onoff_feed = self.mqtt_username + "/feeds/onoff"

    #def create_callback(self, new_callback:function)-> Callback:
        # Initialize an Adafruit IO MQTT Client
        #io = IO_MQTT(self.mqtt_client)

        # Connect the callback methods defined above to Adafruit IO
        #io.on_connect = self.connected
        #io.on_disconnect = self.disconnected
        #io.on_subscribe = self.subscribe
    # Define callback methods which are called when events occur
    # pylint: disable=unused-argument, redefined-outer-name
    def connected(client, userdata, flags, rc):
        # This function will be called when the client is connected
        # successfully to the broker.
        print(f"Connected to Adafruit IO! Listening for topic changes on {onofffeed}")
        # Subscribe to all changes on the onoff_feed.
        client.subscribe(onoff_feed)


    def disconnected(client, userdata, rc):
        # This method is called when the client is disconnected
        print("Disconnected from Adafruit IO!")


    def message(client, topic, message):
        # This method is called when a topic the client is subscribed to
        # has a new message.
        print("New message on topic {0}: {1}".format(topic, message))

    def subscribe(client, userdata, topic, granted_qos):
        # This method is called when the client subscribes to a new feed.
        print("Subscribed to {0} with QOS level {1}".format(topic, granted_qos))

class Callback:
    def __cls__(cls,new_function:function):
        '''
        creates a new callback for Adafruit.IO MQTT
        '''
