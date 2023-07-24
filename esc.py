# This program controls a ESC. This program is designed specifically for the BlueRobotics T200
# Make sure your battery is not connected if you are going to calibrate it at first.

import os     #importing os library so as to communicate with the system
import time   #importing time library to make Rpi wait because its too impatient 
os.system ("sudo pigpiod") #Launching GPIO library
time.sleep(1) # Delay to let the GPIO library initialize
import pigpio #importing GPIO library

ESC=4  #Connect the ESC in this GPIO pin 

pi = pigpio.pi()
pi.set_servo_pulsewidth(ESC, 0) 

max_value = 1900          #ESC max value - max forwards thrust
neutral_value = 1500      #ESC neutral_value 
min_value = 1100          #ESC min value - max backwards thrust

print("Please Calibrate the ESC before arming")
print("Type the exact word for the function you want")
print("calibrate OR manual OR control OR arm OR stop")

def config():
    print("Config Menu")
    print("Type 'calibrate' OR 'arm' OR 'manual' OR 'control' OR 'stop'")  
    while True:
        inp = input()
        if inp == "calibrate":
            calibrate()
            break
        elif inp == "arm":
            arm()
            break
        elif inp == "manual":
            manual()
            break
        elif inp == "control":
            control()
            break
        elif inp == "stop":
            stop()
            break'
        else 
            print("Invalid input")

# Provides manual control over ESC inputs
def manual_drive(): 
    print("Select a value between %d and %d" % min_value % max_value)    
    while True:
        inp = input()
        if inp == "stop":
            stop()
            break
        elif inp == "config":
            config()
            break	
        else:
            pi.set_servo_pulsewidth(ESC,inp)
            
# This is the auto calibration procedure of ESC    
def calibrate():   
    pi.set_servo_pulsewidth(ESC, 0)For first time launch, select calibrate
    print("Disconnect the battery and press Enter")
    inp = input()
    if inp == '':
        pi.set_servo_pulsewidth(ESC, max_value)
        print("Connect the battery now.. you will here two beeps, then wait for a gradual falling tone then press Enter")
        inp = input()
        if inp == '':            
            pi.set_servo_pulsewidth(ESC, min_value)
            print("Please wait")
            time.sleep(12)
            pi.set_servo_pulsewidth(ESC, 0)
            time.sleep(2)
            print("ESC is calibrated")
            config()
            
def control(): 
    print("Starting Motor... ensure that the motos has already been calibrated and armed")
    time.sleep(1)
    speed = neutral_value
    print("Controls - a to decrease speed & d to increase speed OR q to decrease a lot of speed & e to increase a lot of speed")
    while True:
        pi.set_servo_pulsewidth(ESC, speed)
        inp = input()
        
        if inp == "q":
            speed -= 100    # decrementing the speed by 100
            print("speed = %d" % speed)
        elif inp == "e":    
            speed += 100    # incrementing the speed by 100
            print("speed = %d" % speed)
        elif inp == "d":
            speed += 10     # incrementing the speed by 10
            print("speed = %d" % speed)
        elif inp == "a":
            speed -= 10     # decrementing the speed by 10
            print("speed = %d" % speed)
        elif inp == "stop":
            stop()          #going for the stop function
            break
        elif inp == "config":
            config()
            break	
        else:
            print("Invalid Input")
            
# This is the arming procedure of an ESC       
def arm(): 
    print("Connect the battery and press Enter")
    inp = input()    
    if inp == '':
        pi.set_servo_pulsewidth(ESC, 0)
        time.sleep(1)
        pi.set_servo_pulsewidth(ESC, max_value)
        time.sleep(1)
        pi.set_servo_pulsewidth(ESC, min_value)
        time.sleep(1)
        print("ESC is armed")
        config()
        
def stop(): #This will stop every action your Pi is performing for ESC ofcourse.
    pi.set_servo_pulsewidth(ESC, 0)
    pi.stop()

#Start of the program
config()
