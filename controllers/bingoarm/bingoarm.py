"""bingoarm controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot
from controller import Camera


# create the Robot instance.
robot = Robot()
camera = Camera("camera")

# get the time step of the current world.
timestep = int(robot.getBasicTimeStep())

# You should insert a getDevice-like function in order to get the
# instance of a device of the robot. Something like:
#  motor = robot.getMotor('motorname')
#  ds = robot.getDistanceSensor('dsname')
#  ds.enable(timestep)

# camera.enable(1)
joints = []
for joint in ["shoulder_pan_joint", "shoulder_lift_join", "elbow_joint", "wrist_1_joint", "wrist_2_joint", "wrist_3_join"]:
    joints.append(robot.getDevice(joint))
counter = 0
print(joints)


# Main loop:
# - perform simulation steps until Webots is stopping the controller
while robot.step(timestep) != -1:
    # Read the sensors:
    # Enter here functions to read sensor data, like:
    #  val = ds.getValue()

    # Process sensor data here.

    # Enter here functions to send actuator commands, like:
    #  motor.setPosition(10.0)
    pass

# Enter here exit cleanup code.
