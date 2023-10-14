# Wearable_IMU_Based_Teleoperated_Robotic_Arm

This code is used to operate a custom robotic arm using wearable inertial measurement units (IMUs). 
It accomplishes this by creating a kinematic model of the human arm, translating it to a model of the robot arm, 
then sending angle data to the robot arm controller via HTTP. 

<img width="723" alt="image" src="https://github.com/Wesley-Niswander/Wearable_IMU_Based_Teleoperated_Robotic_Arm/assets/147947724/ea14a48b-a4b3-4723-bc63-ab114a691074">

Data for the human arm model comes from BNO055 IMUs fixed to the upper arm, forearm, and hand of
the user. These sensors are interfaced to two Arduinos via I2C. Two Arduinos are used because the
sensors only support two I2C addresses (they also support UART but this proved unreliable). The 
first Arduino collects data from the upper arm and forearm sensors. The second Arduino collects
data from the hand sensor and a potentiometer mounted in a device which measures hand grip.
The Arduinos send data to a laptop via USB serial. A program on the laptop performs the modeling and
calculates joint angles to send to the robot's controller (ESP32 chip) through http requests. The
robot controller then adjusts joint angles as a pwm signals sent to individual servos.

-Using the application
The application can be launched by running main.py. Once run the user will see the five buttons displayed below

![image](https://github.com/Wesley-Niswander/Wearable_IMU_Based_Teleoperated_Robotic_Arm/assets/147947724/653b2430-6029-442a-b091-d2a2b388fb05)

The user should operate this mini-application using the following steps.
1) Turn on the robot and connect to its' wifi access point
2) Launch the application by running main.py
3) Click Open Serial to start serial communications with the two Arduinos responsible for data collection.
4) Click Start to begin running the kinematic model and calculating joint angles.
5) Perform a calibration on the BNO055 sensors. See https://learn.adafruit.com/adafruit-bno055-absolute-orientation-sensor/device-calibration
6) Orient themselves and the robot facing north. (no torso sensor is used so the model assumes the user is facing in a fixed direction)
7) Click Transmit to begin sending data to the robot's ESP32 controller
8) Use the robot
9) Click Stop to end transmission
10) Click Close Serial
11) Close the application and turn off the robot

-Here is a brief description of the individual files.

Main.py
This script launches the application.

GUI.py
This script manages the main elements of the application and graphical user interface. It defines a
QT window with 5 push buttons (start, stop, transmit, open serial, and close serial). It is responsible
for managing and pulling data from the serial connection with the wearable arduinos (NOTE: I'M LAZY AND
HARD CODED COM PORTS. YOU NEED TO FIX THIS). It passes this data to the runModel funcion located in Model.py
and transmits the returned angles to the robot via HTTP requests.

Model.py
This contains the function runModel which is responsible for calculating the joint angles of the robot based
on data from the wearable IMUs.

Quaternion.py
This contains the class Quaternion which has methods for performing quaternion calculations. This is used by
the runModel function to perform certain calculations.

ESP32_Wifi_Robot_Servo.ino
This code lives on the ESP32 robot controller. It pulls angular data over HTTP to update the position of the
robot's motors. Motors are controlled via pwm.

BNO055_Kinematic_Capture.ino
This code lives on the Arduino responsible for the upper arm and forearm IMUs. It collects data from these
sensors via I2C and transmits it over USB serial to the Python application.

BNO055_Kinematic_Capture_Sensor3.ino
This code lives on the Arduino responsible for the collection of the hand IMU data and the poteniometer data.



