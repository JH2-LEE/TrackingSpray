#include <Servo.h>
//assign servo
Servo servo_disk;
Servo servo_right;
Servo servo_left;

//servo port number
const int SERVO_DISK = 9;
const int SERVO_RIGHT = 10;
const int SERVO_LEFT = 11;

int value = 0;

void setup() {
    // start serial communication
    Serial.begin(9600);

    // set servo
    servo_disk.attach(SERVO_DISK);
    servo_right.attach(SERVO_RIGHT);
    servo_left.attach(SERVO_LEFT);

    // initializing
    servo_disk.write(90);
    servo_right.write(0);
    servo_left.write(179);

}

void loop() {
    // operate in every 5s
    delay(2000);
    if(Serial.available()>0){
      value = Serial.read();
      servo_disk.write(value);
      delay(500);
      // pull
      servo_right.write(179);
      servo_left.write(0);
      delay(500);
    }
    // push
    servo_right.write(0);
    servo_left.write(179);
    delay(3000);
    Serial.end();
    Serial.begin(9600);

}
