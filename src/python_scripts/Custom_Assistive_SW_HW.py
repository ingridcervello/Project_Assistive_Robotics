import os
import time
import tkinter as tk
from tkinter import messagebox
from robodk.robolink import *
from robodk.robomath import *

# Define relative path to the .rdk file
#relative_path = "src/roboDK/Assistive_UR5e.rdk"
#absolute_path = os.path.abspath(relative_path)

# Start RoboDK with the project file
RDK = Robolink() #OBRIR MANUALMENT L'ARXIU DE ROBODK PER A EVITAR FINESTRA DE QUE S'ACABA LA PROVA GRATUITA
#RDK.AddFile(absolute_path)

# Retrieve items from the RoboDK station
robot = RDK.Item("UR5e")
base = RDK.Item("UR5e Base")
tool = RDK.Item('Hand')
Init_target = RDK.Item('Init')
Init_hi = RDK.Item('Init_hi')
Hi_right = RDK.Item('Hi_right')
Hi_left = RDK.Item('Hi_left')

# Set robot frame, tool and speed
robot.setPoseFrame(base)
robot.setPoseTool(tool)
robot.setSpeed(50)

# Connect to real robot or simulate
def robot_online(online):
    if online:
        robot.setConnectionParams('192.168.1.5', 30000, '/', 'anonymous', '')
        time.sleep(5)
        success = robot.ConnectSafe('192.168.1.5')
        time.sleep(5)
        status, status_msg = robot.ConnectedState()
        if status != ROBOTCOM_READY:
            raise Exception("Failed to connect: " + status_msg)
        RDK.setRunMode(RUNMODE_RUN_ROBOT)
        print("Connection to UR5e Successful!")
    else:
        RDK.setRunMode(RUNMODE_SIMULATE)
        print("Simulation mode activated.")

# Robot movements
def move_to_init():
    print("Init")
    robot.MoveL(Init_target, True)
    print("Init_target REACHED")


def hi():
    print("Hi!")
    robot.setSpeed(50)
    robot.MoveL(Init_hi, True)
    robot.setSpeed(100)
    robot.MoveL(Hi_left, True)
    robot.MoveL(Hi_right, True)
    robot.MoveL(Hi_left, True)
    robot.MoveL(Hi_right, True)
    robot.MoveL(Init_hi)

# Confirmation dialog to close RoboDK
def confirm_close():
    root = tk.Tk()
    root.withdraw()
    response = messagebox.askquestion(
        "Close RoboDK",
        "Do you want to save changes before closing RoboDK?",
        icon='question'
    )
    if response == 'yes':
        RDK.Save()
        RDK.CloseRoboDK()
        print("RoboDK saved and closed.")
    else:
        RDK.CloseRoboDK()
        print("RoboDK closed without saving.")

# Main function
def main():
    robot_online(False)  # True for real robot, False for simulation
    hi()

# Run main and handle closing
if __name__ == "__main__":
    main()
    #confirm_close()
    
