# -*- coding: utf-8 -*-
"""
Created on Sun May 14 07:53:31 2023

@author: Wesni
"""

import numpy as np
from Quaternion import Quaternion as quat

def runModel(sens1,sens2,sens3,pot):
    #Parse out the data. The first four elements of sens1,2,3 are quaternion values.
    #The last three are values related to calibration quality.
    Quat1 = quat(float(sens1[0]),float(sens1[1]),float(sens1[2]),float(sens1[3]))
    Cal1 = [int(sens1[4]),int(sens1[5]),int(sens1[6])]
    Quat2 = quat(float(sens2[0]),float(sens2[1]),float(sens2[2]),float(sens2[3]))
    Cal2 = [int(sens2[4]),int(sens2[5]),int(sens2[6])]
    Quat3 = quat(float(sens3[0]),float(sens3[1]),float(sens3[2]),float(sens3[3]))
    Cal3 = [int(sens3[4]),int(sens3[5]),int(sens3[6])]
    #get potentiometer value
    pot = float(pot[0])
    
    #Print calibration values to console, for reference. Each time the sensors
    #are powered on the user is obligated to run through a calibration routine.
    #This routine is described here 
    #https://learn.adafruit.com/adafruit-bno055-absolute-orientation-sensor/device-calibration)
    print("------")
    print("Calibration sensor 1: "+ str(Cal1[0])+":"+ str(Cal1[1])+":"+ str(Cal1[2]))
    print("Calibration sensor 2: "+ str(Cal2[0])+":"+ str(Cal2[1])+":"+ str(Cal2[2]))
    print("Calibration sensor 3: "+ str(Cal3[0])+":"+ str(Cal3[1])+":"+ str(Cal3[2]))
    
    #Quaternion rotation of base vectors to get rotated vectors
    #The model of the human arm is described using 4 vectors. Three are the 
    #long axis vectors of the upper arm, lower arm, and hand body segments. A
    #fourth vector is tangent to to the long axis hand vector and coplaner with
    #the palm (aka hand tangent vector). 
    #The long axis vectors of the user's upper arm, lower arm, and hand are
    #represented by the vector [-1,0,0] (quaternion [0,-1,0,0]). The second
    #hand vector is [0,-1,0] (quaternion [0,0,-1,0])
    vect1   = np.array(quat(0,-1,0,0).rotate(Quat1)[:])       
    vect2   = np.array(quat(0,-1,0,0).rotate(Quat2)[:])  
    vect3   = np.array(quat(0,-1,0,0).rotate(Quat3)[:])
    vect3p  = np.array(quat(0,0,-1,0).rotate(Quat3)[:])
       
    #Finding the position of the hand
    L = 100 #Upper and forearm lengths (assumed equal, semi-arbitrarily defined as "100% total length")
    #Position of hand found by adding upper arm and forearm vectors.
    #These are assumed equal length for the purposes of this model. They are
    #close enough in length and the human eye can compensate easily (this is
    #controlled manually after all)
    coord = [(vect1[1]+vect2[1])*L,(vect1[2]+vect2[2])*L,(vect1[3]+vect2[3])*L] 
    
    #These coordinates are mapped to the robot coordinate system. The z and y 
    #vectors needed to be swapped for this to work since the human and robot
    #models define different coordinate systems. The way I set this up the human
    #system treats x-y as horizontal and z as vertical while the robot treats
    #x-z as horizontal and y as vertical. This only has to do with how I did my
    #math.
    x = coord[0]
    y = coord[2]
    z = coord[1]
    
    #--------------------Angles of joints before end effector
    
    l = 100 #Robot arm segment length (also defined as 100% for simplicity)
    
    #q1 is the angle of the first base motor. This is found using the horizontal
    #x and z components
    q1 = np.arctan(z/x)*(360/(2*3.14))
    
    #A new plane is defined to find q2 and q3. This x'z plane is defined where
    #x' is an axis in the x-y plane set q1 degrees from x. Both the upper arm
    #and forearm segments of the robot lie in this plane. The x' component in
    #the x'z plane is first found using the original x and z components. The x'
    #and y components are then used to find the magnitude of r where r is the
    #length between the origin and the end effector.
    xp = np.sqrt(x**2+z**2) #component in the x prime plane
    r = np.sqrt(xp**2+y**2)
    
    #q3 can now be found using r since it forms an isosceles triangle with the
    #two arm segments. This trangle can be bisected into two right triangles where
    #the hypotenus is l and the opposite side (to q3) is r/2. The arc sine of these
    #componentes is used to fine q3/2.
    q3 = 2*(np.arcsin((r/2)/l)).degrees()
    
    #q2 is found as an addition of two angles above and below the r vector. 
    #The angle above the r vector is found using the arc cosine of l and r/2
    #from the right triangle previously described. The angle below r is found
    #from the arc tangent of the y component and x' component.
    q2 = (np.arccos((r/2)/l)+np.arctan(y/xp)).degrees()
 
    #-----------------------Orientation of end effector
    
    #Before the angles of the end effector can be found we first need to define
    #it's base coordinate system (expressed as v1,v2,v3). In other words we need
    #to define the "neutral orientation."
    #v1 is a vector defining the "forward direction" of the end effector. This is
    #defined by normalizing the end effector coordinates vector.
    v1 = coord/(np.sqrt(coord[0]**2+coord[1]**2+coord[2]**2)) #Forward, shoulder to coord
    #The v2 "up direction" vector is defined by the cross product of the v1
    #"forward direction" vector and the upper arm vector of the human model.
    #This vector is colinear with the user's elbow joint and normal to the top
    #of the user's hand when it is held in a neutral position.
    v2 = np.cross(v1,vect1[1:4]) #Up, normal to v1/upper arm plane
    v2 = v2/np.sqrt(v2[0]**2+v2[1]**2+v2[2]**2) #normalization
    #The v3 is the cross between v1 and v2 and completes the coordinate system
    v3 = np.cross(v1,v2) #Right, normal to v1 and v2
    v3 = v3/np.sqrt(v3[0]**2+v3[1]**2+v3[2]**2) #normalization

    #The FE (flexion extension) angle is found using the vect3 (hand long axis)
    #vector. This vector is projected onto the v1 and v2 axes of the end effetor
    #base coordinate system. The FE angle is then found using the arc tangent 
    #of these two components. An additional adjustment is applied to compensate
    #for the q3 angle (since changes to q3 move the end effector away from the v1
    #forward axis)
    FEproj1 = np.dot(vect3[1:4],v1)/1
    FEproj2 = np.dot(vect3[1:4],v2)/1
    FE = np.arctan(FEproj2/FEproj1).degrees() #Flexion Extension angle
    FE = FE + (120-q3)/2 #adjustment since v1 doesn't line up with robot arm segment

    #The ROT rotation angle is found using the human model vect3p (hand tangent
    #vector). Projections are made of this axis into the v2-v3 plane. The angle
    #is found as the arc tangent of these components
    ROTproj1 = np.dot(vect3p[1:4],v3)/1
    ROTproj2 = np.dot(vect3p[1:4],v2)/1
    ROT = np.arctan(ROTproj2/ROTproj1).degrees() #Wrist rotation angle
    
    #Finally the AA (abduction adduction) angle is found in the v1-v3 plane
    #between the projections of the vect3p (hand tangent vector) along the
    #v1 and v3 axes.
    AAproj1 = np.dot(vect3p[1:4],v1)/1
    AA = np.arctan(AAproj1/ROTproj1).degrees() #Abduction Adduction angle

    #The gripper angle is found by mapping the potentiometer value to the gripper
    #angle
    Grip = -1*(pot-0.43)*(100/(0.43-0.29))
    
    #All of the angles are returned from the runModel function
    return q1,q2,q3,FE,ROT,AA,Grip

