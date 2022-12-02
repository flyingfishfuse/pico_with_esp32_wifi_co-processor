# SPDX-FileCopyrightText: 2017 Limor Fried for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""CircuitPython I2C Device Address Scan"""
# If you run this and it seems to hang, try manually unlocking
# your I2C bus from the REPL with
#  >>> import board
#  >>> board.I2C().unlock()

import time
import board

import traceback,sys
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

class I2CScanner:
    def __init__(self):
        """
        scans I2C lines for addresses and reports them in the terminal
        To do an I2C scan on a Raspberry Pi the i2cdetect command is used. 
        If not already done, be sure to enable I2C on the Raspberry Pi via 
        raspi-config. If the i2cdetect command is not found, install it with:
        """
        # To use default I2C bus (most boards)
        self.i2c = board.I2C()

        # To create I2C bus on specific pins
        # import busio
        # i2c = busio.I2C(board.SCL1, board.SDA1)  # QT Py RP2040 STEMMA connector
        # i2c = busio.I2C(board.GP1, board.GP0)    # Pi Pico RP2040

    def scan(self):
        """
        
        """
        while not self.i2c.try_lock():
            pass
        try:
            while True:
                print(
                    "I2C addresses found:",
                        [hex(device_address) for device_address in self.i2c.scan()],
                )
                time.sleep(2)

        finally:  # unlock the i2c bus when ctrl-c'ing out of the loop
            self.i2c.unlock()
