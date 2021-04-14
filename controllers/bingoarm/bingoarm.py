"""bingoarm controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot
from controller import Camera
import random


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
for joint in ["shoulder_pan_joint", "shoulder_lift_joint", "elbow_joint", "wrist_1_joint", "wrist_2_joint", "wrist_3_joint"]:
    joints.append(robot.getDevice(joint))
counter = 0
print(joints)

counter = 0;

random.seed(3)
colors = ["blue", "brown", "green", "orange", "pink", "yellow"]
shapes = ["circle", "diamond", "hexagon", "parallelogram", "trapezoid", "triangle"]
possCombo = [(c, s) for c in colors for s in shapes]
def chooseTarget():
   
    if len(possCombo) <= 0:
        return None
    choice = random.randrange(len(possCombo))
    target = possCombo[choice]
    possCombo.remove(target)
    return target

# Main loop:
# - perform simulation steps until Webots is stopping the controller
while robot.step(timestep) != -1:
    # Read the sensors:
    # Enter here functions to read sensor data, like:
    #  val = ds.getValue()

    # Process sensor data here.
    counter+=1
    if(counter < 100):
        print(counter, chooseTarget(), random.randrange(100))
    # Enter here functions to send actuator commands, like:
    #  motor.setPosition(10.0)
    if not possCombo:
        print(counter)
        break
    pass

# Enter here exit cleanup code.
