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
    # run_test_arm()
    #run_test_move()
    run_test_beep()

    # real_thing()


def run_test_arm():
    robot = rosebot.RoseBot()
    print('Running Test: Calibrate Arm')
    robot.arm_and_claw.calibrate_arm()
    print('Running Test: Move arm to Position')
    robot.arm_and_claw.move_arm_to_position(2500)
    time.sleep(2.5)
    print('Running Test: Raise arm')
    robot.arm_and_claw.raise_arm()
    print('Running Test: Lower arm')
    robot.arm_and_claw.lower_arm()


def real_thing():
    robot = rosebot.RoseBot()
    delegate = shared_gui_delegate_on_robot.ResponderToGUIMessage(robot)
    mqtt_receiver = com.MqttClient(delegate)
    mqtt_receiver.connect_to_pc()
    while True:
        time.sleep(0.01)


def run_test_move():
    robot = rosebot.RoseBot()
    print('Running Test: Go')
    robot.drive_system.go()
    time.sleep(5)
    print('Running Test: Stop')
    robot.drive_system.stop()
    time.sleep(2.5)
    print('Running Test: Go Straight for Seconds')
    robot.drive_system.go_straight_for_seconds(5, 100)
    time.sleep(2.5)
    print('Running Test: Go Straight for Inches Using Time')
    robot.drive_system.go_straight_for_inches_using_time(10, 100)
    time.sleep(2.5)
    print('Running Test: Go Straight for Inches Using Encoder')
    robot.drive_system.go_straight_for_inches_using_encoder(10, 100)
    # More to be added for features 6 & 8


def run_test_beep():
    b = rosebot.Beeper()
    for k in range(10):
        b.beep().wait(200)

    t = rosebot.ToneMaker()
    frequency = 500
    duration = 200
    t.play_tone(frequency, duration)

    s = rosebot.SpeechMaker()
    s.speak('Hello we are team 8')


# -----------------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# -----------------------------------------------------------------------------
main()
