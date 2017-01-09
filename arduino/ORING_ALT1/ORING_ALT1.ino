

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

boolean mb_ored_pwm;
boolean mb_ored_dir;

boolean ab_ored_pwn;
boolean ab_ored_dir;

boolean la_ored_pwm;
boolean la_ored_dir;
  
void setup() {

// Open serial communications and wait for port to open:
  Serial.begin(9600);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }
  Serial.setTimeout(100);

  Serial1.begin(9600);
  while (!Serial1) {
    ; // wait for serial port to connect. Needed for native USB port only
  }
  Serial1.setTimeout(100);

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
  
}

void engageMainBrakes() {
  digitalWrite(mb1_pwm_pin, HIGH);
  digitalWrite(mb2_pwm_pin, HIGH);
  
  digitalWrite(mb1_dir_pin, LOW);
  digitalWrite(mb2_dir_pin, LOW);
}

void releaseMainBrakes() {
  digitalWrite(mb1_pwm_pin, HIGH);
  digitalWrite(mb2_pwm_pin, HIGH);
  
  digitalWrite(mb1_dir_pin, HIGH);
  digitalWrite(mb2_dir_pin, HIGH);
}

void offMainBrakes() {
  digitalWrite(mb1_pwm_pin, LOW);
  digitalWrite(mb2_pwm_pin, LOW);
  
  digitalWrite(mb1_dir_pin, LOW);
  digitalWrite(mb2_dir_pin, LOW);
}

void engageAuxiliaryBrakes() {
  digitalWrite(ab1_pwm_pin, HIGH);
  digitalWrite(ab2_pwm_pin, HIGH);
  
  digitalWrite(ab1_dir_pin, LOW);
  digitalWrite(ab2_dir_pin, LOW);
}

void releaseAuxiliaryBrakes() {
  digitalWrite(ab1_pwm_pin, HIGH);
  digitalWrite(ab2_pwm_pin, HIGH);
  
  digitalWrite(ab1_dir_pin, HIGH);
  digitalWrite(ab2_dir_pin, HIGH);
}

void offAuxiliaryBrakes() {
  digitalWrite(ab1_pwm_pin, LOW);
  digitalWrite(ab2_pwm_pin, LOW);
  
  digitalWrite(ab1_dir_pin, LOW);
  digitalWrite(ab2_dir_pin, LOW);
}

void lowerLinearActuators() {
  digitalWrite(la1_pwm_pin, HIGH);
  digitalWrite(la2_pwm_pin, HIGH); 
  
  digitalWrite(la1_dir_pin, LOW);
  digitalWrite(la2_dir_pin, LOW);
}

void raiseLinearActuators() {
  digitalWrite(la1_pwm_pin, HIGH);
  digitalWrite(la2_pwm_pin, HIGH); 
  
  digitalWrite(la1_dir_pin, HIGH);
  digitalWrite(la2_dir_pin, HIGH);
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
    sendAcknowledgement("EM");
    
  }else if (inByte == "EA") {
    engageAuxiliaryBrakes();
    sendAcknowledgement("EA");
    
  } else if (inByte == "RM") {
    releaseMainBrakes();
    sendAcknowledgement("RM");
    
  } else if (inByte == "RA") {
    releaseAuxiliaryBrakes();
    sendAcknowledgement("RA");
    
  } else if (inByte == "LL") {
    lowerLinearActuators();
    sendAcknowledgement("LL");
    
  } else if (inByte == "RL") {
    raiseLinearActuators();
    sendAcknowledgement("RL");
    
  } else if (inByte == "OM") {
    offMainBrakes();
    sendAcknowledgement("OM");
    
  } else if (inByte == "OA") {
    offAuxiliaryBrakes();
    sendAcknowledgement("OA");
    
  } else if (inByte == "OL") {
    offLinearActuators();
    sendAcknowledgement("OL");
    
  } else if (inByte == "IG") {
    sendAcknowledgement("IG");
  } else {
    return false;
  }

  return true;
}

void loop() {  
  String pi1InByte, pi2InByte;
  if (Serial.available() > 0) 
  {
    pi1InByte = Serial.readString();
  }
  

  if (Serial1.available() > 0) {
    pi2InByte = Serial1.readString();
  }

  if (pi2InByte == "EM") {
    engageMainBrakes();
  } else if(pi2InByte == "EA") {
    engageAuxiliaryBrakes();
  }

  boolean pi1Healthy = takeActionOnByte(pi1InByte);
  boolean pi2Healthy = false;
  if (pi1Healthy) {
    ;
  } else {
    pi2Healthy = takeActionOnByte(pi2InByte);
    if (!pi2Healthy) {
      // send fault state response
      sendAcknowledgement("FT");
    }
  }  
}
