"""
  Capstone Project.  Code to run on the EV3 robot (NOT on a laptop).
  This code is the delegate for handling messages from the shared GUI.

  Author:  Your professors (for the framework)
     and Valeria Paiz, Samuel VanDenburgh, Justin Heinz.
  Winter term, 2018-2019.
"""
import time


class ResponderToGUIMessages(object):
    def __init__(self, robot):
        """
            :type robot: rosebot.RoseBot
        """
        self.robot = robot
        self.stop_program = False

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

    def go_straight_for_seconds(self, seconds, speed):
        self.robot.drive_system.go_straight_for_seconds(int(seconds), int(speed))

    def go_straight_for_inches_using_encoder(self, inches, speed):
        self.robot.drive_system.go_straight_for_inches_using_encoder(int(inches), int(speed))

    def go_straight_for_inches_using_time(self, inches, speed):
        self.robot.drive_system.go_straight_for_inches_using_time(int(inches), int(speed))

    def beep(self, number):
        for k in range(int(number)):
            self.robot.sound_system.beeper.beep().wait()

    def play_tone(self, frequency, duration):
        self.robot.sound_system.tone_maker.play_tone(int(frequency), int(duration)).wait()

    def speak(self, phrase):
        self.robot.sound_system.speech_maker.speak(phrase).wait()

    def quit(self):
        self.stop_program = True

    def m1_greater_intensity(self, intensity_entry):
        self.robot.drive_system.go_straight_until_intensity_is_greater_than(int(intensity_entry))

    def m1_smaller_intensity(self, intensity_entry):
        self.robot.drive_system.go_straight_until_intensity_is_less_than(int(intensity_entry))

    def m1_color_is(self, color):
        self.robot.drive_system.go_straight_until_color_is(color, 100)

    def m1_color_is_not(self, color):
        self.robot.drive_system.go_straight_until_color_is_not(color, 100)

    def m1_pick_up(self, initial, rate, speed):
        self.robot.drive_system.go(speed)
        while self.robot.sensor_system.ir_proximity_sensor.get_distance_in_inches() > 1:
            distance = self.robot.sensor_system.ir_proximity_sensor.get_distance_in_inches()
            seconds = initial + (rate * distance)
            self.robot.sound_system.beeper.beep()
            time.sleep(seconds)
        self.robot.drive_system.stop()
        self.robot.arm_and_claw.raise_arm()

    def m1_camera_pick_up(self, speed, direction):
        pass

    def m3_led_proximity_sensor(self, initial, rate_of_increase):
        secs = float(initial)
        threshold = 20
        self.robot.led_system.left_led.turn_off()
        self.robot.led_system.right_led.turn_off()
        self.robot.arm_and_claw.calibrate_arm()
        self.robot.drive_system.go(50, 50)
        while True:
            distance = self.robot.sensor_system.ir_proximity_sensor.get_distance()
            print(distance)
            # Led Cycle
            self.robot.led_system.left_led.turn_on()
            time.sleep(secs / 4)
            self.robot.led_system.left_led.turn_off()
            self.robot.led_system.right_led.turn_on()
            time.sleep(secs / 4)
            self.robot.led_system.right_led.turn_off()
            self.robot.led_system.left_led.turn_on()
            self.robot.led_system.right_led.turn_on()
            time.sleep(secs / 4)
            self.robot.led_system.left_led.turn_off()
            self.robot.led_system.right_led.turn_off()
            time.sleep(secs / 4)
            if distance < threshold:
                self.robot.drive_system.stop()
                self.robot.arm_and_claw.raise_arm()
                break
            increment = int(distance / 10)
            secs = increment * float(rate_of_increase)
            if secs < 0:
                secs = 0
