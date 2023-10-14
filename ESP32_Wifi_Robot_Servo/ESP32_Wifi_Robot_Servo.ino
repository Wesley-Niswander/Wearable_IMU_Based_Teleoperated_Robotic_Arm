// Import required libraries
#include "WiFi.h"
#include "ESPAsyncWebServer.h"
#include "AsyncJson.h"
#include "ArduinoJson.h"

//ESP32 servo stuff
#if defined(ARDUINO_ESP32S2_DEV)
const int lowestPin = 1;
const int highestPin = 42;
#else
const int lowestPin = 2;
const int highestPin = 33;
#endif
#include <ESP32Servo.h>
Servo myServo1;
Servo myServo2;
Servo myServo3;
Servo myServo4;
Servo myServo5;
Servo myServo6;
Servo myServo7;


// Set your access point network credentials
const char* ssid = "Robot-AP";
const char* password = "fgY34@bt674";

// Create AsyncWebServer object on port 80
AsyncWebServer server(80);


float pos = 0;
int I2Caddress = 42;
int MotorNum[7] = {1, 2, 3, 4, 5, 6, 7};

void setup() {
  //Allocation of all timers to servo 
  ESP32PWM::allocateTimer(0);
  ESP32PWM::allocateTimer(1);
  ESP32PWM::allocateTimer(2);
  ESP32PWM::allocateTimer(3);

  //Set up servos
  myServo1.attach(4, 500, 2500);
  myServo2.attach(2, 500, 2500);
  myServo3.attach(15, 500, 2500);
  myServo4.attach(13, 500, 2500);
  myServo5.attach(12, 500, 2500);
  myServo6.attach(14, 500, 2500);
  myServo7.attach(27, 500, 2500);

//  myServo1.attach(2, 500, 2500);
//  myServo2.attach(4, 500, 2500);
//  myServo3.attach(12, 500, 2500);
//  myServo4.attach(13, 500, 2500);
//  myServo5.attach(15, 500, 2500);
//  myServo6.attach(19, 500, 2500);
//  myServo7.attach(21, 500, 2500);
  
  myServo1.write(0);
  myServo2.write(90);
  myServo3.write(135);
  myServo4.write(60); //90 = 60. Servos 4 and 5 are different...
  myServo5.write(60);
  myServo6.write(50);
  myServo7.write(100);
  
  // Serial port for debugging purposes
  Serial.begin(9600);
  Serial.println();

  // Setting the ESP as an access point
  Serial.print("Setting AP (Access Point)…");
  // Remove the password parameter, if you want the AP (Access Point) to be open
  WiFi.softAP(ssid, password);

  IPAddress IP = WiFi.softAPIP();
  Serial.print("AP IP address: ");
  Serial.println(IP);

  server.on("/moveitmoveit", HTTP_GET, [](AsyncWebServerRequest * request) {
    myServo1.write(atof(request->getParam("M1")->value().c_str()));
    myServo2.write(atof(request->getParam("M2")->value().c_str()));
    myServo3.write(atof(request->getParam("M3")->value().c_str()));
    myServo4.write(atof(request->getParam("M4")->value().c_str()));
    myServo5.write(atof(request->getParam("M5")->value().c_str()));
    myServo6.write(atof(request->getParam("M6")->value().c_str()));
    myServo7.write(atof(request->getParam("M7")->value().c_str()));
    request->send(200, "text/plain", "MOVEIT");
  });

  // Start server
  server.begin();
}

void loop() {

}
