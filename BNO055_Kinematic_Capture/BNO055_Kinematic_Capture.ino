#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>
#include <utility/imumaths.h>

#include <SoftwareSerial.h>

/* This driver uses the Adafruit unified sensor library (Adafruit_Sensor),
   which provides a common 'type' for sensor data and some helper functions.

   To use this driver you will also need to download the Adafruit_Sensor
   library and include it in your libraries folder.

   You should also assign a unique ID to this sensor for use with
   the Adafruit Sensor API so that you can identify this particular
   sensor in any data logs, etc.  To assign a unique ID, simply
   provide an appropriate value in the constructor below (12345
   is used by default in this example).

   Connections
   ===========
   Connect SCL to analog 5
   Connect SDA to analog 4
   Connect VDD to 3.3-5V DC
   Connect GROUND to common ground

   History
   =======
   2015/MAR/03  - First release (KTOWN)
*/

/* Set the delay between fresh samples */
//#define BNO055_SAMPLERATE_DELAY_MS (100)

// Check I2C device address and correct line below (by default address is 0x29 or 0x28)
//                                   id, address
Adafruit_BNO055 bno0 = Adafruit_BNO055(55, 0x28);
Adafruit_BNO055 bno1 = Adafruit_BNO055(55, 0x29);


/**************************************************************************/
/*
    Arduino setup function (automatically called at startup)
*/
/**************************************************************************/
void setup(void)
{
  Serial.begin(115200);

  //Initialization with Adafruit library for sensors 1 and 2
  bno0.begin();
  bno1.begin();
  /* Use external crystal for better accuracy */
  bno0.setExtCrystalUse(true);
  bno1.setExtCrystalUse(true);
}


void loop(void)
{

  if (Serial.read() == 'q') {
    //Get Quaternion values using easy Adafruit library
    uint8_t system, gyro, accel, mag = 0;


    imu::Quaternion quat0 = bno0.getQuat();
    imu::Quaternion quat1 = bno1.getQuat();

    //Print quaternions.
    bno0.getCalibration(&system, &gyro, &accel, &mag);
    print5(quat0.w());
    Serial.print(",");
    print5(quat0.x());
    Serial.print(",");
    print5(quat0.y());
    Serial.print(",");
    print5(quat0.z());
    Serial.print(",");
    Serial.print(gyro);
    Serial.print(",");
    Serial.print(accel);
    Serial.print(",");
    Serial.println(mag);


    bno1.getCalibration(&system, &gyro, &accel, &mag);
    print5(quat1.w());
    Serial.print(",");
    print5(quat1.x());
    Serial.print(",");
    print5(quat1.y());
    Serial.print(",");
    print5(quat1.z());
    Serial.print(",");
    Serial.print(gyro);
    Serial.print(",");
    Serial.print(accel);
    Serial.print(",");
    Serial.println(mag);
  }
}

void print5(float in) {
  if (in < 0) { //negative sign doesn't count as a character in second argument of serial print
    Serial.print(in, 4);
  } else {
    Serial.print(in, 5);
  }
}
