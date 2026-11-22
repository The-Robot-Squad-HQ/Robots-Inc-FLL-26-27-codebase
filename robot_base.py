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
Color.RED = Color(h=356, s=96, v=36)
Color.MAGENTA = Color(h=325, s=88, v=62)
Color.ORANGE = Color(h=13, s=88, v=84)
Color.YELLOW = Color(h=43, s=78, v=58)

# Neutral & Ambient Colors
Color.WHITE = Color(h=165, s=11, v=62)
Color.LIGHT_GREY = Color(h=195, s=42, v=26)
Color.DARK_GREY = Color(h=192, s=46, v=10)
Color.NONE = Color(h=0, s=0, v=0)

# Register all colors (including custom greys)
color_sensor.detectable_colors([
    Color.RED,
    Color.BLUE,
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
