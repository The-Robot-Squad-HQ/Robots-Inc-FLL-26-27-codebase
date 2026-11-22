#___________________________________________________________________________
from robot_base import fullbot

async def teemoXmia():
    robot = fullbot()
    await robot.straight.drive(710, 200)
    await robot.turn.Rwturn(10, 145, 250)
    await robot.front_attach.run_angle(500, 500)
    await robot.straight.drive(-720, 300)
#___________________________________________________________________________