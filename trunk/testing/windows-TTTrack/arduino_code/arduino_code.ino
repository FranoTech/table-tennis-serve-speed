/*
 * Max count in result.val: 4294967295 
 * This will use Timer 1. No PWM on pin 9, 10.  
 * Registers:
 * TCNT1 -stores timer count (set to zero to reset)
 * TIMSK1 = 0x01 is Interrupt Mask Register for Timer 1, we need to enable overflow interrupt, so we set LSB to 1
 * TCCR1A - reset all bits to enable normal timer mode.
 * TCCR1B register’s 3 first bits saves value of counter clock prescaler
 * By setting TCCR1B register to 0×04 we using /256 prescaler.
 * Overflow period = 1/16Mhz * Prescaler * 2^16 = seconds
 * TCCR1B |= (1 << CS12);    // 256 prescaler 
 * TIMSK1 |= (1 << TOIE1);   // enable timer overflow interrupt
 * cli() disables interrupts
 * sei() enaables interrupts

 2  External Interrupt Request 0  (pin D2)          (INT0_vect)
 3  External Interrupt Request 1  (pin D3)          (INT1_vect)

 void TimerOne::stop()
{
  TCCR1B &= ~(_BV(CS10) | _BV(CS11) | _BV(CS12));          // clears all clock selects bits
}


*/

// PORTD &= ~_BV(3)   -- PORTD = PORTD AND (BITWISE NOT (00000100))
// #define LED_ON() PORTB |= _BV(LED_PIN)
// #define LED_OFF() PORTB &= ~_BV(LED_PIN)

/*

https://sites.google.com/site/qeewiki/books/avr-guide/external-interrupts-on-the-atmega328

http://www.gammon.com.au/forum/?id=11488
http://www.cs.washington.edu/education/courses/csep567/10wi/lectures/Lecture7.pdf

ISR(INT0_vect) {
  LED_OFF();
}
void setup() {
  pinMode(13, OUTPUT);
  // enable INT0 interrupt on change
  EICRA = 0×03;  // INT0 – rising edge on SCL
  EIMSK = 0×01;  // enable only int0
}

void loop() {
  LED_ON();
  delayMicroseconds(20);
}
*/

#define TIMER_US_PER_TICK 4 // 16MHz / 64 cycles per tick
#define TIMER_OVERFLOW_US TIMER_US_PER_TICK * 65536 // timer1 is 16bit

volatile int timer1_overflow = 0;

volatile unsigned char sendResult = 0;

volatile unsigned char isRunning = 0;

ISR(TIMER1_OVF_vect) {
  // keep track of timer1 overflows.  
  // these should happen every TIMER_OVERFLOW_US microseconds (approx 4 per second at 16MHz clockspeed)
  timer1_overflow += 1;
};

void startTimerISR(){
  //must check that timer is not already running
  //start timer 1 when gate attached to pin 2 triggers 
}

void stopTimerISR(){
  //must check that timer is already running
  //stop timer 1 when gate attached to pin 3 triggers
}
long microsecs() {
  // for debugging
  long us;
  us = timer1_overflow * 65536;
  us += TCNT1;
  us *= TIMER_US_PER_TICK;
  return us;
}

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
  attachInterrupt(0, startTimerISR, FALLING);
  attachInterrupt(1, stopTimerISR, FALLING);

  //setting up timer
  TCNT1 = 0; // resets timer 1 counter
  TCCR1A = 0x00;   //Normal Timer Operation                                                                 
  TCCR1B = 0x03; // clock/64 = increments every 3.2us  - overflows in 209.7mS  
  TIMSK1 = 0x01; // timer1 overflow interrupt enable TOIE1=1. atmel_doc2545 p. 135 

}

void loop()
{
  result.val = 0xFFFFF;
  sendResult();
  delay(1000)
}
