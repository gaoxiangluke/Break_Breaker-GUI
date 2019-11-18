char dataString[50] = {0};
int a = 0;
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
    if (data==1)
      digitalWrite(13, HIGH);  
    else if (data==2)
       digitalWrite(13, LOW); 
      
     
  }//read data
  delay(1000);                  // give the loop some break
  
}
