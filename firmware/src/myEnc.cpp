

#include "myEnc.hpp"
#include "arduino.h"

MyEnc::MyEnc(uint8_t ck_pin, uint8_t dt_pin, uint8_t bt_pin)
{
  _ck = ck_pin;
  _dt = dt_pin;
  _bt = bt_pin;
  _delta = 0;
  pinMode(dt_pin, INPUT);
  pinMode(ck_pin, INPUT);
  pinMode(bt_pin, INPUT_PULLUP);
}

void MyEnc::setupInterruptHandler(void (*encISR)(void), int type)
{
  attachInterrupt(digitalPinToInterrupt(_ck), encISR, type);
}

void MyEnc::isrDelta()
{
  cli();
  uint8_t c = digitalRead(_ck);
  uint8_t a = digitalRead(_dt);
 
  if(c == LOW){
    // FALLING
    if(a == LOW){
      _delta--;
    }
  }
  else
  {
    // RISING
    if(a == LOW){
      _delta++;
    }
  }
  sei();
}

int16_t MyEnc::getDelta()
{
  return _delta;   
}

void MyEnc::resetDelta()
{
  _delta = 0;
}

bool MyEnc::getBtState()
{
  return digitalRead(_bt);
}
