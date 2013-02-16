/*
Target: Arduino Mega
Site: code.google.com/table-tennis-serve-speed
Desc: Arduino is attached to two specially designed light gates
      One on pin 2 and the other on pin 3
      A 'FALLING' edge on pin two starts Timer1
      A 'FALLING' edge on pin three stops Timer 1
      and triggers serial communication to host program
      TTTrack.py running on windows client. 
Author: Fergal O' Grady

*Global Interrupts:
  cli() disables interrupts
  sei() enables interrupts

*TIMER1:
Registers:
  TCNT1: Stores current timer count
         Set to 0 to reset
  TIMSK1: Timer1 Interrupt Mask Register
          TOIE1 = TIMSK1[0] = Timer overflow interrupt enable bit 
          TIMSK1 |= _BV(TOIE1) ; enables timer one overflow interrupt
  TCCR1A: Timer1 Control Register A
          Set to 0x00 for normal 16 bit counter operation
  TCCR1B: Timer1 Control Register B
          TCCR1B[0:2] - Control clock prescalar
          16 * 10^6 Hz Clock
          **We will set Clk/64 giving a 4 us resolution
          **Timer one will overflow every 0.26214 seconds
          CS12  CS11  CS10  :Mode
          0     0     0      No clock source (stop)
          0     0     1      Clk/1 (Clock ticks 16*10^6 times per second )
          0     1     0      Clk/8
          0     1     1      Clk/64
          1     0     0      Clk/256
          1     0     1      Clk/1024      
          1     1     0      External clock on T1 pin. Falling Edge
          1     0     1      External clock on T1 pin. Rising Edge
Examples:
  Stop Timer 1:
    TCCR1B &= ~(_BV(CS10) | _BV(CS11) | _BV(CS12)); 
  Set prescalar to 256:
    TCCR1B |= (1 << CS12);    // 256 prescaler 
Notes:
  *Overflow period = 1/16Mhz * Prescaler * 2^16 = seconds
  *Max count in result.val: 4294967295    (2^16 - 1)
  *No PWM on pin 9, 10 when Timer 1 in use

*External Interrupts:
  INT0 - ISR(INT0_vect) - Digital pin 2 
  INT1 - ISR(INT1_vect) - Digital pin 3

  EICRA - [0:1] INT0 
          [2:3] INT1
      ISC11 ISC10 Interrupt 1
      0     0     The low level of INT1 generates an interrupt request
      0     1     Any logical change on INT1 generates an interrupt request
      1     0     The falling edge of INT1 generates an interrupt request
      1     1     The rising edge of INT1 generates an interrupt request

      ISC01 ISC00  Description
      0     0      The low level of INT0 generates an interrupt request
      0     1      Any logical change on INT0 generates an interrupt request
      1     0      The falling edge of INT0 generates an interrupt request
      1     1      The rising edge of INT0 generates an interrupt request
  EIMSK - [0] INT0 enable bit
          [1] INT1 enable bit

Use of _BV function:
  PORTD &= ~_BV(3)   -- PORTD = PORTD AND (BITWISE NOT (00000100))
  #define LED_ON() PORTB |= _BV(LED_PIN)
  #define LED_OFF() PORTB &= ~_BV(LED_PIN)

Arduino Chip Data Sheet: 
  http://www.atmel.com/Images/doc8161.pdf

Sites for further information on interrupts:
  https://sites.google.com/site/qeewiki/books/avr-guide/external-interrupts-on-the-atmega328
  http://www.gammon.com.au/forum/?id=11488
  http://www.cs.washington.edu/education/courses/csep567/10wi/lectures/Lecture7.pdf

*/
#define INT0_pin  21
#define INT4_pin  2

#define TIMER_US_PER_TICK 4 // 16MHz / 64 cycles per tick
#define TIMER_OVERFLOW_US TIMER_US_PER_TICK * 65536 // timer1 is 16bit

volatile int timer3_overflow = 0;

volatile unsigned char snd = 0;

volatile long resultCnt = 0; 

volatile int sigPin=0;

ISR(TIMER3_OVF_vect) 
{
  timer3_overflow += 1;
};

ISR(INT0_vect) //Start timer 1 when gate attached to pin 21 triggers 
{ 
   if(TCNT1 > 300)
   {
      sigPin=1;
      TCCR1B =0; //stop Timer 1
      TCNT1 = 0; //reset Timer 1
      timer3_overflow = 0; //timer overflow reset
      TIMSK3 |= _BV(TOIE3); //Timer 3 overflow enabled
      TCCR3A = 0x00; //Normal timer operation
      TCNT3 = 0;
      TCCR3B |= ( _BV(CS30) | _BV(CS31) ); //clock/64
      EIMSK = _BV(INT4); //enable INT1 disable INT0
    }
    TCNT1 = 0; // resets timer 1 counter
    TCCR1A = 0x00;  // Normal Timer Operation                                                                 
    TCCR1B |= ( _BV(CS10) | _BV(CS11) ); // clock/64      
}

ISR(INT4_vect) //Stop timer 1 when gate attached to pin 3 trigger
{
  if(TCNT0 > 300)
  {
    TCCR3B &= ~(_BV(CS30) | _BV(CS31) | _BV(CS32)); //Stop timer 3
    TCCR1B &= ~(_BV(CS10) | _BV(CS11) | _BV(CS12)); //Stop timer 1
    TCCR1B = 0; //stop Timer 1
    TCNT1 = 0; //reset Timer 1
    EIMSK = 0x00; //disable int1 and int0 
    snd = 1;
    sigPin=0;
  }
  TCNT1 = 0;
  TCCR1B =  _BV(CS10) | _BV(CS11); 
}


long microsecs()  //for debugging only
{
  long us;
  us = timer3_overflow * 65536;
  us += TCNT1;
  us *= TIMER_US_PER_TICK;
  return us;
}

//This will be used to store result and snd to host machine
union bindata 
{
  unsigned long val;
  byte b[4];
} resultus;

void sndResult()
{
    Serial.write('H');
    Serial.write(resultus.b,4);
    Serial.write('E');
}
  
void setup()
{
  pinMode(13, OUTPUT);
  Serial.begin(9600);
  //Set up external interrupts
  pinMode(INT0_pin, INPUT);
  pinMode(INT4_pin, INPUT);
  EICRA |=  _BV(ISC00); //set INT0 and INT1 to change detect
  EICRB |= _BV(ISC40);
  EIMSK = _BV(INT0);  //enable INT0 
  sei(); // enables interrupts
}

void loop()
{
  digitalWrite(13,sigPin);
  if(snd){
    cli();
    resultCnt = timer3_overflow * 65536; 
    resultCnt += TCNT3;
    resultus.val = resultCnt * TIMER_US_PER_TICK; //turns Timer count to microseconds
    sndResult();
    EIMSK = _BV(INT0); //enable INT0 again
    sei();
  }
}
