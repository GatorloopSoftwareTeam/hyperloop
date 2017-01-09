#include <Arduino.h>

// constants won't change. They're used here to
// set pin numbers:
//INPUTS FOR PI 1
// Input A is PWM
String inByte;
String inByte1;

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

boolean stopped_flag;

void setup() {

// Open serial communications and wait for port to open:
  Serial.begin(9600);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }
  Serial.setTimeout(10);

  Serial1.begin(9600);
  while (!Serial1) {
    ; // wait for serial port to connect. Needed for native USB port only
  }
  Serial1.setTimeout(10);

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

  stopped_flag = false;
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
}

void sendAcknowledgement(String state) {
  Serial.print(state);
  Serial1.print(state);
}

boolean takeActionOnByte(String inByte){
  if (inByte == "EM") {
    engageMainBrakes();
    sendAcknowledgement(inByte);

  } else if (inByte == "EA") {
    engageAuxiliaryBrakes();
    sendAcknowledgement(inByte);

  } else if (inByte == "RM" && stopped_flag) {
    releaseMainBrakes();
    sendAcknowledgement(inByte);

  } else if (inByte == "RA" && stopped_flag) {
    releaseAuxiliaryBrakes();
    sendAcknowledgement(inByte);

  } else if (inByte == "LL" && stopped_flag) {
    lowerLinearActuators();
    sendAcknowledgement(inByte);

  } else if (inByte == "RL" && stopped_flag) {
    raiseLinearActuators();
    sendAcknowledgement(inByte);

  } else if (inByte == "OM" && stopped_flag) {
    offMainBrakes();
    sendAcknowledgement(inByte);

  } else if (inByte == "OA" && stopped_flag) {
    offAuxiliaryBrakes();
    sendAcknowledgement(inByte);

  } else if (inByte == "OL" && stopped_flag) {
    offLinearActuators();
    sendAcknowledgement(inByte);

  } else if (inByte == "IG") {
    sendAcknowledgement(inByte);

  } else if (inByte == "RUOK") {
    sendAcknowledgement("IMOK");

  } else if (inByte == "KILLALL"){
    offMainBrakes();
    offAuxiliaryBrakes();
    offLinearActuators();
    sendAcknowledgement(inByte);

  } else if (inByte == "STOPPED"){
    stopped_flag = true;
    sendAcknowledgement(inByte);

  } else if (inByte == "RUNNING"){
    stopped_flag = false;
    sendAcknowledgement(inByte);

  } else {
    return false;

  }

  return true;
}

void loop() {
  String pi1InByte, pi2InByte;

  if (Serial.available() > 0)
  {
    pi1InByte = Serial.readStringUntil('*');
  }

  if (Serial1.available() > 0) {
    pi2InByte = Serial1.readStringUntil('*');
  }

  takeActionOnByte(pi1InByte);
  takeActionOnByte(pi2InByte);

  // if (pi1InByte == "EM" || pi2InByte == "EM") {
  //   takeActionOnByte("EM");
  //
  // } else if (pi1InByte == "EA" || pi2InByte == "EA") {
  //   takeActionOnByte("EA");
  //
  // } else if (pi1InByte == "STOPPED" || pi2InByte == "STOPPED") {
  //   takeActionOnByte("STOPPED");
  //
  // } else{
  //   ;
  // }
}
