import board
    
######################
#   oled pins
#######################

oled_sda    = board.GP18
oled_scl    = board.GP19
oled_reset  = None

######################
#  WIFI CO PROCESSOR
#######################

wifi_esp32_sck    = board.GP10
wifi_esp32_miso   = board.GP12
wifi_esp32_mosi   = board.GP11
wifi_esp32_cs     = board.GP13
wifi_esp32_ready  = board.GP14
wifi_esp32_reset  = board.GP15
