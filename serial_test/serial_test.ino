char dataString[50] = {0};
int a = 0;
int speed = 1;
void PrepareMotor(){
}
void PrepareTemp(){
}
void PrepareLoad(){
}
void PrepareHall(){
}
void setMotorSpeed(){
}
void disablemotor(){}
float ReadHall(){}
float ReadTemp(){}
float Read
void setup() {
  pinMode(13, OUTPUT);
Serial.begin(9600);   //Starting serial communication
 digitalWrite(13, LOW);   
}
void loop() {
  a++;
  Serial.println(a);   // send the data
  if (Serial.available()){
    int data =Serial.read() ;
    if (speedmod = 0){
    if (data==1) 
    else if (data==2)
       digitalWrite(13, LOW); 
    else if (data == 3){
      digitalWrite(13, HIGH); 
       speed = 3;
    }
    else if (data == 4)
    {
      speed = 2;
    }
    else if (data == 5){
      speed = 1;
    }
        
  }//read data
  delay(250);                  // give the loop some break
  
}
