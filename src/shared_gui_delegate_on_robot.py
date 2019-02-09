"""
  Capstone Project.  Code to run on the EV3 robot (NOT on a laptop).
  This code is the delegate for handling messages from the shared GUI.

  Author:  Your professors (for the framework)
     and Valeria Paiz, Samuel VanDenburgh, Justin Heinz.
  Winter term, 2018-2019.
"""


class ResponderToGUIMessages(object):
    def __init__(self, robot):
        """
            :type robot: rosebot.RoseBot
        """
        self.robot = robot

    def go(self, left_wheel_speed, right_wheel_speed):
        left = int(left_wheel_speed)
        right = int(right_wheel_speed)
        self.robot.drive_system.go(left, right)
        print('went forward')

    def stop(self):
        self.robot.drive_system.stop()
        print('stopped')

    def raise_arm(self):
        self.robot.arm_and_claw.raise_arm()
        print('arm up')

    def lower_arm(self):
        self.robot.arm_and_claw.lower_arm()
        print('arm down')

    def calibrate_arm(self):
        self.robot.arm_and_claw.calibrate_arm()
        print('calibrated')

    def move_arm_to_position(self, position):
        self.robot.arm_and_claw.move_arm_to_position(int(position))
        print('moved')
