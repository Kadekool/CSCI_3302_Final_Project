"""bingoarm controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot
from controller import Camera
from controller import Receiver
from controller import Pen
from controller import Emitter
import random
import struct


# create the Robot instance.
robot = Robot()
camera = robot.getDevice("camera")
pen = robot.getDevice("pen")
emitter = robot.getDevice("emitter")
emitter.setChannel(1)
receiver = robot.getDevice("receiver")
receiver.enable(1)
receiver.setChannel(0)


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
pen.write(False)

joints = []
for joint in ["shoulder_pan_joint", "shoulder_lift_joint", "elbow_joint", "wrist_1_joint", "wrist_2_joint", "wrist_3_joint"]:
    joints.append(robot.getDevice(joint))


joints[1].setPosition(0)


counter = 0
found = True
snapshotTaken = False

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
 
def moveArmToTarget(target):
    angles = targetToJointsMap[target]
    for i in range(len(joints)):
        joints[i].setPosition(angles[i])
    robot.step(timestep*200)

def draw():
    pen.write(True)
    joints[5].setPosition(6.28)
    robot.step(timestep*149)
    joints[5].setPosition(-6.28)
    robot.step(timestep*149)
    pen.write(False)
    

targetToJointsMap = {
    0 : (-0.73, -1.34, 2.43, 3.59, 4.76, 0),
    1 : (-0.54, -1.1, 2.055, 3.69, 4.76, 0.18),
    2 : (-0.43, -0.87, 1.6, 3.92, 4.76, 0.27),
    3 : (-0.36, -0.56, 1, 4.2, 4.76, 0.35),
    4 : (-0.18, -0.55, 0.96, 4.3, 4.76, 0.55),
    5 : (-0.22, -0.87, 1.6, 3.97, 4.76, 0.5),
    6 : (-0.28, -1.105, 2.09, 3.69, 4.76, 0.5),
    7 : (-0.385, -1.37, 2.5, 3.57, 4.76, 0.37),
    8 : (0.015, -1.33, 2.43, 3.57, 4.76, 0.72),
    9: (0.005, -1.12, 2.07, 3.66, 4.76, 0.72),
    10: (0.005, -0.85, 1.58, 3.92, 4.76, 0.72),
    11 : (0, -0.55, 0.95, 4.25, 4.76, 0.72),
    12 : (0.175, -0.46, 0.78, 4.3, 4.76, 0.9),
    13 : (0.21, -0.74, 1.33, 4.15, 4.76, 0.95),
    14 : (0.27, -1.01, 1.86, 3.8, 4.76, 1),
    15 : (0.355, -1.19, 2.22, 3.65, 4.76, 1.08),
}


targetToCoordMap = {
}
#      COL 0  1  2  3
#  ROW
#  0       0  7  8  15
#  1       1  6  9  14
#  2       2  5  10 13
#  3       3  4  11 12
#


numSquares = 16
row_index = 0
for i in range(numSquares):
    col = i // 4
    
    targetToCoordMap[i] = (row_index, col)
    if col % 2 == 0:
        row_index += 1
        if ((i+1)//4) % 2 == 1:
            row_index -= 1
    else:
        row_index -= 1
        if ((i+1)//4) % 2 == 0:
           row_index += 1
 
       
numTargets = 25
randomTargets = random.sample(range(numTargets), numTargets)
targetCounter = 0


L = 4

bingoBoard = [[0 for w in range(L)] for j in range(L)]

def isBingo():
    bingo = True
    for i in range(L):
        if bingoBoard[i][i] == 0:
            bingo = False
    if bingo: return bingo
    
    bingo = True
    for i in range(L):
        if bingoBoard[L - i - 1][i] == 0: bingo = False
    
    if bingo: return bingo
    
    
    for row in range(L):
        bingo = True
        for col in range(L):
            if bingoBoard[row][col] == 0: bingo = False
        if bingo: return bingo
    for col in range(L):
        bingo = True
        for row in range(L):
            if bingoBoard[row][col] == 0: bingo = False
        if bingo: return bingo
    
    
    
    
    
        

isBingo()
# Main loop:
# - perform simulation steps until Webots is stopping the controller
newTarget = None
state="process"
a = 0
while robot.step(timestep) != -1:
    # Read the sensors:
    # Enter here functions to read sensor data, like:
    #  val = ds.getValue()
        
    # Process sensor data here.
    if state == "process":
        for squareNum in range(numSquares):
            moveArmToTarget(squareNum)
        print("ROBOT IS DONE PROCESSING")
        emitter.send(bytes("Ready", 'utf-8'))
        state = "wait"
               
    if state == "play":
       
        if targetCounter >= len(randomTargets):
            break
        targetCounter += 1
        if newTarget < numSquares:
            moveArmToTarget(newTarget)
            if found:
                x, y = targetToCoordMap[newTarget]
                bingoBoard[x][y] = 1
                draw()
                if isBingo():
                    print("BINGO!")
                    emitter.send(bytes(robot.getName(), 'utf-8'))
                    break
                
                
        emitter.send(bytes("Ready", 'utf-8'))
        
        state = "wait"
            
    if state == "wait":
        if receiver.getQueueLength() > 0:
            newTarget = receiver.getData().decode()
            
            newTarget = randomTargets[int(newTarget.split()[0])] # for testing just get int for now
            if newTarget <= 16:
                a += 1
            # print("FINDING: " + str(newTarget) + " " + str(a))
            receiver.nextPacket()
            state = "play"
     
     
     
     
 ###################################################################################  
     # NOT USING ANYTHING BELOW: KEEP FOR REFERENCE
     # TODO: MOVE SNAPSHOT FEATURE TO CODE ABOVE IF POSSIBLE
 ################################################################################
     
            
    # Move arm to square 1
    elif state==1:
        if counter==0:
            moveArm(joints,-0.73, -1.34, 2.43, 3.59, 4.76, 0)
            counter = counter+1
        elif counter<200:
            counter = counter+1
            pass
        elif found and counter<201:
            if snapshotTaken==False:
                snapshotTaken=True
                camera.saveImage("square1.jpg", 100)
                pass
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
           snapshotTaken=False
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
            if snapshotTaken==False:
                snapshotTaken=True
                camera.saveImage("square2.jpg", 100)
                pass
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
           snapshotTaken=False
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
            if snapshotTaken==False:
                snapshotTaken=True
                camera.saveImage("square3.jpg", 100)
                pass
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
           snapshotTaken=False
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
            if snapshotTaken==False:
                snapshotTaken=True
                camera.saveImage("square4.jpg", 100)
                pass
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
           snapshotTaken=False
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
            if snapshotTaken==False:
                snapshotTaken=True
                camera.saveImage("square5.jpg", 100)
                pass
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
           snapshotTaken=False
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
