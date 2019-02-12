"""
  Capstone Project.  Code to run on a LAPTOP (NOT the robot).
  Displays the Graphical User Interface (GUI) and communicates with the robot.

  Authors:  Your professors (for the framework)
    and Justin Heinz.
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
    root.title('CSSE 120 Capstone Project, winter 2018-19')

    # -------------------------------------------------------------------------
    # The main frame, upon which the other frames are placed.
    # -------------------------------------------------------------------------
    main_frame = ttk.Frame(root, padding=10, borderwidth=5, relief='groove')
    main_frame.grid()

    # -------------------------------------------------------------------------
    # Sub-frames for the shared GUI that the team developed:
    # -------------------------------------------------------------------------
    teleop_frame, arm_frame, control_frame, driver_frame, sound_frame, pick_up_with_proximity_sensor_frame = get_shared_frames(main_frame, mqtt_sender)

    # -------------------------------------------------------------------------
    # Frames that are particular to my individual contributions to the project.
    # -------------------------------------------------------------------------
    # TODO: Implement and call get_my_frames(...)

    # -------------------------------------------------------------------------
    # Grid the frames.
    # -------------------------------------------------------------------------
    grid_frames(teleop_frame, arm_frame, control_frame, driver_frame, sound_frame, pick_up_with_proximity_sensor_frame)

    # -------------------------------------------------------------------------
    # The event loop:
    # -------------------------------------------------------------------------
    root.mainloop()


def get_shared_frames(main_frame, mqtt_sender):
    teleop_frame = shared_gui.get_teleoperation_frame(main_frame, mqtt_sender)
    arm_frame = shared_gui.get_arm_frame(main_frame, mqtt_sender)
    control_frame = shared_gui.get_control_frame(main_frame, mqtt_sender)
    driver_frame = shared_gui.get_driver_frame(main_frame, mqtt_sender)
    sound_frame = shared_gui.get_sound_frame(main_frame, mqtt_sender)
    pick_up_with_proximity_sensor_frame = get_pick_up_with_proximity_sensor_frame(main_frame, mqtt_sender)
    return teleop_frame, arm_frame, control_frame, driver_frame, sound_frame, pick_up_with_proximity_sensor_frame


def grid_frames(teleop_frame, arm_frame, control_frame, driver_frame, sound_frame, pick_up_with_proximity_sensor_frame):
    teleop_frame.grid(row=0, column=0)
    arm_frame.grid(row=1, column=0)
    control_frame.grid(row=2, column=0)
    driver_frame.grid(row=0, column=1)
    sound_frame.grid(row=1, column=1)
    pick_up_with_proximity_sensor_frame.grid(row=2, column=1)


def get_pick_up_with_proximity_sensor_frame(window, mqtt_sender):
    frame = ttk.Frame(window, padding=10, borderwidth=5, relief="ridge")
    frame.grid()

    # Construct the widgets on the frame:
    frame_label1 = ttk.Label(frame, text="Initial: ")
    frame_label2 = ttk.Label(frame, text="Rate of Increase: ")
    initial_entry = ttk.Entry(frame, width=8)
    rate_of_increase_entry = ttk.Entry(frame, width=8)
    go_button = ttk.Button(frame, text='Go')

    # Grid the widgets:
    frame_label1.grid(row=0, column=0)
    frame_label2.grid(row=0, column=3)
    initial_entry.grid(row=0, column=1)
    rate_of_increase_entry.grid(row=0, column=4)
    go_button.grid(row=0, column=5)

    # Set the Button callbacks:
    go_button["command"] = lambda: handle_pick_up_with_proximity_sensor(initial_entry, rate_of_increase_entry, mqtt_sender)

    return frame


def handle_pick_up_with_proximity_sensor(initial_entry, rate_of_increase_entry, mqtt_sender):
    print("Initial", initial_entry.get(), "Rate of increase", rate_of_increase_entry.get())
    mqtt_sender.send_message("pick_up_with_proximity_sensor", [initial_entry.get(), rate_of_increase_entry.get()])

# -----------------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# -----------------------------------------------------------------------------
main()