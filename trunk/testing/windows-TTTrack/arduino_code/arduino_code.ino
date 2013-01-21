/*
 * Max count in result.val: 4294967295 
 * 
*/

//This will be used to store result and send to host machine
union bindata {
  unsigned long val;
  byte b[4];
} result;

void sendResult()
{
    Serial.write('H');
    Serial.write(result.b,4);
    Serial.write('E');
}
  
void setup()
{
  Serial.begin(9600);
}

void loop()
{
  result.val = 0xFFFFF;
  sendResult();
  delay (10000);
  result.val = 0xFFFF;
  sendResult();
  delay (10000);
  result.val = 0xFFF;
  sendResult();
  delay (10000);
  result.val = 0xFF;
  sendResult();
  delay (10000);
  result.val = 0xFF;
  sendResult();
  delay (10000);
  result.val = 0xF;
  sendResult();
  delay (10000);
  result.val = 0x1;
  sendResult();
  delay (10000);
}
