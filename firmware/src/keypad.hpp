//--------------------------------------
// Controllo Keypad
//--------------------------------------

#ifndef KEYPAD8_H
#define KEYPAD8_H

#include "arduino.h"

class MyKeypad
{
  private:
    
    uint8_t ROW0;
    uint8_t ROW1;
    uint8_t ROW2;
    uint8_t ROW3;
    uint8_t COL0;
    uint8_t COL1;
    uint8_t LCOL0;
    uint8_t LCOL1;
  
  public:

    MyKeypad(uint8_t row0_pin, uint8_t row1_pin, uint8_t row2_pin, uint8_t row3_pin, uint8_t col0_pin, uint8_t col1_pin, uint8_t lcol0_pin, uint8_t lcol1_pin);
    byte scan(void);

    char keys[9] = "12345678";

    byte key_state;
    byte key_pressed;
    byte key_released;
    byte key_prev_state;

};

#endif
