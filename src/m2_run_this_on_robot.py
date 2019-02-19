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
    #infrared_test()

def robot_run():
    robot = rosebot.RoseBot()
    robot.speed = 0
    robot.m2_stop = False
    robot.m2_start_game = False
    delegate = shared_gui_delegate_on_robot.ResponderToGUIMessages(robot)
    mqtt_receiver = com.MqttClient(delegate)
    mqtt_receiver.connect_to_pc()

    delegate.m2_wait_for_finish()

''' while True:
        if robot.m2_stop == False:
            robot.drive_system.go(robot.speed, robot.speed)
        else:
            robot.drive_system.stop()
        if delegate.stop_program:
            break
        time.sleep(0.01)'''

def infrared_test():
    robot = rosebot.RoseBot()
    delegate = shared_gui_delegate_on_robot.ResponderToGUIMessages(robot)
    mqtt_receiver = com.MqttClient(delegate)
    mqtt_receiver.connect_to_pc()

    robot.drive_system.go_forward_until_distance_is_less_than(5, 50)

# -----------------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# -----------------------------------------------------------------------------
main()