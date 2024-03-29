//hall effect senor part
// digital pin 2 is the hall pin
int hall_pin = 2;
volatile byte half_revolutions;
double rpm;
double timeold;
double timenew;
void magnet_detect();
int buttonPin = 0;
//temp part
// which analog pin to connect
#define THERMISTORPIN A0         
// resistance at 25 degrees C
#define THERMISTORNOMINAL 100000      
// temp. for nominal resistance (almost always 25 C)
#define TEMPERATURENOMINAL 25   
// how many samples to take and average, more takes longer
// but is more 'smooth'
#define NUMSAMPLES 5
// The beta coefficient of the thermistor (usually 3000-4000)
#define BCOEFFICIENT 3950
// the value of the 'other' resistor
#define SERIESRESISTOR 10000   
int samples[NUMSAMPLES];
float tempsensor;
//motor part
int RPWM=9;
int LPWM=10;
int L_EN=11;
int R_EN=12;
int dutycycle=60;
int buttonEnable = 0;
//system set up part
int speed = 1;
bool systemOn = true;

void PrepareMotor(){
   // put your setup code here, to run once:
  for(int i=9;i<13;i++){
   pinMode(i,OUTPUT);
  }
   for(int i=9;i<13;i++){
   digitalWrite(i,LOW);
  }
  
}
void PrepareTemp(){
   analogReference(EXTERNAL);
}
void PrepareLoad(){
}
void PrepareHall(){
   pinMode(2, INPUT_PULLUP);
   attachInterrupt(0, magnet_detect, FALLING);//Initialize the intterrupt pin (Arduino digital pin 2)
   half_revolutions = 0;
   rpm = 0;
   timeold = 0;
}
void disablemotor(){
   for(int i=9;i<13;i++){
   digitalWrite(i,LOW);
  }
}
void turnOnMotor(){
  digitalWrite(R_EN,HIGH);
  digitalWrite(L_EN,HIGH);
  analogWrite(RPWM,dutycycle);
 }
void prepareSerial(){
   pinMode(13, OUTPUT);
  Serial.begin(9600);   //Starting serial communication
 digitalWrite(13, LOW);
    pinMode(buttonPin, INPUT_PULLUP);
 }
void ReadHall(){
  if (half_revolutions >= 4) { 
      timenew = micros();
    // Serial.print(timenew);
     rpm = 30*1000000.0/(timenew - timeold)*half_revolutions;
     timeold = timenew;
     half_revolutions = 0;
     //Serial.println(rpm,DEC);
   }
}
void ReadTemp(){
    uint8_t i;
  float average;
 
  // take N samples in a row, with a slight delay
  for (i=0; i< NUMSAMPLES; i++) {
   samples[i] = analogRead(THERMISTORPIN);
   delay(10);
  }
  
  // average all the samples out
  average = 0;
  for (i=0; i< NUMSAMPLES; i++) {
     average += samples[i];
  }
  average /= NUMSAMPLES;

  
  // convert the value to resistance
  average = 1023 / average - 1;
  average = SERIESRESISTOR / average;

  
  float steinhart;
  steinhart = average / THERMISTORNOMINAL;     // (R/Ro)
  steinhart = log(steinhart);                  // ln(R/Ro)
  steinhart /= BCOEFFICIENT;                   // 1/B * ln(R/Ro)
  steinhart += 1.0 / (TEMPERATURENOMINAL + 273.15); // + (1/To)
  steinhart = 1.0 / steinhart;                 // Invert
  steinhart -= 273.15;                         // convert to C
  tempsensor = steinhart;
 
  }
void setup() {
  prepareSerial();
  PrepareTemp();
  PrepareMotor();
  PrepareHall();                            
}
void loop() {
  int buttonValue = digitalRead(buttonPin);
   //disablemotor();
  //check button
  if (buttonValue == LOW){
      // If button pushed, turn LED on
      systemOn = false;
      disablemotor();
   } 
  //read data
 turnOnMotor();
  if (Serial.available() && buttonEnable == 0){
    int data =Serial.read() ;
    //turn on the system
    if (data==1){
      systemOn = true;
     turnOnMotor();
    }
    //turn of the system
    else if (data==2){
      systemOn = false;
      disablemotor();
    }
    //set speed low 
    else if (data == 3){
      digitalWrite(13, HIGH); 
       dutycycle = 20;
    }
    //set speed med 
    else if (data == 4)
    {
     dutycycle=40;
    }
    //set speed high
    else if (data == 5){
      dutycycle=200;
    }
  }
   //take and send data
   if (systemOn == true){
      ReadTemp();
      ReadHall();
     // Serial.println(rpm);
     // Serial.println(tempsensor);
      Serial.println(rpm,8);
      Serial.println("\n");
   }
   delay(1);                  // give the loop some break
  
}
void magnet_detect()//This function is called whenever a magnet/interrupt is detected by the arduino
 {
   if (systemOn == true){
     half_revolutions++;
  }
 }
  
  
 



