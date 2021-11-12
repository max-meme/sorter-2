#include <Wire.h>

//---Globals---

// x y z stuff
int x = 0;
int y = 0;
int z = 0;

//consts
const int DRV_count = 6;
const int adress = 0x8;
const int stepdelay = 0.01;
const int arglenght = 8;

//All pins used
const int pins[] = {2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 20, 21, LED_BUILTIN};

//All DRVs in with their respective pins in the following order: x1, x2, y, z
const int DRVs[DRV_count][2] = {{2, 3}, {4, 5}, {6, 7}, {8, 9}, {10, 11}, {14, 15}};

//what to set the dir pin so the stepper moves backwards / forwards
const int DRV_dirs[DRV_count][2] = {{1, 0}, {1, 0}, {1, 0}, {1, 0}, {1, 0}, {1, 0}};

const int ah[DRV_count][2] = {{3, -1}, {0, 1}, {2, -1}};

char temp[32];
String cmd = "";
String args[arglenght];
bool limit = false;

void setup() {
  //set all pins as out
  for(int i = 0; i < 19; i++)
  {
    pinMode(pins[i], OUTPUT);
  }
  //setup I2C between Pi and Nano
  Wire.begin(adress);
  Wire.onReceive(recieveEvent);
  Serial.begin(9600);
  Serial.println("Ready!");
}

void loop() {
  delay(100);
}

//executes I2C command
void exec() {
  if(cmd == "selftest") {
    for(int i = 0; i < 5; i++) {
      blinkLED();
    }
    testDRVs();
  }

  if(cmd == "ah"){
    autohome(agrs[0]);
  }
  else if(cmd == "moveto") {

  }
  else if(cmd == "ah") {
    autohome(args[0].toInt(), args[1].toInt(), args[2].toInt(), args[3].toInt());
  }
  else if(cmd == "limit") {
    limit = true;
  }
  cmd = "";
  for(int i = 0; i < arglenght; i++) {
    args[i] = "";
  }
}

void autohome(int ms) {
  for(int i = 0; i < 3; i++) {
    limit = false;

    int drv = ah[i][1];
    int drv2 = ah[i][2];
    
    int step_pin = DRVs[drv][1];
    int dir_pin = DRVs[drv][2];
    digitalWrite(dir_pin, ah[drv]);

    if(drv2 != -1) {
      int step_pin2 = DRVs[drv][1];
      int dir_pin2 = DRVs[drv2][2];
      digitalWrite(dir_pin2, ah[drv2]);

      while(limit == false) {
        step2(step_pin, step_pin2, ms);
      }
    }
    else {
      while(limit == false) {
        step(step_pin, ms);
      }
    }
  }
  x = 0;
  y = 0;
  z = 0;
}

//axis: 0 = x; 1 = y; 2 = z;
void home(int axis) {
  
}

void step(int pin, int ms) {
  digitalWrite(pin, HIGH);
  delay(stepdelay / ms);
  digitalWrite(pin, LOW);
  delay(stepdelay / ms);
}

void step2(int pin , int pin2, int ms) {
  digitalWrite(pin, HIGH);
  digitalWrite(pin2, HIGH);
  delay(stepdelay / ms);
  digitalWrite(pin, LOW);
  digitalWrite(pin2, LOW);
  delay(stepdelay / ms);
}

//called when I2C revieves a message
void recieveEvent(int howMany) {  
  for (int i = 0; i < howMany; i++) {
      temp[i] = Wire.read();
      temp[i + 1] = '\0'; //add null after ea. char
    }

  //RPi first byte is cmd byte so shift everything to the left 1 pos so temp contains our string
  for (int i = 0; i < howMany; ++i){
    temp[i] = temp[i + 1];
  }

  //build cmd and args
  int b = 0;
  for (int i = 0; i < howMany; ++i){
    if(temp[i] == *"-") {
      b++;
    }
    else if(b == 0) {
      cmd = cmd + temp[i];
    }
    else {
      args[b] = args[b] + temp[i];
    }
  }

  //blink and log message
  blinkLED();
  Serial.println("cmd: " + cmd + "\nargs");
  for(int i = 0; i < 8; i++) {
    Serial.println(args[i]);
  }
  exec();
}

//tests all DRV stepper drivers
void testDRVs() {
  for(int i = 0; i < DRV_count; i++) {
    Serial.println("Testing DRV " + i);
    int step_pin = DRVs[i][1];
    int dir_pin = DRVs[i][2];

    digitalWrite(dir_pin, LOW);
    for(int j = 0; j < 100; j++) {
      digitalWrite(step_pin, HIGH);
      delay(0.01);
      digitalWrite(step_pin, LOW);
      delay(0.01);
    }

    digitalWrite(dir_pin, HIGH);
    for(int j = 0; j < 100; j++) {
      digitalWrite(step_pin, HIGH);
      delay(0.01);
      digitalWrite(step_pin, LOW);
      delay(0.01);
    }
  }
}

void blinkLED() {
  digitalWrite(LED_BUILTIN, HIGH);
  delay(100);
  digitalWrite(LED_BUILTIN, LOW);
  delay(100);
}