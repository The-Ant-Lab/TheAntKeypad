//--------------------------------------
// Gestione Programmi
//--------------------------------------

#ifndef KBPROG_H
#define KBPROG_H

#include "arduino.h"
#include <EEPROM.h>

#define MAX_PROG_NUM 5
#define PROG_SEQ_NUM 3
#define KEY_NUM 11
#define LED_NUM 8
#define PROG_NAME_LEN 9
#define EEPROM_OFFSET 10

typedef struct
{
  char prog_name[PROG_NAME_LEN+1];
  char keys_sequence[PROG_SEQ_NUM*KEY_NUM];
  char led_behavior[LED_NUM];
} ProgSetup;

class ProgHandler
{  
  public:
    ProgSetup * progs;
    uint8_t active;
    uint8_t progs_num;
    ProgHandler(void);
    uint8_t getMaxProgsNumber(void);
    uint8_t getProgNameLen(void);
    uint8_t getKeysNumber(void);
    uint8_t getKeyCharsNumber(void);
    uint8_t getLEDsNumber(void);
    void setProgKey(uint8_t key_id, byte key);
    bool setActiveProgById(uint8_t id);
    void loadDefaultProgs(void);
    void loadProgsFromEEPROM(void);
    void writeProgsToEEPROM(void);
    char * getButtonSequenceById(uint8_t button_id);
};

#endif
