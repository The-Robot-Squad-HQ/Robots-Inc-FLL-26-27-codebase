#___________________________________________________________________________
from robot_base import fullbot

async def swapside():
    robot = fullbot()
    await robot.straight.drive(1900, 500)
#___________________________________________________________________________