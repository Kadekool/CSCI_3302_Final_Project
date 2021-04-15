"""bingomaster controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
# from controller import Robot
from controller import Supervisor
import random
# create the Robot instance.
# robot = Robot()
supervisor = Supervisor()
# get the time step of the current world.
timestep = int(supervisor.getBasicTimeStep())

# You should insert a getDevice-like function in order to get the
# instance of a device of the robot. Something like:
#  motor = robot.getMotor('motorname')
#  ds = robot.getDistanceSensor('dsname')
#  ds.enable(timestep)

# Main loop:
# - perform simulation steps until Webots is stopping the controller
NUMSQUARES = 16 # board size
colors = ["blue", "brown", "green", "orange", "pink", "yellow"]
shapes = ["circle", "diamond", "hexagon", "parallelogram", "trapezoid", "triangle"]
allCombo = [(c, s) for c in colors for s in shapes]
possCombo = allCombo.copy()
def chooseTarget():
    if len(possCombo) <= 0:
        return None
    choice = random.randrange(len(possCombo))
    target = possCombo[choice]
    possCombo.remove(target)
    return target
def randomize_boards():
    
    for boardName in ["board1"]:
        board = supervisor.getFromDef(boardName)
        
        children = board.getField("children")
        
        if children:
            numSquares = children.getCount()
            randIndexes = random.sample(range(len(allCombo)), numSquares)
            for i in range(numSquares):
                child = children.getMFNode(i)
                shape = child.getField("children").getMFNode(0)
                combo = allCombo[randIndexes[i]]
                shapeName = combo[0] + combo[1].capitalize()
                shape.getField("textureUrl").setMFString(0, "textures/" + shapeName + ".jpg")

randomize_boards()
while supervisor.step(timestep) != -1:
    # Read the sensors:
    # Enter here functions to read sensor data, like:
    #  val = ds.getValue()

    # Process sensor data here.

    # Enter here functions to send actuator commands, like:
    #  motor.setPosition(10.0)

    pass

# Enter here exit cleanup code.
