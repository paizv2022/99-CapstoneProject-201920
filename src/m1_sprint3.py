import rosebot
import math
import time


def forward(robot, speed):
    robot.drive_system.left_motor.reset_position()
    robot.drive_system.right_motor.reset_position()

    robot.drive_system.go(speed, speed)


def stop_robot(robot, mqtt_sender):
    robot.drive_system.stop()
    movement = (robot.drive_system.right_motor.get_position() * ((1.3 * math.pi)/360))
    mqtt_sender.send_message('update_robot_gui', [movement])


def right(robot, angle, mqtt_sender):
    robot.drive_system.left_motor.reset_position()
    robot.drive_system.right_motor.reset_position()

    robot.drive_system.go(100, -100)

    while True:
        if robot.drive_system.left_motor.get_position() >= angle * 5:
            robot.drive_system.stop()
            break

    mqtt_sender.send_message('update_robot_direction', [-angle])

    robot.drive_system.left_motor.reset_position()
    robot.drive_system.right_motor.reset_position()


def left(robot, angle, mqtt_sender):
    robot.drive_system.left_motor.reset_position()
    robot.drive_system.right_motor.reset_position()

    robot.drive_system.go(-100, 100)

    while True:
        if robot.drive_system.right_motor.get_position() >= angle * 5:
            robot.drive_system.stop()
            break

    mqtt_sender.send_message('update_robot_direction', [angle])

    robot.drive_system.left_motor.reset_position()
    robot.drive_system.right_motor.reset_position()




