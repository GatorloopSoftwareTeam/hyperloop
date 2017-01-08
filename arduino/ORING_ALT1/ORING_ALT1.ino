

// constants won't change. They're used here to
// set pin numbers:
//INPUTS FOR PI 1
// Input A is PWM
boolean pi1_mb_pwm[2];
boolean pi1_mb_dir[2];

boolean pi1_ab_pwm[2];
boolean pi1_ab_dir[2];

boolean pi1_la_pwm[2];
boolean pi1_la_dir[2];

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


void readByte(String inByte, int pi){
  if ( inByte == "EM")
    {
      pi1_mb_pwm[0] = 1;
      // DIR  States of Pi 1
      pi1_mb_dir[0] = 0;
      
      pi1_mb_pwm[1] = 1;
      // DIR  States of Pi 1
      pi1_mb_dir[1] = 0;
    }
    else if ( inByte == "RM")
    {
      pi1_mb_pwm[0] = 1;        
      // DIR  States of Pi 1
      pi1_mb_dir[0] = 1;
      
      pi1_mb_pwm[1] = 1;        
      // DIR  States of Pi 1
      pi1_mb_dir[1] = 1;
    }
    else if ( inByte == "EA")
    {
      pi1_ab_pwm[0] = 1;      
      // DIR  States of Pi 1
      pi1_ab_dir[0] = 0;
      
      pi1_ab_pwm[1] = 1;      
      // DIR  States of Pi 1
      pi1_ab_dir[1] = 0;
    }
    else if ( inByte == "RA")
    {
      pi1_ab_pwm[0] = 1;      
      // DIR  States of Pi 1
      pi1_ab_dir[0] = 1;
      
      pi1_ab_pwm[1] = 1;      
      // DIR  States of Pi 1
      pi1_ab_dir[1] = 1;
    }

    else if ( inByte == "LL")
    {
      pi1_la_pwm[0] = 1;
      // DIR  States of Pi 1
      pi1_la_dir[0] = 0;

      pi1_la_pwm[1] = 1;
      // DIR  States of Pi 1
      pi1_la_dir[1] = 0;
    }
    else if ( inByte == "RL")
    {
      pi1_la_pwm[0] = 1;
      // DIR  States of Pi 1
      pi1_la_dir[0] = 1;

      pi1_la_pwm[1] = 1;
      // DIR  States of Pi 1
      pi1_la_dir[1] = 1;
    }
    else if ( inByte == "OM")
    {
      pi1_mb_pwm[0] = 0;
      pi1_mb_dir[0] = 0;
      
      pi1_mb_pwm[1] = 0;
      pi1_mb_dir[1] = 0;
    }
    else if ( inByte == "OA")
    {
      pi1_ab_pwm[0] = 0;
      pi1_ab_dir[0] = 0;

      pi1_ab_pwm[1] = 0;
      pi1_ab_dir[1] = 0;
    }
    else if ( inByte == "OL")
    {
      pi1_la_pwm[0] = 0;
      pi1_la_dir[0] = 0;

      pi1_la_pwm[1] = 0;
      pi1_la_dir[1] = 0;
    }


    else if ( inByte == "IG")
    {
      ;
    }
    return;
}

void writePins(){
  //PWM OR OUT STATES
  mb_ored_pwm = pi1_mb_pwm[0] || pi1_mb_pwm[1];
  mb_ored_dir = pi1_mb_dir[0] || pi1_mb_dir[1];

  ab_ored_pwn = pi1_ab_pwm[0] || pi1_ab_pwm[1];
  ab_ored_dir = pi1_ab_dir[0] || pi1_ab_dir[1];

  la_ored_pwm = pi1_la_pwm[0] || pi1_la_pwm[1];
  la_ored_dir = pi1_la_dir[0] || pi1_la_dir[1];


  digitalWrite(mb1_dir_pin, mb_ored_dir);
  digitalWrite(mb2_dir_pin, mb_ored_dir);

  digitalWrite(mb1_pwm_pin, mb_ored_pwm);
  digitalWrite(mb2_pwm_pin, mb_ored_pwm);

  digitalWrite(ab1_dir_pin, ab_ored_dir);
  digitalWrite(ab2_dir_pin, ab_ored_dir);

  digitalWrite(ab1_pwm_pin, ab_ored_pwn);
  digitalWrite(ab2_pwm_pin, ab_ored_pwn);

  digitalWrite(la1_dir_pin, la_ored_dir);
  digitalWrite(la2_dir_pin, la_ored_dir);

  digitalWrite(la1_pwm_pin, la_ored_pwm);
  digitalWrite(la2_pwm_pin, la_ored_pwm); 

}

void loop() {
  while (Serial.available() > 0) 
  {
    String inByte = Serial.readString();
    readByte(inByte, 0);
  }
  writePins();

  while (Serial1.available() > 0) {
    String inByte1 = Serial1.readString();
    readByte(inByte1, 1);
  }
  writePins();
}
