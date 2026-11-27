from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor
from pybricks.parameters import Port, Direction, Stop, Color
from pybricks.robotics import DriveBase
from pybricks.tools import wait

# Initialize Hub, Motors, and Sensors once
hub = PrimeHub()
left_motor = Motor(Port.D, Direction.COUNTERCLOCKWISE)
right_motor = Motor(Port.C)
color_sensor = ColorSensor(Port.F)

front_attach = Motor(Port.E)
top_attach = Motor(Port.A)

drive_base = DriveBase(left_motor, right_motor, wheel_diameter=102, axle_track=120)
drive_base.use_gyro(True)

drive_base.distance_control.stall_tolerances(speed=20, time=100)

# 2. Allow the heading PID controller to build up power faster when pushing against resistance
drive_base.heading_control.pid(ki=2500)  # Default ki is around 1500–2000; higher = stronger push when stuck

# Chromatic Colors
Color.RED = Color(h=354, s=96, v=46) #Color.MAGENTA Color(h=354, s=96, v=66)
Color.MAGENTA = Color(h=338, s=91, v=54) #Color.RED Color(h=339, s=93, v=39)
Color.ORANGE = Color(h=14, s=88, v=86)
Color.YELLOW = Color(h=42, s=78, v=74)
Color.LIGHT_BLUE = Color(h=196, s=89, v=81)

# Neutral & Ambient Colors
Color.WHITE = Color(h=160, s=5, v=95) #Color.WHITE Color(h=173, s=17, v=84)
Color.LIGHT_GREY = Color(h=193, s=36, v=65) # Color.LIGHT_GREY Color(h=191, s=36, v=55)
Color.DARK_GREY = Color(h=192, s=46, v=10)
Color.NONE = Color(h=0, s=0, v=0)

color_sensor.detectable_colors([
    Color.RED,
    Color.LIGHT_BLUE,
    Color.YELLOW,
    Color.MAGENTA,
    Color.ORANGE,
    Color.WHITE,
    Color.LIGHT_GREY,
    Color.NONE,
])

class robot_base_class:
    def __init__(self):
        self.hub = hub
        self.db = drive_base
        self.front_attach = front_attach
        self.top_attach = top_attach
        self.sensor = color_sensor
        self.trackwidth = 120


class straight_base_class(robot_base_class):
    async def drive(self, dist, velo, wait=True):
        self.db.settings(straight_speed=abs(velo))
        if wait:
            await self.db.straight(dist, then=Stop.COAST)
        else:
            self.db.straight(dist, then=Stop.COAST, wait=False)


class time_class(robot_base_class):
    def stop(self):
        self.db.stop()

    async def wait(self, duration):
        await wait(duration)


class turn_base_class(robot_base_class):
    async def Ltturn(self, angle, velo, wait=True):
        self.db.settings(turn_rate=abs(velo))
        if wait:
            await self.db.turn(-angle)
        else:
            self.db.turn(-angle, wait=False)

    async def Rtturn(self, angle, velo, wait=True):
        self.db.settings(turn_rate=abs(velo))
        if wait:
            await self.db.turn(angle)
        else:
            self.db.turn(angle, wait=False)

    async def Lwturn(self, radius, angle, velo):
        self.db.settings(straight_speed=abs(velo))
        await self.db.curve(abs(radius) + (self.trackwidth / 2), -angle)

    async def Rwturn(self, radius, angle, velo):
        self.db.settings(straight_speed=abs(velo))
        await self.db.curve(abs(radius) + (self.trackwidth / 2), angle)

    async def Larc_turn(self, angle, velo):
        await self.Lwturn(0, angle, velo)

    async def Rarc_turn(self, angle, velo):
        await self.Rwturn(0, angle, velo)


class fullbot(robot_base_class):
    def __init__(self):
        super().__init__()
        self.straight = straight_base_class()
        self.turn = turn_base_class()
        self.time = time_class()
