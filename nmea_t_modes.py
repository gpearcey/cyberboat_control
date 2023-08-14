import os     #importing os library so as to communicate with the system
import pigpio #importing pigpio library

LSB = 23  #Connect to ESP32 pin 18
MSB = 24 # Connect to ESP32 pin 19

pi = pigpio.pi()

# --------------------------------------------------------------------------------------------------------
# Helper Functions
# --------------------------------------------------------------------------------------------------------------
      
def clear_screen():
    print("\033c", end="")

def show_menu(mode):
    print("==== CyberBoat Attack Modes ====")
    print("")
    print(" Current Mode: ",mode)
    print("")
    print("Select Mode:")
    print("1. Off")
    print("2. Passive")
    print("3. GPS Attack")
    #print("4. Extra")  
    print("q. Quit")

def get_choice():
    while True:
        choice = input("Enter your choice: ")
        if choice.lower() in ['1', '2', '3', '4','q']:
            return choice.lower()

    
# ----------------------------------------------------------------------------------------------------------------------
# Main Menu
# --------------------------------------------------------------------------------------------------------------------------
def main():
    clear_screen()
    manual_steering = False
    mode = "Passive"
    pi.write(LSB,1)
    pi.write(MSB,0)
    while True:
        show_menu(mode)
        choice = get_choice()
        if choice == '1':
            mode = "Off"
            pi.write(LSB,0)
            pi.write(MSB,0)            
            clear_screen()
        elif choice == '2':
            mode = "Passive"
            pi.write(LSB,1)
            pi.write(MSB,0)
            clear_screen()
        elif choice == '3':
            mode = "GPS Attack"
            pi.write(LSB,0)
            pi.write(MSB,1)
            clear_screen()
        elif choice == '4':
            mode = "Extra"
            pi.write(LSB,1)
            pi.write(MSB,1)
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
