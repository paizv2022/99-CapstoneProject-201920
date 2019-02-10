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

    def stop(self):
        self.robot.drive_system.stop()

    def raise_arm(self):
        self.robot.arm_and_claw.raise_arm()

    def lower_arm(self):
        self.robot.arm_and_claw.lower_arm()

    def calibrate_arm(self):
        self.robot.arm_and_claw.calibrate_arm()

    def move_arm_to_position(self, position):
        self.robot.arm_and_claw.move_arm_to_position(int(position))

    def beep(self, number):
        for k in range(int(number)):
            self.robot.sound_system.beeper.beep()

    def play_tone(self, frequency):
        self.robot.sound_system.tone_maker.play_tone(int(frequency))

    def speak(self, phrase):
        self.robot.sound_system.speech_maker.speak(phrase)

