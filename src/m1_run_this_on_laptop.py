"""
  Capstone Project.  Code to run on a LAPTOP (NOT the robot).
  Displays the Graphical User Interface (GUI) and communicates with the robot.

  Authors:  Your professors (for the framework)
    and Valeria Paiz.
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
    root.title('Capstone Project CSSE120-Valeria Paiz')

    # -------------------------------------------------------------------------
    # The main frame, upon which the other frames are placed.
    # -------------------------------------------------------------------------
    main_frame = ttk.Frame(root, padding=10, borderwidth=5, relief='groove')
    main_frame.grid()

    # -------------------------------------------------------------------------
    # Sub-frames for the shared GUI that the team developed:
    # -------------------------------------------------------------------------
    teleop_frame, arm_frame, control_frame, driver_frame, sound_frame, colors_frame, collect_frames = get_shared_frames(main_frame, mqtt_sender)

    # -------------------------------------------------------------------------
    # Grid the frames.
    # -------------------------------------------------------------------------
    grid_frames(teleop_frame, arm_frame, control_frame, driver_frame, sound_frame, colors_frame, collect_frames)

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
    color_frames = color_frame(main_frame, mqtt_sender)
    collect_frames = collect_frame(main_frame, mqtt_sender)

    return teleop_frame, arm_frame, control_frame, driver_frame, sound_frame, color_frames, collect_frames


def grid_frames(teleop_frame, arm_frame, control_frame, driver_frame, sound_frame, color_frames, collect_frames):
    teleop_frame.grid(row=0, column=0)
    arm_frame.grid(row=1, column=0)
    driver_frame.grid(row=2, column=0)
    sound_frame.grid(row=3, column=0)
    control_frame.grid(row=4, column=0)
    collect_frames.grid(row=0, column=1)
    color_frames.grid(row=1, column=1)


def color_frame(window, mqtt_sender):
    frame = ttk.Frame(window, padding=10, borderwidth=5, relief="ridge")
    frame.grid()

    frame_label = ttk.Label(frame, text='Color Sensor')
    intensity_label = ttk.Label(frame, text='Intensity:')
    color_label = ttk.Label(frame, text='Color:')
    go_label = ttk.Label(frame, text='Go Until:')
    blank_label = ttk.Label(frame, text='')
    go2_label = ttk.Label(frame, text='Go Until:')

    intensity_entry = ttk.Entry(frame, width=8)
    color_entry = ttk.Entry(frame, width=8)

    greater_int_button = ttk.Button(frame, text='Intensity is Greater')
    smaller_int_button = ttk.Button(frame, text='Intensity is Smaller')
    is_color_button = ttk.Button(frame, text='Color is')
    is_not_color_button = ttk.Button(frame, text='Color is Not')

    frame_label.grid(row=0, column=3)
    intensity_label.grid(row=1, column=0)
    intensity_entry.grid(row=1, column=1)
    color_label.grid(row=3, column=0)
    color_entry.grid(row=3, column=1)
    go_label.grid(row=1, column=2)
    go2_label.grid(row=3, column=2)
    greater_int_button.grid(row=1, column=3)
    smaller_int_button.grid(row=1, column=4)
    is_color_button.grid(row=3, column=3)
    is_not_color_button.grid(row=3, column=4)
    blank_label.grid(row=2, column=0)

    greater_int_button["command"] = lambda: handle_greater_int(mqtt_sender, intensity_entry)
    smaller_int_button["command"] = lambda: handle_smaller_int(mqtt_sender, intensity_entry)
    is_color_button["command"] = lambda: handle_is_color(mqtt_sender, color_entry)
    is_not_color_button["command"] = lambda: handle_is_not_color(mqtt_sender, color_entry)

    return frame


def collect_frame(window, mqtt_sender):
    frame = ttk.Frame(window, padding=10, borderwidth=5, relief="ridge")
    frame.grid()

    frame_label = ttk.Label(frame, text='Collect Objects')
    speed_label = ttk.Label(frame, text='Speed:')
    direction_label = ttk.Label(frame, text='Direction (CW or CCW) & Area:')
    initial_label = ttk.Label(frame, text='Initial Rate:')
    rate_label = ttk.Label(frame, text='Increase Rate:')

    speed_entry = ttk.Entry(frame, width=8)
    direction_entry = ttk.Entry(frame, width=8)
    initial_entry = ttk.Entry(frame, width=8)
    rate_entry = ttk.Entry(frame, width=8)
    area_entry = ttk.Entry(frame, width=8)

    pick_up_button = ttk.Button(frame, text='Pick Up Object')
    camera_pick_up_button = ttk.Button(frame, text='Pick Up Object with Camera')

    frame_label.grid(row=0, column=1)
    speed_label.grid(row=1, column=0)
    direction_label.grid(row=4, column=0)
    initial_label.grid(row=3, column=0)
    rate_label.grid(row=2, column=0)
    speed_entry.grid(row=1, column=2)
    direction_entry.grid(row=4, column=1)
    area_entry.grid(row=4, column=2)
    initial_entry.grid(row=3, column=2)
    rate_entry.grid(row=2, column=2)
    pick_up_button.grid(row=5, column=0)
    camera_pick_up_button.grid(row=5, column=2)

    pick_up_button["command"] = lambda: handle_pick_up(mqtt_sender, initial_entry, rate_entry, speed_entry)
    camera_pick_up_button["command"] = lambda: handle_camera_pick_up(mqtt_sender, initial_entry, rate_entry, speed_entry, direction_entry, area_entry)

    return frame


def handle_greater_int(mqtt_sender, intensity_entry):
    mqtt_sender.send_message("m1_greater_intensity", [intensity_entry.get()])


def handle_smaller_int(mqtt_sender, intensity_entry):
    mqtt_sender.send_message("m1_smaller_intensity", [intensity_entry.get()])


def handle_is_color(mqtt_sender, color_entry):
    mqtt_sender.send_message("m1_color_is", [color_entry.get()])


def handle_is_not_color(mqtt_sender, color_entry):
    mqtt_sender.send_message("m1_color_is_not", [color_entry.get()])


def handle_pick_up(mqtt_sender, initial_entry, rate_entry, speed_entry):
    mqtt_sender.send_message("m1_pick_up", [initial_entry.get(), rate_entry.get(), speed_entry.get()])


def handle_camera_pick_up(mqtt_sender, initial_entry, rate_entry, speed_entry, direction_entry, area_entry):
    mqtt_sender.send_message("m1_camera_pick_up", [initial_entry.get(), rate_entry.get(), speed_entry.get(), direction_entry.get(), area_entry.get()])


# -----------------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# -----------------------------------------------------------------------------
main()