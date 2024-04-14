#include <avr/wdt.h>

#define WATER_DETECTOR_PIN A0
#define PUMP_ACTIVATION_PIN 4
#define NUM_SECONDS_TO_ACTIVATE 172800
#define MAX_TIME_PUMP_ACTIVE 5
#define TIME_INDICATOR_PIN 13
#define ACTIVATION_CHAR 'A'

enum state {
  WAITING,
  PUMP_ACTIVE,
  CRITICAL_FAILURE
};
typedef enum state state;

state CURRENT_STATE = WAITING;
volatile unsigned long SECONDS_PASSED = 0;
volatile int NEW_SECOND_FLAG = 0;

void setup_interrupt_one_sec() {
  TCCR1A = _BV(COM1B1) | _BV(WGM11) | _BV(WGM10);
  TCCR1B = _BV(WGM13) | _BV(WGM12) | _BV(CS12);
  TIMSK1 = _BV(OCIE1A);
  OCR1A = 0xF424;
  OCR1B = 0x0064;
}

void setup_watchdog() {
  wdt_enable(WDTO_2S);
}

ISR( TIMER1_COMPA_vect )
{
  NEW_SECOND_FLAG = 1;
  SECONDS_PASSED++;
}

void setup() {
  pinMode(PUMP_ACTIVATION_PIN, OUTPUT);
  pinMode(TIME_INDICATOR_PIN, OUTPUT);
  digitalWrite(TIME_INDICATOR_PIN, LOW);
  setup_interrupt_one_sec();
  setup_watchdog();
  Serial.begin(9600);
}

void loop() {
  int WATER_DETECTION_STATE = analogRead(WATER_DETECTOR_PIN);
  
  if (NEW_SECOND_FLAG) {
    if(CURRENT_STATE != CRITICAL_FAILURE)digitalWrite(TIME_INDICATOR_PIN, SECONDS_PASSED % 2);
    NEW_SECOND_FLAG = 0;
  }

  switch(CURRENT_STATE) {
    case WAITING:
      while(Serial.available() > 0) {
        char c = Serial.read();
        if (c == ACTIVATION_CHAR) { 
          CURRENT_STATE = PUMP_ACTIVE;
          SECONDS_PASSED = 0;
          Serial.println("Activating pump...");
        }    
      }
      break;
    case PUMP_ACTIVE:
      if (WATER_DETECTION_STATE > 800) {
        //Serial.println("Waiting for water");
        if (SECONDS_PASSED > MAX_TIME_PUMP_ACTIVE) CURRENT_STATE = CRITICAL_FAILURE;
        digitalWrite(PUMP_ACTIVATION_PIN, HIGH);
      } else {
        Serial.println("Water found. Turning off");
        digitalWrite(PUMP_ACTIVATION_PIN, LOW);
        CURRENT_STATE = WAITING;
        SECONDS_PASSED = 0;
      }
      break;
    case CRITICAL_FAILURE:
      Serial.println("No water found after timeout. Turning off");
      digitalWrite(PUMP_ACTIVATION_PIN, LOW);
      CURRENT_STATE = WAITING;
      break;
    default:
      break;
  }
  wdt_reset();
}
