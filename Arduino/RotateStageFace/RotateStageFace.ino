//--------------------
// Stepper Setup
//--------------------
#include <Stepper.h>

// Define L298N Pins for Stepper Motor and
#define IN_1 8
#define IN_2 9
#define IN_3 12
#define IN_4 11
#define EN_A 3
#define EN_B 5

// Create an instance of the stepper class, specifying
// steps per revolution = 200
const int STEPS = 200;
Stepper stepper(STEPS, IN_1, IN_2, IN_3, IN_4);

//--------------------
// Servo Setup
//--------------------
#include <Servo.h>

// Define Servo Pins
#define servoPin 10
int pos = 0;          // variable to store the servo position
Servo myservo;        // create servo object to control a servo

//--------------------
// Set up BLDC Motor switch and PWM signal pin
//--------------------
#define sensorPin A0  // Ambient light sensor analog input
#define pwmPin 6      // YEECO BLDC Controller PWM output signal
int sensorValue = 0;  // variable to store the value coming from the sensor
int sensorCalibrate = 0;
int pwmValue = 0;

//--------------------
// Define RaspberryPi GPIO Pins
//--------------------
#define PIN_LEFT 2
#define PIN_RIGHT 4

//--------------------
// Define Functions
//--------------------
int motor_speed(int pinLeft, int pinRight) {
  if (pinLeft==1 && pinRight==0) {
    int motorSpeed = -400;
    return motorSpeed;
  }
  else if (pinLeft==1 && pinRight==1) {
    int motorSpeed = 0;
    return motorSpeed;
  }
  else if (pinLeft==0 && pinRight==1) {
    int motorSpeed = 400;
    return motorSpeed;
  }
  else {
    int motorSpeed = 0;
    return motorSpeed;
  }
}

//--------------------
// Run Arduino
//--------------------
void setup() {
  Serial.begin(9600);
  pinMode(PIN_LEFT, INPUT);
  pinMode(PIN_RIGHT, INPUT);
  pinMode(EN_A, OUTPUT);
  digitalWrite(EN_A, HIGH);
  pinMode(EN_B, OUTPUT);
  digitalWrite(EN_B, HIGH);
  delay(1000);
  sensorCalibrate = analogRead(sensorPin);  // Calibrate ALS to ambient light
  stepper.setSpeed(0);                      // Set the initial speed of the motor to 0
  myservo.attach(servoPin);                 // Attach servo
  myservo.write(100);                       // Turn servo to starting position
}

void loop() {
  // read the sensor value:
  int pinLeft = digitalRead(PIN_LEFT);
  int pinRight = digitalRead(PIN_RIGHT);

  // read the value from the sensor:
  sensorValue = analogRead(sensorPin);
  Serial.print("ALS Reading: ");
  Serial.println(sensorValue);
    
  // set the motor speed:
  int motorSpeed = motor_speed(pinLeft, pinRight);
  //Serial.println(motorSpeed);
  
  // set the motor speed:
  if (motorSpeed > 0) {
    stepper.setSpeed(motorSpeed);
    // Rotate a full revolution:
    stepper.step(STEPS);
  }
  else if (motorSpeed < 0) {
    motorSpeed *= -1;
    stepper.setSpeed(motorSpeed);
    // step 1/100 of a revolution:
    stepper.step(-1 * STEPS);
  }
  else if (motorSpeed == 0 && (pinLeft==1 && pinRight==1)) {
    stepper.setSpeed(0);
    stepper.step(0);
    while (sensorValue > sensorCalibrate + 20) {
      Serial.println("FIRE!!!");
      pwmValue = 255
      ;
      analogWrite(pwmPin, pwmValue);
      delay(1000);
      for (pos = 100; pos >= 10; pos -= 1) { // servo goes from 100 to 10 degrees to allow loading
        myservo.write(pos);                  // tell servo to go to position in variable 'pos'
        delay(15);                           // waits 15ms for the servo to reach the position
      }
      for (pos = 10; pos <= 100; pos += 1) { // goes from 10 degrees to 100 degrees to arm
        myservo.write(pos);                  // tell servo to go to position in variable 'pos'
        delay(15);                           // waits 15ms for the servo to reach the position
      }
      delay(1000);
      sensorValue = analogRead(sensorPin);   // Read ALS in order to break while loop
    }
    analogWrite(pwmPin, 0);                  // Reset PWM signal
    myservo.write(100);                      // Reset servo position
  }
  else {
    stepper.setSpeed(0);
    stepper.step(0);
  }
}
