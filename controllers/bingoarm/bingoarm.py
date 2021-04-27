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
import ikpy
from ikpy.chain import Chain
import math
import tempfile
import math
import pickle
import gzip
import numpy as np
from PIL import Image
import cv2
import os
from sklearn.neighbors import KNeighborsClassifier
import copy

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
    jointToAdd = robot.getDevice(joint)
    position_sensor = jointToAdd.getPositionSensor()
    position_sensor.enable(1)
    joints.append(jointToAdd)
    


joints[1].setPosition(0)


counter = 0
found = True
snapshotTaken = False


class KNN():
    def __init__(self, directory = 'Shapes'):
        file = open('data.pkl', 'wb') 
        self.y = []
        temp = []
        self.dict = {}
        self.index = 0

        self.name_finder = {}

        colors = ['blue', 'pink', 'yellow', 'green', 'orange']
        shapes = ['Circle', 'Diamond', 'Parallelogram', 'Trapezoid', 'Triangle']

        self.found = set()
        self.indices = {}

        i = 0
        for filename in os.listdir('Shapes'):
            if 'jpg' not in filename:
                continue

            for color in colors:
                for shape in shapes:
                    if color in filename and shape in filename:
                        
                        if str(color + ' ' + shape) not in self.indices:
                            self.indices[str(color + ' ' + shape)] = []
                        else:
                            self.indices[str(color + ' ' + shape)].append(i)

                        self.name_finder[i] = str(color + ' ' + shape)

                        self.y.append(str(filename))
                        string = 'Shapes/'+ filename
                        im = cv2.imread(string)
                        temp.append(im)
                        i += 1

        pickle.dump(temp, file)
        file.close()

        self.X = ""
        with open('data.pkl', 'rb') as pickle_file:
            self.X = pickle.load(pickle_file)
    
    def setup(self):
        X_temp = []
        maxSize = 0

        for row in self.X:
            temp = []
            if row is None:
                continue
            for item1 in row:
                for item in item1:
                    for c in item:
                        temp.append(c)
            maxSize = max(len(temp), maxSize)

        for row in self.X:
            temp = []
            if row is None:
                continue
            for item1 in row:
                for item in item1:
                    for c in item:
                        temp.append(c)

            temp = [temp[i] if i < len(temp) else 0 for i in range(maxSize) ]
            temp = np.array(temp)
            X_temp.append(temp)

        self.X = [X_temp[i] for i in range(len(X_temp))]

        namestore = {i:self.y[i] for i in range(len(self.y))}

        self.y = [i for i in range(len(X_temp))]

        self.neigh = KNeighborsClassifier(n_neighbors=3)

        self.neigh.fit(self.X, self.y)
        self.maxSize = maxSize
        
    def run(self, path = None):
        
        file = open('data2.pkl', 'wb') 
        y_2 = []
        temp = []

        y_2.append(path)

        im = cv2.imread(path)
        temp.append(im)

        pickle.dump(temp, file)
        file.close()

        X_t = ""
        try:
            with open('data2.pkl', 'rb') as pickle_file:
                X_t = pickle.load(pickle_file)
            for row in X_t:
    
                temp = []
                for item1 in row:
                    for item in item1:
                        for c in item:
                            temp.append(c)
    
                temp = [temp[i] if i < len(temp) else 0 for i in range(self.maxSize) ]
                X_t = temp
    
            print(self.name_finder[self.neigh.predict(np.array(X_t).reshape(1, -1))[0]])
    
            self.found.add(self.name_finder[self.neigh.predict(np.array(X_t).reshape(1, -1))[0]])
            self.dict[self.name_finder[self.neigh.predict(np.array(X_t).reshape(1, -1))[0]]] = self.index
    
            self.neigh = KNeighborsClassifier(n_neighbors=3)
    
            self.neigh.fit([self.X[i] for i in range(len(self.X)) if self.name_finder[i] not in self.found], [self.y[i] for i in range(len(self.y)) if self.name_finder[i] not in self.found])
        except:
            pass
        self.index += 1
    def get_dict(self):
        return self.dict







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
knn1 = KNN()
knn2 = KNN()

if(robot.getName() == "player1"):
    knn = knn1
else:
    knn = knn2
knn.setup()


shapeToTargetMap = {}

def moveArmToTarget(target, squareNum):
    angles = targetToJointsMap[target]
    for i in range(len(joints)):
        joints[i].setPosition(angles[i])
    robot.step(timestep*200)
    if (squareNum!=-1):
         filename = "square" + str(squareNum) + str(robot.getName()) +".jpg"
         camera.saveImage(filename, 100)
         knn.run(filename)
             

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
        

#ATTEMPTED TO USE IKPY BUT COULDN't get it to work
"""

filename = None
with tempfile.NamedTemporaryFile(suffix='.urdf', delete=False) as file:
    filename = file.name
    file.write(robot.getUrdf().encode('utf-8'))
    
armChain = Chain.from_urdf_file(filename)   
for i in [0, 6]:
    armChain.active_links_mask[0] = False
    
def ikHelper(xyz,xyzO, orientation_axis):
    ik = armChain.inverse_kinematics(xyz)
    ikResults = armChain.inverse_kinematics(target_position=xyz, target_orientation=xyzO, initial_position=ik, orientation_mode=orientation_axis)
    ikResults = ikResults[1:]
    return ikResults
  
def calculateIk():
    #Square1  
    xyz = [0.37138053,-0.15253127, 0.23241167]
    xyzO = [0.02, 0.007, -0.38]
    orientation_axis = "Y"
    ikResults = ikHelper(xyz,xyzO,orientation_axis)
    targetToJointsMap[0] = ikResults
    
    
    #Square2
    xyz = [0.51402271, -0.15189024, 0.22850214]
    xyzO = [0.04,0, -0.48]
    ikResults = ikHelper(xyz,xyzO,orientation_axis)
    ikResults[5] = 0.18
    targetToJointsMap[1] = ikResults
    
    
    #Square3
    xyz = [0.66120012,-0.15581998, 0.232662]
    xyzO = [0.1 ,-0.2,-1.9]
    ikResults = ikHelper(xyz,xyzO,orientation_axis)
    ikResults[5] = 0.25
    targetToJointsMap[2] = ikResults
    
    #Square4
    xyz = [0.80947788, -0.16151161, 0.22901874]
    xyzO = [0,0, -0.25]
    ikResults = ikHelper(xyz,xyzO,orientation_axis)
    #ikResults[5] = 0.18
    targetToJointsMap[3] = ikResults
    
    #Square5
    xyz = [0.83254614, -0.01529753, 0.22912641]
    xyzO = [0,0, -10]
    ikResults = ikHelper(xyz,xyzO,orientation_axis)
    #ikResults[5] = 0.18
    targetToJointsMap[4] = ikResults
    
    #Square6
    xyz = [0.67933876,-0.01460383, 0.22766602]
    xyzO = [0,0, 0]
    ikResults = ikHelper(xyz,xyzO,orientation_axis)
    #ikResults[5] = 0.18
    targetToJointsMap[5] = ikResults
    
    #Square7
    xyz = [0.52480051,-0.01147862,0.21981785]
    xyzO = [0,0, 0]
    ikResults = ikHelper(xyz,xyzO,orientation_axis)
    #ikResults[5] = 0.18
    targetToJointsMap[6] = ikResults
    
    #Square8
    xyz = [0.37656639,-0.00800924,0.22617036]
    xyzO = [0,0, 0]
    ikResults = ikHelper(xyz,xyzO,orientation_axis)
    #ikResults[5] = 0.18
    targetToJointsMap[7] = ikResults
    
    #Square9
    xyz = [3.77019582e-01,1.39670794e-01,2.30622561e-01 ]
    xyzO = [0,0, 0]
    ikResults = ikHelper(xyz,xyzO,orientation_axis)
    #ikResults[5] = 0.18
    targetToJointsMap[8] = ikResults
    
    #Square10
    xyz = [0.51198466, 0.13656162, 0.23690503]
    xyzO = [0,0,0]
    ikResults = ikHelper(xyz,xyzO,orientation_axis)
    #ikResults[5] = 0.18
    targetToJointsMap[9] = ikResults
    
    #Square11
    xyz = [0.67172822,0.13736034,0.22711638]
    xyzO = [0,0,0]
    ikResults = ikHelper(xyz,xyzO,orientation_axis)
    #ikResults[5] = 0.18
    targetToJointsMap[10] = ikResults
    
    #Square12
    xyz = [0.82318425,0.134,0.23872524]
    xyzO = [0,0,0]
    ikResults = ikHelper(xyz,xyzO,orientation_axis)
    #ikResults[5] = 0.18
    targetToJointsMap[11] = ikResults
    
    #Square13
    xyz = [0.81614503,0.28037986,0.23759393]
    xyzO = [0,0,0]
    ikResults = ikHelper(xyz,xyzO,orientation_axis)
    #ikResults[5] = 0.18
    targetToJointsMap[12] = ikResults
    
    #Square14
    xyz = [0.69535911,0.28522052,0.22871836]
    xyzO = [0,0,0]
    ikResults = ikHelper(xyz,xyzO,orientation_axis)
    #ikResults[5] = 0.18
    targetToJointsMap[13] = ikResults
    
    #Square15
    xyz = [0.52763953,0.28506573,0.23463669]
    xyzO = [0,0,0]
    ikResults = ikHelper(xyz,xyzO,orientation_axis)
    #ikResults[5] = 0.18
    targetToJointsMap[14] = ikResults
    
    #Square16
    xyz = [0.3844702,0.28543608,0.22473412]
    xyzO = [0,0,0]
    ikResults = ikHelper(xyz,xyzO,orientation_axis)
    #ikResults[5] = 0.18
    targetToJointsMap[15] = ikResult    
"""
        

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
            moveArmToTarget(squareNum, squareNum)
        print("ROBOT IS DONE PROCESSING")
        shapeToTargetMap = knn.get_dict()
        print(shapeToTargetMap)
        emitter.send(bytes("Ready", 'utf-8'))
        state = "wait"
               
    if state == "play":
       
        if targetCounter >= len(randomTargets):
            break
        targetCounter += 1
        if newTarget:
            moveArmToTarget(newTarget, -1)
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
            if newTarget in shapeToTargetMap:
                newTarget = shapeToTargetMap[newTarget]
            else:
                newTarget = None
            receiver.nextPacket()
            state = "play"
     

    
         
# Enter here exit cleanup code.
