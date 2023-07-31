# This program controls a ESC. This program is designed specifically for the BlueRobotics T200
# Make sure your battery is not connected if you are going to calibrate it at first.
# If you get a message that says 'Can't initialise pigpio library', the pigpio daemon likely needs to be restarted. Run "sudo killall pigpiod" then rerun the program.

import os     #importing os library so as to communicate with the system
import time 
os.system ("sudo killall pigppiod") # Kill any exsiting pigpiod daemon
os.system ("sudo pigpiod") # Start the pigpio daemon
time.sleep(1) # Delay to let the pigpio library initialize
import pigpio #importing pigpio library
import readchar
import serial

ESC=4  #Connect the ESC to this GPIO pin 
RUDDER_MODE_PIN = 17

pi = pigpio.pi()
pi.set_servo_pulsewidth(ESC, 0) 

max_forward = 1900          #ESC max value - max forwards thrust
neutral_value = 1500      #ESC neutral_value 
max_reverse = 1100          #ESC min value - max backwards thrust
speed_step = 10           #Value to increment/decrement the speed by
angle_step = 1
max_angle = 180
min_angle = 0
straight_rudder = 90
manual_steering = True

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
    if speed > max_forward:
        return max_forward
    elif speed < max_reverse:
        return max_reverse
    else:
        return speed    
        
def check_angle(angle):
    if angle > max_angle:
        return max_angle
    elif angle < min_angle:
        return min_angle
    else:
        return angle      
                
def clear_screen():
    print("\033c", end="")

def show_menu():
    print("==== CyberBoat Propulsion and Steerting Menu ====")
    print("1. Calibrate ESC")
    print("2. Arm ESC")
    print("3. Manual Control ESC")
    print("4. Set Steering Mode")  
    print("5. Control")
    print("q. Quit")

def get_choice():
    while True:
        choice = input("Enter your choice: ")
        if choice.lower() in ['1', '2', '3', '4', '5', 'q']:
            return choice.lower()
def get_steering_choice():
    while True:
        choice = input("Enter your choice: ")
        if choice.lower() in ['1', '2','q']:
            return choice.lower()

# -------------------------------------------------------------------------------------------------------------------------
# Mode functions
# -------------------------------------------------------------------------------------------------------------------------
           


# Provides manual control over ESC inputs
def manual_control_esc(): 
    print("Select a value between %d and %d to set speed" %(max_reverse,max_forward))  
    print("Select 'n' to reset to neutral speed")
    print("Select 'm' to return to the menu")
    print("Select 'q' to quit") 
    while True:
        inp = input()
        if inp == "q":
            pi.set_servo_pulsewidth(ESC,neutral_value)
            exit()
            break
        elif inp == "m":
            pi.set_servo_pulsewidth(ESC,neutral_value)
            return	
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
        pi.set_servo_pulsewidth(ESC, max_forward)
        print("Connect the battery, wait for the beeps, and press Enter")
        inp = input()
        if inp == '':            
            pi.set_servo_pulsewidth(ESC, max_reverse)
            print("Please wait")
            time.sleep(12)
            pi.set_servo_pulsewidth(ESC, 0)
            time.sleep(2)
            print("ESC is calibrated")
            return
   
# Allows incrementing and decrementing esc speed with arrow keys         
def control_esc(): 
    print("Starting Motor... ensure that the motos has already been calibrated and armed")
    time.sleep(1)
    speed = neutral_value
    angle = straight_rudder
    print("Up/Down arrow keys to control speed")
    print("Select 'n' to reset to neutral speed")
    print("Select 'r' to reset to straight rudder position")
    print("Select 'm' to return to the menu")
    print("Select 'q' to quit") 
    while True:
        speed = check_speed(speed)
        angle = check_angle(angle)
        pi.set_servo_pulsewidth(ESC, speed)
        time.sleep(0.01)
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
            pi.set_servo_pulsewidth(ESC,neutral_value)
            exit()          #going for the stop function
            break
        elif key == "m":
            pi.set_servo_pulsewidth(ESC,neutral_value)
            return

            break	
        else:
            print("Invalid Input")
           
# Allows incrementing and decrementing esc speed with arrow keys         
def control_esc_and_rudder(): 
    ser = serial.Serial('/dev/ttyACM0',9600,timeout=1)
    ser.reset_input_buffer()
    print("Starting Motor... ensure that the motos has already been calibrated and armed")
    print("Please wait... calibrating servo")
    time.sleep(11)
    speed = neutral_value
    angle = straight_rudder
    print("Up/Down arrow keys to control speed")
    print("Left/Right arrow keys to control rudder")
    print("Select 'n' to reset to neutral speed")
    print("Select 'r' to reset to straight rudder position")
    print("Select 'm' to return to the menu")
    print("Select 'q' to quit") 
    while True:
        speed = check_speed(speed)
        angle = check_angle(angle)
        pi.set_servo_pulsewidth(ESC, speed)
        ser.write(b"%d\n" % angle)
        time.sleep(0.01)
        key = get_key()
        
        if key == "DOWN":
            speed -= speed_step    
            print("speed = %d" % speed)
        elif key == "UP":    
            speed += speed_step 
            print("speed = %d" % speed)
        elif key == "LEFT":     # turn to starboard side - increment
            angle = angle + angle_step; 
            print("angle = %d" % angle)
        elif key == "RIGHT":    # turn to port side - decrement
            angle = angle - angle_step
            print("angle = %d" % angle)
        elif key == "n":
            speed = neutral_value
            print("speed = %d" % speed)
        elif key == "q":
            pi.set_servo_pulsewidth(ESC,neutral_value)
            ser = serial.Serial('/dev/ttyACM0',9600,timeout=1).close()
            exit()          #going for the stop function
            break
        elif key == "m":
            pi.set_servo_pulsewidth(ESC,neutral_value)
            ser = serial.Serial('/dev/ttyACM0',9600,timeout=1).close()
            return

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
        pi.set_servo_pulsewidth(ESC, max_forward)
        time.sleep(1)
        pi.set_servo_pulsewidth(ESC, max_reverse)
        time.sleep(1)
        print("ESC is armed")
        return
        
def exit(): #Stops all pigpio actions

    pi.set_servo_pulsewidth(ESC, 0)
    pi.stop()
    os.system ("sudo killall pigppiod") # Kill the pigpio daemon

def set_rudder_mode():
    clear_screen()
    invalid = False
    while True:
        if (invalid == True):
            print("Invalid Input")
        print("==== Steering Mode Menu ====")
        print("1. Enable Autopilot")
        print("2. Manual")
        print("q. Return")
        choice = get_steering_choice();
        if (choice == '1'):
            pi.write(RUDDER_MODE_PIN,0)
            return False
        elif (choice == '2'):
            os.system ("sudo systemctl stop pypilot.service")
            pi.write(RUDDER_MODE_PIN,1);
            return True
        elif (choice == 'q'):
            return False
        else:
            invalid = True
            

     
    
# ----------------------------------------------------------------------------------------------------------------------
# Main Menu
# --------------------------------------------------------------------------------------------------------------------------
def main():
    clear_screen()
    manual_steering = False
    while True:
        show_menu()
        choice = get_choice()
        if choice == '1':
            calibrate_esc()
            clear_screen()
        elif choice == '2':
            arm_esc()
            clear_screen()
        elif choice == '3':
            manual_control_esc()
            clear_screen()
        elif choice == '4':
            manual_steering = set_rudder_mode()
            clear_screen()
        elif choice == '5':
            if (manual_steering == True):
                control_esc_and_rudder()
            else:
                control_esc()
            clear_screen()
        elif choice == 'q':
            print("Exiting the program.")
            exit()
            break
        else:
            print("Invalid Input")

#Start of the program
if __name__ == "__main__":

    main()
