"""bingoarm controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot
from controller import Camera
from controller import Receiver
from controller import Pen
import random
import struct


# create the Robot instance.
robot = Robot()
camera = robot.getDevice("camera")
receiver = robot.getDevice("receiver")
pen = robot.getDevice("pen")

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

receiver.enable(1)
pen.write(False)

joints = []
for joint in ["shoulder_pan_joint", "shoulder_lift_joint", "elbow_joint", "wrist_1_joint", "wrist_2_joint", "wrist_3_joint"]:
    joints.append(robot.getDevice(joint))


joints[1].setPosition(0)
state=0

counter = 0
found = True

# colors = ["blue", "brown", "green", "orange", "pink", "yellow"]
# shapes = ["circle", "diamond", "hexagon", "parallelogram", "trapezoid", "triangle"]
# possCombo = [(c, s) for c in colors for s in shapes]
# def chooseTarget():

    # if len(possCombo) <= 0:
        # return None
    # choice = random.randrange(len(possCombo))
    # target = possCombo[choice]
    # possCombo.remove(target)
    # return target

def moveArm(joints, one, two, three, four, five, six):
    joints[0].setPosition(one)
    joints[1].setPosition(two)
    joints[2].setPosition(three)
    joints[3].setPosition(four)
    joints[4].setPosition(five)
    joints[5].setPosition(six)
    

targetToJointsMap = {
    1 : (-0.73, -1.34, 2.43, 3.59, 4.76, 0),
    2 : (-0.54, -1.1, 2.055, 3.69, 4.76, 0.18),
    3 : (-0.43, -0.87, 1.6, 3.92, 4.76, 0.27),
    4 : (-0.36, -0.56, 1, 4.2, 4.76, 0.35),
    5 : (-0.18, -0.55, 0.96, 4.3, 4.76, 0.55),
    6 : (-0.22, -0.87, 1.6, 3.97, 4.76, 0.5),
    7 : (-0.28, -1.105, 2.09, 3.69, 4.76, 0.5),
    8 : (-0.385, -1.37, 2.5, 3.57, 4.76, 0.37),
    9 : (0.015, -1.33, 2.43, 3.57, 4.76, 0.72),
    10: (0.005, -1.12, 2.07, 3.66, 4.76, 0.72),
    11: (0.005, -0.85, 1.58, 3.92, 4.76, 0.72),
    12 : (0, -0.55, 0.95, 4.25, 4.76, 0.72),
    13 : (0.175, -0.46, 0.78, 4.3, 4.76, 0.9),
    14 : (,
    15 : (,
    16 : (,
}


targetToCoordMap = {
}

numSquares = 16
row_index = 0
for i in range(numSquares):
    targetToCoordMap[i] = (row_index, i // 4)
    row_index += 1
    if row_index == 4:
        row_index = 0
       
numTargets = 5
randomTargets = random.sample(range(numSquares), numTargets)

targetCounter = 0
# Main loop:
# - perform simulation steps until Webots is stopping the controller
while robot.step(timestep) != -1:
    # Read the sensors:
    # Enter here functions to read sensor data, like:
    #  val = ds.getValue()
    
    if receiver.getQueueLength() > 0:
        print("GOT AT " + robot.getName() + " " + receiver.getData().decode())
        receiver.nextPacket()
        
    # Process sensor data here.
    if state == 0:
        newTarget = randomTargets[targetCounter]
        targetCounter += 1
        if targetCounter >= numTargets:
            break
        state = newTarget
        
    # Move arm to square 1
    elif state==1:
        if counter==0:
            moveArm(joints,-0.73, -1.34, 2.43, 3.59, 4.76, 0)
            counter = counter+1
        elif counter<200:
            counter = counter+1
            pass
        elif found and counter<201:
            pen.write(True)
            moveArm(joints,-0.73, -1.34, 2.43, 3.59, 4.76, 6.28)
            counter=counter+1
        elif found and counter<350:
            counter = counter+1
            pass
        elif found and counter<351:
            moveArm(joints,-0.73, -1.34, 2.43, 3.59, 4.76, -6.28)
            counter=counter+1
        elif found and counter<500:
            counter = counter+1
            pass
        else:
           pen.write(False)
           counter=0
           state=2

    # Move arm to square 2
    elif state==2:
        if counter==0:
            moveArm(joints,-0.54, -1.1, 2.055, 3.69, 4.76, 0.18)
            counter = counter+1
        elif counter<200:
            counter = counter+1
            pass
        elif found and counter<201:
            pen.write(True)
            moveArm(joints,-0.54, -1.1, 2.055, 3.69, 4.76, 6.28)
            counter=counter+1
        elif found and counter<350:
            counter = counter+1
            pass
        elif found and counter<351:
            moveArm(joints,-0.54, -1.1, 2.055, 3.69, 4.76, -6.28)
            counter=counter+1
        elif found and counter<500:
            counter = counter+1
            pass
        else:
           pen.write(False)
           counter=0
           state=3

    # Move arm to square 3
    elif state==3:
        if counter==0:
            moveArm(joints,-0.43, -0.87, 1.6, 3.92, 4.76, 0.27)
            counter = counter+1
        elif counter<200:
            counter = counter+1
            pass
        elif found and counter<201:
            pen.write(True)
            moveArm(joints,-0.43, -0.87, 1.6, 3.92, 4.76, 6.28)
            counter=counter+1
        elif found and counter<350:
            counter = counter+1
            pass
        elif found and counter<351:
            moveArm(joints,-0.43, -0.87, 1.6, 3.92, 4.76, -6.28)
            counter=counter+1
        elif found and counter<500:
            counter = counter+1
            pass
        else:
           pen.write(False)
           counter=0
           state=4

    # Move arm to square 4
    elif state==4:
        if counter==0:
            moveArm(joints,-0.36, -0.56, 1, 4.2, 4.76, 0.35)
            counter = counter+1
        elif counter<200:
            counter = counter+1
            pass
        elif found and counter<201:
            pen.write(True)
            moveArm(joints,-0.36, -0.56, 1, 4.2, 4.76, 6.28)
            counter=counter+1
        elif found and counter<350:
            counter = counter+1
            pass
        elif found and counter<351:
            moveArm(joints,-0.36, -0.56, 1, 4.2, 4.76, -6.28)
            counter=counter+1
        elif found and counter<500:
            counter = counter+1
            pass
        else:
           pen.write(False)
           counter=0
           state=5

    # Move arm to square 5
    elif state==5:
        if counter==0:
            moveArm(joints,-0.18, -0.55, 0.96, 4.3, 4.76, 0.55)
            counter = counter+1
        elif counter<200:
            counter = counter+1
            pass
        elif found and counter<201:
            pen.write(True)
            moveArm(joints,-0.18, -0.55, 0.96, 4.3, 4.76, 6.28)
            counter=counter+1
        elif found and counter<350:
            counter = counter+1
            pass
        elif found and counter<351:
            moveArm(joints,-0.18, -0.55, 0.96, 4.3, 4.76, -6.28)
            counter=counter+1
        elif found and counter<500:
            counter = counter+1
            pass
        else:
           pen.write(False)
           counter=0
           state=6

    # Move arm to square 6
    elif state==6:
        if counter==0:
            moveArm(joints,-0.22, -0.87, 1.6, 3.97, 4.76, 0.5)
            counter = counter+1
        elif counter<200:
            counter = counter+1
            pass
        elif found and counter<201:
            pen.write(True)
            moveArm(joints,-0.22, -0.87, 1.6, 3.97, 4.76, 6.28)
            counter=counter+1
        elif found and counter<350:
            counter = counter+1
            pass
        elif found and counter<351:
            moveArm(joints,-0.22, -0.87, 1.6, 3.97, 4.76, -6.28)
            counter=counter+1
        elif found and counter<500:
            counter = counter+1
            pass
        else:
           pen.write(False)
           counter=0
           state=7


   # Move arm to square 7
    elif state==7:
        if counter==0:
            moveArm(joints,-0.28, -1.105, 2.09, 3.69, 4.76, 0.5)
            counter = counter+1
        elif counter<200:
            counter = counter+1
            pass
        elif found and counter<201:
            pen.write(True)
            moveArm(joints,-0.28, -1.105, 2.09, 3.69, 4.76, 6.28)
            counter=counter+1
        elif found and counter<350:
            counter = counter+1
            pass
        elif found and counter<351:
            moveArm(joints,-0.28, -1.105, 2.09, 3.69, 4.76, -6.28)
            counter=counter+1
        elif found and counter<500:
            counter = counter+1
            pass
        else:
           pen.write(False)
           counter=0
           state=8

   # Move arm to square 8
    elif state==8:
        if counter==0:
            moveArm(joints,-0.385, -1.37, 2.5, 3.57, 4.76, 0.37)
            counter = counter+1
        elif counter<200:
            counter = counter+1
            pass
        elif found and counter<201:
            pen.write(True)
            moveArm(joints,-0.385, -1.37, 2.5, 3.57, 4.76, 6.28)
            counter=counter+1
        elif found and counter<350:
            counter = counter+1
            pass
        elif found and counter<351:
            moveArm(joints,-0.385, -1.37, 2.5, 3.57, 4.76, -6.28)
            counter=counter+1
        elif found and counter<500:
            counter = counter+1
            pass
        else:
           pen.write(False)
           counter=0
           state=9
           
   # Move arm to square 9
    elif state==9:
        if counter==0:
            moveArm(joints,0.015, -1.33, 2.43, 3.57, 4.76, 0.72)
            counter = counter+1
        elif counter<200:
            counter = counter+1
            pass
        elif found and counter<201:
            pen.write(True)
            moveArm(joints,0.015, -1.33, 2.43, 3.57, 4.76, 6.28)
            counter=counter+1
        elif found and counter<350:
            counter = counter+1
            pass
        elif found and counter<351:
            moveArm(joints,0.015, -1.33, 2.43, 3.57, 4.76, -6.28)
            counter=counter+1
        elif found and counter<500:
            counter = counter+1
            pass
        else:
           pen.write(False)
           counter=0
           state=10
            
   # Move arm to square 10
    elif state==10:
        if counter==0:
            moveArm(joints,0.005, -1.12, 2.07, 3.66, 4.76, 0.72)
            counter = counter+1
        elif counter<200:
            counter = counter+1
            pass
        elif found and counter<201:
            pen.write(True)
            moveArm(joints,0.005, -1.12, 2.07, 3.66, 4.76, 6.28)
            counter=counter+1
        elif found and counter<350:
            counter = counter+1
            pass
        elif found and counter<351:
            moveArm(joints,0.005, -1.12, 2.07, 3.66, 4.76, -6.28)
            counter=counter+1
        elif found and counter<500:
            counter = counter+1
            pass
        else:
           pen.write(False)
           counter=0
           state=11
            
   # Move arm to square 11      
    elif state==11:
        if counter==0:
            moveArm(joints,0.005, -0.85, 1.58, 3.92, 4.76, 0.72)
            counter = counter+1
        elif counter<200:
            counter = counter+1
            pass
        elif found and counter<201:
            pen.write(True)
            moveArm(joints,0.005, -0.85, 1.58, 3.92, 4.76, 6.28)
            counter=counter+1
        elif found and counter<350:
            counter = counter+1
            pass
        elif found and counter<351:
            moveArm(joints,0.005, -0.85, 1.58, 3.92, 4.76, -6.28)
            counter=counter+1
        elif found and counter<500:
            counter = counter+1
            pass
        else:
           pen.write(False)
           counter=0
           state=12
            
   # Move arm to square 12      
    elif state==12:
        if counter==0:
            moveArm(joints,0, -0.55, 0.95, 4.25, 4.76, 0.72)
            counter = counter+1
        elif counter<200:
            counter = counter+1
            pass
        elif found and counter<201:
            pen.write(True)
            moveArm(joints,0, -0.55, 0.95, 4.25, 4.76, 6.28)
            counter=counter+1
        elif found and counter<350:
            counter = counter+1
            pass
        elif found and counter<351:
            moveArm(joints,0, -0.55, 0.95, 4.25, 4.76, -6.28)
            counter=counter+1
        elif found and counter<500:
            counter = counter+1
            pass
        else:
           pen.write(False)
           counter=0
           state=13    
         
   # Move arm to square 13      
    elif state==13:
        if counter==0:
            moveArm(joints,0.175, -0.46, 0.78, 4.3, 4.76, 0.9)
            counter = counter+1
        elif counter<200:
            counter = counter+1
            pass
        elif found and counter<201:
            pen.write(True)
            moveArm(joints,0.175, -0.46, 0.78, 4.3, 4.76, 6.28)
            counter=counter+1
        elif found and counter<350:
            counter = counter+1
            pass
        elif found and counter<351:
            moveArm(joints,0.175, -0.46, 0.78, 4.3, 4.76, -6.28)
            counter=counter+1
        elif found and counter<500:
            counter = counter+1
            pass
        else:
           pen.write(False)
           counter=0
           state=14  
            
   # Move arm to square 14      
    elif state==14:
        if counter==0:
            moveArm(joints,0.21, -0.74, 1.33, 4.15, 4.76, 0.95)
            counter = counter+1
        elif counter<200:
            counter = counter+1
            pass
        elif found and counter<201:
            pen.write(True)
            moveArm(joints,0.21, -0.74, 1.33, 4.15, 4.76, 6.28)
            counter=counter+1
        elif found and counter<350:
            counter = counter+1
            pass
        elif found and counter<351:
            moveArm(joints,0.21, -0.74, 1.33, 4.15, 4.76, -6.28)
            counter=counter+1
        elif found and counter<500:
            counter = counter+1
            pass
        else:
           pen.write(False)
           counter=0
           state=15
             
   # Move arm to square 15      
    elif state==15:
        if counter==0:
            moveArm(joints,0.27, -1.01, 1.86, 3.8, 4.76, 1)
            counter = counter+1
        elif counter<200:
            counter = counter+1
            pass
        elif found and counter<201:
            pen.write(True)
            moveArm(joints,0.27, -1.01, 1.86, 3.8, 4.76, 6.28)
            counter=counter+1
        elif found and counter<350:
            counter = counter+1
            pass
        elif found and counter<351:
            moveArm(joints,0.27, -1.01, 1.86, 3.8, 4.76, -6.28)
            counter=counter+1
        elif found and counter<500:
            counter = counter+1
            pass
        else:
           pen.write(False)
           counter=0
           state=16 
            
   # Move arm to square 16      
    elif state==16:
        if counter==0:
            moveArm(joints,0.355, -1.19, 2.22, 3.65, 4.76, 1.08)
            counter = counter+1
        elif counter<200:
            counter = counter+1
            pass
        elif found and counter<201:
            pen.write(True)
            moveArm(joints,0.355, -1.19, 2.22, 3.65, 4.76, 6.28)
            counter=counter+1
        elif found and counter<350:
            counter = counter+1
            pass
        elif found and counter<351:
            moveArm(joints,0.355, -1.19, 2.22, 3.65, 4.76, -6.28)
            counter=counter+1
        elif found and counter<500:
            counter = counter+1
            pass
        else:
           pen.write(False)
           counter=0
           state=1
         
# Enter here exit cleanup code.
