"""! @file encoder_reader.py
This program creates the class "Encoder" which initializes the timers/counters required for the encoder using provided channel pins and a timer/counter.
This class also contains the ability to set the read the overall motor position (being able to bypass overflow and underflow), and is able to zero at any position.
"""
import motor_driver
import utime
import pyb

class Encoder:
    """! 
    This class implements the encoder in the motor for an ME405 kit. 
    """
    def __init__(self, in6pin, in7pin, timer):
        """! 
        Creates an encoder by initializing timers as counters given their respective pins 
        @param in6pin The set up X6 encoder pin  
        @param in7pin The set up X7 encoder pin
        @param timer The set up counter with AR = period
        """
        self.prev_count = 0
        self.tot_count = 0
        
        try:
            # Initialized Counter  
            self.timer = timer
            # Initializing the Timer Channels
            self.timer_Encoder_6 = self.timer.channel(1,
                                                      pyb.Timer.ENC_AB,
                                                      pin=in6pin)
            self.timer_Encoder_7 = self.timer.channel(2,
                                                      pyb.Timer.ENC_AB,
                                                      pin=in7pin)
            print ("Created a encoder")
        except Exception as e:
            print(e)


    def read(self):
        """!
        This method calculates the current motor position
        and prints out the result. This motor position bypasses
        overflow and underflow, meaning it can count below and above
        the given timer period.
        """
        count = self.timer.counter()
        
        delta = count-self.prev_count
        AR = int(self.timer.period())
        
        # For overflow
        if delta <= -(AR+1)/2:
            self.tot_count += (AR+1)+delta
        # For underflow
        elif delta >= (AR+1)/2:
            self.tot_count += delta-(AR+1)
        else:
            self.tot_count += delta
        print(self.tot_count)
        self.prev_count = count
        
        
    def zero(self):
        """!
        This method zeros the encoder at the current motor position.
        """
        self.tot_count = 0
        print(self.tot_count)
  
           
# Test Code
if __name__ == "__main__":
    # Initializing the Encoder Counters
    timer_B = pyb.Timer(4, period=65535, prescaler=0)
    timer_C = pyb.Timer(8, period=65535, prescaler=0)

    # Initializing the PWM Timers
    pinB6 = pyb.Pin(pyb.Pin.board.PB6)
    pinB7 = pyb.Pin(pyb.Pin.board.PB7)
    
    pinC6 = pyb.Pin(pyb.Pin.board.PC6)
    pinC7 = pyb.Pin(pyb.Pin.board.PC7)
    
    encoder_B = Encoder(pinB6, pinB7, timer_B)
    encoder_C = Encoder(pinC6, pinC7, timer_C)
    
    # Hand Test
    while True:
        try:
            while True:
                encoder_B.read()
                encoder_C.read()
                utime.sleep_ms(100)
        except KeyboardInterrupt:
            encoder_B.zero()
            encoder_C.zero()
