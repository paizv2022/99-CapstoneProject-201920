import math
import time


def forward(robot, speed):
    robot.drive_system.left_motor.reset_position()
    robot.drive_system.right_motor.reset_position()

    robot.drive_system.go(speed, speed)


def stop_robot(robot, mqtt_sender, color):
    robot.drive_system.stop()
    movement = (robot.drive_system.right_motor.get_position() * ((1.3 * math.pi)/360))
    mqtt_sender.send_message('update_robot_gui', [movement])
    robot.drive_system.right_motor.reset_position()
    robot.drive_system.left_motor.reset_position()
    if color == 'White':
        mqtt_sender.send_message('update_score', [10])
    elif color == 'Red':
        mqtt_sender.send_message('update_score', [-10])
    elif robot.sensor_system.ir_proximity_sensor.get_distance_in_inches() <= 5:
        time.sleep(10)


def right(robot, angle, mqtt_sender):
    robot.drive_system.left_motor.reset_position()
    robot.drive_system.right_motor.reset_position()

    robot.drive_system.go(100, -100)

    while True:
        if robot.drive_system.left_motor.get_position() >= angle * 4.65:
            robot.drive_system.stop()
            break

    mqtt_sender.send_message('update_robot_direction', [angle])

    robot.drive_system.left_motor.reset_position()
    robot.drive_system.right_motor.reset_position()


def left(robot, angle, mqtt_sender):
    robot.drive_system.left_motor.reset_position()
    robot.drive_system.right_motor.reset_position()

    robot.drive_system.go(-100, 100)

    while True:
        if robot.drive_system.right_motor.get_position() >= angle * 4.65:
            robot.drive_system.stop()
            break

    mqtt_sender.send_message('update_robot_direction', [-angle])

    robot.drive_system.left_motor.reset_position()
    robot.drive_system.right_motor.reset_position()




