"""
  Capstone Project.  Code to run on the EV3 robot (NOT on a laptop).
  Author:  Your professors (for the framework)
    and Valeria Paiz.
  Winter term, 2018-2019.
"""

import rosebot
import mqtt_remote_method_calls as com
import time
import shared_gui_delegate_on_robot


def main():
    """
    This code, which must run on the EV3 ROBOT:
      1. Makes the EV3 robot do various things.
      2. Communicates via MQTT with the GUI code that runs on the LAPTOP.
    """
    print("Attempting Connection")
    robot_run()
    print("Ended Connection")


def test():
    robot = rosebot.RoseBot()
    robot.drive_system.go_straight_until_intensity_is_less_than(50)


def robot_run():
    robot = rosebot.RoseBot()
    delegate = shared_gui_delegate_on_robot.ResponderToGUIMessages(robot)
    mqtt_receiver = com.MqttClient(delegate)
    mqtt_receiver.connect_to_pc()

    robot.drive_system.go_straight_until_intensity_is_greater_than(50, 100)

    # while True:
    #     if delegate.stop_program:
    #         break
    #     time.sleep(0.01)


# -----------------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# -----------------------------------------------------------------------------
main()