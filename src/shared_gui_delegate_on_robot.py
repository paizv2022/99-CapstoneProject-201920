"""
  Capstone Project.  Code to run on the EV3 robot (NOT on a laptop).
  This code is the delegate for handling messages from the shared GUI.

  Author:  Your professors (for the framework)
     and Valeria Paiz, Samuel VanDenburgh, Justin Heinz.
  Winter term, 2018-2019.
"""
import time
import math
import m3_extra as m3
import m1_sprint3 as m1


class ResponderToGUIMessages(object):
    def __init__(self, robot, mqtt_sender=None):
        """
            :type robot: rosebot.RoseBot
        """
        self.robot = robot
        self.stop_program = False
        self.stop_tone = False
        self.mqtt_sender = mqtt_sender

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

    def m1_forward(self, speed_entry):
        m1.forward(self.robot, speed_entry)

    def m1_stop(self):
        m1.stop_robot(self.robot, self.mqtt_sender)

    def m1_left(self, angle_entry):
        m1.left(self.robot, angle_entry, self.mqtt_sender)

    def m1_right(self, angle_entry):
        m1.right(self.robot, angle_entry, self.mqtt_sender)

    def m1_greater_intensity(self, intensity_entry):
        self.robot.drive_system.go_straight_until_intensity_is_greater_than(int(intensity_entry), 100)

    def m1_smaller_intensity(self, intensity_entry):
        self.robot.drive_system.go_straight_until_intensity_is_less_than(int(intensity_entry), 100)

    def m1_color_is(self, color):
        self.robot.drive_system.go_straight_until_color_is(color, 100)

    def m1_color_is_not(self, color):
        self.robot.drive_system.go_straight_until_color_is_not(color, 100)

    def m1_pick_up(self, initial, rate, speed):
        initial = int(initial)
        rate = int(rate)
        speed = int(speed)
        self.robot.drive_system.go(speed, speed)
        while True:
            if self.robot.sensor_system.ir_proximity_sensor.get_distance_in_inches() <= 1.5:
                break
            distance = self.robot.sensor_system.ir_proximity_sensor.get_distance_in_inches()
            value = initial + int(((rate * 10) / (math.sqrt(distance))))
            for k in range(value):
                self.robot.sound_system.beeper.beep()
        self.robot.drive_system.stop()
        self.robot.arm_and_claw.raise_arm()

    def m1_camera_pick_up(self, initial, rate, speed, direction, area):
        if direction == 'CW':
            self.robot.drive_system.spin_clockwise_until_sees_object(int(speed), int(area))
        elif direction == 'CCW':
            self.robot.drive_system.spin_counterclockwise_until_sees_object(int(speed), int(area))
        self.m1_pick_up(initial, rate, speed)

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
            increment = float(initial)/float(rate_of_increase)
            sub = 70/increment
            pos = 100 - distance
            x = pos/sub
            secs = float(initial) - (float(rate_of_increase) * x)
            if secs < 0:
                secs = 0

    def m3_spin_counterclockwise_until_sees_object(self, speed, area):
        speed = int(speed)
        area = int(area)
        self.robot.drive_system.spin_counterclockwise_until_sees_object(speed, area)

    def m3_spin_clockwise_until_sees_object(self, speed, area):
        speed = int(speed)
        area = int(area)
        self.robot.drive_system.spin_clockwise_until_sees_object(speed, area)

    def m2_go_forward_until_distance_is_less_than(self, inches, speed):
        self.robot.drive_system.go_forward_until_distance_is_less_than(inches, speed)

    def m2_go_backward_until_distance_is_greater_than(self, inches, speed):
        self.robot.drive_system.go_backward_until_distance_is_greater_than(inches,speed)

    def m2_go_until_distance_is_within(selfs, delta, inches, speed):
        selfs.robot.drive_system.go_until_distance_is_within(delta, inches, speed)

    def m2_tone_to_distance(self, initial_frequency, frequency_rate):
        self.stop_tone = False
        average = 0
        start = self.robot.sensor_system.ir_proximity_sensor.get_distance_in_inches()
        while True:
            frequency = initial_frequency - (frequency_rate * (average - start))
            self.robot.sound_system.tone_maker.play_tone(frequency, 100)
            a = self.robot.sensor_system.ir_proximity_sensor.get_distance_in_inches()
            time.sleep(.2)
            b = self.robot.sensor_system.ir_proximity_sensor.get_distance_in_inches()
            average = (a + b) / 2
            if average <= 2:
                break
        print("Tone has stopped")
        return

    def m2_stop_tone(self):
        self.stop_tone = True

    def m3_led_pick_up(self, speed, area, direction, initial, rate):
        print('Spin unit see object')
        if direction == 'CCW':
            self.robot.drive_system.spin_counterclockwise_until_sees_object(float(speed), int(area))
        elif direction == 'CW':
            self.robot.drive_system.spin_clockwise_until_sees_object(float(speed), int(area))
        else:
            print('Entered Invalid Direction')
            print('Default Direction is CounterClockWise')
            self.robot.drive_system.spin_clockwise_until_sees_object(float(speed), int(area))
        time.sleep(2)
        blob = self.robot.sensor_system.camera.get_biggest_blob()
        blob_center = blob.center.x
        print(blob_center)
        if blob_center > 160 and blob_center > 0:
            self.robot.drive_system.go(30, -30)
            while True:
                print(blob_center)
                blob = self.robot.sensor_system.camera.get_biggest_blob()
                blob_center = blob.center.x
                if 157 < blob_center and blob_center > 162:
                    self.robot.drive_system.stop()
                    break
        elif blob_center < 160 or blob_center == 0:
            self.robot.drive_system.go(-30, 30)
            while True:
                print(blob_center)
                blob = self.robot.sensor_system.camera.get_biggest_blob()
                blob_center = blob.center.x
                if 157 < blob_center and blob_center > 162:
                    self.robot.drive_system.stop()
                    break
        self.m3_led_proximity_sensor(int(initial), float(rate))

    def m3_beep_pick_up(self, speed, area, direction, initial, rate):
        print('Spin unit see object')
        if direction == 'CCW':
            self.robot.drive_system.spin_counterclockwise_until_sees_object(float(speed), int(area))
        elif direction == 'CW':
            self.robot.drive_system.spin_clockwise_until_sees_object(float(speed), int(area))
        else:
            print('Entered Invalid Direction')
            print('Default Direction is CounterClockWise')
            self.robot.drive_system.spin_clockwise_until_sees_object(float(speed), int(area))
        time.sleep(2)
        blob = self.robot.sensor_system.camera.get_biggest_blob()
        blob_center = blob.center.x
        print(blob_center)
        if blob_center > 160 and blob_center > 0:
            self.robot.drive_system.go(30, -30)
            while True:
                print(blob_center)
                blob = self.robot.sensor_system.camera.get_biggest_blob()
                blob_center = blob.center.x
                if 157 < blob_center and blob_center > 162:
                    self.robot.drive_system.stop()
                    break
        elif blob_center < 160 or blob_center == 0:
            self.robot.drive_system.go(-30, 30)
            while True:
                print(blob_center)
                blob = self.robot.sensor_system.camera.get_biggest_blob()
                blob_center = blob.center.x
                if 157 < blob_center and blob_center > 162:
                    self.robot.drive_system.stop()
                    break
        self.m1_pick_up(int(initial), float(rate), float(speed))

    def m3_tone_pick_up(self, speed, area, direction, initial, rate):
        print('Spin unit see object')
        if direction == 'CCW':
            self.robot.drive_system.spin_counterclockwise_until_sees_object(float(speed), int(area))
        elif direction == 'CW':
            self.robot.drive_system.spin_clockwise_until_sees_object(float(speed), int(area))
        else:
            print('Entered Invalid Direction')
            print('Default Direction is CounterClockWise')
            self.robot.drive_system.spin_clockwise_until_sees_object(float(speed), int(area))
        time.sleep(2)
        blob = self.robot.sensor_system.camera.get_biggest_blob()
        blob_center = blob.center.x
        print(blob_center)
        if blob_center > 160 and blob_center > 0:
            self.robot.drive_system.go(30, -30)
            while True:
                print(blob_center)
                blob = self.robot.sensor_system.camera.get_biggest_blob()
                blob_center = blob.center.x
                if 157 < blob_center and blob_center > 162:
                    self.robot.drive_system.stop()
                    break
        elif blob_center < 160 or blob_center == 0:
            self.robot.drive_system.go(-30, 30)
            while True:
                print(blob_center)
                blob = self.robot.sensor_system.camera.get_biggest_blob()
                blob_center = blob.center.x
                if 157 < blob_center and blob_center > 162:
                    self.robot.drive_system.stop()
                    break
        self.m2_tone_to_distance(int(initial), float(rate))

    def m2_tone_pick_up(self, initial_frequency, frequency_rate, speed):
        self.robot.drive_system.go(speed, speed)
        self.m2_tone_to_distance(initial_frequency, frequency_rate)
        while True:
            if self.robot.sensor_system.ir_proximity_sensor.get_distance_in_inches() <= 2:
                break
        self.robot.drive_system.stop()
        self.robot.arm_and_claw.raise_arm()

    def m2_tone_and_camera_pick_up(self, spin, speed, area, initial_frequency, frequency_rate,):
        if spin == 'CW':
            self.robot.drive_system.spin_clockwise_until_sees_object(speed, area)
        elif spin == 'CC':
            self.robot.drive_system.spin_counterclockwise_until_sees_object(speed, area)
        self.m2_tone_pick_up(initial_frequency, frequency_rate, speed)

    def m3_tag(self, speed):
        m3.m3_tag(float(speed))

    def m3_rps(self, chosen_play):
        m3.m3_rps(chosen_play)

    def m3_i_spy(self, area):
        m3.i_spy(int(area))
