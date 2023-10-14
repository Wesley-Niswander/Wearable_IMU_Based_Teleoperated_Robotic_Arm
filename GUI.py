# -*- coding: utf-8 -*-
"""
Created on Sun Nov  6 17:36:08 2022

@author: Wesni
"""

import serial
import requests
from PyQt5.QtWidgets import QWidget,QPushButton,QListWidget,QGridLayout
from PyQt5.QtCore import QTimer
import time

from Model import runModel

class WinForm(QWidget):
    def __init__(self,parent=None):
        super(WinForm, self).__init__(parent)
        self.setWindowTitle('TRS')
        
        self.listFile=QListWidget()
        
        # Set up buttons
        self.startBtn=QPushButton('Start')
        self.transBtn=QPushButton('Transmit')
        self.serOpenBtn=QPushButton('Open Serial')
        self.serBtn=QPushButton('Close Serial')
        self.endBtn=QPushButton('Stop')
        
        layout=QGridLayout()
        
        #arrange buttons in window
        layout.addWidget(self.startBtn,1,0)
        layout.addWidget(self.endBtn,1,1)
        layout.addWidget(self.transBtn,1,2)
        layout.addWidget(self.serOpenBtn,1,3)
        layout.addWidget(self.serBtn,1,4)
        
        # Timer allows for continual running of runModel event so that the 
        # robot can continuously be sent data
        self.timer=QTimer()
        self.timer.timeout.connect(self.runModel)
        
        #Timing button callbacks for starting and stopping timer. Starting timer
        #triggers the continual calling of runModel. Stopping the timer ends this.
        self.startBtn.clicked.connect(self.startTimer)
        self.endBtn.clicked.connect(self.endTimer)
        
        #Transmission button callback. This event sets the variable self.transmitting
        #to true. When true, this variable triggers the transmit event from within
        #the runModel event. ie it runs the model AND sends data.
        self.transBtn.clicked.connect(self.beginTransmission)
        self.transmitting = False
        
        #Serial connect/disconnect callbacks for arm-mounted Arduinos
        self.serOpenBtn.clicked.connect(self.openSer)
        self.serBtn.clicked.connect(self.CloseSer)
        
        self.setLayout(layout)
        
        #Set up persistent TCP session
        self.s = requests.Session() #Opens a session which can be reused

    def runModel(self):
        
        #Get data from Arduinos over Serial
        self.ser.write(b'q') #q for query, triggers Arduino to spit out data
        sens1 = self.ser.readline().decode('utf-8').split(",") #first Arduino handles IMU 1 and 2
        sens2 = self.ser.readline().decode('utf-8').split(",")
        self.ser_2.write(b'q')
        sens3 = self.ser_2.readline().decode('utf-8').split(",") #second Arduino handles IMU 3 and potentiometer
        pot = self.ser_2.readline().decode('utf-8').split(",")
        
        #Run the kinematic model itself. Returns angles for robot.
        self.q1,self.q2,self.q3,self.FE,self.ROT,self.AA,self.Grip = runModel(sens1,sens2,sens3,pot)  
        
        #The model is in bounds. Coerce the values and tranform them to 
        #the motor reference frames (i.e. zero in the model might not
        #be zero for the motor. Need to mirror/ offset things...)
        
        #Coercions to avoid over turning motors/breaking things...
        #FE between -90 and +90
        if self.FE > 90:
            self.FE = 90
        if self.FE < -90:
            self.FE = -90
        #ROT between -90 and +90
        if self.ROT > 90:
            self.ROT = 90
        if self.ROT < -90:
            self.ROT = -90
        #AA between -50 and +50
        if self.AA > 50:
            self.AA = 50
        if self.AA < -50:
            self.AA = -50
        #Grip between 0 and 100
        if self.Grip > 100:
            self.Grip = 100
        if self.Grip < 0:
            self.Grip = 0
            
        #Transform model angles to motor angles. Apply mirroring/offsets as necessary.   
        self.Angles = [90-self.q1,self.q2,self.q3,180-(90+self.FE),-1*self.ROT+90,self.AA+103/2,self.Grip]
        print(self.Angles)
        
        if  self.q3 > 180. or self.q3 < 0. or self.q2 > 180. or self.q2 < 0. or self.q1 > 180. or self.q1 < 0.:
            #Don't do anything if outside of working box. Working box is the
            #North-East quadrant when the user faces north.
            print("Out of bounds")
        else:
            if self.transmitting == True: 
                #Transmit data over wifi to ESP32
                self.Transmit()
                
    def Transmit(self):
        #Send motor angles to ESP32 server via HTTP request
        payload = {'M1':self.Angles[0],
                   'M2':self.Angles[1],
                   'M3':self.Angles[2], 
                   'M4':self.Angles[3],
                   'M5':self.Angles[4],
                   'M6':self.Angles[5],
                   'M7':self.Angles[6]}
        timebefore = time.time()
        r = self.s.get('http://192.168.4.1/moveitmoveit',params=payload)
        print("time to send: ",end = " ")
        print(time.time()-timebefore)
        #send time of request is about 15ms typically. Bottleneck is still at
        #the BNO055 sensors.
        print(r)
        
    def startTimer(self):
        #Begins data collection and modeling by continually running runModel event
        self.timer.start(20) #sample rate of sensor is 100ms. This is being oversampled. 
        self.startBtn.setEnabled(False)
        self.endBtn.setEnabled(True)
        
    def endTimer(self):
        #Stops the timer from running. Ends data collection.
        self.timer.stop()
        self.startBtn.setEnabled(True)
        self.endBtn.setEnabled(False)
        
    def beginTransmission(self):
        #Sets self.transmitting to true. Consequently data will be sent over 
        #http when the runModel event is called.
        if self.transmitting == False:
            self.transmitting = True
            print("Begin Transmission")
        else:
            self.transmitting = False
            print("End Transmission")
            
    def openSer(self):
        #Opens two USB serial connections with the Arduinos collecting the
        #BNO055 sensor data
        try:
            #ATTENTION: HARD CODED COM PORTS!!!! MUST CHANGE THESE!!!
            self.ser = serial.Serial('COM5',115200, timeout=1)
            self.ser_2 = serial.Serial('COM3',115200, timeout=1)
        except:
            print("failed to open serial")

    def CloseSer(self):
        #Closes the serial connections so that the app can be safely exited.
        self.ser.close()
        self.ser_2.close()
        print("Closing serial, safe to exit app")     
