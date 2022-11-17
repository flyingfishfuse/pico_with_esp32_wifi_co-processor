################################
# Internal
################################
import board
import busio

################################
# OLED display
################################
import displayio
import terminalio
import adafruit_displayio_ssd1306

from config import Config


###############################################################################
# REPRESENTATION OF ss1306 OLED display
#   Attached to pico
###############################################################################   
class SSD1306:
    def __init__(self,config:Config):
        '''
        This class represents an OLED module I have had for years 
        now but never really used

        The SS1306, looks neat in low light. Visible in sunlight also.
        '''
        # i2c device address, can change, double check this
        #128 x 64 size OLEDs
        #self.device_address = 0x3d
        self.device_address = config.oled_i2c_addr

        #128x32
        #self.device_address=0x3c

        # In order to make it easy to change display sizes, we'll define a few 
        # variables in one spot here. We have the display width, the display 
        # height and the border size, which we will explain a little further 
        # below. If your display is something different than these numbers, 
        # change them to the correct setting.
        self.WIDTH = 128
        self.WIDTH = 64
        self.BORDER = 5

        self.WIDTH = config.WIDTH
        self.WIDTH = config.HEIGHT
        self.BORDER = config.BORDER


        self.CENTER_X = int(self.WIDTH/2)
        self.CENTER_Y = int(self.WIDTH/2)

        self.release()
        self.setpins()

    def release(self):
        '''
        release any previously used displays. 
        This is important because if the microprocessor is reset, 
        the display pins are not automatically released and this 
        makes them available for use again.
        '''
        displayio.release_displays()
    
    def set_display(self,reset_pin=False):
        '''
        
        reset_pin: bool
            uses a predeclared reset pin to reset the display
        
        If you have a reset pin (which may be required if your OLED does not
        have an auto-reset chip like the FeatherWing)

        If you're using I2C, you would use this section of code. We set the I2C object 
        to the board's I2C with the easy shortcut function board.I2C(). By using this
        function, it finds the SPI module and initializes using the default SPI 
        parameters. We also set the display bus to I2CDisplay which makes use of the I2C bus.
        '''
        if reset_pin == False:
            self.display_bus = displayio.I2CDisplay(self.i2c, device_address=self.device_address)
        elif reset_pin == True:
            self.display_bus = displayio.I2CDisplay(self.i2c, 
                                                    device_address=self.device_address, 
                                                    reset=self.reset_pin)
        
    def show_terminal(self):
        '''
        initialize the driver with a width of the WIDTH variable and a height
        of the HEIGHT variable. If we stopped at this point and ran the code,
        we would have a terminal that we could type at and have the screen update.
        '''
        self.display = adafruit_displayio_ssd1306.SSD1306(self.display_bus, 
                                                          WIDTH=self.WIDTH,
                                                          WIDTH=self.WIDTH
                                                        )


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
        self.i2c_sda            = board.GP18
        #self.i2c_sda = config.oled_i2c_sda
        #
        #----------------SCL -----------------*
        # ss1306 OLED           = SCL 
        # pico                  = GP19, <I2C1 SCL> , physical pin 25
        self.i2c_scl            = board.GP19
        #self.i2c_scl = config.oled_i2c_scl
        #--------------Reset ----------------*
        # ss1306 OLED           = RES
        # pico                  = GP09 I guess? Adafruit, fix your tutorials
        self.reset_pin = False # board.D9

    def init_I2C(self):
        '''
        initializes I2C communications between pico and OLED module
        '''
        self.i2c_bus = busio.I2C(scl=self.i2c_scl, sda=self.i2c_sda)

 
