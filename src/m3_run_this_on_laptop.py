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
    teleop_frame, arm_frame, control_frame, driver_frame, sound_frame, m3_proximity_sensor_frame,\
        camera_frame, choose_pick_up_frame = get_shared_frames(main_frame, mqtt_sender)

    # -------------------------------------------------------------------------
    # Frames that are particular to my individual contributions to the project.
    # -------------------------------------------------------------------------
    # TODO: Implement and call get_my_frames(...)

    # -------------------------------------------------------------------------
    # Grid the frames.
    # -------------------------------------------------------------------------
    grid_frames(teleop_frame, arm_frame, control_frame, driver_frame, sound_frame, m3_proximity_sensor_frame,
                camera_frame, choose_pick_up_frame)

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
    m3_camera_frame = get_camera_frame(main_frame, mqtt_sender)
    choose_pick_up_frame = get_choose_pick_up_frame(main_frame, mqtt_sender)
    return teleop_frame, arm_frame, control_frame, driver_frame, sound_frame, \
        pick_up_with_proximity_sensor_frame, m3_camera_frame, choose_pick_up_frame


def grid_frames(teleop_frame, arm_frame, control_frame, driver_frame, sound_frame, pick_up_with_proximity_sensor_frame,
                camera_frame, choose_pick_up_frame):
    teleop_frame.grid(row=0, column=0)
    arm_frame.grid(row=1, column=0)
    control_frame.grid(row=2, column=0)
    driver_frame.grid(row=0, column=1)
    sound_frame.grid(row=1, column=1)
    pick_up_with_proximity_sensor_frame.grid(row=2, column=1)
    camera_frame.grid(row=3, column=1)
    choose_pick_up_frame.grid(row=3, column=0)


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
    go_button["command"] = lambda: handle_pick_up_with_proximity_sensor(initial_entry, rate_of_increase_entry,
                                                                        mqtt_sender)

    return frame


def get_camera_frame(window, mqtt_sender):
    frame = ttk.Frame(window, padding=10, borderwidth=5, relief="ridge")
    frame.grid()

    # Construct the widgets on the frame:
    frame_label1 = ttk.Label(frame, text="Turing speed: ")
    frame_label2 = ttk.Label(frame, text="Area: ")
    frame_label3 = ttk.Label(frame, text='Spin Until Sees Object')
    speed_entry = ttk.Entry(frame, width=8)
    area_entry = ttk.Entry(frame, width=8)
    clockwise_button = ttk.Button(frame, text='Clockwise')
    counter_clockwise_button = ttk.Button(frame, text='Counter Clockwise')

    # Grid the widgets:
    frame_label3.grid(row=0, column=1)
    frame_label1.grid(row=1, column=0)
    frame_label2.grid(row=1, column=3)
    speed_entry.grid(row=1, column=1)
    area_entry.grid(row=1, column=4)
    clockwise_button.grid(row=2, column=4)
    counter_clockwise_button.grid(row=2, column=1)

    # Set the Button callbacks:
    clockwise_button["command"] = lambda: handle_camera_clockwise(speed_entry, area_entry, mqtt_sender)
    counter_clockwise_button['command'] = lambda: handle_camera_counterclockwise(speed_entry, area_entry, mqtt_sender)

    return frame


def get_choose_pick_up_frame(window, mqtt_sender):
    frame = ttk.Frame(window, padding=10, borderwidth=5, relief="ridge")
    frame.grid()

    # Construct the widgets on the frame:
    frame_label1 = ttk.Label(frame, text="Turn and Choose Pick up Method")
    frame_label2 = ttk.Label(frame, text='Speed: ')
    frame_label3 = ttk.Label(frame, text='Area: ')
    frame_label4 = ttk.Label(frame, text='Direction: ')
    frame_label5 = ttk.Label(frame, text='Initial : ')
    frame_label6 = ttk.Label(frame, text="Rate of Increase: ")
    speed_entry = ttk.Entry(frame, width=8)
    area_entry = ttk.Entry(frame, width=8)
    direction_entry = ttk.Entry(frame, width=8)
    initial_entry = ttk.Entry(frame, width=8)
    rate_entry = ttk.Entry(frame, width=8)

    led_button = ttk.Button(frame, text='LED Method')
    beeping_button = ttk.Button(frame, text='Beeping Method')
    tone_button = ttk.Button(frame, text='Tone Method')

    # Grid the widgets:
    frame_label1.grid(row=0, column=1)
    frame_label2.grid(row=1, column=0)
    frame_label3.grid(row=2, column=0)
    frame_label4.grid(row=3, column=0)
    frame_label5.grid(row=4, column=0)
    frame_label6.grid(row=5, column=0)
    speed_entry.grid(row=1, column=1)
    area_entry.grid(row=2, column=1)
    direction_entry.grid(row=3, column=1)
    initial_entry.grid(row=4, column=1)
    rate_entry.grid(row=5, column=1)
    led_button.grid(row=6, column=0)
    beeping_button.grid(row=6, column=1)
    tone_button.grid(row=6, column=2)

    # Set the Button callbacks:
    led_button["command"] = lambda: handle_led(speed_entry, area_entry, direction_entry, initial_entry, rate_entry, mqtt_sender)
    beeping_button['command'] = lambda: handle_beep(speed_entry, area_entry, direction_entry, initial_entry, rate_entry, mqtt_sender)
    tone_button['command'] = lambda: handle_tone(speed_entry, area_entry, direction_entry, initial_entry, rate_entry, mqtt_sender)

    return frame


def handle_pick_up_with_proximity_sensor(initial_entry, rate_of_increase_entry, mqtt_sender):
    print("Initial:", initial_entry.get(), "Rate of increase:", rate_of_increase_entry.get())
    mqtt_sender.send_message("m3_led_proximity_sensor", [initial_entry.get(), rate_of_increase_entry.get()])


def handle_camera_clockwise(speed_entry, area_entry, mqtt_sender):
    print('Turning Speed:', speed_entry.get(), 'Area:', area_entry.get())
    mqtt_sender.send_message('m3_spin_clockwise_until_sees_object', [speed_entry.get(), area_entry.get()])


def handle_camera_counterclockwise(speed_entry, area_entry, mqtt_sender):
    print('Turning Speed:', speed_entry.get(), 'Area:', area_entry.get())
    mqtt_sender.send_message('m3_spin_counterclockwise_until_sees_object', [speed_entry.get(), area_entry.get()])


def handle_led(speed_entry, area_entry, direction_entry, initial_entry, rate_entry, mqtt_sender):
    print('LED Pick up Method')
    print('Speed:', speed_entry.get(), 'Area:', area_entry.get())
    print('Direction:', direction_entry.get())
    print("Initial:", initial_entry.get(), "Rate of increase:", rate_entry.get())
    mqtt_sender.send_message('m3_led_pick_up', [speed_entry.get(), area_entry.get(), direction_entry.get(),
                                                initial_entry.get(), rate_entry.get()])


def handle_beep(speed_entry, area_entry, direction_entry, initial_entry, rate_entry, mqtt_sender):
    print('Beep Pick up Method')
    print('Speed:', speed_entry.get(), 'Area:', area_entry.get())
    print('Direction:', direction_entry.get())
    print("Initial:", initial_entry.get(), "Rate of increase:", rate_entry.get())
    mqtt_sender.send_message('m3_beep_pick_up', [speed_entry.get(), area_entry.get(), direction_entry.get(),
                                                 initial_entry.get(), rate_entry.get()])


def handle_tone(speed_entry, area_entry, direction_entry, initial_entry, rate_entry, mqtt_sender):
    print('Tone Pick up Method')
    print('Speed:', speed_entry.get(), 'Area:', area_entry.get())
    print('Direction:', direction_entry.get())
    print("Initial:", initial_entry.get(), "Rate of increase:", rate_entry.get())
    mqtt_sender.send_message('m3_tone_pick_up', [speed_entry.get(), area_entry.get(), direction_entry.get(),
                                                 initial_entry.get(), rate_entry.get()])


# -----------------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# -----------------------------------------------------------------------------
main()
