"""
Author: Jordan Angus @CL_Projects
Version: Python 3.9
Description: This program launches a designated function(on_app_launch) once
a target app(app_name) has been executed.
"""
import psutil
import os

# Function to be executed when a particular application is launched
"""
Description: Downloads the necessary modules for the sequence of programs expected to run as
a result of entering this method.
Input: None
Output: None
"""
def on_app_launch():
    print("The target app has been launched!")
    """
    os.system("pip install pygame")
    os.system("pip install pytube")
    os.system("pip install google-api-python-client")
    
    # Virtual Environment is under works...
    os.system("pip3 install virtualenv")
    os.system("virtualenv venv")
    os.system("source venv/bin/activate")
    os.system("venv/bin/pip install google-api-python-client")
    """
    os.chdir('/Users/clever_lazinezz/Documents/Terminal_Projects')
    os.system('Python "Collect Data Script.py" https://example-files.online-convert.com/document/txt/example.txt')
    

# Application to be monitored - needs additional work across os systems(maybe change to target_app_name)
app_name = "Music"

# Continuously monitor the list of running processes for the target application. 
# ISSUE 1(Resolved): Executes on_app_launch function repeatedly. Add a break from the loop 
# once the target app is executed and on_app_launch function has been called a SINGLE time
while True:
    for process in psutil.process_iter():
        try:
            # Check if the process name matches the application name
            if process.name() == app_name:
                on_app_launch()
                break
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    # Goes to next while loop iteration - done to create a break statement for when
    # the target app is launched so the on_app_launch function is only called once
    else:
        continue
    
    break

"""
Alternative Periodic Monitoring Code:
# Periodically checks if the target application has been executed
while True:
    # Gets a list of running processes
    running_processes = [p.name() for p in psutil.process_iter()]

    # Checks if target application is running
    if app_name in running_processes:
        # If the target application was just launched, this executes the on_app_launch() function
        if app_name not in last_running_processes:
            on_app_launch()

    # Store the current list of running processes for comparison in the next loop iteration
    last_running_processes = running_processes

    # Sleep for a short interval before checking again
    time.sleep(1)
"""
        
        
        
"""
Important Info:
psutil.process_iter() is a function provided by the Python library psutil.
It returns an iterator that yields a psutil.Process object for every running
process on the system. Each psutil.Process object provides various information
and methods related to the process, such as its name, ID, memory usage, CPU 
usage, status, and more. You can use this information to monitor, manage, or 
analyze the running processes on the system.
"""