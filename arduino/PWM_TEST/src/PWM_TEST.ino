#include <Arduino.h>

void pwm_out(){
  // digitalWrite(13, HIGH);
  // delayMicroseconds(60);
  // digitalWrite(13, LOW);
  // delayMicroseconds(60);
  analogWrite(13, 255);
//   int y=1;
//   while(y==1){
//
//
//   for (int x=0; x<255;x++){
//     analogWrite(13, x);
//     delay(100);
//   }
//   for (int x=255; x>0;x--){
//     analogWrite(13, x);
//     delay(100);
//   }
// }
}

void setup(){
  pinMode(13, OUTPUT); // PWM
  pinMode(44, OUTPUT); // Enable
  pinMode(42, OUTPUT); // FWD, BCK
  pinMode(46, OUTPUT); // BR

  // int myEraser = 7;
  // TCCR0B &= ~myEraser;
  // int myPrescaler = 2;
  // TCCR0B |= myPrescaler;
}

void loop(){
  digitalWrite(44, LOW);
  digitalWrite(42, HIGH);
  digitalWrite(46, LOW);
  delay(5000);
  pwm_out();

}
