#___________________________________________________________________________
from robot_base import fullbot

async def teemoxmia():
    robot = fullbot()
    await robot.straight.drive(710, 200)
    await robot.wturn.Rwturn(10, 145, 250)
    await robot.front_attach.run_angle(500, 500)
    await robot.straight.drive(-720, 300)
    ___________________________________________________