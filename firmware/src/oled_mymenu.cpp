
#include "oled_mymenu.hpp"
#include "arduino.h"

ListMenu::ListMenu(ProgHandler * ph)
{
  prog_handler = ph;
  _draw(255, 0, 0);
  current = 0;
}

char * ListMenu::get_prog_name(int i)
{
  if(prog_handler->progs_num != 255)
  {
    if(i < prog_handler->progs_num)
    {
      // Serial.println(i,DEC);
      // Serial.println(prog_handler->progs[i].prog_name);
      return prog_handler->progs[i].prog_name;
    }
  }
  return "";
}

char * ListMenu::get_prog_key(uint8_t i)
{
  return prog_handler->getButtonSequenceById(i);
}

void ListMenu::update_prog()
{
  if(prog_handler->progs_num != 255)
  {
    uint8_t menu_prog_num = prog_handler->progs_num;
    uint8_t current = prog_handler->active;
    uint8_t prog_id = current;
    _draw(255, prog_id, 1);
    prog_handler->active = prog_id;
  }
}

void ListMenu::inc_prog()
{
  if(prog_handler->progs_num != 255)
  {
    uint8_t menu_prog_num = prog_handler->progs_num;
    uint8_t current = prog_handler->active;
    uint8_t prog_id = (current + 1) % menu_prog_num;
    _draw(255, prog_id, 0);
    prog_handler->active = prog_id;
  }
}

void ListMenu::dec_prog()
{
  if(prog_handler->progs_num != 255)
  {
    uint8_t menu_prog_num = prog_handler->progs_num;
    uint8_t current = prog_handler->active;
    uint8_t prog_id = (current + menu_prog_num - 1) % menu_prog_num;
    _draw(255, prog_id, 1);
    prog_handler->active = prog_id;
  }
}

void ListMenu::_draw(uint8_t contrast, uint8_t prog_id, uint8_t reverse)
{
  char *curr_prog;
  char *next_prog;
  char *prev_prog;

  uint8_t frames = 3;
  uint8_t menu_prog_num = prog_handler->progs_num;
  
  if(reverse == 1)
  {
    curr_prog = get_prog_name(prog_id % menu_prog_num);
    next_prog = get_prog_name((prog_id + 1) % menu_prog_num);
    prev_prog = get_prog_name((prog_id + menu_prog_num - 1) % menu_prog_num);
  }
  else
  {
    curr_prog = get_prog_name(prog_id % menu_prog_num);
    next_prog = get_prog_name((prog_id + 1) % menu_prog_num);
    prev_prog = get_prog_name((prog_id + menu_prog_num - 1) % menu_prog_num);
  }
  
  u8g.setContrast(contrast);

  if(prog_handler->active != (prog_id % menu_prog_num))
  {

    if(reverse == 1)
    {
      // Serial.print("Reversed");
      
      for(uint8_t i=frames;i>0;i--)
      { 
        u8g.firstPage();
        do
        {
          u8g.setFont(u8g_font_profont15r);        
          u8g.setPrintPos(1, (i-1) * 4);
          u8g.println(prev_prog);

          u8g.setFont(u8g_font_profont15r);        
          u8g.setPrintPos((i-1) * 6 + 2, 12 + (i-1) * 12);
          u8g.println(next_prog);

          u8g.setFont(u8g_font_profont15r);        
          u8g.setPrintPos(14 - ((i-1) * 6 + 1) , 48 + (i-1) * 6);
          u8g.println(curr_prog);
        
          u8g.setFont(u8g_font_profont15r);        
          u8g.setPrintPos(1, 60 + ((i-1) + 1) * 6);
          u8g.println(prev_prog);
          
          // Set to draws frame with rounded edges
          u8g.drawRFrame(4, 17, 124, 28, 10);
        }
        while ( u8g.nextPage() );
      }

    }
    else
    {
      // Serial.print("Not Reversed");
      for(int i=0;i<frames;i++)
      { 
        u8g.firstPage();
        do
        {
          u8g.setFont(u8g_font_profont15r);
          u8g.setPrintPos(1, i * 4);
          u8g.println(next_prog);

          u8g.setFont(u8g_font_profont15r);
          u8g.setPrintPos(i * 6 + 2, 12 + i * 12);
          u8g.println(curr_prog);

          u8g.setFont(u8g_font_profont15r);
          u8g.setPrintPos(14 - (i * 6 + 1) , 48 + i * 6);
          u8g.println(prev_prog);
        
          u8g.setFont(u8g_font_profont15r);
          u8g.setPrintPos(1, 60 + (i + 1) * 6);
          u8g.println(next_prog);

          // Set to draws frame with rounded edges
          u8g.drawRFrame(4, 17, 124, 28, 10);
        }
        while ( u8g.nextPage() );
      }
    }
  }

  u8g.firstPage();
  do
  {
    u8g.setFont(u8g_font_profont15r);        // Set display font 1
    u8g.setPrintPos(1, 12);
    u8g.println(next_prog);

    u8g.setFont(u8g_font_profont22r);        // Set display font 1
    u8g.setPrintPos(14, 38);
    u8g.println(curr_prog);

    u8g.setFont(u8g_font_profont15r);        // Set display font 1
    u8g.setPrintPos(1, 60);
    u8g.println(prev_prog);
    u8g.drawRFrame(4, 17, 124, 28, 10);      // Set to draws frame with rounded edges
  }
  while ( u8g.nextPage() );
}

void ListMenu::show_prog(bool prog)
{
  if(prog)
  {
    u8g.firstPage();
    do {
    } while(u8g.nextPage());
    u8g.firstPage();
    do {
        u8g.drawStr(20, 40, "PROG!");
    } while (u8g.nextPage());
  }
  else
  {
    update_prog();
  }
}
