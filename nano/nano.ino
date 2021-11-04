#include <Wire.h>

//---Globals---

//consts
const int DRV_count = 6;
const int adress = 0x8;
const int stepdelay = 0.01;
const int arglenght = 8;

//All pins used
const int pins[] = {2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 20, 21, LED_BUILTIN};

//All DRVs in with their respective pins
const int DRVs[DRV_count][2] = {{2, 3}, {4, 5}, {6, 7}, {8, 9}, {10, 11}, {14, 15}};

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
  if(cmd == "step"){
    step(args[0].toInt(), args[1].toInt(), args[2].toInt(), args[3].toInt());
  }
  else if(cmd == "step2") {
    step2(args[0].toInt(), args[1].toInt(), args[2].toInt(), args[3].toInt(), args[4].toInt());
  }
  else if(cmd == "ah") {
    autohome(args[0].toInt(), args[1].toInt(), args[2].toInt(), args[3].toInt());
  }
  else if(cmd == "limit") {
    limit++;
  }
  cmd = "";
  for(int i = 0; i < arglenght; i++) {
    args[i] = "";
  }
}

void autohome(int drv1, int drv2, int dir, int divider) {
  while(limit == false) {
    if(drv2 == 0) {
      step(drv1, 10, dir, divider);
    }
    else {
      step2(drv1, drv2, 10, dir, divider);
    }
  }
}

//makes as many steps as given in the direction given and with the controller given
void step(int drv, int steps, int dir, int divider) {
  int step_pin = DRVs[drv][1];
  int dir_pin = DRVs[drv][2];
  digitalWrite(dir_pin, dir);
  for(int i = 0; i < steps; i++) {
    digitalWrite(step_pin, HIGH);
    delay(stepdelay / divider);
    digitalWrite(step_pin, LOW);
    delay(stepdelay / divider);
  }
}

//makes as many steps as given in the direction given and with the controller given for 2 motors at the same time
void step2(int drv1, int drv2, int steps, int dir, int divider) {
  int step_pin1 = DRVs[drv1][1];
  int dir_pin1 = DRVs[drv1][2];
  int step_pin2 = DRVs[drv2][1];
  int dir_pin2 = DRVs[drv2][2];
  digitalWrite(dir_pin1, dir);
  digitalWrite(dir_pin2, dir);
  for(int i = 0; i < steps; i++) {
    digitalWrite(step_pin1, HIGH);
    digitalWrite(step_pin2, HIGH);
    delay(stepdelay / divider);
    digitalWrite(step_pin1, LOW);
    digitalWrite(step_pin2, LOW);
    delay(stepdelay / divider);
  }
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