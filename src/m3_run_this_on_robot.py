"""
  Capstone Project.  Code to run on the EV3 robot (NOT on a laptop).
  Author:  Your professors (for the framework)
    and Justin Heinz.
  Winter term, 2018-2019.
"""

import rosebot
import mqtt_remote_method_calls as com
import time
import shared_gui_delegate_on_robot


def main():
    """
    This code, which must run on the EV3 ROBOT:
      1. Makes the EV3 robot to various things.
      2. Communicates via MQTT with the GUI code that runs on the LAPTOP.
    """
    #run_test_arm()
    #real_thing()
    run_test_move()


def run_test_arm():
    robot = rosebot.RoseBot()
    robot.arm_and_claw.lower_arm()


def real_thing():
    robot = rosebot.RoseBot()
    delegate = shared_gui_delegate_on_robot.ResponderToGuiMessages(robot)
    mqtt_receiver = com.MqttClient(delegate)
    mqtt_receiver.connect_to_pc()
    while True:
        time.sleep(0.01)

def run_test_move():
    robot = rosebot.RoseBot()
    robot.drive_system.go_straight_for_seconds(5, 100)
    time.sleep(5)
    robot.drive_system.go_straight_for_inches_using_time(10, 100)
# -----------------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# -----------------------------------------------------------------------------
main()
