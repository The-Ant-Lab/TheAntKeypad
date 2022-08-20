//--------------------------------------
// Serial Programmer
//--------------------------------------

#ifndef SERIALPROGRAMMER_H
#define SERIALPROGRAMMER_H

#include "keyboard_prog.hpp"
#include "arduino.h"

#define SERIAL_BAUND_RATE 115200

#define SERIAL_PROG_OFF 'o'
#define SERIAL_PROG_ON  'i'
#define SERIAL_GET_PROG_STATE 'x'

#define SERIAL_GET_SETUP 'l'
#define SERIAL_SEND_PROG 's'

#define SERIAL_GET_PROG_NUM 'p'
#define SERIAL_SET_PROG_NUM 'y'

#define SERIAL_GET_CURRENT_PROG 'c'
#define SERIAL_SET_CURRENT_PROG 'h'

#define SERIAL_GET_PROG_NAME 'n'
#define SERIAL_SET_PROG_NAME 'm'

#define SERIAL_SET_PROG_KEYS 'k'

#define SERIAL_WRITE_PROG_ON_EEPROM 'w'
#define SERIAL_LOAD_PROG_FROM_EEPROM 'd'

class SerialProgrammer
{  
  public:
    bool prog_on;
    uint8_t prog_name_len;
    String input, last_command;
    ProgHandler * prog_handler;
    SerialProgrammer(ProgHandler * prog_handler_in);
    bool checkForCommand(void);
    bool commandInterp(void);
};

#endif
