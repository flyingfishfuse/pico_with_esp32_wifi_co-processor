# overview
    This is a more robust implementation of the wifi coprocessor setup using 
    a circuitpython enabled microprocessor in combination with an esp32 for WLAN
    functionality using SPI bridging between devices

    This also contains code for interacting with the system via a 4x4 keypad and oled

    I am building this for the monitoring of lizard and bug farm enclosures, with expansion 
    into game bird hatching chambers and garden monitoring systems for the enabling of self sufficient
    suburban farming

# components
    
    Config()
        stores global configuration variables, for most people this is all you need to change around

    Pico()
        representation of a pico main board

    ESP32WifiDevice()
        ditto

    SSD1306()
        ditto

    MQTTManagment()
        put mqtt interactions here
        
# how to use

    main.py has an example of the most basic implementation
