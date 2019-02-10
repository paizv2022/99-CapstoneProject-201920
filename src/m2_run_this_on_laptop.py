"""
  Capstone Project.  Code to run on a LAPTOP (NOT the robot).
  Displays the Graphical User Interface (GUI) and communicates with the robot.

  Authors:  Your professors (for the framework)
    and Samuel VanDenburgh.
  Winter term, 2018-2019.
"""

import mqtt_remote_method_calls as com
import tkinter
from tkinter import ttk
import shared_gui


def main():
    """
    This code, which must run on a LAPTOP:
      1. Constructs a GUI for my part of the Capstone Project.
      2. Communicates via MQTT with the code that runs on the EV3 robot.
    """
    # -------------------------------------------------------------------------
    # Construct and connect the MQTT Client:
    # -------------------------------------------------------------------------

    mqtt_sender = com.MqttClient()
    mqtt_sender.connect_to_ev3()

    # -------------------------------------------------------------------------
    # The root TK object for the GUI:
    # -------------------------------------------------------------------------

    root = tkinter.Tk()
    root.title("CSSE 120 Capstone Project, Winter 2018-2019")

    # -------------------------------------------------------------------------
    # The main frame, upon which the other frames are placed.
    # -------------------------------------------------------------------------

    main_frame = ttk.Frame(root, padding=10, borderwidth=5, relief='groove')
    main_frame.grid()

    # -------------------------------------------------------------------------
    # Sub-frames for the shared GUI that the team developed:
    # -------------------------------------------------------------------------

    teleop_frame, arm_frame, control_frame, driver_frame = get_shared_frames(main_frame, mqtt_sender)

    # -------------------------------------------------------------------------
    # Frames that are particular to my individual contributions to the project.
    # -------------------------------------------------------------------------
    # TODO: Implement and call get_my_frames(...)

    # -------------------------------------------------------------------------
    # Grid the frames.
    # -------------------------------------------------------------------------
    grid_frames(teleop_frame, arm_frame, control_frame, driver_frame)
    # -------------------------------------------------------------------------
    # The event loop:
    # -------------------------------------------------------------------------

    root.mainloop()


def get_shared_frames(main_frame, mqtt_sender):
    teleop_frame = shared_gui.get_teleoperation_frame(main_frame, mqtt_sender)
    arm_frame = shared_gui.get_arm_frame(main_frame, mqtt_sender)
    control_frame = shared_gui.get_control_frame(main_frame, mqtt_sender)
    driver_frame = shared_gui.get_driver_frame(main_frame, mqtt_sender)

    return teleop_frame, arm_frame, control_frame, driver_frame

def grid_frames(teleop_frame, arm_frame, control_frame, driver_frame):
    teleop_frame.grid(row=0, column=0)
    arm_frame.grid(row=1, column = 0)
    control_frame.grid(row=2, column=0)
    driver_frame.grid(row=0,column=1)


def handle_go_for_seconds(mqtt_sender, seconds_entry, speed_entry):
    print("Go Straight for", seconds_entry.get(), "seconds at a speed of", speed_entry.get())
    mqtt_sender.send_message("go_straight_for_seconds", [seconds_entry.get(), speed_entry.get()])


def handle_go_for_inches_encoder(mqtt_sender, inches_entry, speed_entry):
    print("Go Straight for", seconds_entry.get(), "inches at a speed of", speed_entry.get(), "using encoder")
    mqtt_sender.send_message("go_straight_for_inches_using_encoder", [inches_entry.get(), speed_entry.get()])


def handle_go_for_inches_encoder(mqtt_sender, inches_entry, speed_entry):
    print("Go Straight for", seconds_entry.get(), "inches at a speed of", speed_entry.get(), "using time")
    mqtt_sender.send_message("go_straight_for_inches_using_time", [inches_entry.get(), speed_entry.get()])

def get_driver_frame(window, mqtt_sender):
    #creates frame
    frame = ttk.Frame(window, padding=10, borderwidth=5, relief="ridge")
    frame.grid()


    # feature 6 widgets
    frame_label = ttk.Label(frame, text="Driver")
    seconds_label = ttk.Label(frame, text="Seconds")
    inches_label = ttk.Label(frame, text="Inches")
    speed_label = ttk.Label(frame, text="Speed")

    seconds_input = ttk.Entry(frame, width=8)
    inches_input = ttk.Entry(frame, width=8)
    speed_input = ttk.Entry(frame, width=8)

    go_for_sec_button = ttk.Button(frame, text="go for seconds")
    go_for_inches_encoder_button = ttk.Button(frame, text="go for inches (encoder)")
    go_for_inches_time_button = ttk.Button(frame, text="go for inches (time-based)")

    #grids the buttons/labels/entry boxes
    frame_label.grid(row=0, column=1)
    seconds_label.grid(row=1, column=0)
    inches_label.grid(row=1, column=2)
    speed_label.grid(row=1,column=1)

    go_for_sec_button.grid(row=3, column=1)
    go_for_inches_encoder_button.grid(row=4, column=0)
    go_for_inches_time_button.grid(row=4, column=2)

    seconds_input.grid(row=2, column=0)
    inches_input.grid(row=2, column=2)
    speed_input.grid(row=2, column=1)
    return frame

# -----------------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# -----------------------------------------------------------------------------
main()