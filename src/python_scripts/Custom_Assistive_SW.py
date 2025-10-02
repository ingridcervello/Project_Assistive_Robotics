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
RDK = Robolink()
#RDK.AddFile(absolute_path)

# Retrieve items from the RoboDK station
robot = RDK.Item("UR5e")
base = RDK.Item("UR5e Base")
tool = RDK.Item("Hand")
Init_target = RDK.Item("Init")
App_shake_target = RDK.Item("App_shake")
Shake_target = RDK.Item("Shake")
App_give5_target = RDK.Item("App_give5")
Give5_target = RDK.Item("Give5")
Init_hi_target = RDK.Item("Init_hi")
Hi_left_target = RDK.Item("Hi_left")
Hi_right_target = RDK.Item("Hi_right")
Init_dj_target = RDK.Item("Init_dj")
Dj_right_target = RDK.Item("Dj_right")
Dj_left_target = RDK.Item("Dj_left")

# Set robot frame, tool and speed
robot.setPoseFrame(base)
robot.setPoseTool(tool)
robot.setSpeed(20)


    
# Perform "Hi" sequence
def say_hi():
    print("Saying Hi!")
    robot.setSpeed(20)
    robot.MoveL(Init_dj_target, True)
    robot.MoveL(Hi_right_target, True)
    robot.MoveL(Hi_left_target, True)
    robot.MoveL(Hi_right_target, True)
    robot.MoveL(Hi_left_target, True)
    robot.MoveL(Init_hi_target, True)
    print("Saying Hi! FINISHED")
    
def dj():
    print("DJ!")
    robot.setSpeed(50)
    robot.MoveL(Init_dj_target, True)
    robot.MoveL(Dj_right_target, True)
    robot.MoveL(Dj_left_target, True)
    robot.MoveL(Dj_right_target, True)
    robot.MoveL(Dj_left_target, True)
    robot.MoveL(Init_dj_target, True)
    print("DJ! FINISHED")

# Main sequence
def main():
    say_hi()
    dj()

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

# Run main and handle closing
if __name__ == "__main__":
    main()
    #confirm_close()
