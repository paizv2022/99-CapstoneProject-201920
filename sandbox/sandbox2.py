# Put whatever you want in this module and do whatever you want with it.
# It exists here as a place where you can "try out" things without harm.

import mqtt_remote_method_calls as com
import tkinter
from tkinter import ttk
from tkinter import *
import shared_gui
import random

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
    # Frames for the type racer game
    # -------------------------------------------------------------------------
    def get_title_frame(window):
        # creates frame
        frame = ttk.Frame(window, padding=10, borderwidth=5, relief="ridge")
        frame.grid()

        #creates widgets
        style = ttk.Style()

        button = ttk.Button(window, width=8)
        root.title("Robot Type Racer")
        photo = PhotoImage(file='Type Racer title.gif')
        graphic = ttk.Label(window, image=photo)
        graphic.image = photo

        #displays widgets
        graphic.grid(row=0, column=0)
        button.grid(row=0, column=0)
        return frame

    def get_game_frame(window, mqtt_sender):
        speed = 0
        # creates frame
        frame = ttk.Frame(window, padding=10, borderwidth=5, relief="ridge")
        frame.grid()
        ttk.Style().configure("TFrame", background="black")

        #creates widgets
        frame_label = ttk.Label(frame, text="Enter the Below Word to make the robot move faster")

        word = pick_word()
        word_display = ttk.Label(frame, text=word)

        word_entry = ttk.Entry(frame, width=10)

        enter_button = ttk.Button(frame, text="Enter Word")

        start_button = ttk.Button(frame, text="Start Game")
        stop_button = ttk.Button(frame, text="Stop Game")
        ttk.Style().configure("TButton", relief="flat", background="green", foreground="green", inground="red")

        #displays widgets
        frame_label.grid(row=0 , column=1)
        word_display.grid(row=1, column=1)

        word_entry.grid(row=2, column=1)

        enter_button.grid(row=3, column=1)
        start_button.grid(row=2, column=0)
        #stop_button.grid(row=2, column=3)

        #sets buttons to speed up or stop robot depending on if the input is correct.
        start_button["command"] = lambda: handle_start_game(mqtt_sender)
        enter_button["command"] = lambda: handle_word_entry(mqtt_sender, word, str(word_entry.get()))
        return frame

    title_frame = get_title_frame(main_frame)
    game_frame = get_game_frame(main_frame, mqtt_sender)
    # -------------------------------------------------------------------------
    # Grid the frames.
    # -------------------------------------------------------------------------
    grid_frames(title_frame, game_frame)

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


def grid_frames(title_frame, game_frame):
    #row = up and down, column = left and right
    title_frame.grid(row=0 , column=0)
    game_frame.grid(row=1, column=0)

###############################################################################
# Handlers for Buttons in the game frame
###############################################################################
def handle_word_entry(mqtt_sender, word, word_entry):
    print("Input entered, checking and responding to input.")
    if len(word) != len(word_entry):
        print("Word incorrect, stopping")
        mqtt_sender.send_message("m2_stop")
        return
    else:
        for k in range (len(word_entry)):
            if word_entry[k] != word[k]:
                print("Word incorrect, stopping")
                mqtt_sender.send_message("m2_stop")
                return
    print("word correct, speeding up")
    mqtt_sender.send_message("m2_speed_up")
    return

def handle_start_game(mqtt_sender):
    print("starting game")
    mqtt_sender.send_message("m2_start_game")

#pick word for type racer game
def pick_word():
    with open('words.txt') as f:
        f.readline()
        string = f.read()
    words = string.split()
    r = random.randrange(0, len(words))
    picked = words[r]
    word = []
    for k in range (len(picked)):
        word = word + [picked[k]]
    string = ""
    for k in range (len(word)):
        string = string + str(word[k])
    print(string)
    return string

# -----------------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# -----------------------------------------------------------------------------
main()