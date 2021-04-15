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
#ds = robot.getDistanceSensor('dsname')
#ds.enable(timestep)

shoulderPanPos = 0.0
shoulderLiftPos = 0.0
elbowPos = 0.0
wrist1Pos = 0.0
wrist2Pos = 0.0
wrist3Pos = 0.0


camera.enable(1)
joints = []
for joint in ["shoulder_pan_joint", "shoulder_lift_joint", "elbow_joint", "wrist_1_joint", "wrist_2_joint", "wrist_3_joint"]:
    joints.append(robot.getDevice(joint))


counter = 0
joints[1].setPosition(0)
state=1

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

def moveArm(joints, one, two, three, four, five, six):
    joints[0].setPosition(one)
    joints[1].setPosition(two)
    joints[2].setPosition(three)
    joints[3].setPosition(four)
    joints[4].setPosition(five)
    joints[5].setPosition(six)


# Main loop:
# - perform simulation steps until Webots is stopping the controller
while robot.step(timestep) != -1:
    # Read the sensors:
    # Enter here functions to read sensor data, like:
    #  val = ds.getValue()

    # Process sensor data here.
    if state == 0:
        counter+=1
        if(counter < 100):
            print(counter, chooseTarget(), random.randrange(100))
        pass
        
    # Move arm to square 1
    elif state==1:
        if counter==0:
            moveArm(joints,-0.73, -1.34, 2.43, 3.59, 4.76, 0)
            counter = counter+1
        elif counter<300:
            counter = counter+1
            pass
        else:
           counter=0
           state=2

    # Move arm to square 2
    elif state==2:
        if counter==0:
            moveArm(joints,-0.54, -1.1, 2.055, 3.69, 4.76, 0.18)
            counter = counter+1
        elif counter<300:
            counter = counter+1
            pass
        else:
           counter=0
           state=3

    # Move arm to square 3
    elif state==3:
        if counter==0:
            moveArm(joints,-0.43, -0.87, 1.6, 3.92, 4.76, 0.27)
            counter = counter+1
        elif counter<300:
            counter = counter+1
            pass
        else:
           counter=0
           state=4

    # Move arm to square 4
    elif state==4:
        if counter==0:
            moveArm(joints,-0.36, -0.56, 1, 4.2, 4.76, 0.35)
            counter = counter+1
        elif counter<300:
            counter = counter+1
            pass
        else:
           counter=0
           state=5

    # Move arm to square 5
    elif state==5:
        if counter==0:
            moveArm(joints,-0.18, -0.55, 0.96, 4.3, 4.76, 0.55)
            counter = counter+1
        elif counter<300:
            counter = counter+1
            pass
        else:
           counter=0
           state=6

    # Move arm to square 6
    elif state==6:
        if counter==0:
            moveArm(joints,-0.22, -0.87, 1.6, 3.97, 4.76, 0.5)
            counter = counter+1
        elif counter<300:
            counter = counter+1
            pass
        else:
           counter=0
           state=7


   # Move arm to square 7
    elif state==7:
        if counter==0:
            moveArm(joints,-0.28, -1.105, 2.09, 3.69, 4.76, 0.5)
            counter = counter+1
        elif counter<300:
            counter = counter+1
            pass
        else:
           counter=0
           state=8

   # Move arm to square 8
    elif state==8:
        if counter==0:
            moveArm(joints,-0.385, -1.37, 2.5, 3.57, 4.76, 0.37)
            counter = counter+1
        elif counter<300:
            counter = counter+1
            pass
        else:
           counter=0
           state=9
           
   # Move arm to square 9
    elif state==9:
        if counter==0:
            moveArm(joints,0.015, -1.33, 2.43, 3.57, 4.76, 0.72)
            counter = counter+1
        elif counter<300:
            counter = counter+1
            pass
        else:
            counter=0
            state=10
            
   # Move arm to square 10
    elif state==10:
        if counter==0:
            moveArm(joints,0.005, -1.12, 2.07, 3.66, 4.76, 0.72)
            counter = counter+1
        elif counter<300:
            counter = counter+1
            pass
        else:
            counter=0
            state=11
            
   # Move arm to square 11      
    elif state==11:
        if counter==0:
            moveArm(joints,0.005, -0.85, 1.58, 3.92, 4.76, 0.72)
            counter = counter+1
        elif counter<300:
            counter = counter+1
            pass
        else:
            counter=0
            state=12
            
   # Move arm to square 12      
    elif state==12:
        if counter==0:
            moveArm(joints,0, -0.55, 0.95, 4.25, 4.76, 0.72)
            counter = counter+1
        elif counter<300:
            counter = counter+1
            pass
        else:
            counter=0
            state=13      
         
   # Move arm to square 13      
    elif state==13:
        if counter==0:
            moveArm(joints,0.175, -0.46, 0.78, 4.3, 4.76, 0.9)
            counter = counter+1
        elif counter<300:
            counter = counter+1
            pass
        else:
            counter=0
            state=14  
            
   # Move arm to square 14      
    elif state==14:
        if counter==0:
            moveArm(joints,0.21, -0.74, 1.33, 4.15, 4.76, 0.95)
            counter = counter+1
        elif counter<300:
            counter = counter+1
            pass
        else:
            counter=0
            state=15  
   
   # Move arm to square 15      
    elif state==15:
        if counter==0:
            moveArm(joints,0.27, -1.01, 1.86, 3.8, 4.76, 1)
            counter = counter+1
        elif counter<300:
            counter = counter+1
            pass
        else:
            counter=0
            state=16  
            
   # Move arm to square 16      
    elif state==16:
        if counter==0:
            moveArm(joints,0.355, -1.19, 2.22, 3.65, 4.76, 1.08)
            counter = counter+1
        elif counter<300:
            counter = counter+1
            pass
        else:
            counter=0
            state=1  
         
# Enter here exit cleanup code.
