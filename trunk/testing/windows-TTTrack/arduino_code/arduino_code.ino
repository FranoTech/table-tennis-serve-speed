/*
 * Max count in result.val: 4294967295 
 * 
*/
 //http://arduino-info.wikispaces.com/Popular-ICs
 //http://pcbheaven.com/drcalculus/index.php?calc=st_sym

#define TIMER_US_PER_TICK 4 // 16MHz / 64 cycles per tick
#define TIMER_OVERFLOW_US TIMER_US_PER_TICK * 65536 // timer1 is 16bit

volatile int timer1_overflow = 0;

ISR(SIG_OVERFLOW1) {
  // keep track of timer1 overflows.  
  // these should happen every TIMER_OVERFLOW_US microseconds (approx 4 per second at 16MHz clockspeed)
  timer1_overflow += 1;
};

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
  delay(1000)
}
