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
import random
import math


class RobotLoc(object):
    def __init__(self, frame):
        self.canvas = tkinter.Canvas(frame, width=500, height=500, background='darkgrey')
        self.current_setting = "initial_gui"
        self.x = 0
        self.y = 0
        self.direction = 0
        self.direction_label = ttk.Label(frame, text="Robot Angle: " + str(self.direction))
        self.boxes = []
        for k in range(5):
            box = boxLoc()
            if k == 4:
                box.isTreasure = True
            box.x = random.randint(0, 500 - 32)
            box.y = random.randint(0, 500 - 32)
            self.boxes.append(box)

    def update_canvas(self):
        self.canvas.delete("all")
        self.direction_label['text'] = "Robot Angle: " + str(self.direction)
        self.canvas.create_oval(self.x, self.y, self.x+32, self.y+32, fill="black")
        for k in range(len(self.boxes)):
            if not self.boxes[k].isTreasure:
                self.canvas.create_rectangle(self.boxes[k].x, self.boxes[k].y, self.boxes[k].x + 32, self.boxes[k].y + 32, fill="red")
            else:
                self.canvas.create_rectangle(self.boxes[k].x, self.boxes[k].y, self.boxes[k].x + 32, self.boxes[k].y + 32, fill="green")


class boxLoc(object):
    def __init__(self):
        self.x = 0
        self.y = 0
        self.isTreasure = False


class LaptopResponder(object):
    def __init__(self, robot_gui):
        """
            :type robot_gui: RobotLoc
        """
        self.robot_gui = robot_gui

    def update_robot_gui(self, inches_traveled):
        self.robot_gui.x += ((math.cos(self.robot_gui.direction)) * inches_traveled) * 11.1
        self.robot_gui.y += (-(math.sin(self.robot_gui.direction)) * inches_traveled) * 11.1
        self.robot_gui.update_canvas()

    def update_robot_direction(self, angle):
        self.robot_gui.direction += angle
        if self.robot_gui.direction > 360:
            self.robot_gui.direction -= 360
        elif self.robot_gui.direction < -360:
            self.robot_gui.direction += 360
        self.robot_gui.update_canvas()


def sprint_3():
    root = tkinter.Tk()
    root.title('Final Capstone Project CSSE120-Valeria Paiz')

    main_frame = ttk.Frame(root, padding=10, borderwidth=5, relief='groove')
    main_frame.grid()

    initial_frame = initial_gui(main_frame)
    initial_frame.grid(row=0, column=0)

    root.mainloop()


def initial_gui(window):
    frame = ttk.Frame(window, padding=10, borderwidth=5, relief="ridge")
    frame.grid()

    robot_gui = RobotLoc(frame)

    delegate = LaptopResponder(robot_gui)
    mqtt_sender = com.MqttClient(delegate)
    mqtt_sender.connect_to_ev3()

    frame_label = ttk.Label(frame, text='Sprint 3: No Help')
    forward_label = ttk.Label(frame, text='Speed (0 to 100)')
    angle_label = ttk.Label(frame, text='Turn Angle (0 to 180)')
    empty_label = ttk.Label(frame, text='')
    empty2_label = ttk.Label(frame, text='')

    forward_slider = ttk.Scale(frame, from_=0, to=100)
    angle_slider = ttk.Scale(frame, from_=0, to=180)

    forward_button = ttk.Button(frame, text='Forward')
    backward_button = ttk.Button(frame, text='Backward')
    stop_button = ttk.Button(frame, text='Stop')
    left_button = ttk.Button(frame, text='Left')
    right_button = ttk.Button(frame, text='Right')
    switch_button = ttk.Button(frame, text='Help Frame')

    chosen_speed_label = ttk.Label(frame, text='Speed: ' + str(forward_slider.get()))
    chosen_angle_label = ttk.Label(frame, text='Angle: ' + str(angle_slider.get()))

    frame_label.grid(row=0, column=1)
    forward_label.grid(row=1, column=0)
    angle_label.grid(row=1, column=2)
    forward_slider.grid(row=2, column=0)
    angle_slider.grid(row=2, column=2)
    empty_label.grid(row=3, column=0)
    forward_button.grid(row=4, column=1)
    backward_button.grid(row=6, column=1)
    stop_button.grid(row=5, column=1)
    left_button.grid(row=5, column=0)
    right_button.grid(row=5, column=2)
    empty2_label.grid(row=7, column=0)
    switch_button.grid(row=8, column=1)
    chosen_speed_label.grid(row=9, column=1)
    chosen_angle_label.grid(row=10, column=1)

    forward_button["command"] = lambda: handle_forward(mqtt_sender, forward_slider)
    backward_button["command"] = lambda: handle_backward(mqtt_sender, forward_slider)
    stop_button["command"] = lambda: handle_stop(mqtt_sender)
    left_button["command"] = lambda: handle_left(mqtt_sender, angle_slider)
    right_button["command"] = lambda: handle_right(mqtt_sender, angle_slider)
    switch_button["command"] = lambda: handle_switch(robot_gui, forward_slider, forward_button, forward_label,
                                                     backward_button, stop_button, left_button, right_button,
                                                     angle_slider, angle_label, empty2_label, empty_label, switch_button,
                                                     frame_label, chosen_speed_label, chosen_angle_label)

    frame.bind_all('<Key-w>', lambda event: handle_forward(mqtt_sender, forward_slider))
    frame.bind_all('<Key-s>', lambda event: handle_backward(mqtt_sender, forward_slider))
    frame.bind_all('<Key-a>', lambda event: handle_left(mqtt_sender, angle_slider))
    frame.bind_all('<Key-d>', lambda event: handle_right(mqtt_sender, angle_slider))
    frame.bind_all('<Key-x>', lambda event: handle_stop(mqtt_sender))

    return frame

def handle_forward(mqtt_sender, forward_slider):
    mqtt_sender.send_message("m1_forward", [forward_slider.get()])


def handle_stop(mqtt_sender):
    mqtt_sender.send_message("m1_stop", [])


def handle_backward(mqtt_sender, forward_slider):
    speed = int(forward_slider.get())
    mqtt_sender.send_message("m1_forward", [-speed])


def handle_left(mqtt_sender, angle_slider):
    mqtt_sender.send_message("m1_left", [angle_slider.get()])


def handle_right(mqtt_sender, angle_slider):
    mqtt_sender.send_message("m1_right", [angle_slider.get()])


def handle_switch(robot, forward_slider, forward_button, forward_label, backward_button, stop_button, left_button, right_button, angle_slider, angle_label, empty2_label, empty_label, switch_button, frame_label, chosen_speed_label, chosen_angle_label):
    robot.canvas.grid_forget()
    robot.direction_label.grid_forget()
    forward_slider.grid_forget()
    forward_button.grid_forget()
    forward_label.grid_forget()
    backward_button.grid_forget()
    stop_button.grid_forget()
    left_button.grid_forget()
    right_button.grid_forget()
    angle_slider.grid_forget()
    angle_label.grid_forget()
    empty2_label.grid_forget()
    empty_label.grid_forget()
    switch_button.grid_forget()
    frame_label.grid_forget()

    chosen_angle_label["text"] = "Angle: " + str(angle_slider.get())
    chosen_speed_label["text"] = "Speed: " + str(forward_slider.get())

    if robot.current_setting == "initial_gui":
        robot.canvas.grid(row=0, column=0)
        switch_button.grid(row=1, column=0)
        robot.direction_label.grid(row=0, column=1)
        robot.current_setting = "help_gui"
        robot.update_canvas()

    elif robot.current_setting == "help_gui":
        frame_label.grid(row=0, column=1)
        forward_label.grid(row=1, column=0)
        angle_label.grid(row=1, column=2)
        forward_slider.grid(row=2, column=0)
        angle_slider.grid(row=2, column=2)
        empty_label.grid(row=3, column=0)
        forward_button.grid(row=4, column=1)
        backward_button.grid(row=6, column=1)
        stop_button.grid(row=5, column=1)
        left_button.grid(row=5, column=0)
        right_button.grid(row=5, column=2)
        empty2_label.grid(row=7, column=0)
        switch_button.grid(row=8, column=1)
        robot.current_setting = "initial_gui"


# -----------------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# -----------------------------------------------------------------------------
sprint_3()
