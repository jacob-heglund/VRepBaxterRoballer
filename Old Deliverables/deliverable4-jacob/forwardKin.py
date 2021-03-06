import numpy as np
import scipy as sp
from numpy import linalg as nl
from scipy import linalg as sl
import math
from math import factorial
import vrep
import time
import scipy

def skew(x):
    return np.array([[0, -x[2], x[1]],
                     [x[2], 0, -x[0]],
                     [-x[1], x[0], 0]])
def dskew(x):
    return np.array[[x[2][1]],[x[0][2]],[x[1][0]]]
def vskew(x):
    return np.array([[0,-x[2],x[1],x[3]],
                     [x[2],0,-x[0],x[4]],
                     [-x[1],x[0],0,x[5]],
                     [0,0,0,0]])  
def dvskew(x):
    return np.array([[x[2][1]],
                    [x[0][2]],
                    [x[1][0]],
                    [x[0][3]],
                    [x[1][3]],
                    [x[2][3]]])
    
  
def Jmaker(theta,s):
    joints = s.shape[1];
    temp = np.zeros((6,joints))
    for i in range(joints):
        if(i == 0):
            temp[:,0] = s[:,0].reshape((6))
            continue 
        cur = sl.expm(vskew(s[:,0])*theta[0])
        for y in range(1,i):
            cur = cur.dot(sl.expm(vskew(s[:,y])*theta[y]))
        temp[:,i] = admaker(cur).dot(s[:,i])
    return temp


def exp(s,t):
    return sl.expm(vskew(s)*t)
    
    
def admaker(x):
    temp = np.zeros((6,6))
    temp[:3,:3] = np.copy(x[:3,:3])
    temp[3:,:3] = np.dot(skew(x[:3,3]), x[:3,:3])
    temp[3:,3:] = np.copy(x[:3,:3])
    return temp


def rad(x):
    return math.radians(x)

def sind(x):
    return np.sin(rad(x))

def cosd(x):
    return np.cos(rad(x))

def TtoM(theta, s,M):
    T = np.identity(4)
    for i in range(theta.size):
        T = T.dot(sl.expm(vskew(s[:,i])*theta[i,0]))
    return T.dot(M)

def td(J, V):
    return nl.inv(np.transpose(J)@J+.1*np.identity(J.shape[1]))@np.transpose(J)@V

def moveObj(T, clientID, objHandle):    
    R = T[0:3, 0:3]
    p = T[0:3, 3]
    cy_thresh = 0
    _FLOAT_EPS_4 = np.finfo(float).eps * 4.0
    try:
        cy_thresh = np.finfo(R.dtype).eps * 4
    except ValueError:
        cy_thresh = _FLOAT_EPS_4 
    r11, r12, r13, r21, r22, r23, r31, r32, r33 = R.flat
    cy = math.sqrt(r33*r33 + r23*r23)
    if cy > cy_thresh: # cos(y) not close to zero, standard form
        z = math.atan2(-r12,  r11) # atan2(cos(y)*sin(z), cos(y)*cos(z))
        y = math.atan2(r13,  cy) # atan2(sin(y), cy)
        x = math.atan2(-r23, r33) # atan2(cos(y)*sin(x), cos(x)*cos(y))
    else: # cos(y) (close to) zero, so x -> 0.0 (see above)
        # so r21 -> sin(z), r22 -> cos(z) and
        z = math.atan2(r21,  r22)
        y = math.atan2(r13,  cy) # atan2(sin(y), cy)
        x = 0.0
    E = np.array([x, y, z])
    
    vrep.simxSetObjectPosition(clientID, objHandle, -1, p, vrep.simx_opmode_streaming)
    vrep.simxSetObjectOrientation(clientID, objHandle, -1, E, vrep.simx_opmode_oneshot)

def leftArmPose(t1,t2,t3,t4,t5,t6,t7,t8):
    #left arm (facing towards baxter)
    thetaLeft = np.array([[math.radians(t1)], [math.radians(t2)], [math.radians(t3)], [math.radians(t4)], [math.radians(t5)], [math.radians(t6)], [math.radians(t7)], [math.radians(t8)]])
    ML = np.array([[1,0,0,.0815],
                  [0,1,0,1.2993],
                  [0,0,1,1.2454],
                  [0,0,0,1]])
        
    a0 = np.array([[0],[0],[1]])
    q0 = np.array([[.0177],[.0032],[.8777]])
    bottom0 = np.dot(-skew(a0),q0)
    S0 = np.zeros((6,1))
    S0[:3] = np.copy(a0)
    S0[3:] = np.copy(bottom0)
        
    a1 = np.array([[0],[0],[1]])
    q1 = np.array([[.0815],[.2622],[1.0540]])
    bottom1 = np.dot(-skew(a1),q1)
    S1 = np.zeros((6,1))
    S1[:3] = np.copy(a1)
    S1[3:] = np.copy(bottom1)
    
    a2 = np.array([[-1],[0],[0]])
    q2 = np.array([[.0815],[.3312],[1.3244]])
    bottom2 = np.dot(-skew(a2),q2)
    S2 = np.zeros((6,1))
    S2[:3] = np.copy(a2)
    S2[3:] = np.copy(bottom2)
    
    a3 = np.array([[0],[1],[0]])
    q3 = np.array([[.0815],[.4332],[1.3244]])
    bottom3 = np.dot(-skew(a3),q3)
    S3 = np.zeros((6,1))
    S3[:3] = np.copy(a3)
    S3[3:] = np.copy(bottom3)
    
    a4 = np.array([[-1],[0],[0]])
    q4 = np.array([[.0815],[.6956],[1.2554]])
    bottom4 = np.dot(-skew(a4),q4)
    S4 = np.zeros((6,1))
    S4[:3] = np.copy(a4)
    S4[3:] = np.copy(bottom4)
    
    a5 = np.array([[0],[1],[0]])
    q5 = np.array([[.0815],[.7992],[1.2554]])
    bottom5 = np.dot(-skew(a5),q5)
    S5 = np.zeros((6,1))
    S5[:3] = np.copy(a5)
    S5[3:] = np.copy(bottom5)
    
    a6 = np.array([[-1],[0],[0]])
    q6 = np.array([[.0815],[1.0699],[1.2454]])
    bottom6 = np.dot(-skew(a6),q6)
    S6 = np.zeros((6,1))
    S6[:3] = np.copy(a6)
    S6[3:] = np.copy(bottom6)
    
    a7 = np.array([[0],[1],[0]])
    q7 = np.array([[.0815],[1.1859],[1.2454]])
    bottom7 = np.dot(-skew(a7),q7)
    S7 = np.zeros((6,1))
    S7[:3] = np.copy(a7)
    S7[3:] = np.copy(bottom7)
    
    s = np.zeros((6,thetaLeft.size))
    s[:,0] = S0.reshape((6))
    s[:,1] = S1.reshape((6))
    s[:,2] = S2.reshape((6))
    s[:,3] = S3.reshape((6))
    s[:,4] = S4.reshape((6))
    s[:,5] = S5.reshape((6))
    s[:,6] = S6.reshape((6))
    s[:,7] = S7.reshape((6))
    
    
    finalLeft = TtoM(thetaLeft,s,ML )
    return finalLeft, s, ML, thetaLeft

def rightArmPose(t1,t2,t3,t4,t5,t6,t7,t8):
    #right arm
    thetaRight= np.array([[math.radians(t1)], [math.radians(t2)], [math.radians(t3)], [math.radians(t4)], [math.radians(t5)], [math.radians(t6)], [math.radians(t7)], [math.radians(t8)]])
    MR = np.array([[1,0,0,.0818],
                  [0,1,0,-1.2929],
                  [0,0,1,1.2454],
                  [0,0,0,1]])
        
    a0 = np.array([[0],[0],[1]])
    q0 = np.array([[.0177],[.0032],[.8777]])
    bottom0 = np.dot(-skew(a0),q0)
    S0 = np.zeros((6,1))
    S0[:3] = np.copy(a0)
    S0[3:] = np.copy(bottom0)
        
    a1 = np.array([[0],[0],[1]])
    q1 = np.array([[.0818],[-.2558],[1.0540]])
    bottom1 = np.dot(-skew(a1),q1)
    S1 = np.zeros((6,1))
    S1[:3] = np.copy(a1)
    S1[3:] = np.copy(bottom1)
    
    a2 = np.array([[1],[0],[0]])
    q2 = np.array([[.0818],[-.3248],[1.3244]])
    bottom2 = np.dot(-skew(a2),q2)
    S2 = np.zeros((6,1))
    S2[:3] = np.copy(a2)
    S2[3:] = np.copy(bottom2)
    
    a3 = np.array([[0],[-1],[0]])
    q3 = np.array([[.0818],[-.4268],[1.3244]])
    bottom3 = np.dot(-skew(a3),q3)
    S3 = np.zeros((6,1))
    S3[:3] = np.copy(a3)
    S3[3:] = np.copy(bottom3)
    
    a4 = np.array([[1],[0],[0]])
    q4 = np.array([[.0818],[-.6892],[1.2554]])
    bottom4 = np.dot(-skew(a4),q4)
    S4 = np.zeros((6,1))
    S4[:3] = np.copy(a4)
    S4[3:] = np.copy(bottom4)
    
    a5 = np.array([[0],[-1],[0]])
    q5 = np.array([[.0818],[-.7928],[1.2554]])
    bottom5 = np.dot(-skew(a5),q5)
    S5 = np.zeros((6,1))
    S5[:3] = np.copy(a5)
    S5[3:] = np.copy(bottom5)
    
    a6 = np.array([[1],[0],[0]])
    q6 = np.array([[.0818],[-1.0635],[1.2454]])
    bottom6 = np.dot(-skew(a6),q6)
    S6 = np.zeros((6,1))
    S6[:3] = np.copy(a6)
    S6[3:] = np.copy(bottom6)
    
    a7 = np.array([[0],[-1],[0]])
    q7 = np.array([[.0818],[-1.1795],[1.2454]])
    bottom7 = np.dot(-skew(a7),q7)
    S7 = np.zeros((6,1))
    S7[:3] = np.copy(a7)
    S7[3:] = np.copy(bottom7)
    
    s = np.zeros((6,thetaRight.size))
    s[:,0] = S0.reshape((6))
    s[:,1] = S1.reshape((6))
    s[:,2] = S2.reshape((6))
    s[:,3] = S3.reshape((6))
    s[:,4] = S4.reshape((6))
    s[:,5] = S5.reshape((6))
    s[:,6] = S6.reshape((6))
    s[:,7] = S7.reshape((6))
    
    
    finalRight = TtoM(thetaRight,s,MR)
    return finalRight, s, MR, thetaRight

# Close all open connections (just in case)
vrep.simxFinish(-1)

# Connect to V-REP (raise exception on failure)
clientID = vrep.simxStart('127.0.0.1', 19997, True, True, 5000, 5)
if clientID == -1:
    raise Exception('Failed connecting to remote API server')

## define Baxter's joints
# define the body joints
bodyJoints = np.zeros(3)
bodyError = np.zeros(3)
vertError, vertJoint = vrep.simxGetObjectHandle(clientID, 'Baxter_verticalJoint', vrep.simx_opmode_blocking)
rotError, rotJoint = vrep.simxGetObjectHandle(clientID, 'Baxter_rotationJoint', vrep.simx_opmode_blocking)
monitorError, monitorJoint = vrep.simxGetObjectHandle(clientID, 'Baxter_monitorJoint', vrep.simx_opmode_blocking)

bodyJoints[0]= vertJoint
bodyError[0] = vertError
bodyJoints[1]= rotJoint
bodyError[1] = rotError
bodyJoints[2]= monitorJoint
bodyError[2] = monitorError
bodyJoints = bodyJoints.astype(int)
bodyError = bodyError.astype(int)

# define the arm joints
# the number of joints per arm
num_joints = 7
i = 0
rightArm = np.zeros(num_joints)
rightError = np.zeros(num_joints)
leftArm = np.zeros(num_joints)
leftError = np.zeros(num_joints)

for i in range(7):
    # define the joint names we ask from v-rep
    rightJointName = 'Baxter_rightArm_joint' + str(i+1)
    leftJointName = 'Baxter_leftArm_joint' + str(i+1)
    
    # get the joint names from v-rep
    rightError[i], rightArm[i] = vrep.simxGetObjectHandle(clientID, rightJointName, vrep.simx_opmode_blocking)
    leftError[i], leftArm[i] = vrep.simxGetObjectHandle(clientID, leftJointName, vrep.simx_opmode_blocking)
rightArm = rightArm.astype(int)
rightError = rightError.astype(int)
leftArm = leftArm.astype(int)
leftError = leftError.astype(int)


# starting position
print('Moving to Initial Position')

r=0
rpose = rightArmPose(0,r,r,r,r,r,r,r)[0] 
l=0
lpose = leftArmPose(45,45,45,45,l,l,l,l)[0]
for i in range(0,7):
    vrep.simxSetJointTargetPosition(clientID, rightArm[i], math.radians(rpose[i]), vrep.simx_opmode_oneshot)
    vrep.simxSetJointTargetPosition(clientID, leftArm[i], math.radians(lpose[i]), vrep.simx_opmode_oneshot)


#TODO: create an array of 30 positions from theta
'''
t1 = np.radians(10)
t2 = np.radians(25)
theta1 = np.array([t1,t1,t1,t1,t1,t1,t1,t1])
theta2 = np.array([t2,t2,t2,t2,t2,t2,t2,t2])


theta = np.array((theta1, theta2))
theta = np.transpose(theta)
'''
time.sleep(3)


for i in range(0,7):
    vrep.simxSetJointTargetPosition(clientID, rightArm[i], math.radians(r), vrep.simx_opmode_oneshot)
    vrep.simxSetJointTargetPosition(clientID, leftArm[i], math.radians(l), vrep.simx_opmode_oneshot)
    
time.sleep(2)



# Before closing the connection to V-REP, make sure that the last command sent out had time to arrive. You can guarantee this with (for example):
vrep.simxGetPingTime(clientID)

# Close the connection to V-REP
vrep.simxFinish(clientID)

























