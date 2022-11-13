
from config import Config
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

    def subscribe(client, userdata, topic, granted_qos):
        # This method is called when the client subscribes to a new feed.
        print("Subscribed to {0} with QOS level {1}".format(topic, granted_qos))

