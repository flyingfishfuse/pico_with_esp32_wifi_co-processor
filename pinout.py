import board
#
# pico to esp32

######################
#   UART PINOUT
#######################
uart_rx     = board.RX
usrt_tx     = board.TX


######################
#   oled pins
#######################

oled_sda    = board.GP18
oled_scl    = board.GP19
oled_reset  = None

######################
#  WIFI CO PROCESSOR
#######################
# you need to reference the esp32 module schematic to find these pins
# if your module differs
#ESP32SPI/NINA expects ESP32 pins 5,14,18,23,33 ...RX/TX for debug UART, GPIO for bootloading.

    #-----------------------------------------------------------------#
    # POWER             |                                             #
    # Vin 3.3v-5v / 250ma required for WiFi use. (Pin Position 40)    #
    # 3v Out - upto 50ma for other devices (not used)                 #
    # GND               | Ground (Pin Position 13)                    #
    #                                                                 #
    ###-------------------------------------------------------------###
    #                         SPI PINOUT                              #
    ###-------------------------------------------------------------###
    # (there has been a movement to change miso/mosi naming)          #
    # MISO                  = Peripheral Out Controller In (PoCi)     #
    # MOSI                  = Peripheral In Controller Out (PiCo)     #
    #---------------------------------------------------------------###
#done
#esp32-S_NINA_firmware = IO14 (hiletgo esp32d gpio14)
wifi_esp32_mosi        = board.GP11 #pico

#done
#esp32-S_NINA_firmware = IO23 (hiletgo esp32d gpio23)
wifi_esp32_miso        = board.GP12 #pico

#done
#esp32-S_NINA_firmware = IO5 (hiletgo esp32d GPIO5) (logical pin 29)
wifi_esp32_cs          = board.GP13 #pico

#done
#esp32-S_NINA_firmware = IO18 (hiletgo esp32d gpio18)
wifi_esp32_sck         = board.GP14 #pico

#done
#esp32-S_NINA_firmware = IO33 
wifi_esp32_ready       = board.GP20 #pico

#done
#esp32-S_NINA_firmware = label:  RESET  | MODULE pin 2
#                        IC pin: chp_pu | PHYSICAL pin 3
wifi_esp32_reset       = board.GP21 #pico

#done
#esp32-S_NINA_firmware = IO0 (hiletgo esp32d gpio0)
esp_gpio0              = board.GP22 #pico

#
#esp32-S_NINA_firmware = RX_D0 (hiletgo esp32d RX0)
#esp_rx                 = board. #pico

#
#esp32-S_NINA_firmware = TX_D0 (hiletgo esp32d TX0)
#esp_tx                 = board. #pico
