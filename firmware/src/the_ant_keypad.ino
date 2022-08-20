#include "oled_mymenu.hpp"
#include "myEnc.hpp"
#include "Keyboard.h"
#include "keyboard_prog.hpp"
#include "keypad.hpp"
#include "serial_programmer.hpp"
#include "arduino.h"

ProgHandler * prog_handler;
ListMenu * list_menu;
SerialProgrammer * serial_programmer;

MyEnc *enc;

MyKeypad *keypad;
byte key_state;

int16_t last, value;
bool bt, prev_bt, prog_state;
int delta;
volatile bool isrf;

int SUP = A2;
int SDW = A3;
bool sup_state, sdw_state, sup_prev, sdw_prev;
bool sup_pressed, sdw_pressed;


void encCkIsr() {
  enc->isrDelta();
  isrf = true;
}

void setup(void)
{
  pinMode(SUP, INPUT_PULLUP);    // sets the digital pin A2 as input
  pinMode(SDW, INPUT_PULLUP);    // sets the digital pin A3 as input
  delay(2000); //Set delay 2 Second
  Serial.begin(SERIAL_BAUND_RATE);
  delay(1000); //Set delay 1 Second
  Serial.print("TheAntKeypad v0.9\n");
  prog_handler = new ProgHandler();
  list_menu = new ListMenu(prog_handler);
  serial_programmer = new SerialProgrammer(prog_handler);
  keypad = new MyKeypad(10, 16, 14, 15, A0, A1, 9, 8);
  enc = new MyEnc(7, 6, 5);
  enc->setupInterruptHandler(encCkIsr, CHANGE);
  prev_bt = HIGH;
  Keyboard.begin();
  delay(1000); //Set delay 1 Second
  sup_prev = HIGH;
  sdw_prev = HIGH;
  Serial.print("Initialized\n");
  prog_state = false;
  isrf = false;
}

void loop(void)
{
  // Check For Commands
  if( serial_programmer->checkForCommand())
  {
    if(!prog_state){
      list_menu->show_prog(serial_programmer->prog_on);
      prog_state = true;
    }
    if(prog_state && !serial_programmer->prog_on){
      list_menu->show_prog(serial_programmer->prog_on);
    }
    //Serial.print("ok\n");
  }
  
  if(!serial_programmer->prog_on)
  {
    prog_state = false;
    sup_state = digitalRead(SUP);
    sdw_state = digitalRead(SDW);
    sup_pressed = !sup_state and sup_prev;
    sdw_pressed = !sdw_state and sdw_prev;

    key_state = keypad->scan();
    
    //Serial.print("Loop\n");
    value = enc->getDelta();
    if(sup_pressed || sdw_pressed)
    {
      if(sdw_pressed)
      {
        list_menu->dec_prog();
      }
      if(sup_pressed)
      {
        list_menu->inc_prog();
      }
    }
    bt = enc->getBtState();
    if (bt != prev_bt)
    {
      if (bt == LOW)
      {
        for(int j=0;j<3;j++)
        {
          char p = list_menu->get_prog_key(8)[j];
          if(p != '\0')
          {
            Keyboard.press(list_menu->get_prog_key(8)[j]);
          }
        }
      }
      else
      {
        for(int j=2;j>=0;j--)
        {
          char p = list_menu->get_prog_key(8)[j];
          if(p != '\0')
          {
            Keyboard.release(list_menu->get_prog_key(8)[j]);
          }
        }
        Keyboard.releaseAll();
      }
    }
    
    delta = enc->getDelta();
    if (delta != 0)
    {
      Serial.println("I\n");
      if (delta < 0)
      {
        for(int i=delta;i<0;i++){
          for(int j=0;j<3;j++)
          {
            char p = list_menu->get_prog_key(9)[j];
            if(p != '\0')
            {
              Keyboard.press(list_menu->get_prog_key(9)[j]);
            }
          }
          delay(50);
          for(int j=0;j<3;j++)
          {
            char p = list_menu->get_prog_key(9)[2-j];
            if(p != '\0')
            {
              Keyboard.release(list_menu->get_prog_key(9)[2-j]);
            }
          }
          //Keyboard.releaseAll();
        }
      }
      else
      {
        for(int i=0;i<delta;i++){
          for(int j=0;j<3;j++)
          {
            char p = list_menu->get_prog_key(10)[j];
            if(p != '\0')
            {
              Keyboard.press(list_menu->get_prog_key(10)[j]);
            }
          }
          delay(50);
          for(int j=0;j<3;j++)
          {
            char p = list_menu->get_prog_key(10)[2-j];
            if(p != '\0')
            {
              Keyboard.release(list_menu->get_prog_key(10)[2-j]);
            }
          }
          //Keyboard.releaseAll();
        }
      }
      enc->resetDelta();
    }
    
    for(int i=0;i<8;i++)
    {
      if(keypad->key_pressed & (0x1<<i))
      {
        for(int j=0;j<3;j++)
        {
          char p = list_menu->get_prog_key(i)[j];
          if(p != '\0')
          {
            Keyboard.press(list_menu->get_prog_key(i)[j]);
          }
        }
      }
      if(keypad->key_released & (0x1<<i))
      {
        for(int j=0;j<3;j++)
        {
          char p = list_menu->get_prog_key(i)[2-j];
          if(p != '\0')
          {
            Keyboard.release(list_menu->get_prog_key(i)[2-j]);
          }
        }
        //Keyboard.releaseAll();
      }
    }
    prev_bt = bt;
    sup_prev = sup_state;
    sdw_prev = sdw_state;
  }
  delay(2);
}
