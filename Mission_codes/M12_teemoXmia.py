#___________________________________________________________________________
from robot_base import fullbot

async def teemoXmia():
    robot = fullbot()
    await robot.straight.drive(710, 400)
    await robot.turn.Rtturn(120, 350)
    await robot.straight.drive(-150, 250)
    await robot.turn.Rtturn(-90, 350)
    await robot.straight.drive(-720, 500)
#___________________________________________________________________________