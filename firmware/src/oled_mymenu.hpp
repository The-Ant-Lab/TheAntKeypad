//--------------------------------------
// Piccolo Menu
//--------------------------------------

#ifndef OLEDMYMENU_H
#define OLEDMYMENU_H

#include "keyboard_prog.hpp"
#include "U8glib.h"            // U8glib library for the OLED you download below
#include <Wire.h>              // Set Wire library for I2C communication

//U8GLIB_SSD1306_128X64 the_u8g(U8G_I2C_OPT_NONE);  // I2C / TWI

class ListMenu
{
  private:
    ProgHandler * prog_handler;
    void _draw(uint8_t contrast, uint8_t prog_id, uint8_t reverse);
  public:
    ListMenu(ProgHandler * ph);
    uint8_t current = 0;
    uint8_t menu_prog_num = 0;
    void update_prog();
    void inc_prog(void);
    void dec_prog(void);
    char * get_prog_name(int i);
    char * get_prog_key(uint8_t i);
    void show_prog(bool prog);
    U8GLIB_SSD1306_128X64 u8g = U8GLIB_SSD1306_128X64(U8G_I2C_OPT_NONE);
};

#endif
