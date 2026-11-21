from robot_base import fullbot

async def khai():
    robot = fullbot()
    await robot.straight.drive(500, 1000)
    await robot.straight.drive(-350, 500)
     #500 forward then 350 backward