#define DISTANCE 100
#define dirPin 26
#define pulPin 27
#define enaPin 25

//digitalread == low means wet

long StepCounter = 0;
bool isOpen = true;
bool permission = false;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(dirPin,OUTPUT);
  pinMode(pulPin,OUTPUT);
  digitalWrite(dirPin,LOW);
  digitalWrite(pulPin,LOW);
}

int driveTheMotor(long i){
  if(i >= DISTANCE){
      for(i = DISTANCE; i > 0; i--){
      digitalWrite(pulPin,HIGH);
      delayMicroseconds(200);
      digitalWrite(pulPin,LOW);
      delayMicroseconds(200);
    }
  }
  else{
    for(i = 0; i <= DISTANCE; i++){
      digitalWrite(pulPin,HIGH);
      delayMicroseconds(200);
      digitalWrite(pulPin,LOW);
      delayMicroseconds(200);
    }
  }
  return(i);
}

void changeDirection(){
  if(digitalRead(dirPin) == LOW){
    digitalWrite(dirPin,HIGH);
  }
  else{
    digitalWrite(dirPin,LOW);
  }
}

void checkPermission(){
  if(StepCounter >= DISTANCE && digitalRead(dirPin) == HIGH){
    permission = true;
  }
  else if(StepCounter < DISTANCE && digitalRead(dirPin) == LOW){
    permission = true;
  }
  else{
    permission = false;
  }
}

void loop() {
  //arahan untuk membuka
  while(permission == false){
    changeDirection();
    checkPermission();
  }
  StepCounter = driveTheMotor(StepCounter);
  Serial.print("Step:       ");
  Serial.println(StepCounter);
  Serial.print("Permission: ");
  Serial.println(permission);
  Serial.print("Direction:  ");
  Serial.println(digitalRead(dirPin));
  delay(1000);
}
