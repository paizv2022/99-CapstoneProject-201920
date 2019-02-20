"""
  Capstone Project.  Code to run on the EV3 robot (NOT on a laptop).
  Author:  Your professors (for the framework)
    and Samuel VanDenburgh
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
    robot_run()

def robot_run():
    robot = rosebot.RoseBot()
    robot.speed = 0
    robot.m2_stop = False
    delegate = shared_gui_delegate_on_robot.ResponderToGUIMessages(robot)
    robot.m2_start_game = False
    mqtt_receiver = com.MqttClient(delegate)
    mqtt_receiver.connect_to_pc()

    while True:
        if robot.m2_start_game == True:
            delegate.m2_wait_for_finish()
        time.sleep(0.01)

# -----------------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# -----------------------------------------------------------------------------
main()