# Wearable_IMU_Based_Teleoperated_Robotic_Arm

This code is used to operate a custom robotic arm using wearable inertial measurement units (IMUs). 
It accomplishes this by creating a kinematic model of the human arm, translating it to a model of the robot arm, 
then sending angle data to the robot arm controller via HTTP. 

Data for the human model comes from BNO055 IMUs fixed to the upper arm, forearm, and hand of
the user. These sensors are interfaced to two Arduino's via I2C. Two Arduino's are used

<img width="723" alt="image" src="https://github.com/Wesley-Niswander/Wearable_IMU_Based_Teleoperated_Robotic_Arm/assets/147947724/ea14a48b-a4b3-4723-bc63-ab114a691074">
