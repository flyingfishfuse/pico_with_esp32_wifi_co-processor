import board

class Config:
    '''
    Config class for holding all your secrets and endpoints
    '''
    def __init__(self):
        '''
        waaat
        '''
        self.debug          =  True
        self.ssid           = "Untrusted Network"
        self.password       = 'Whatapassword1!'
        # the name is important, read the code in:
        #   Pico.set_mqtt_secret()
        # and
        #   Pico.init_mqtt_client()
        # do not change names, these items are for specific activities
        self.mqtt_username   = 'your_adafruit_io_username_'
        self.mqtt_key        = 'your_big_huge_super_long_aio_key_'
        self.broker          = 'io.adafruit.com',
        self.port            = '1883'

        #oled settings

        #pinout
        # was thinking of moving this here but I might just
        # put "pinout" in its own file or class
        #self.oled_i2c_sda    = board.GP18 
        #self.oled_i2c_scl    = board.GP19 
        self.HEIGHT          = 128
        self.WIDTH           = 64
        self.BORDER          = 5
        self.oled_i2c_addr   = 0x3c
        
