import os
import time
import socket
import tkinter as tk
from tkinter import messagebox
from math import radians, degrees, pi
import numpy as np
from robodk.robolink import *
from robodk.robomath import *

# Load RoboDK project from relative path
relative_path = "src/roboDK/Assistive_UR5e.rdk"
absolute_path = os.path.abspath(relative_path)
RDK = Robolink()
#RDK.AddFile(absolute_path)

# Robot setup
robot = RDK.Item("UR5e")
base = RDK.Item("UR5e Base")
tool = RDK.Item('Hand')
Init_target = RDK.Item('Init')
Init_hi_target = RDK.Item("Init_hi")
Hi_left_target = RDK.Item("Hi_left")
Hi_right_target = RDK.Item("Hi_right")
Init_dj_target = RDK.Item("Init_dj") 
Dj_left_target = RDK.Item("Dj_left")
Dj_right_target = RDK.Item("Dj_right")

robot.setPoseFrame(base)
robot.setPoseTool(tool)
robot.setSpeed(20)

# Robot Constants
ROBOT_IP = '192.168.1.5'
ROBOT_PORT = 30002
accel_mss = 1.2
speed_ms = 0.75
blend_r = 0.0
timej = 6
timel = 4
time_high = 3

# URScript commands
set_tcp = "set_tcp(p[0.000000, 0.000000, 0.050000, 0.000000, 0.000000, 0.000000])"
#movej_init = f"movej([-1.009423, -1.141297, -1.870417, 3.011723, -1.009423, 0.000000],1.20000,0.75000,{timel},0.0000)"
#movel_app_shake = f"movel([-2.268404, -1.482966, -2.153143, -2.647089, -2.268404, 0.000000],{accel_mss},{speed_ms},{timel},0.000)"
#movel_shake = f"movel([-2.268404, -1.663850, -2.294637, -2.324691, -2.268404, 0.000000],{accel_mss},{speed_ms},{timel/2},0.000)"
#movel_app_give5 = f"movel([-2.280779, -1.556743, -2.129529, 5.257071, -1.570796, 2.280779],{accel_mss},{speed_ms},{timel},0.000)"
#movel_give5 = f"movel([-2.195869, -1.642206, -2.040971, 5.253965, -1.570796, 2.195869],{accel_mss},{speed_ms},{timel/2},0.000)"

#Init
j1, j2, j3, j4, j5, j6 = list(np.radians(Init_target.Joints()).tolist()[0])
movej_init = f"movej([{j1},{j2}, {j3}, {j4}, {j5}, {j6}],{accel_mss},{speed_ms},{time_high},{blend_r})"
#Init_hi
j1, j2, j3, j4, j5, j6 = list(np.radians(Init_hi_target.Joints()).tolist()[0])
movej_init_hi = f"movel([{j1},{j2}, {j3}, {j4}, {j5}, {j6}],{accel_mss},{speed_ms},{time_high},{blend_r})"
#Hi_right
j1, j2, j3, j4, j5, j6 = list(np.radians(Hi_right_target.Joints()).tolist()[0])
#X, Y, Z, Roll, Pitch, Yaw = Pose_2_TxyzRxyz(Hi_right_target.Pose())
#movel_hi_right = f"movel(p[{X}, {Y}, {Z}, {Roll}, {Pitch}, {Yaw}], a={accel_mss}, v={speed_ms}, t={timel}, r={blend_r})"
movel_hi_right = f"movel([{j1},{j2}, {j3}, {j4}, {j5}, {j6}],{accel_mss},{speed_ms},{time_high},{blend_r})"

#Hi_left
j1, j2, j3, j4, j5, j6 = list(np.radians(Hi_left_target.Joints()).tolist()[0])
#X, Y, Z, Roll, Pitch, Yaw = Pose_2_TxyzRxyz(Hi_left_target.Pose())
#movel_hi_left = f"movel(p[{X}, {Y}, {Z}, {Roll}, {Pitch}, {Yaw}], a={accel_mss}, v={speed_ms}, t={timel}, r={blend_r})"
movel_hi_left = f"movel([{j1},{j2}, {j3}, {j4}, {j5}, {j6}],{accel_mss},{speed_ms},{time_high},{blend_r})"

#Init_dj
j1, j2, j3, j4, j5, j6 = list(np.radians(Init_dj_target.Joints()).tolist()[0])
movej_init_dj = f"movej([{j1},{j2}, {j3}, {j4}, {j5}, {j6}],{accel_mss},{speed_ms},{time_high},{blend_r})"
#Dj_right
X, Y, Z, Roll, Pitch, Yaw = Pose_2_TxyzRxyz(Dj_right_target.Pose())
movel_dj_right = f"movel(p[{X}, {Y}, {Z}, {Roll}, {Pitch}, {Yaw}], a={accel_mss}, v={speed_ms}, t={timel}, r={blend_r})"
#Dj_left
X, Y, Z, Roll, Pitch, Yaw = Pose_2_TxyzRxyz(Dj_left_target.Pose())
movel_dj_left = f"movel(p[{X}, {Y}, {Z}, {Roll}, {Pitch}, {Yaw}], a={accel_mss}, v={speed_ms}, t={timel}, r={blend_r})"


# Check robot connection
def check_robot_port(ip, port):
    global robot_socket
    try:
        robot_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        robot_socket.settimeout(1)
        robot_socket.connect((ip, port))
        return True
    except (socket.timeout, ConnectionRefusedError):
        return False
# Send URScript command
def send_ur_script(command):
    robot_socket.send((command + "\n").encode())

# Wait for robot response
def receive_response(t):
    time.sleep(t)

# Movements
def Init():
    print("Init")
    robot.MoveL(Init_target, True)
    print("Init_target REACHED")
    if robot_is_connected:
        print("Init REAL UR5e")
        send_ur_script(set_tcp)
        receive_response(1)
        send_ur_script(movej_init)
        receive_response(timej)
    else:
        print("UR5e not connected. Simulation only.")

def hi():
    print("Hi!")
    robot.setSpeed(20)
    robot.MoveL(Init_hi_target, True)
    robot.MoveL(Hi_right_target, True)
    robot.MoveL(Hi_left_target, True)
    robot.MoveL(Hi_right_target, True)
    robot.MoveL(Hi_left_target, True)
    robot.MoveL(Init_hi_target, True)
    print("Hi FINISHED")
    if robot_is_connected:
        print("App_hi REAL UR5e")
        send_ur_script(set_tcp)
        receive_response(1)
        send_ur_script(movej_init_hi)
        receive_response(timel)
        send_ur_script(movel_hi_right)
        receive_response(timel)
        send_ur_script(movel_hi_left)
        receive_response(timel)
        send_ur_script(movel_hi_right)
        receive_response(timel)
        send_ur_script(movel_hi_left)
        receive_response(timel)
        
def dj():
    print("DJ")
    robot.setSpeed(50)
    robot.MoveL(Init_dj_target, True)
    robot.MoveL(Dj_right_target, True)
    robot.MoveL(Dj_left_target, True)
    robot.MoveL(Dj_right_target, True)
    robot.MoveL(Dj_left_target, True)
    robot.MoveL(Init_dj_target, True)
    print("DJ FINISHED")
    if robot_is_connected:
        print("App_dj REAL UR5e")
        send_ur_script(set_tcp)
        receive_response(1)
        send_ur_script(movej_init_dj)
        receive_response(timel)
        send_ur_script(movel_dj_right)
        receive_response(timel)
        send_ur_script(movel_dj_left)
        receive_response(timel)
        send_ur_script(movel_dj_right)
        receive_response(timel)
        send_ur_script(movel_dj_left)
        receive_response(timel)

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
    global robot_is_connected
    robot_is_connected = check_robot_port(ROBOT_IP, ROBOT_PORT)
    hi()
    #dj()
    if robot_is_connected:
        robot_socket.close()

# Run and close
if __name__ == "__main__":
    main()
    #confirm_close()