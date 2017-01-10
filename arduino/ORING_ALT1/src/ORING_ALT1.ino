#include <Arduino.h>
#include <Servo.h>

// Specify pins
int mb1_dir_pin = 52;
int mb2_dir_pin = 50;

int mb1_pwm_pin = 2;
int mb2_pwm_pin = 3;

int ab1_dir_pin = 48;
int ab2_dir_pin = 46;

int ab1_pwm_pin = 4;
int ab2_pwm_pin = 5;

int la1_dir_pin = 53;
int la2_dir_pin = 51;

int la1_pwm_pin = 6;
int la2_pwm_pin = 7;

boolean stopped_flag = false;
long brake_release_time = 1.5 * 1000;
long actuator_active_time = 1.5 * 1000;

Servo myservo, myservo2;
int pos = 90;

void setup() {

  // Open serial communications and wait for port to open:
  Serial1.begin(9600);
  while (!Serial1) {
    ; // wait for serial port to connect. Needed for native USB port only
  }
  Serial1.setTimeout(10);
  Serial1.print("Serial for Pi1 initialized\n");

  Serial2.begin(9600);
  while (!Serial2) {
    ; // wait for serial port to connect. Needed for native USB port only
  }
  Serial2.setTimeout(10);
  Serial2.print("Serial for Pi2 initialized\n");

  // Set pin directions
  pinMode(mb1_dir_pin, OUTPUT);
  pinMode(mb2_dir_pin, OUTPUT);
  pinMode(mb1_pwm_pin, OUTPUT);
  pinMode(mb2_pwm_pin, OUTPUT);

  pinMode(ab1_dir_pin, OUTPUT);
  pinMode(ab2_dir_pin, OUTPUT);
  pinMode(ab1_pwm_pin, OUTPUT);
  pinMode(ab2_pwm_pin, OUTPUT);

  pinMode(la1_dir_pin, OUTPUT);
  pinMode(la2_dir_pin, OUTPUT);
  pinMode(la1_pwm_pin, OUTPUT);
  pinMode(la2_pwm_pin, OUTPUT);

  // Clear stopped_flag
  stopped_flag = false;

  // Init Servo
  myservo.attach(9); // Servo to Pin9
  myservo2.attach(10); // Servo to Pin9
}

void engageMainBrakes() {
  digitalWrite(mb1_dir_pin, LOW);
  digitalWrite(mb2_dir_pin, LOW);

  digitalWrite(mb1_pwm_pin, HIGH);
  digitalWrite(mb2_pwm_pin, HIGH);
}

void releaseMainBrakes() {
  digitalWrite(mb1_dir_pin, HIGH);
  digitalWrite(mb2_dir_pin, HIGH);

  digitalWrite(mb1_pwm_pin, HIGH);
  digitalWrite(mb2_pwm_pin, HIGH);
}

void offMainBrakes() {
  digitalWrite(mb1_pwm_pin, LOW);
  digitalWrite(mb2_pwm_pin, LOW);

  digitalWrite(mb1_dir_pin, LOW);
  digitalWrite(mb2_dir_pin, LOW);

  delay(1000);
}

void engageAuxiliaryBrakes() {
  digitalWrite(ab1_dir_pin, LOW);
  digitalWrite(ab2_dir_pin, LOW);

  digitalWrite(ab1_pwm_pin, HIGH);
  digitalWrite(ab2_pwm_pin, HIGH);
}

void releaseAuxiliaryBrakes() {
  digitalWrite(ab1_dir_pin, HIGH);
  digitalWrite(ab2_dir_pin, HIGH);

  digitalWrite(ab1_pwm_pin, HIGH);
  digitalWrite(ab2_pwm_pin, HIGH);
}

void offAuxiliaryBrakes() {
  digitalWrite(ab1_pwm_pin, LOW);
  digitalWrite(ab2_pwm_pin, LOW);

  digitalWrite(ab1_dir_pin, LOW);
  digitalWrite(ab2_dir_pin, LOW);

  delay(1000);
}

void lowerLinearActuators() {
  digitalWrite(la1_dir_pin, LOW);
  digitalWrite(la2_dir_pin, LOW);

  digitalWrite(la1_pwm_pin, HIGH);
  digitalWrite(la2_pwm_pin, HIGH);
}

void raiseLinearActuators() {
  digitalWrite(la1_dir_pin, HIGH);
  digitalWrite(la2_dir_pin, HIGH);

  digitalWrite(la1_pwm_pin, HIGH);
  digitalWrite(la2_pwm_pin, HIGH);
}

void offLinearActuators() {
  digitalWrite(la1_pwm_pin, LOW);
  digitalWrite(la2_pwm_pin, LOW);

  digitalWrite(la1_dir_pin, LOW);
  digitalWrite(la2_dir_pin, LOW);

  delay(1000);
}

void sendAcknowledgement(String state, int piNumber) {
  if (piNumber == 1){
    Serial1.print(state);

  } else if (piNumber == 2) {
    Serial2.print(state);

  } else {
    Serial1.print(state);
    Serial2.print(state);

  }
}

void sendStatus(int piNumber){
  if (stopped_flag == true) {
    sendAcknowledgement("Pod is Stopped\n", piNumber);
  } else{
    sendAcknowledgement("Pod is Running\n", piNumber);
  }
}

void kill_switch(){
  for (pos = 90; pos <= 300; pos += 10) { // goes from 90 degrees to 270 degrees
    // in steps of 1 degree
    myservo.write(pos);              // tell servo to go to position in variable 'pos'
    myservo2.write(pos);
    delay(30);                       // waits 15ms for the servo to reach the position
  }
  for (pos = 180; pos >= 90; pos -= 10) { // goes from 180 degrees to 0 degrees
    myservo.write(pos);              // tell servo to go to position in variable 'pos'
    myservo2.write(pos);
    delay(30);                       // waits 15ms for the servo to reach the position
  }
}

boolean takeActionOnByte(String inByte, int piNumber){
  if (inByte == "EM") {
    // Engage Main Brakes
    engageMainBrakes();
    sendAcknowledgement(inByte + "\n", piNumber);

  } else if (inByte == "EA") {
    // Engage Auxiliary Brakes
    engageAuxiliaryBrakes();
    sendAcknowledgement(inByte + "\n", piNumber);

  } else if (inByte == "KILLPOD"){
    for (int i = 0; i < 3; i+=1){
        kill_switch();
    }
    sendAcknowledgement("KILLPOD\n", piNumber);

  }else if (inByte == "RM") {
    // Release Main Brakes
    if (stopped_flag == true){
      offMainBrakes();
      releaseMainBrakes();
      delay(brake_release_time);
      offMainBrakes();
      sendAcknowledgement(inByte + "\n", piNumber);
    } else{
      sendAcknowledgement(inByte + " Ignored\n", piNumber);
    }

  } else if (inByte == "RA") {
    // Release Auxiliary Brakes
    if (stopped_flag == true){
      offAuxiliaryBrakes();
      releaseAuxiliaryBrakes();
      delay(brake_release_time);
      offAuxiliaryBrakes();
      sendAcknowledgement(inByte + "\n", piNumber);
    } else{
      sendAcknowledgement(inByte + " Ignored\n", piNumber);
    }

  } else if (inByte == "LL") {
    // Lower Linear Actuators
    if (stopped_flag == true){
      offLinearActuators();
      lowerLinearActuators();
      delay(actuator_active_time);
      offLinearActuators();
      sendAcknowledgement(inByte + "\n", piNumber);
    } else{
      sendAcknowledgement(inByte + " Ignored\n", piNumber);
    }

  } else if (inByte == "RL") {
    // Raise Linear Actuators
    if (stopped_flag == true){
      offLinearActuators();
      raiseLinearActuators();
      delay(actuator_active_time);
      offLinearActuators();
      sendAcknowledgement(inByte + "\n", piNumber);
    } else{
      sendAcknowledgement(inByte + " Ignored\n", piNumber);
    }

  } else if (inByte == "OM") {
    // Turn off Main Brakes
    if (stopped_flag == true){
      offMainBrakes();
      sendAcknowledgement(inByte + "\n", piNumber);
    } else{
      sendAcknowledgement(inByte + " Ignored\n", piNumber);
    }

  } else if (inByte == "OA") {
    // Turn off Auxiliary Brakes
    if (stopped_flag == true){
      offAuxiliaryBrakes();
      sendAcknowledgement(inByte + "\n", piNumber);
    } else{
      sendAcknowledgement(inByte + " Ignored\n", piNumber);
    }

  } else if (inByte == "OL") {
    // Turn off Linear Actuators
    if (stopped_flag == true){
      offLinearActuators();
      sendAcknowledgement(inByte + "\n", piNumber);
    } else{
      sendAcknowledgement(inByte + " Ignored\n", piNumber);
    }

  } else if (inByte == "RUOK") {
    sendAcknowledgement("IMOK\n", piNumber);

  } else if (inByte == "KILLALL"){
    // Turn off All motors
    offMainBrakes();
    offAuxiliaryBrakes();
    offLinearActuators();
    sendAcknowledgement(inByte + "\n", piNumber);

  } else if (inByte == "STOPPED"){
    stopped_flag = true;
    sendAcknowledgement(inByte + "\n", piNumber);

  } else if (inByte == "RUNNING"){
    stopped_flag = false;
    sendAcknowledgement(inByte + "\n", piNumber);

  } else if (inByte == "STATUS"){
    sendStatus(piNumber);

  } else {
    // Handle invalid or empty commands
    if (inByte.length() != 0){
        sendAcknowledgement(inByte + " Invalid Command\n", piNumber);
    }

    return false;

  }

  return true;
}

void loop() {
  String pi1InByte, pi2InByte;

  // Read serial input if available. Each command should end with the
  // asterisk (*) to be able to distinguish them.
  if (Serial1.available() > 0)
  {
    pi1InByte = Serial1.readStringUntil('*');
  }

  if (Serial2.available() > 0) {
    pi2InByte = Serial2.readStringUntil('*');
  }
  if (pi1InByte.length() != 0){
    takeActionOnByte(pi1InByte, 1);
  }
  if (pi2InByte.length() != 0){
    takeActionOnByte(pi2InByte, 2);
  }
}
