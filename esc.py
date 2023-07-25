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
speed_step = 10           #Value to increment/decrement the speed by

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
        elif key == 'q':
            return "q"
        elif key == 'r':
            return "r"
        elif key == 'n':
            return "n"
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
                
def clear_screen():
    print("\033c", end="")

def show_menu():
    print("==== CyberBoat Propulsion and Steerting Menu ====")
    print("1. Calibrate ESC")
    print("2. Arm ESC")
    print("3. Manual Control ESC")
    print("4. Set Rudder Mode")
    print("5. Manual Control Rudder")    
    print("6. Control")
    print("q. Quit")

def get_choice():
    while True:
        choice = input("Enter your choice: ")
        if choice.lower() in ['1', '2', '3', '4', '5', '6', 'q']:
            return choice.lower()

# -------------------------------------------------------------------------------------------------------------------------
# Mode functions
# -------------------------------------------------------------------------------------------------------------------------
           


# Provides manual control over ESC inputs
def manual_control_esc(): 
    print("Select a value between %d and %d to set speed" % min_value % max_value)  
    print("Select 'n' to reset to neutral speed")
    print("Select 'm' to return to the menu")
    print("Select 'q' to quit") 
    while True:
        inp = input()
        if inp == "q":
            exit()
            break
        elif inp == "m":
            main()
            break	
        elif inp == "n":
            pi.set_servo_pulsewidth(ESC,neutral_value)
        else:
            pi.set_servo_pulsewidth(ESC,inp)
            
# This is the auto calibration procedure of ESC    
def calibrate_esc():   
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
            main()
   
# Allows incrementing and decrementing esc speed with arrow keys         
def control(): 
    print("Starting Motor... ensure that the motos has already been calibrated and armed")
    time.sleep(1)
    speed = neutral_value
    print("Up/Down arrow keys to control speed")
    print("Left/Right arrow keys to control rudder")
    print("Select 'n' to reset to neutral speed")
    print("Select 'r' to reset to straight rudder position")
    print("Select 'm' to return to the menu")
    print("Select 'q' to quit") 
    while True:
        speed = check_speed(speed)
        pi.set_servo_pulsewidth(ESC, speed)
        time.sleep(0.1)
        key = get_key()
        
        if key == "DOWN":
            speed -= speed_step    
            print("speed = %d" % speed)
        elif key == "UP":    
            speed += speed_step 
            print("speed = %d" % speed)
        elif key == "n":
            speed = neutral_value
            print("speed = %d" % speed)
        elif key == "q":
            exit()          #going for the stop function
            break
        elif key == "m":
            main()
            break	
        else:
            print("Invalid Input")
           
            
# This is the arming procedure of an ESC       
def arm_esc(): 
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
        main()
        
def exit(): #Stops all pigpio actions

    pi.set_servo_pulsewidth(ESC, 0)
    pi.stop()
    os.system ("sudo killall pigppiod") # Kill the pigpio daemon

#def set_rudder_mode():

#def control_rudder():
    
# ----------------------------------------------------------------------------------------------------------------------
# Main Menu
# --------------------------------------------------------------------------------------------------------------------------
def main():
    clear_screen()
    while True:
        show_menu()
        choice = get_choice()
        if choice == '1':
            calibrate_esc()
        elif choice == '2':
            arm_esc()
        elif choice == '3':
            manual_control_esc()
        elif choice == '4':
            set_rudder_mode()
        elif choice == '5':
            manual_rudder_control()
        elif choice == '6':
            control()
        elif choice == 'q':
            print("Exiting the program.")
            exit()
        else:
            print("Invalid Input")

#Start of the program
if __name__ == "__main__":
    main()