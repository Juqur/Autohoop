int dirX = 5; //13
int motorX = 4;
int stepsX = 0;

int dirY1 = 3; //11
int motorY1 = 2;

int dirY2 = 7; //12
int motorY2 = 6;

int stepsY = 0;

bool pin11State = HIGH;
bool pin12State = HIGH;
bool pin13State = HIGH;

bool stepDelay = 1000;

void setup() {
  Serial.begin(9600);
  pinMode(dirX, OUTPUT);     
  pinMode(motorX, OUTPUT);
  pinMode(dirY1, OUTPUT);     
  pinMode(motorY1, OUTPUT);
  pinMode(dirY2, OUTPUT);     
  pinMode(motorY2, OUTPUT);
  reset();
}

void loop() {
    while (Serial.available() > 0) {
      String receivedData = Serial.readStringUntil('\n');
      double x = receivedData.substring(0, receivedData.indexOf(',')).toInt();
      double y = receivedData.substring(receivedData.indexOf(',') + 1).toInt();
      Serial.println(x);
      if (x > 0 && x < 100 && y > 0 && y < 100){
          goTo(x, y);
      }
    }
}

void goTo(double x, double y){
  x = (x/100) * 1700;
  y = (y/100) * 1900;
  digitalWrite(dirX, x < stepsX);
  digitalWrite(dirY1, y >= stepsY);
  digitalWrite(dirY2, y >= stepsY);
  int moveAmountX = abs(stepsX - x);
  int moveAmountY = abs(stepsY - y);
  Serial.println(moveAmountX);
  Serial.println(moveAmountY);
  if (moveAmountX > moveAmountY){
    for (int i = 0; i < moveAmountX; i++){
      digitalWrite(motorX, HIGH); 
      digitalWrite(motorX, LOW);
      if (i < moveAmountY) {
        digitalWrite(motorY1, HIGH); 
        digitalWrite(motorY1, LOW);
        digitalWrite(motorY2, HIGH); 
        digitalWrite(motorY2, LOW);
      }
      delayMicroseconds(750);
    }
  } else {
    for (int i = 0; i < moveAmountY; i++){
        digitalWrite(motorY1, HIGH); 
        digitalWrite(motorY1, LOW);
        digitalWrite(motorY2, HIGH); 
        digitalWrite(motorY2, LOW);
      if (i < moveAmountX) {
        digitalWrite(motorX, HIGH); 
        digitalWrite(motorX, LOW);
      }
      delayMicroseconds(750);
    }
  }
  reset();
}

void reset(){
  digitalWrite(dirX, HIGH);
  digitalWrite(dirY1, LOW);
  digitalWrite(dirY2, LOW);
  while (pin11State || pin12State || pin13State) {
    if (pin13State = digitalRead(13) == HIGH) {
      digitalWrite(motorX, HIGH); 
      digitalWrite(motorX, LOW);
    }
    if (pin11State = digitalRead(11) == HIGH) {
      digitalWrite(motorY1, HIGH); 
      digitalWrite(motorY1, LOW);
    }
    if (pin12State = digitalRead(12) == HIGH) {
      digitalWrite(motorY2, HIGH); 
      digitalWrite(motorY2, LOW);
    }
    delayMicroseconds(750);
  }
  pin11State = HIGH;
  pin12State = HIGH;
  pin13State = HIGH;
  digitalWrite(dirX, LOW);
  digitalWrite(dirY1, HIGH);
  digitalWrite(dirY2, HIGH);
  for (int i = 0; i < 950; i++){
    if (i <= 850){
        digitalWrite(motorX, HIGH); 
        digitalWrite(motorX, LOW);
    }
    digitalWrite(motorY1, HIGH); 
    digitalWrite(motorY1, LOW);
    digitalWrite(motorY2, HIGH); 
    digitalWrite(motorY2, LOW);
    delayMicroseconds(750);
  }
  stepsX = 850;
  stepsY = 950;
}