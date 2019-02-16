import rosebot
import time
import random


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
            time.sleep(2)
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
        if chosen_play == 'Paper':
            time.sleep(2)
            robot.sound_system.speech_maker.speak('You win')
        elif chosen_play == 'Rock':
            time.sleep(2)
            robot.sound_system.speech_maker.speak('We tie')
        else:
            time.sleep(2)
            robot.sound_system.speech_maker.speak('You lose')
    elif x == 2:  # Paper
        robot.arm_and_claw.move_arm_to_position(0)
        robot.sound_system.speech_maker.speak('I chose Paper')
        time.sleep(2)
        if chosen_play == 'Scissors':
            time.sleep(2)
            robot.sound_system.speech_maker.speak('You win')
        elif chosen_play == 'Paper':
            time.sleep(2)
            robot.sound_system.speech_maker.speak('We tie')
        else:
            time.sleep(2)
            robot.sound_system.speech_maker.speak('You lose')
    elif x == 3:  # Scissors
        robot.arm_and_claw.move_arm_to_position(2500)
        robot.sound_system.speech_maker.speak('I chose Scissors')
        if chosen_play == 'Rock':
            time.sleep(2)
            robot.sound_system.speech_maker.speak('You win')
        elif chosen_play == 'Scissors':
            time.sleep(2)
            robot.sound_system.speech_maker.speak('We tie')
        else:
            time.sleep(2)
            robot.sound_system.speech_maker.speak('You lose')
    time.sleep(2)
    robot.arm_and_claw.move_arm_to_position(0)


def i_spy(area):
    print('Running I spy')
    robot = rosebot.RoseBot()
    while True:
        blob = robot.sensor_system.camera.get_biggest_blob()
        actual_area = blob.get_area()
        print(actual_area)
        time.sleep(.5)
        if actual_area > area:
            robot.sound_system.speech_maker.speak('I spy with my little eye, the color blue')
            break
