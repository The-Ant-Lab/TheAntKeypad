
#include "keyboard_prog.hpp"
#include "Keyboard.h"

ProgHandler::ProgHandler()
{
  progs = NULL;
  //loadDefaultProgs();  
  Serial.print("Prog Init\n");
  loadProgsFromEEPROM();
};

char * ProgHandler::getButtonSequenceById(uint8_t button_id)
{
  return progs[active].keys_sequence + PROG_SEQ_NUM * button_id;
};

uint8_t ProgHandler::getMaxProgsNumber(void)
{
  return MAX_PROG_NUM;
};

uint8_t ProgHandler::getProgNameLen(void)
{
  return PROG_NAME_LEN;
};

uint8_t ProgHandler::getKeysNumber(void)
{
  return KEY_NUM;
};

uint8_t ProgHandler::getKeyCharsNumber(void)
{
  return PROG_SEQ_NUM;
};

uint8_t ProgHandler::getLEDsNumber(void)
{
  return LED_NUM;
};

void ProgHandler::setProgKey(uint8_t key_id, byte key)
{
  progs[active].keys_sequence[key_id] = key;
}

bool ProgHandler::setActiveProgById(uint8_t id)
{
  if(id < progs_num)
  {
    active = id;
    return true;
  }
  else
  {
    return false;
  }
};

void ProgHandler::loadProgsFromEEPROM(void)
{
  Serial.println("Load EEPROM");
  //byte value;
  //char nc;
  int id = EEPROM_OFFSET;
  progs_num = uint8_t(EEPROM.read(id++));
  
  uint8_t prog_seq_num = uint8_t(EEPROM.read(id++));
  uint8_t key_num = uint8_t(EEPROM.read(id++));
  uint8_t clen = prog_seq_num * key_num;

  active = 0;

  if(progs != NULL)
  {
    free(progs);
  }
  progs = (ProgSetup *)calloc(MAX_PROG_NUM, sizeof(ProgSetup));

  for(int i;i<progs_num;i++)
  {
    // memcpy(progs[i].prog_name, 0, sizeof(progs[i].prog_name));
    for(int j=0;j<PROG_NAME_LEN;j++)
    {
      progs[i].prog_name[j] = char(EEPROM.read(id++));
    }
    for(int j=0;j<clen;j++)
    {
      progs[i].keys_sequence[j] = char(EEPROM.read(id++));
    }
  }
};

void ProgHandler::writeProgsToEEPROM(void)
{
  Serial.println("Write EEPROM");
  uint8_t id = EEPROM_OFFSET;
  uint8_t clen = PROG_SEQ_NUM*KEY_NUM;
  EEPROM.write(id++, progs_num);
  EEPROM.write(id++, PROG_SEQ_NUM);
  EEPROM.write(id++, KEY_NUM);
  for(uint8_t i=0;i<progs_num;i++)
  {
    for(uint8_t j=0;j<PROG_NAME_LEN;j++)
    {
      EEPROM.write(id + j, 0);
    }
    for(uint8_t j=0;j<strlen(progs[i].prog_name);j++)
    {
      EEPROM.write(id + j, progs[i].prog_name[j]);
    }
    id += PROG_NAME_LEN;
    for(int j=0;j<clen;j++)
    {
      EEPROM.write(id++, progs[i].keys_sequence[j]);
    }
  }
};

void ProgHandler::loadDefaultProgs()
{
  active = 0;
  progs_num = 3;
  
  if(progs != NULL)
  {
    free(progs);
  }
  progs = (ProgSetup *)calloc(MAX_PROG_NUM, sizeof(ProgSetup));

  memcpy(progs[0].prog_name, 0, sizeof(progs[0].prog_name));
  strcpy(progs[0].prog_name, "Eagle");
  
  // BT 1 MOVE
  progs[0].keys_sequence[0] = KEY_LEFT_CTRL;
  progs[0].keys_sequence[1] = 'm';
  progs[0].keys_sequence[2] = '\0';
  
  // BT 2 ROUTE
  progs[0].keys_sequence[3] = KEY_LEFT_CTRL;
  progs[0].keys_sequence[4] = 'r';
  progs[0].keys_sequence[5] = '\0';
  
  // BT 3 ROTATE
  progs[0].keys_sequence[6] = KEY_LEFT_CTRL;
  progs[0].keys_sequence[7] = KEY_LEFT_SHIFT;
  progs[0].keys_sequence[8] = 'x';
  
  // BT 4 MIRROR
  progs[0].keys_sequence[9] = KEY_LEFT_CTRL;
  progs[0].keys_sequence[10] = KEY_LEFT_SHIFT;
  progs[0].keys_sequence[11] = 'm';

  // BT 5 RIPUP
  progs[0].keys_sequence[12] = KEY_LEFT_CTRL;
  progs[0].keys_sequence[13] = KEY_LEFT_SHIFT;
  progs[0].keys_sequence[14] = 'r';
  
  // BT 6 ADD
  progs[0].keys_sequence[15] = KEY_LEFT_CTRL;
  progs[0].keys_sequence[16] = KEY_LEFT_SHIFT;
  progs[0].keys_sequence[17] = 'a';
  
  // BT 7 SELECT
  progs[0].keys_sequence[18] = KEY_LEFT_CTRL;
  progs[0].keys_sequence[19] = 'G';
  progs[0].keys_sequence[20] = '\0';
  
  // BT 8 ESC
  progs[0].keys_sequence[21] = KEY_ESC;
  progs[0].keys_sequence[22] = '\0';
  progs[0].keys_sequence[23] = '\0';

  // BT 9
  progs[0].keys_sequence[24] = 'k';
  progs[0].keys_sequence[25] = '\0';
  progs[0].keys_sequence[26] = '\0';

  // BT 10
  progs[0].keys_sequence[27] = '+';
  progs[0].keys_sequence[28] = '\0';
  progs[0].keys_sequence[29] = '\0';

  // BT 11
  progs[0].keys_sequence[30] = '-';
  progs[0].keys_sequence[31] = '\0';
  progs[0].keys_sequence[32] = '\0';

  //progs[0].led_behavior = {'\0','\0','\0','\0','\0','\0','\0','\0'};

  memcpy(progs[1].prog_name, 0, sizeof(progs[1].prog_name));
  strcpy(progs[1].prog_name, "DaVinci");
  
  // BT 1
  progs[1].keys_sequence[0] = 'A';
  progs[1].keys_sequence[1] = '\0';
  progs[1].keys_sequence[2] = '\0';
  
  // BT 2
  progs[1].keys_sequence[3] = 'B';
  progs[1].keys_sequence[4] = '\0';
  progs[1].keys_sequence[5] = '\0';
  
  // BT 3
  progs[1].keys_sequence[6] = 'C';
  progs[1].keys_sequence[7] = '\0';
  progs[1].keys_sequence[8] = '\0';
  
  // BT 4
  progs[1].keys_sequence[9] = 'D';
  progs[1].keys_sequence[10] = '\0';
  progs[1].keys_sequence[11] = '\0';

  // BT 5
  progs[1].keys_sequence[12] = 'E';
  progs[1].keys_sequence[13] = '\0';
  progs[1].keys_sequence[14] = '\0';
  
  // BT 6
  progs[1].keys_sequence[15] = 'F';
  progs[1].keys_sequence[16] = '\0';
  progs[1].keys_sequence[17] = '\0';
  
  // BT 7
  progs[1].keys_sequence[18] = 'G';
  progs[1].keys_sequence[19] = '\0';
  progs[1].keys_sequence[20] = '\0';
  
  // BT 8
  progs[1].keys_sequence[21] = 'H';
  progs[1].keys_sequence[22] = '\0';
  progs[1].keys_sequence[23] = '\0';

  // BT 9
  progs[1].keys_sequence[24] = 'I';
  progs[1].keys_sequence[25] = '\0';
  progs[1].keys_sequence[26] = '\0';

  // BT 10
  progs[1].keys_sequence[27] = '+';
  progs[1].keys_sequence[28] = '\0';
  progs[1].keys_sequence[29] = '\0';

  // BT 11
  progs[1].keys_sequence[30] = '-';
  progs[1].keys_sequence[31] = '\0';
  progs[1].keys_sequence[32] = '\0';

  //progs[1].led_behavior = {'\0','\0','\0','\0','\0','\0','\0','\0'};

  memcpy(progs[2].prog_name, 0, sizeof(progs[2].prog_name));
  strcpy(progs[2].prog_name, "OBS");
  
  // BT 1
  progs[2].keys_sequence[0] = 'a';
  progs[2].keys_sequence[1] = '\0';
  progs[2].keys_sequence[2] = '\0';
  
  // BT 2
  progs[2].keys_sequence[3] = 'b';
  progs[2].keys_sequence[4] = '\0';
  progs[2].keys_sequence[5] = '\0';
  
  // BT 3
  progs[2].keys_sequence[6] = 'c';
  progs[2].keys_sequence[7] = '\0';
  progs[2].keys_sequence[8] = '\0';
  
  // BT 4
  progs[2].keys_sequence[9] = 'd';
  progs[2].keys_sequence[10] = '\0';
  progs[2].keys_sequence[11] = '\0';

  // BT 5
  progs[2].keys_sequence[12] = 'e';
  progs[2].keys_sequence[13] = '\0';
  progs[2].keys_sequence[14] = '\0';
  
  // BT 6
  progs[2].keys_sequence[15] = 'f';
  progs[2].keys_sequence[16] = '\0';
  progs[2].keys_sequence[17] = '\0';
  
  // BT 7
  progs[2].keys_sequence[18] = 'g';
  progs[2].keys_sequence[19] = '\0';
  progs[2].keys_sequence[20] = '\0';
  
  // BT 8
  progs[2].keys_sequence[21] = 'h';
  progs[2].keys_sequence[22] = '\0';
  progs[2].keys_sequence[23] = '\0';

  // BT 9
  progs[2].keys_sequence[24] = 'i';
  progs[2].keys_sequence[25] = '\0';
  progs[2].keys_sequence[26] = '\0';

  // BT 10
  progs[2].keys_sequence[27] = '+';
  progs[2].keys_sequence[28] = '\0';
  progs[2].keys_sequence[29] = '\0';

  // BT 11
  progs[2].keys_sequence[30] = '-';
  progs[2].keys_sequence[31] = '\0';
  progs[2].keys_sequence[32] = '\0';

  //progs[2].led_behavior = {'\0','\0','\0','\0','\0','\0','\0','\0'};
};
