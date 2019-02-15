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
import random


def main():
    """
    This code, which must run on the EV3 ROBOT:
      1. Makes the EV3 robot to various things.
      2. Communicates via MQTT with the GUI code that runs on the LAPTOP.
    """
    # run_test_arm()
    # run_test_move()
    # run_test_beep()
    # real_thing()
    # camera()
    # pick_up_with_proximity_sensor(2, .3)
    # led_test()
    # m3_chose_pick_up(1, .2, 'Clockwise', 30, 250, 'LED')
    m3_rps("Rock")


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
    delegate = shared_gui_delegate_on_robot.ResponderToGUIMessages(robot)
    mqtt_receiver = com.MqttClient(delegate)
    mqtt_receiver.connect_to_pc()
    while True:
        time.sleep(0.01)
        if delegate.stop_program:
            break


def run_test_move():
    robot = rosebot.RoseBot()
    print('Running Test: Go')
    robot.drive_system.go(100, 100)
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
    for k in range(5):
        b.beep().wait(200)

    time.sleep(3)

    t = rosebot.ToneMaker()
    frequency = 500
    duration = 200
    t.play_tone(frequency, duration)

    time.sleep(3)

    s = rosebot.SpeechMaker()
    s.speak('Hello we are team 8')


def camera():
    robot = rosebot.RoseBot()
    robot.drive_system.display_camera_data()
    robot.drive_system.spin_clockwise_until_sees_object(50, 250)
    # robot.drive_system.spin_counterclockwise_until_sees_object(50, 250)
    robot.drive_system.display_camera_data()


def m3_led_proximity_sensor(initial, rate_of_increase):
    robot = rosebot.RoseBot()
    secs = float(initial)
    threshold = 20
    robot.led_system.left_led.turn_off()
    robot.led_system.right_led.turn_off()
    robot.arm_and_claw.calibrate_arm()
    robot.drive_system.go(50, 50)
    while True:
        distance = robot.sensor_system.ir_proximity_sensor.get_distance()
        print(distance)
        # Led Cycle
        robot.led_system.left_led.turn_on()
        time.sleep(secs / 4)
        robot.led_system.left_led.turn_off()
        robot.led_system.right_led.turn_on()
        time.sleep(secs / 4)
        robot.led_system.right_led.turn_off()
        robot.led_system.left_led.turn_on()
        robot.led_system.right_led.turn_on()
        time.sleep(secs / 4)
        robot.led_system.left_led.turn_off()
        robot.led_system.right_led.turn_off()
        time.sleep(secs / 4)
        if distance < threshold:
            robot.drive_system.stop()
            robot.arm_and_claw.raise_arm()
            break
        increment = float(initial)/float(rate_of_increase)
        sub = 100/increment
        pos = 100 - distance
        x = pos/sub
        secs = initial - (float(rate_of_increase) * x)
        if secs < 0:
            secs = 0


def led_test():
    while True:
        robot = rosebot.RoseBot()
        robot.led_system.left_led.turn_on()
        time.sleep(3)
        robot.led_system.left_led.turn_off()
        time.sleep(3)
        robot.led_system.right_led.turn_on()
        time.sleep(3)
        robot.led_system.right_led.turn_off()
        time.sleep(3)


def m3_led_pick_up(speed, area, direction, initial, rate):
    robot = rosebot.RoseBot()
    print('Spin unit see object')
    if direction == 'CCW':
        robot.drive_system.spin_counterclockwise_until_sees_object(float(speed), int(area))
    elif direction == 'CW':
        robot.drive_system.spin_clockwise_until_sees_object(float(speed), int(area))
    else:
        print('Entered Invalid Direction')
        print('Default Direction is CounterClockWise')
        robot.drive_system.spin_clockwise_until_sees_object(float(speed), int(area))
    time.sleep(2)
    blob = robot.sensor_system.camera.get_biggest_blob()
    blob_center = blob.center.x
    print(blob_center)
    if blob_center > 160 and blob_center > 0:
        robot.drive_system.go(30, -30)
        while True:
            print(blob_center)
            blob = robot.sensor_system.camera.get_biggest_blob()
            blob_center = blob.center.x
            if 157 < blob_center and blob_center > 162:
                robot.drive_system.stop()
                break
    elif blob_center < 160 or blob_center == 0:
        robot.drive_system.go(-30, 30)
        while True:
            print(blob_center)
            blob = robot.sensor_system.camera.get_biggest_blob()
            blob_center = blob.center.x
            if 157 < blob_center and blob_center > 162:
                robot.drive_system.stop()
                break
    m3_led_proximity_sensor(int(initial), float(rate))


def m3_beep_pick_up(speed, area, direction, initial, rate):
    robot = rosebot.RoseBot()
    print('Spin unit see object')
    if direction == 'CCW':
        robot.drive_system.spin_counterclockwise_until_sees_object(float(speed), int(area))
    elif direction == 'CW':
        robot.drive_system.spin_clockwise_until_sees_object(float(speed), int(area))
    else:
        print('Entered Invalid Direction')
        print('Default Direction is CounterClockWise')
        robot.drive_system.spin_clockwise_until_sees_object(float(speed), int(area))
    time.sleep(2)
    blob = robot.sensor_system.camera.get_biggest_blob()
    blob_center = blob.center.x
    print(blob_center)
    if blob_center > 160 and blob_center > 0:
        robot.drive_system.go(30, -30)
        while True:
            print(blob_center)
            blob = robot.sensor_system.camera.get_biggest_blob()
            blob_center = blob.center.x
            if 157 < blob_center and blob_center > 162:
                robot.drive_system.stop()
                break
    elif blob_center < 160 or blob_center == 0:
        robot.drive_system.go(-30, 30)
        while True:
            print(blob_center)
            blob = robot.sensor_system.camera.get_biggest_blob()
            blob_center = blob.center.x
            if 157 < blob_center and blob_center > 162:
                robot.drive_system.stop()
                break
    m1_pick_up(int(initial), float(rate), float(speed))
    # runs in delegate but they haven't pulled over code so I can run


def m3_tone_pick_up(speed, area, direction, initial, rate):
    robot = rosebot.RoseBot()
    print('Spin unit see object')
    if direction == 'CCW':
        robot.drive_system.spin_counterclockwise_until_sees_object(float(speed), int(area))
    elif direction == 'CW':
        robot.drive_system.spin_clockwise_until_sees_object(float(speed), int(area))
    else:
        print('Entered Invalid Direction')
        print('Default Direction is CounterClockWise')
        robot.drive_system.spin_clockwise_until_sees_object(float(speed), int(area))
    time.sleep(2)
    blob = robot.sensor_system.camera.get_biggest_blob()
    blob_center = blob.center.x
    print(blob_center)
    if blob_center > 160 and blob_center > 0:
        robot.drive_system.go(30, -30)
        while True:
            print(blob_center)
            blob = robot.sensor_system.camera.get_biggest_blob()
            blob_center = blob.center.x
            if 157 < blob_center and blob_center > 162:
                robot.drive_system.stop()
                break
    elif blob_center < 160 or blob_center == 0:
        robot.drive_system.go(-30, 30)
        while True:
            print(blob_center)
            blob = robot.sensor_system.camera.get_biggest_blob()
            blob_center = blob.center.x
            if 157 < blob_center and blob_center > 162:
                robot.drive_system.stop()
                break
    m2_tone_to_distance(int(initial), float(rate))
    # runs in delegate but they haven't pulled over code so I can run


def m3_tag(speed):
    print('Running Tag!')
    print(speed)
    robot = rosebot.RoseBot()
    robot.sound_system.speech_maker.speak('Im it')
    robot.drive_system.go(speed, speed)
    while True:
        distance = robot.sensor_system.ir_proximity_sensor.get_distance_in_inches()
        if distance < 2:
            robot.drive_system.stop()
            robot.sound_system.speech_maker.speak('You are it')
            robot.drive_system.go(-50, 50)
            time.sleep(3)
            robot.drive_system.go(speed, speed)
            break
    while True:
        if robot.sensor_system.touch_sensor.is_pressed():
            robot.drive_system.stop()
            robot.sound_system.speech_maker.speak('Game over')
            break


def m3_rps(chosen_play):
    print('Running rps')
    robot = rosebot.RoseBot()
    x = random.randrange(1, 4)
    print(x)
    if x == 1:  # Rock
        robot.arm_and_claw.raise_arm()
        robot.sound_system.speech_maker.speak('I chose Rock')
        if chosen_play is 'Paper':
            robot.sound_system.speech_maker.speak('You win')
        else:
            robot.sound_system.speech_maker.speak('You lose')
    elif x == 2:  # Paper
        robot.arm_and_claw.move_arm_to_position(0)
        robot.sound_system.speech_maker.speak('I chose Paper')
        if chosen_play is 'Scissors':
            robot.sound_system.speech_maker.speak('You win')
        else:
            robot.sound_system.speech_maker.speak('You lose')
    elif x == 3:  # Scissors
        robot.arm_and_claw.move_arm_to_position(2500)
        robot.sound_system.speech_maker.speak('I chose Scissors')
        if chosen_play is 'Rock':
            robot.sound_system.speech_maker.speak('You win')
        else:
            robot.sound_system.speech_maker.speak('You lose')
    robot.arm_and_claw.move_arm_to_position(0)


# -----------------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# -----------------------------------------------------------------------------
main()
