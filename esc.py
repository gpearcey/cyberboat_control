# This program controls a ESC. This program is designed specifically for the BlueRobotics T200
# Make sure your battery is not connected if you are going to calibrate it at first.
# If you get a message that says 'Can't initialise pigpio library', the pigpio daemon likely needs to be restarted. Run "sudo killall pigpiod" then rerun the program.

import os     #importing os library so as to communicate with the system
import time 
os.system ("sudo pigpiod") # Start the pigpio daemon
time.sleep(1) # Delay to let the pigpio library initialize
import pigpio #importing pigpio library
import readchar

ESC=4  #Connect the ESC to this GPIO pin 

pi = pigpio.pi()
pi.set_servo_pulsewidth(ESC, 0) 

max_value = 1900          #ESC max value - max forwards thrust
neutral_value = 1500      #ESC neutral_value 
min_value = 1100          #ESC min value - max backwards thrust

print("Please Calibrate the ESC before arming")

# --------------------------------------------------------------------------------------------------------
# Helper Functions
# --------------------------------------------------------------------------------------------------------------

# Processes user input - returns a string
def get_key():
    while True:
        key = readchar.readkey()
        if key == '\x1b[A': 
            return "UP"
        elif key == '\x1b[B': 
            return "DOWN"
        elif key == '\x1b[C': 
            return "RIGHT"
        elif key == '\x1b[D': 
            return "LEFT"
        elif key == 'm':
            return "m"
        elif key == 's':
            return "s"
        elif key == 'r':
            return "r"
        else:
            return "INVALID"
        
# Limits the speed if the input speedis greater than the max value, or less than the min value 
def check_speed(speed):
    if speed > max_value:
        return max_value
    elif speed < min_value:
        return min_value
    else:
        return speed        
                
# -------------------------------------------------------------------------------------------------------------------------
# Mode functions
# -------------------------------------------------------------------------------------------------------------------------
           


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
    pi.set_servo_pulsewidth(ESC, 0)
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
   
# Allows incrementing and decrementing esc speed with arrow keys         
def control(): 
    print("Starting Motor... ensure that the motos has already been calibrated and armed")
    time.sleep(1)
    speed = neutral_value
    print("Controls - up arrow to increase, down arrow to increase, c to go to config menu, s to stop")
    while True:
        speed = check_speed(speed);
        pi.set_servo_pulsewidth(ESC, speed)
        time.sleep(0.1)
        key = get_arrow_key()
        
        if key == "DOWN":
            speed -= 10    # decrementing the speed by 10
            print("speed = %d" % speed)
        elif key == "UP":    
            speed += 10    # incrementing the speed by 10
            print("speed = %d" % speed)
        elif key == "s":
            stop()          #going for the stop function
            break
        elif key == "c":
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
        
def stop(): #Stops all pigpio actions

    pi.set_servo_pulsewidth(ESC, 0)
    pi.stop()
    os.system ("sudo killall pigppiod") # Kill the pigpio daemon
    
# ----------------------------------------------------------------------------------------------------------------------
# Main Menu
# --------------------------------------------------------------------------------------------------------------------------
def menu():
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
            break
        else:
            print("Invalid input")

#Start of the program
menu()
