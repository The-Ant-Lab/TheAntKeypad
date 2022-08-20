
#include "serial_programmer.hpp"

SerialProgrammer::SerialProgrammer(ProgHandler * prog_handler_in)
{
  prog_handler = prog_handler_in;
  prog_name_len = prog_handler->getProgNameLen();
  prog_on = false;
  input.reserve(PROG_NAME_LEN + 1);
  last_command.reserve(PROG_NAME_LEN + 1);
};

bool SerialProgrammer::checkForCommand(void)
{
  if(Serial.available() > 0)
  {
    bool ret;
    last_command = Serial.readStringUntil('\n');
    ret = commandInterp();
    return ret;
  }
  return false;
};

bool SerialProgrammer::commandInterp(void)
{
  bool ret = false;
  uint8_t c, d, e;
  
  if(last_command != "")
  {
    switch(last_command[0])
    {
      case SERIAL_PROG_OFF:
        prog_on = false;
        last_command = "";
        ret = true;
        break;

      case SERIAL_PROG_ON:
        prog_on = true;
        last_command = "";
        ret = true;
        break;
      
      case SERIAL_GET_PROG_STATE:
        if(prog_on)
        {
          Serial.write("1");
        }
        else{
          Serial.write("0");
        }
        last_command = "";
        Serial.write("\n");
        ret = true;
        break;

      case SERIAL_GET_SETUP:
        Serial.write(prog_handler->getMaxProgsNumber());
        Serial.write(prog_handler->getProgNameLen());
        Serial.write(prog_handler->getKeysNumber());
        Serial.write(prog_handler->getKeyCharsNumber());
        Serial.write(prog_handler->getLEDsNumber());
        last_command = "";
        Serial.write("\n");
        ret = true;
        break;

      case SERIAL_GET_PROG_NUM:
        Serial.write(prog_handler->progs_num);
        last_command = "";
        Serial.write("\n");
        ret = true;
        break;

      case SERIAL_GET_PROG_NAME:
        Serial.write(strlen(prog_handler->progs[prog_handler->active].prog_name));
        Serial.print(prog_handler->progs[prog_handler->active].prog_name);
        last_command = "";
        Serial.write("\n");
        ret = true;
        break;
      
      case SERIAL_SET_PROG_NAME:
        //char new_name[PROG_NAME_LEN + 1];
        input = Serial.readStringUntil('\n');
        c = input.toInt();
        Serial.write(c);
        Serial.write("\n");
        input = Serial.readStringUntil('\n');
        if(c <= PROG_NAME_LEN)
        {
          memcpy(prog_handler->progs[prog_handler->active].prog_name, 0, sizeof(prog_handler->progs[prog_handler->active].prog_name));
          strcpy(prog_handler->progs[prog_handler->active].prog_name, input.c_str());
          ret = true;
        }
        input = "";
        last_command = "";
        ret = false;
        break;

      case SERIAL_GET_CURRENT_PROG:
        Serial.write(prog_handler->active);
        last_command = "";
        Serial.write("\n");
        ret = true;
        break;

      case SERIAL_SET_CURRENT_PROG:
        input = Serial.readStringUntil('\n');
        c = input.toInt();
        prog_handler->setActiveProgById(c);
        last_command = "";
        ret = true;
        break;

      case SERIAL_WRITE_PROG_ON_EEPROM:
        last_command = "";
        prog_handler->writeProgsToEEPROM();
        ret = true;
        break;
      
      case SERIAL_LOAD_PROG_FROM_EEPROM:
        last_command = "";
        prog_handler->loadProgsFromEEPROM();
        ret = true;
        break;

      case SERIAL_SET_PROG_KEYS:
        input = Serial.readStringUntil('\n');
        c = input.toInt(); // c contains the starting id
        c = c*prog_handler->getKeyCharsNumber();
        input = "";
        input = Serial.readStringUntil('\n'); // inputs conatin the new keys
        //Serial.print(input);
        //Serial.write("\n");
        for(uint8_t i=0;i<prog_handler->getKeyCharsNumber();i++)
        {
          if( i < input.length())
          {
            prog_handler->setProgKey(c+i, input[i]);
          }
          else
          {
            prog_handler->setProgKey(c+i, '\0');
          }
        }
        last_command = "";
        ret = true;
        break;

      case SERIAL_SEND_PROG:
        Serial.write(prog_handler->progs[prog_handler->active].keys_sequence, prog_handler->getKeysNumber()*prog_handler->getKeyCharsNumber());
        last_command = "";
        Serial.write("\n");
        ret = true;
        break;

      default:
        last_command = "";
    }
  }
  return ret;
}
