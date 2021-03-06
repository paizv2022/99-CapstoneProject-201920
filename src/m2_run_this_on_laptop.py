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
    root.title('Capstone Project CSSE120-Samuel VanDenburgh')

    # -------------------------------------------------------------------------
    # The main frame, upon which the other frames are placed.
    # -------------------------------------------------------------------------
    main_frame = ttk.Frame(root, padding=10, borderwidth=5, relief='groove')
    main_frame.grid()

    # -------------------------------------------------------------------------
    # Sub-frames for the shared GUI that the team developed:
    # -------------------------------------------------------------------------
    teleop_frame, arm_frame, control_frame, driver_frame, sound_frame = get_shared_frames(main_frame, mqtt_sender)

    # -------------------------------------------------------------------------
    # Frames that are particular to my individual contributions to the project.
    # -------------------------------------------------------------------------
    # TODO: Implement and call get_my_frames(...)
    def get_infrared_frame(window, mqtt_sender):
        # creates frame
        frame = ttk.Frame(window, padding=10, borderwidth=5, relief="ridge")
        frame.grid()

        #creates widgets
        frame_label = ttk.Label(frame, text="Infrared")

        inches_label = ttk.Label(frame, text="inches")
        speed_label = ttk.Label(frame, text="speed")
        range_label = ttk.Label(frame, text="range")

        inches_entry = ttk.Entry(frame, width=8)
        speed_entry = ttk.Entry(frame, width=8)
        range_entry = ttk.Entry(frame, width=8)

        go_until_less_button = ttk.Button(frame, text="Go forwards until distance is less than inches")
        go_until_greater_button = ttk.Button(frame, text="Go backwards until distance is greater than inches")
        go_until_within_button = ttk.Button(frame, text="Go backwards or forwards until distance is within inches + or - range")

        #displays widgets
        frame_label.grid(row=0, column=1)
        inches_label.grid(row=1, column=0)
        speed_label.grid(row=1, column=1)
        range_label.grid(row=1, column=2)
        inches_entry.grid(row=2, column=0)
        speed_entry.grid(row=2, column=1)
        go_until_less_button.grid(row=3, column=1)
        range_entry.grid(row=2, column=2)
        go_until_greater_button.grid(row=4, column=1)
        go_until_within_button.grid(row=5, column=1)

        #sets buttons to run functions
        go_until_less_button["command"] = lambda: handle_go_until_less_than(mqtt_sender, inches_entry, speed_entry)
        go_until_greater_button["command"] = lambda: handle_go_until_greater_than(mqtt_sender, inches_entry, speed_entry)
        go_until_within_button["command"] = lambda: handle_go_until_within(mqtt_sender, range_entry, inches_entry, speed_entry)

        return frame

    def get_tone_frame(window, mqtt_sender):
        # creates frame
        frame = ttk.Frame(window, padding=10, borderwidth=5, relief="ridge")
        frame.grid()

        # creates widgets
        frame_label = ttk.Label(frame, text="Tone Frequency to Object")

        initial_frequency_label = ttk.Label(frame, text="inital frequency")
        frequency_rate_label = ttk.Label(frame, text="frequency increase rate (per inch)")

        initial_frequency_entry = ttk.Entry(frame, width=8)
        frequency_rate_entry = ttk.Entry(frame, width=8)

        start_tone_button = ttk.Button(frame, text="Start Playing Tone")
        stop_tone_button = ttk.Button(frame, text="Stop Playing Tone")
        pick_up_button = ttk.Button(frame, text="Pick up Object")

        # displays widgets
        frame_label.grid(row=0, column=1)
        initial_frequency_label.grid(row=1, column=0)
        frequency_rate_label.grid(row=1, column=2)
        initial_frequency_entry.grid(row=2, column=0)
        frequency_rate_entry.grid(row=2, column=2)
        start_tone_button.grid(row=2, column=1)
        stop_tone_button.grid(row=3, column=1)
        pick_up_button.grid(row=4, column=1)

        #sets buttons to run functions
        start_tone_button["command"] = lambda: handle_start_tone(mqtt_sender, initial_frequency_entry, frequency_rate_entry)
        stop_tone_button["command"] = lambda: handle_stop_tone(mqtt_sender)
        return frame

    def get_pick_up_frame(window, mqtt_sender):
        frame = ttk.Frame(window, padding=10, borderwidth=5, relief="ridge")
        frame.grid()

        frame_label = ttk.Label(frame, text='Find and pick up object')
        speed_label = ttk.Label(frame, text='Speed')
        spin_label = ttk.Label(frame, text='Spin direction (CC or CW)')
        initial_label = ttk.Label(frame, text='Initial frequency:')
        rate_label = ttk.Label(frame, text='Increase rate (Hz per Inch)')
        pick_up_label = ttk.Label(frame, text="find and pick up object")
        area_label = ttk.Label(frame, text="area (for camera to sense object)")


        speed_entry = ttk.Entry(frame, width=8)
        spin_entry = ttk.Entry(frame, width=8)
        initial_entry = ttk.Entry(frame, width=8)
        rate_entry = ttk.Entry(frame, width=8)
        area_entry = ttk.Entry(frame, width=8)

        pick_up_button = ttk.Button(frame, text='Find and Pick up')

        frame_label.grid(row=0, column=0)
        speed_label.grid(row=3, column=0)
        speed_entry.grid(row=4, column=0)
        spin_label.grid(row=1, column=0)
        spin_entry.grid(row=2, column=0)
        area_label.grid(row=5, column=0)
        area_entry.grid(row=6, column=0)
        initial_label.grid(row=7, column=0)
        initial_entry.grid(row=8, column=0)
        rate_label.grid(row=9, column=0)
        rate_entry.grid(row=10, column=0)
        pick_up_label.grid(row=11, column=0)
        pick_up_button.grid(row=12, column=0)

        pick_up_button["command"] = lambda: handle_pick_up(mqtt_sender, spin_entry, speed_entry, area_entry, initial_entry, rate_entry)

        return frame

    infrared_frame = get_infrared_frame(main_frame, mqtt_sender)
    tone_frame = get_tone_frame(main_frame, mqtt_sender)
    pick_up_Frame = get_pick_up_frame(main_frame, mqtt_sender)
    # -------------------------------------------------------------------------
    # Grid the frames.
    # -------------------------------------------------------------------------
    grid_frames(teleop_frame, arm_frame, control_frame, driver_frame, sound_frame, infrared_frame, tone_frame, pick_up_Frame)

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

    return teleop_frame, arm_frame, control_frame, driver_frame, sound_frame


def grid_frames(teleop_frame, arm_frame, control_frame, driver_frame, sound_frame, infrared_frame, tone_frame, pick_up_frame):
    #row = up + down, column = left and right
    teleop_frame.grid(row=0, column=0)
    arm_frame.grid(row=1, column=0)
    control_frame.grid(row=2, column=0)
    driver_frame.grid(row=0, column=1)
    sound_frame.grid(row=1, column=1)
    infrared_frame.grid(row=2, column=1)
    tone_frame.grid(row=0, column=2)
    pick_up_frame.grid(row=1, column=2)

###############################################################################
# Handlers for Buttons in the Infrared frame
###############################################################################
def handle_go_until_less_than(mqtt_sender, inches_entry, speed_entry):
    print("Driving forward until I am less than", inches_entry.get(), "inches from an object at a speed of", speed_entry.get())
    mqtt_sender.send_message("m2_go_forward_until_distance_is_less_than", [float(inches_entry.get()), float(speed_entry.get())])

def handle_go_until_greater_than(mqtt_sender, inches_entry, speed_entry):
    print("Driving backward until I am greater than", inches_entry.get(), "inches from an object at a speed of", speed_entry.get())
    mqtt_sender.send_message("m2_go_backward_until_distance_is_greater_than", [float(inches_entry.get()), float(speed_entry.get())])

def handle_go_until_within(mqtt_sender, range_entry, inches_entry, speed_entry):
    print("Driving forwards and backwards until I am within", inches_entry.get(), "+ or - ", range_entry.get(), "inches from an object at a speed of", speed_entry.get())
    mqtt_sender.send_message("m2_go_until_distance_is_within", [float(range_entry.get()) ,float(inches_entry.get()), float(speed_entry.get())])

###############################################################################
# Handlers for Buttons in the Tone frame
###############################################################################
def handle_start_tone(mqtt_sender, initial_frequency_entry, frequency_rate_entry):
    print("Playing a tone corresponding to IR distance starting at", initial_frequency_entry.get(), "Hz nd changing at a rate of", frequency_rate_entry.get(),"Hz per inch")
    mqtt_sender.send_message("m2_tone_to_distance", [float(initial_frequency_entry.get()), float(frequency_rate_entry.get())])

def handle_stop_tone(mqtt_sender):
    print("Stopping tone")
    mqtt_sender.send_message("m2_stop_tone")

###############################################################################
# Handler for Button in the pick_up frame
###############################################################################
def handle_pick_up(mqtt_sender, spin, speed, area, frequency, rate):
    print("Finding and Picking up object")
    mqtt_sender.send_message("m2_tone_and_camera_pick_up", [spin.get(), int(speed.get()), int(area.get()), int(frequency.get()), int(rate.get())])

# -----------------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# -----------------------------------------------------------------------------
main()


