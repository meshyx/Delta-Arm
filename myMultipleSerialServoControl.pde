/*
 * ------------------------------
 *   MultipleSerialServoControl
 * ------------------------------
 *
 * Uses the Arduino Serial library
 *  (http://arduino.cc/en/Reference/Serial)
 * and the Arduino Servo library
 *  (http://arduino.cc/en/Reference/Servo)
 * to control multiple servos from a PC using a USB cable.
 *
 * Dependencies:
 *   Arduino 0017 or higher
 *     (http://www.arduino.cc/en/Main/Software)
 *   Python servo.py module
 *     (http://principialabs.com/arduino-python-4-axis-servo-control/)
 *
 * Created:  23 December 2009
 * Author:   Brian D. Wendt
 *   (http://principialabs.com/)
 * Version:  1.1
 * License:  GPLv3
 *   (http://www.fsf.org/licensing/)
 *
 */

// Import the Arduino Servo library
#include <Servo.h> 

// Create a Servo object for each servo
Servo servo1;
Servo servo2;
Servo servo3;
// TO ADD SERVOS:
//   Servo servo5;
//   etc...

// Common servo setup values
int minPulse = 500;   // minimum servo position, us (microseconds)
int maxPulse = 2800;  // maximum servo position, us

// User input for servo and position
int userInput[4];    // raw input from serial buffer, 3 bytes
int startbyte;       // start byte, begin reading input
int servo;           // which servo to pulse?
int pos1;            // servo ms as two chars
int pos2;
int pos;
int i;               // iterator

void setup() 
{ 
  // Attach each Servo object to a digital pin
  servo1.attach(43, minPulse, maxPulse);
  servo2.attach(44, minPulse, maxPulse);
  servo3.attach(45, minPulse, maxPulse);
  //servo4.attach(5, minPulse, maxPulse);
  // TO ADD SERVOS:
  //   servo5.attach(YOUR_PIN, minPulse, maxPulse);
  //   etc...

  // Open the serial connection, 9600 baud
  Serial.begin(9600);
} 

void loop() 
{ 
  // Wait for serial input (min 4 bytes in buffer)
  if (Serial.available() > 3) {
    // Read the first byte
    startbyte = Serial.read();
    // If it's really the startbyte (255) ...
    if (startbyte == 255) {
      // ... then get the next two bytes
      for (i=0;i<3;i++) {
        userInput[i] = Serial.read();
      }
      // First byte = servo to move?
      servo = userInput[0];
      // Second byte = which position?
      pos1 = userInput[1];
      pos2 = userInput[2];
      pos = pos1 * 256 + pos2;
      // Packet error checking and recovery
      if (pos == 255) { servo = 255; }

      // Assign new position to appropriate servo
      switch (servo) {
        case 1:
          servo1.writeMicroseconds(pos);    // move servo1 to 'pos'
          break;
        case 2:
          servo2.writeMicroseconds(pos);
          break;
        case 3:
          servo3.writeMicroseconds(pos);
          break;

   // TO ADD SERVOS:
   //     case 5:
   //       servo5.write(pos);
   //       break;
   // etc...

        // LED on Pin 13 for digital on/off demo
      }
    }
  }
}

