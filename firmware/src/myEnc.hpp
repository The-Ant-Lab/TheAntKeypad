
#ifndef MYENC_H
#define MYENC_H
#include "arduino.h"

class MyEnc
{
  private:
    volatile int16_t _delta;
    uint8_t _ck;
    uint8_t _dt;
    uint8_t _bt;
        
  public:
    MyEnc(uint8_t ck_pin, uint8_t dt_pin, uint8_t bt_pin);
    void setupInterruptHandler(void (*encISR)(void), int type);
    void isrDelta();
    int16_t getDelta();
    void resetDelta();
    bool getBtState();
};

#endif
