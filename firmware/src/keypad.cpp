

#include "keypad.hpp"
//#include "arduino.h"

byte MyKeypad::scan(void)
{
  
  digitalWrite(ROW0, LOW);
  delay(1);
  bitWrite(key_state, 0, !digitalRead(COL0));
  bitWrite(key_state, 1, !digitalRead(COL1));
  digitalWrite(ROW0, HIGH);
  
  digitalWrite(ROW1, LOW);
  delay(1);
  bitWrite(key_state, 2, !digitalRead(COL0));
  bitWrite(key_state, 3, !digitalRead(COL1));
  digitalWrite(ROW1, HIGH);
  
  digitalWrite(ROW2, LOW);
  delay(1);
  bitWrite(key_state, 4, !digitalRead(COL0));
  bitWrite(key_state, 5, !digitalRead(COL1));
  digitalWrite(ROW2, HIGH);
  
  digitalWrite(ROW3, LOW);
  delay(1);
  bitWrite(key_state, 6, !digitalRead(COL0));
  bitWrite(key_state, 7, !digitalRead(COL1));
  digitalWrite(ROW3, HIGH);

  // check pressed and released

  key_pressed = (~key_prev_state) & key_state;
  key_released = key_prev_state & ~key_state;

  //Serial.println(key_state+256, BIN);
  //Serial.println(~key_prev_state+256, BIN);
  //Serial.println(key_pressed+256, BIN);
  //Serial.println(key_released+256, BIN);
  //Serial.println("-------------------------");
  
  // save previous state
  key_prev_state = key_state;
  return key_state;
  
}

MyKeypad::MyKeypad(uint8_t row0_pin, uint8_t row1_pin, uint8_t row2_pin, uint8_t row3_pin, uint8_t col0_pin, uint8_t col1_pin, uint8_t lcol0_pin, uint8_t lcol1_pin)
{
  
  ROW0 = row0_pin;
  ROW1 = row1_pin;
  ROW2 = row2_pin;
  ROW3 = row3_pin;
  COL0 = col0_pin;
  COL1 = col1_pin;
  LCOL0 = lcol0_pin;
  LCOL1 = lcol1_pin;
  
  pinMode(ROW0, OUTPUT);
  digitalWrite(ROW0, HIGH);
  
  pinMode(ROW1, OUTPUT);
  digitalWrite(ROW1, HIGH);
  
  pinMode(ROW2, OUTPUT);
  digitalWrite(ROW2, HIGH);
  
  pinMode(ROW3, OUTPUT);
  digitalWrite(ROW3, HIGH);

  pinMode(COL0, INPUT_PULLUP);
  pinMode(COL1, INPUT_PULLUP);

  // per ora
  pinMode(LCOL0, INPUT_PULLUP);
  pinMode(LCOL1, INPUT_PULLUP);

  key_pressed = 0;
  key_released = 0;
  
  key_state = 0;
  key_prev_state = 0;

};
