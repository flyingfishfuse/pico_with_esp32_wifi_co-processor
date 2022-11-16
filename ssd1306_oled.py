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
from adafruit_display_text import label


###############################################################################
# REPRESENTATION OF ss1306 OLED display
#   Attached to pico
###############################################################################   
class SSD1306:
    def __init__(self):
        '''
        This class represents an OLED module I have had for years 
        now but never really used

        The SS1306, looks neat in low light. Visible in sunlight also.
        '''
        # i2c device address, can change, double check this
        #128 x 64 size OLEDs
        self.device_address = 0x3d
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
        self.i2c_sda = board.GP18
        #
        #----------------SCL -----------------*
        # ss1306 OLED           = SCL 
        # pico                  = GP19, <I2C1 SCL> , physical pin 25
        self.i2c_sda = board.GP19
        #--------------Reset ----------------*
        # ss1306 OLED           = RES
        # pico                  = GP09 I guess? Adafruit, fix your tutorials
        self.reset_pin = False # board.D9

    def init_I2C(self):
        '''
        initializes I2C communications between pico and OLED module
        '''
        self.i2c = busio.I2C(scl=board.GP5, sda=board.GP4) # This RPi Pico way to call I2C<br>

    def test_picture(self):
        """
        prints a message in a outline for testing
        """
        # create a background splash image. We do this by creating a group that
        # we can add elements to and adding that group to the display. 
        # In this example, we are limiting the maximum number of elements to 10, 
        # but this can be increased if you would like. 
        # The display will automatically handle updating the group.
        # Make the display context
        splash = displayio.Group()
        self.display.show(splash)

        # create a Bitmap that is the full width and height of the display. The
        # Bitmap is like a canvas that we can draw on. In this case we are 
        # creating the Bitmap to be the same size as the screen, but only have 
        # one color. Although the Bitmaps can handle up to 256 different colors,
        # the display is monochrome so we only need one. 
        # Create a Palette with one color and set that color to 0xFFFFFF (white)
        # If were to place a different color here, displayio handles color 
        # conversion automatically, so it may end up black or white depending 
        # on the calculation.
        color_bitmap = displayio.Bitmap(self.WIDTH, self.WIDTH, 1)
        color_palette = displayio.Palette(1)
        color_palette[0] = 0xFFFFFF  # White

        # we create a TileGrid by passing the bitmap and palette and draw it 
        # at (0, 0) which represents the display's upper left.
        bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
        splash.append(bg_sprite)

        #create a smaller black rectangle. The easiest way to do this is to 
        # create a new bitmap that is a little smaller than the full screen 
        # with a single color of 0x000000 (black) , and place it in a 
        # specific location. In this case, we will create a bitmap that is 
        # 5 pixels smaller on each side. This is where the BORDER variable comes into use. 
        # It makes calculating the size of the second rectangle much easier. 
        # The screen we're using here is 128x64 and we have the BORDER set to 5 
        # so we'll want to subtract 10 from each of those numbers.
        # 
        # We'll also want to place it at the position (5, 5) so that it ends up centered.
        # Draw a smaller inner rectangle
        inner_bitmap = displayio.Bitmap(self.WIDTH - self.BORDER * 2, self.WIDTH - self.BORDER * 2, 1)
        inner_palette = displayio.Palette(1)
        inner_palette[0] = 0x000000  # Black
        inner_sprite = displayio.TileGrid(
            inner_bitmap, pixel_shader=inner_palette, x=self.BORDER, y=self.BORDER
        )
        splash.append(inner_sprite)

        #add a label that says "Hello World!" on top of that. 
        # using the built-in Terminal Font. 
        # In this example, we won't be doing any scaling because of the small resolution, 
        # so we'll add the label directly the main group. If we were scaling, we would have used a subgroup.

        #Labels are centered vertically, so we'll place it at half the HEIGHT for the Y coordinate
        # and subtract one so it looks good. 
        # We use the // operator to divide because we want a whole number returned and it's an
        # easy way to round it. 
        # We'll set the width to around 28 pixels make it appear to be centered horizontally, 
        # but if you want to change the text, change this to whatever looks good to you. 
        # Let's go with some white text, so we'll pass it a value of 0xFFFFFF.
        # Draw a label
        text = "Hello World!"
        text_area = label.Label(
            terminalio.FONT, text=text, color=0xFFFFFF, x=28, y=self.WIDTH // 2 - 1
        )
        splash.append(text_area)
        #an infinite loop at the end so that the graphics screen remains in 
        # place and isn't replaced by a terminal.
        while True:
            pass
