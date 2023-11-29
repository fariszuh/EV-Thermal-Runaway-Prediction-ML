
#include <SD.h>
#include <SPI.h>
#include <Wire.h>
#include "RTClib.h"

RTC_DS3231 rtc;
File myFile;
int pinCS = 53;

#define pinVolt A0
#define pinVolt A1
#define pinVolt A2
#define pinNTCAccumulator1 A3
#define pinNTCAccumulator2 A4
#define pinNTCAccumulator3 A5

//Untuk Temperatur
float Vo, Vout;
float Vin = 5.0;
float R1 = 9880; //adjust based on   
float logR2, R2, T, Tc, Tf;
float c1 = 1.009249522e-03, c2 = 2.378405444e-04, c3 = 2.019202697e-07;
float valueTempAccumulator1, valueTempAccumulator2, valueTempAccumulator3;
String data,tampil;

//untuk Voltage
float adc_voltage = 0.0;
float in_voltage = 0.0;
float R1 = 30000.0;
float R2 = 7500.0; 
float ref_voltage = 5.0;
int adc_value = 0;
float Volt;

//untuk RPM dan Kecepatan
float rev=0;
int rpm;
int oldtime=0;
int time;
int kmh;

void setRealTimeClock(){
  if (! rtc.begin()) {
    Serial.println("Couldn't find RTC");
    Serial.flush();
    while (1) delay(10);
  }

  if (rtc.lostPower()) {
    Serial.println("RTC lost power, let's set the time!");
    rtc.adjust(DateTime(F(__DATE__), F(__TIME__)));
  }
}

void setDataLogger(){
  pinMode(pinCS, OUTPUT);
  SD.begin();
}

void setPin(){
  pinMode(pinNTCAccumulator1,INPUT);
  pinMode(pinNTCAccumulator2,INPUT);
  pinMode(pinNTCAccumulator3,INPUT);
  attachInterrupt(2, isr, RISING);
}

void isr()
{
  rev++;
}

float calculateTemp(int pinTemp){
  Vo = analogRead(pinTemp);
  R2 = R1 * (1023.0 / (float)Vo - 1.0);
  logR2 = log(R2);
  T = (1.0 / (c1 + c2*logR2 + c3*logR2*logR2*logR2));
  Tc = T - 273.15;
  return Tc;
}

float calculateVoltage(int pinVolt){
  adc_value = analogRead(pinVolt);
  adc_voltage  = (adc_value * ref_voltage) / 1024.0; 
  in_voltage = adc_voltage / (R2/(R1+R2));
  return in_voltage;
}

void logTheData(float valueTempAccumulator1,float valueTempAccumulator2,float valueTempAccumulator3, float Volt, int rpm, int kmh){
  myFile = SD.open("testPlis.txt", FILE_WRITE);
  if(myFile){
    DateTime now = rtc.now();

    myFile.print(now.year(), DEC);
    myFile.print('/');
    myFile.print(now.month(), DEC);
    myFile.print('/');
    myFile.print(now.day(), DEC);
    myFile.print(" ");
    myFile.print(now.hour(), DEC);
    myFile.print(':');
    myFile.print(now.minute(), DEC);
    myFile.print(':');
    myFile.print(now.second(), DEC);
    myFile.println();

    myFile.print("Temperature NTC Accumulator 1: ");
    myFile.println(valueTempAccumulator1);
    myFile.print("Temperature NTC Accumulator 2: ");
    myFile.println(valueTempAccumulator2);
    myFile.print("Temperature NTC Accumulator 3: ");
    myFile.println(valueTempAccumulator3);
    myFile.print("Battery Voltage: ");
    myFile.println(Volt);
    myFile.print("Engine RPM: ");
    myFile.println(rpm);
    myFile.print("Vehicle Speed: ");
    myFile.println(kmh);
    myFile.close();
    Serial.println("success");
  }
  else {
    Serial.println("error writing testPlis.txt");
  }
  /*myFile = SD.open("testPlis.txt");
  if (myFile) {
    Serial.println("Read:");
    // Reading the whole file
    while (myFile.available()) {
      Serial.write(myFile.read());
   }
    myFile.close();
  }
  else {
    Serial.println("error reading testPlis.txt");
  }*/
}

void sendToESP(float accuNTC1, float accuNTC2, float accuNTC3, float GLVVolt, float HVVolt, int RPM, int velocity){
  //belum ditambah ke main code
  Serial2.print(accuNTC1);
  Serial2.print("\t1");
  Serial2.print(accuNTC2);
  Serial2.print("\t2");
  Serial2.print(accuNTC3);
  Serial2.print("\t3");
  Serial2.print(Volt);
  Serial2.print("\lv");
  Serial2.print(Volt);
  Serial2.print("\hv");
  Serial2.print(RPM);
  Serial2.print("\r");
  Serial2.print(velocity);
  Serial2.print("\s");
}

void debug(float accuNTC1, float accuNTC2, float accuNTC3, float GLVVolt, int RPM, int velocity){
  DateTime now = rtc.now();

    Serial.print(now.year(), DEC);
    Serial.print('/');
    Serial.print(now.month(), DEC);
    Serial.print('/');
    Serial.print(now.day(), DEC);
    Serial.print(" ");
    Serial.print(now.hour(), DEC);
    Serial.print(':');
    Serial.print(now.minute(), DEC);
    Serial.print(':');
    Serial.print(now.second(), DEC);
    Serial.println();
    
  Serial.print("accuNTC1  ");
  Serial.println(accuNTC1);
  Serial.print("accuNTC2  ");
  Serial.println(accuNTC2);
  Serial.print("accuNTC3  ");
  Serial.println(accuNTC3);
  Serial.print("Volt   ");
  Serial.println(Volt);
  Serial.print("RPM       ");
  Serial.println(RPM);
  Serial.print("velocity  ");
  Serial.println(velocity);

  Serial.print("digitalRead(2)");
  Serial.println(digitalRead(2));
}

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  Serial1.begin(9600);
  Serial2.begin(115200);
  setDataLogger();
  setPin();
  setRealTimeClock();
}

void loop() {
  // put your main code here, to run repeatedly:
  // ini bisa diiterasi
  valueTempAccumulator1 = calculateTemp(pinNTCAccumulator1);
  valueTempAccumulator2 = calculateTemp(pinNTCAccumulator2);
  valueTempAccumulator3 = calculateTemp(pinNTCAccumulator3);
  GLVVolt = calculateGLVVoltage(pinGLVVolt);
  calculateRPMandSpeed();
  logTheData(valueTempAccumulator1,valueTempAccumulator2,valueTempAccumulator3,GLVVolt,rpm,kmh);
  displayIt(valueTempAccumulator1, valueTempAccumulator2);
  debug(valueTempAccumulator1,valueTempAccumulator2,valueTempAccumulator3,GLVVolt,rpm,kmh);
  delay(1000);
}
