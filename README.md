# Lab 2
 Group 18's Lab 2

This project contains the main.py, motor_driver.py, encoder_reader.py programs. As made previously, the module, motor_driver.py, creates the class "MotorDriver" which initializes the GPIO pins as PWM outputs for one motor and allows the PWM duty cycle to be set. The module, encoder_reader.py, creates the class "Encoder" which initializes the timers/counters required for on motor encoder using provided channel pins and a timer/counter and allows the absolute position (accounting for overflow and underflow) to be read and zeroed. The program, main.py, is used to test the encoder using a hand test in which the position is read as the motor is allowed to spin freely and is used to test the encoder with varying PWM inputs to the motor.
