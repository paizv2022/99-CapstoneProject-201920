"""
  Capstone Project.  Code to run on a LAPTOP (NOT the robot).
  Constructs and returns Frame objects for the basics:
  -- teleoperation
  -- arm movement
  -- stopping the robot program

  This code is SHARED by all team members.  It contains both:
    -- High-level, general-purpose methods for a Snatch3r EV3 robot.
    -- Lower-level code to interact with the EV3 robot library.

  Author:  Your professors (for the framework and lower-level code)
    and Samuel VanDenburgh, Valeria Paiz, and Justin Heinz.
  Winter term, 2018-2019.
"""

import tkinter
from tkinter import ttk


def get_teleoperation_frame(window, mqtt_sender):
    """
    Constructs and returns a frame on the given window, where the frame
    has Entry and Button objects that control the EV3 robot's motion
    by passing messages using the given MQTT Sender.
      :type  window:       ttk.Frame | ttk.Toplevel
      :type  mqtt_sender:  com.MqttClient
    """
    # Construct the frame to return:
    frame = ttk.Frame(window, padding=10, borderwidth=5, relief="ridge")
    frame.grid()

    # Construct the widgets on the frame:
    frame_label = ttk.Label(frame, text="Teleoperation")
    left_speed_label = ttk.Label(frame, text="Left wheel speed (0 to 100)")
    right_speed_label = ttk.Label(frame, text="Right wheel speed (0 to 100)")

    left_speed_entry = ttk.Entry(frame, width=8)
    left_speed_entry.insert(0, "100")
    right_speed_entry = ttk.Entry(frame, width=8, justify=tkinter.RIGHT)
    right_speed_entry.insert(0, "100")

    forward_button = ttk.Button(frame, text="Forward")
    backward_button = ttk.Button(frame, text="Backward")
    left_button = ttk.Button(frame, text="Left")
    right_button = ttk.Button(frame, text="Right")
    stop_button = ttk.Button(frame, text="Stop")

    # Grid the widgets:
    frame_label.grid(row=0, column=1)
    left_speed_label.grid(row=1, column=0)
    right_speed_label.grid(row=1, column=2)
    left_speed_entry.grid(row=2, column=0)
    right_speed_entry.grid(row=2, column=2)

    forward_button.grid(row=3, column=1)
    left_button.grid(row=4, column=0)
    stop_button.grid(row=4, column=1)
    right_button.grid(row=4, column=2)
    backward_button.grid(row=5, column=1)

    # Set the button callbacks:
    forward_button["command"] = lambda: handle_forward(
        left_speed_entry, right_speed_entry, mqtt_sender)
    backward_button["command"] = lambda: handle_backward(
        left_speed_entry, right_speed_entry, mqtt_sender)
    left_button["command"] = lambda: handle_left(
        left_speed_entry, right_speed_entry, mqtt_sender)
    right_button["command"] = lambda: handle_right(
        left_speed_entry, right_speed_entry, mqtt_sender)
    stop_button["command"] = lambda: handle_stop(mqtt_sender)

    return frame


def get_arm_frame(window, mqtt_sender):
    """
    Constructs and returns a frame on the given window, where the frame
    has Entry and Button objects that control the EV3 robot's Arm
    by passing messages using the given MQTT Sender.
      :type  window:       ttk.Frame | ttk.Toplevel
      :type  mqtt_sender:  com.MqttClient
    """
    # Construct the frame to return:
    frame = ttk.Frame(window, padding=10, borderwidth=5, relief="ridge")
    frame.grid()

    # Construct the widgets on the frame:
    frame_label = ttk.Label(frame, text="Arm and Claw")
    position_label = ttk.Label(frame, text="Desired arm position:")
    position_entry = ttk.Entry(frame, width=8)

    raise_arm_button = ttk.Button(frame, text="Raise arm")
    lower_arm_button = ttk.Button(frame, text="Lower arm")
    calibrate_arm_button = ttk.Button(frame, text="Calibrate arm")
    move_arm_button = ttk.Button(frame,
                                 text="Move arm to position (0 to 5112)")
    blank_label = ttk.Label(frame, text="")

    # Grid the widgets:
    frame_label.grid(row=0, column=1)
    position_label.grid(row=1, column=0)
    position_entry.grid(row=1, column=1)
    move_arm_button.grid(row=1, column=2)

    blank_label.grid(row=2, column=1)
    raise_arm_button.grid(row=3, column=0)
    lower_arm_button.grid(row=3, column=1)
    calibrate_arm_button.grid(row=3, column=2)

    # Set the Button callbacks:
    raise_arm_button["command"] = lambda: handle_raise_arm(mqtt_sender)
    lower_arm_button["command"] = lambda: handle_lower_arm(mqtt_sender)
    calibrate_arm_button["command"] = lambda: handle_calibrate_arm(mqtt_sender)
    move_arm_button["command"] = lambda: handle_move_arm_to_position(
        position_entry, mqtt_sender)

    return frame


def get_control_frame(window, mqtt_sender):
    """
    Constructs and returns a frame on the given window, where the frame has
    Button objects to exit this program and/or the robot's program (via MQTT).
      :type  window:       ttk.Frame | ttk.Toplevel
      :type  mqtt_sender:  com.MqttClient
    """
    # Construct the frame to return:
    frame = ttk.Frame(window, padding=10, borderwidth=5, relief="ridge")
    frame.grid()

    # Construct the widgets on the frame:
    frame_label = ttk.Label(frame, text="Control")
    quit_robot_button = ttk.Button(frame, text="Stop the robot's program")
    exit_button = ttk.Button(frame, text="Stop this and the robot's program")

    # Grid the widgets:
    frame_label.grid(row=0, column=1)
    quit_robot_button.grid(row=1, column=0)
    exit_button.grid(row=1, column=2)

    # Set the Button callbacks:
    quit_robot_button["command"] = lambda: handle_quit(mqtt_sender)
    exit_button["command"] = lambda: handle_exit(mqtt_sender)

    return frame


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

    # Set the button callbacks:
    go_for_sec_button["command"] = lambda: handle_go_for_seconds(mqtt_sender,
        seconds_input, speed_input)
    go_for_inches_encoder_button["command"] = lambda: handle_go_for_inches_encoder(mqtt_sender,
        inches_input, speed_input)
    go_for_inches_time_button["command"] = lambda: handle_go_for_inches_time(mqtt_sender,
        inches_input, speed_input)

    return frame

def get_sound_frame(window, mqtt_sender):
    frame = ttk.Frame(window, padding=10, borderwidth=5, relief="ridge")
    frame.grid()

    frame_label = ttk.Label(frame, text="Sounds")
    number_label = ttk.Label(frame, text="Number")
    frequency_label = ttk.Label(frame, text="Frequency")
    phrase_label = ttk.Label(frame, text='Phrase')
    duration_label = ttk.Label(frame, text='Duration')

    number_entry = ttk.Entry(frame, width=8)
    frequency_entry = ttk.Entry(frame, width=8)
    phrase_entry = ttk.Entry(frame, width=8)
    duration_entry = ttk.Entry(frame, width=8)

    beep_button = ttk.Button(frame, text='Beep')
    tone_button = ttk.Button(frame, text='Tone')
    phrase_button = ttk.Button(frame, text='Speak')

    frame_label.grid(row=0, column=1)
    number_label.grid(row=1, column=0)
    frequency_label.grid(row=1, column=1)
    duration_label.grid(row=1, column=2)
    phrase_label.grid(row=1, column=3)

    number_entry.grid(row=2, column=0)
    frequency_entry.grid(row=2, column=1)
    duration_entry.grid(row=2, column=2)
    phrase_entry.grid(row=2, column=3)

    beep_button.grid(row=3, column=0)
    tone_button.grid(row=3, column=1)
    phrase_button.grid(row=3, column=3)

    beep_button["command"] = lambda: handle_beep(number_entry, mqtt_sender)
    tone_button["command"] = lambda: handle_play_tone(frequency_entry, duration_entry, mqtt_sender)
    phrase_button["command"] = lambda: handle_speak(phrase_entry, mqtt_sender)

    return frame


###############################################################################
# Handlers for Buttons in the Teleoperation frame.
###############################################################################
def handle_forward(left_entry_box, right_entry_box, mqtt_sender):
    """
    Tells the robot to move using the speeds in the given entry boxes,
    with the speeds used as given.
      :type  left_entry_box:   ttk.Entry
      :type  right_entry_box:  ttk.Entry
      :type  mqtt_sender:      com.MqttClient
    """
    print("Forward", left_entry_box.get(), right_entry_box.get())
    mqtt_sender.send_message("go", [left_entry_box.get(),
                                    right_entry_box.get()])


def handle_backward(left_entry_box, right_entry_box, mqtt_sender):
    """
    Tells the robot to move using the speeds in the given entry boxes,
    but using the negatives of the speeds in the entry boxes.
      :type  left_entry_box:   ttk.Entry
      :type  right_entry_box:  ttk.Entry
      :type  mqtt_sender:      com.MqttClient
    """
    print("Backward", left_entry_box.get(), right_entry_box.get())
    left = -int(left_entry_box.get())
    right = -int(right_entry_box.get())
    mqtt_sender.send_message("go", [str(left), str(right)])


def handle_left(left_entry_box, right_entry_box, mqtt_sender):
    """
    Tells the robot to move using the speeds in the given entry boxes,
    but using the negative of the speed in the left entry box.
      :type  left_entry_box:   ttk.Entry
      :type  right_entry_box:  ttk.Entry
      :type  mqtt_sender:      com.MqttClient
    """
    print("Left", left_entry_box.get(), right_entry_box.get())
    left = -int(left_entry_box.get())
    right = right_entry_box.get()
    mqtt_sender.send_message("go", [str(left), right])


def handle_right(left_entry_box, right_entry_box, mqtt_sender):
    """
    Tells the robot to move using the speeds in the given entry boxes,
    but using the negative of the speed in the right entry box.
      :type  left_entry_box:   ttk.Entry
      :type  right_entry_box:  ttk.Entry
      :type  mqtt_sender:      com.MqttClient
    """
    print("Right", left_entry_box.get(), right_entry_box.get())
    left = left_entry_box.get()
    right = -int(right_entry_box.get())
    mqtt_sender.send_message("go", [left, str(right)])


def handle_stop(mqtt_sender):
    """
    Tells the robot to stop.
      :type  mqtt_sender:  com.MqttClient
    """
    print("Stop")
    mqtt_sender.send_message("stop")


###############################################################################
# Handlers for Buttons in the ArmAndClaw frame.
###############################################################################
def handle_raise_arm(mqtt_sender):
    """
    Tells the robot to raise its Arm until its touch sensor is pressed.
      :type  mqtt_sender:  com.MqttClient
    """
    print('Raise Arm')
    mqtt_sender.send_message("raise_arm")


def handle_lower_arm(mqtt_sender):
    """
    Tells the robot to lower its Arm until it is all the way down.
      :type  mqtt_sender:  com.MqttClient
    """
    print('Lower Arm')
    mqtt_sender.send_message("lower_arm")


def handle_calibrate_arm(mqtt_sender):
    """
    Tells the robot to calibrate its Arm, that is, first to raise its Arm
    until its touch sensor is pressed, then to lower its Arm until it is
    all the way down, and then to mark taht position as position 0.
      :type  mqtt_sender:  com.MqttClient
    """
    print('Calibrate Arm')
    mqtt_sender.send_message("calibrate_arm")


def handle_move_arm_to_position(arm_position_entry, mqtt_sender):
    """
    Tells the robot to move its Arm to the position in the given Entry box.
    The robot must have previously calibrated its Arm.
      :type  arm_position_entry  ttk.Entry
      :type  mqtt_sender:        com.MqttClient
    """
    print('Move to Position', arm_position_entry.get())
    mqtt_sender.send_message("move_arm_to_position", [arm_position_entry.get()])


###############################################################################
# Handlers for Buttons in the Control frame.
###############################################################################
def handle_quit(mqtt_sender):
    """
    Tell the robot's program to stop its loop (and hence quit).
      :type  mqtt_sender:  com.MqttClient
    """
    print('Quit')
    mqtt_sender.send_message("quit")


def handle_exit(mqtt_sender):
    """
    Tell the robot's program to stop its loop (and hence quit).
    Then exit this program.
      :type mqtt_sender: com.MqttClient
    """
    print('Exit')
    mqtt_sender.send_message("exit")


###############################################################################
# Handlers for Buttons in the Driver frame.
###############################################################################
def handle_go_for_seconds(mqtt_sender, seconds_entry, speed_entry):
    print("Go Straight for", seconds_entry.get(), "seconds at a speed of", speed_entry.get())
    mqtt_sender.send_message("go_straight_for_seconds", [seconds_entry.get(), speed_entry.get()])


def handle_go_for_inches_encoder(mqtt_sender, inches_entry, speed_entry):
    print("Go Straight for", inches_entry.get(), "inches at a speed of", speed_entry.get(), "using encoder")
    mqtt_sender.send_message("go_straight_for_inches_using_encoder", [inches_entry.get(), speed_entry.get()])


def handle_go_for_inches_time(mqtt_sender, inches_entry, speed_entry):
    print("Go Straight for", inches_entry.get(), "inches at a speed of", speed_entry.get(), "using time")
    mqtt_sender.send_message("go_straight_for_inches_using_time", [inches_entry.get(), speed_entry.get()])
    

###############################################################################
# Handlers for Buttons in the Sounds frame.
###############################################################################
def handle_beep(number_entry, mqtt_sender):
    """
    Tell the robot's program to stop its loop (and hence quit).
      :type  mqtt_sender:  com.MqttClient
      :type  number_entry:   ttk.Entry
    """
    print('Beep', number_entry.get())
    mqtt_sender.send_message("beep", [number_entry.get()])


def handle_play_tone(frequency_entry, duration_entry, mqtt_sender):
    """
    Tell the robot's program to stop its loop (and hence quit).
      :type  mqtt_sender:  com.MqttClient
      :type  frequency_entry:   ttk.Entry
      :type  duration_entry:    ttk.Entry
    """
    print('Play Tone', frequency_entry.get(), duration_entry.get())
    mqtt_sender.send_message("play_tone", [frequency_entry.get(), duration_entry.get()])


def handle_speak(phrase_entry, mqtt_sender):
    """
    Tell the robot's program to stop its loop (and hence quit).
      :type  mqtt_sender:  com.MqttClient
      :type  phrase_entry:   ttk.Entry
    """
    print('Speak', phrase_entry.get())
    mqtt_sender.send_message("speak", [phrase_entry.get()])