"""! @file main.py
This program sets up the pins and timers required for a "MotorDriver" and two "Encoder" objects and creates the objects.
It then turns the motor to spin from 0% PWM to 100% PWM to -100% PWM to 0% and waits to repeat again.
Simultaneously, the encoder prints out values until Ctrl-C is pressed, in which it zeros the encoder.
"""
import utime
import pyb
import encoder_reader
import motor_driver

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
    
    encoder_B = encoder_reader.Encoder(pinB6, pinB7, timer_B)
    encoder_C = encoder_reader.Encoder(pinC6, pinC7, timer_C)
    
#     # Hand Test
#     while True:
#         try:
#             while True:
#                 encoder_B.read()
#                 encoder_C.read()
#                 utime.sleep_ms(100)
#         except KeyboardInterrupt:
#             encoder_B.zero()
#             encoder_C.zero()
    
    
    # Motor Test
    
    # Sets up pins and timers
    a_pin = pyb.Pin(pyb.Pin.board.PA10, pyb.Pin.OUT_PP)
    in1pin = pyb.Pin(pyb.Pin.board.PB4, pyb.Pin.OUT_PP)
    in2pin = pyb.Pin(pyb.Pin.board.PB5, pyb.Pin.OUT_PP)
    a_timer = pyb.Timer(3, freq=1000)

    moe = motor_driver.MotorDriver(a_pin, in1pin, in2pin, a_timer)
        
    # Cycles between -100% and 100% PWM and waiting
    PW = 0
    time_range = 5
    interval = 0.05
    try:
        while True:
            for value in range(5/interval):
                PW += 100/(5/interval)
                moe.set_duty_cycle(PW)
                encoder_B.read()
                encoder_C.read()
                utime.sleep(interval)
            for value in range(2*5/interval):
                PW -= 100/(5/interval)
                moe.set_duty_cycle(PW)
                encoder_B.read()
                encoder_C.read()
                utime.sleep(interval)
            for value in range(5/interval):
                PW += 100/(5/interval)
                moe.set_duty_cycle(PW)
                encoder_B.read()
                encoder_C.read()
                utime.sleep(interval)
            for value in range(5/interval):
                PW = 0
                moe.set_duty_cycle(PW)
                encoder_B.read()
                encoder_C.read()
                utime.sleep(interval)
    except KeyboardInterrupt:
        PW = 0
        moe.set_duty_cycle(PW)
        encoder_B.zero()
        encoder_C.zero()
        print("stopped")
