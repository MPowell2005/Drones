'''
Author: Michael Powell 
Narrative
    This program allows the user to collect data for temperature in terms of height by using a Tello drone.

Features:
    - Allows the user to choose how the high the drone can go.
    - Allows the user to choose the height increment of the drone (height per data point).
    - Sends the data into a file of the user's choosing.

Bugs:
    - The drone cannot fly higher than 1000 centimeters due to "Big Wind Error."
    
Finished on May 3rd, 2022
@author: mpowell23
'''



# Imports
import math                                                                                                 # Import math. This will allow the program to use mathematical operations.
import time                                                                                                 # Import time. This will allow the program to pause for a certain amount of time.
from djitellopy import Tello                                                                                # Import the Tello. This will allow the program to access the drone's code.



def get_temperature_height(drone, height_increment, planned_height):
    '''
        Summary and Description of Function:
        This function returns a list that contains lists with two elements being height and temperature. 
        A list is a data structure that contains items called 'elements,' which may include strings, floats, tuples, or integers.
                
        Parameter(s):
        drone: The drone connected through Tello.
        height_increment (integer): The height that the drone goes up per data point.
        planned_height (integer): The maximum height the drone will reach.
        
        Returns:
        temperature_height_data (list): The list that relates the temperature in terms of the height at different increments.
    '''
    
    # Establishing the function's local variables.
    drone.connect()                                                                                         # Connect the drone to Tello.
    temperature_height_data = []                                                                            # Establish a list that collects temperature in terms of height.
    drone_height = 0                                                                                        # Set drone_height equal to 0.
    
    # Data Point 1 at height = 0.
    temperature_height_data.append([drone_height, drone.get_temperature()])                                 # Append a list into temperature_height_data that contains the drone height and the temperature using drone.get_temperature().
    print(temperature_height_data)                                                                          # Print the list onto the console.
    
    # Data Point 2 at take off height.
    drone.takeoff()                                                                                         # Let drone take off to 60 centimeters.
    drone_height = drone.get_height()                                                                       # Get the height at 60 centimeters.
    temperature_height_data.append([drone_height, drone.get_temperature()])                                 # Append a list into temperature_height_data that contains the drone height and the temperature using drone.get_temperature().
    print(temperature_height_data)                                                                          # Print the updated list onto the console.
    
    # Stop the drone for 2 seconds. This allows the drone to recover.
    time.sleep(2)
    
    # Remaining data points.
    while drone_height <= planned_height :                                                                  # Use a while loop to collect each temperature at each height increment.
        remaining_height = planned_height - drone_height                                                    # Establish a variable that gets the remaining height left.
        
        # Condition if the remaining height is less than 20 centimeters and cannot move up anymore. While loop breaks.
        if remaining_height < 20 :                                                                      
            break
        
        # Condition if the height increment is greater than the remaining height. This conditions ensures that the drone will not go above its planned height.
        elif height_increment > remaining_height :
            drone.move_up(remaining_height)         
        
        # Condition if the drone can move up its height increment.
        else :
            drone.move_up(height_increment)
        
        drone_height = drone.get_height()                                                                   # Get the drone's height.
        temperature_height_data.append([drone_height, drone.get_temperature()])                             # Append a list into temperature_height_data that contains the drone height and the temperature using drone.get_temperature().
        
        # Stop the drone for 2 seconds. This allows the drone to recover.
        time.sleep(2)
        
        print(temperature_height_data)                                                                      # Print the temperature_height_data list on the console.
    
    print('\nThe final height of the drone was ' + str(drone_height) + '.')                                 # Print the drone's final height onto the console.
    
    # Landing process
    drone_height = drone.get_height()                                                                       # Get the drone's height.
    while drone_height > 100 :                                                                              # While the drone's height is greater than 100, move the drone down.
        if drone_height > 500 :                                                                             # If the drone has a height greater than 500 centimeters, make it move down 500.
            drone_height = 560
        
        drone.move_down(drone_height - 60)                                                                  # Else, make it move down until it reaches 60 centimeters.
        drone_height = drone.get_height()                                                                   # Get the drone's height
    
    time.sleep(2)                                                                                           # Let the drone wait for 2 seconds.
    drone.land()                                                                                            # Make the drone land once its height is less than or equal to 100 centimeters.
        
    return temperature_height_data                                                                          # Return the temperature_height_data list.



def main():
    # Program Description.
    print('Dear user,\nThis program allows you to collect data for temperature in terms of height by using a Tello drone.\nThe data will be printed on the console as the drone moves up and eventually it will ask you to write it in a CSV.')
    # Activate the Tello import.
    drone = Tello()
    
    
    # Ask for the height increment.
    while True :
        height_increment = input('\nHow many centimeters do you want the drone to go up for each data point after its take off?\nYour height increment must be an integer greater than or equal to 20.\n')               
        height_increment = height_increment.strip()                                                         # Remove unnecessary spaces inserted by the user.
        
        try :
            height_increment = int(height_increment)                                                        # Try to convert the input into a float.
            
            if height_increment >= 20 :                                                                     # If the input is greater than 0, break the while True loop.
                break
            
            else :                                                                                          # If the input is not greater than zero, continue the while True loop.
                print('Please insert a height increment greater than or equal to 20 that is an integer.')
                continue
        
        except :                                                                                            # If the input cannot be converted into a float, continue the while True loop.
            print('Please insert a height increment greater than or equal to 20. Your value must be a integer.')
        
    
    # Ask for the planned height.
    while True :
        planned_height = input('\nWhat is the maximum height of the drone in centimeters?\nYour height must be an integer greater than or equal to 60.\n')                               
        planned_height = planned_height.strip()                                                             # Remove unnecessary spaces inserted by the user.
        
        try :  
            planned_height = int(planned_height)                                                            # Try to convert the input into a float.
            
            if planned_height >= 60 :                                                                       # If the input is greater than 0, break the while True loop.
                break
            
            else :                                                                                          # If the input is not greater than 0, continue the while True loop.
                print('Please insert a height that is greater than or equal to 60 centimeters.\n')
                continue
        
        except :                                                                                            # If the input cannot be converted into a float, continue the while True loop.
            print('Please insert a height that is greater than or equal to 60 centimeters. Your height must be an integer.\n')
            continue
    
    
    # Get a list with temperature and height.
    temperature_height = get_temperature_height(drone, height_increment, planned_height)                    # Use the get_temperature_height function to return a list relating height and temperature.
    print('\nThe drone collected the following data (height, temperature):')
    print(temperature_height)
    
    
    # Write the temperature_height list into a CSV.
    while True :
        file_name = input('\nWhat file do you want to write the data in?\n')                                # Ask the user for their file.
        file_name = file_name.strip()
        
        try :
            file_handle = open(file_name, 'w')                                                              # If the file can be found in the user's console, open the file in write mode.
            break
            
        except :
            print('Please insert a file name that is accessible on your computer.')
            continue
    
    file_handle.truncate()                                                                                  # Clear the contents of the file.
    file_handle.write('Height, Temperature')                                                                # Write a heading with height and temperature.
    file_handle.write('\n')                                                                                 # Put a line break in the file.
    for element in temperature_height :                                                                     # Write the elements into a CSV file.
        file_handle.write(str(element[0]) + ',' + str(element[1]))
        file_handle.write('\n')
    
    file_handle.close()                                                                                     # Close the file.
    
    
    
    print('The temperature in terms of the height data has been written into a CSV.')
    print('Thanks for using this program.')
if __name__ == '__main__':
    main()