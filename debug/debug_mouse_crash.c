#include <unistd.h>
#include <stdint.h>
#include <string.h>
#include "libtermbox.h"


void tbPrint(int x, int y, uint16_t fg, uint16_t bg, char *msg) {
  int len = strlen(msg);
  int i;
  for(i=0;i<len;i++){
    SetCell(x, y, msg[i], fg, bg);
    x++;
  }
};

void update_and_redraw(char *s) {
  Clear(0, 0);
  tbPrint(0, 0, 0, 0, s);
  Flush();
}

int main()
{
  int mx = 0;
  int my = 0;
  Init();
  SetInputMode(5);
  while (1) {
    Event *evt = PollEvent();
    if (evt->Type == 0) {
      if (evt->Key == 27) {
        break;
      }
    } else if (evt->Type == 2) {
      if (evt->Key == 65512) {
        mx = evt->MouseX;
        my = evt->MouseY;
      }
    }
    freeEvent(evt);
    char s[20];
    sprintf(s, "x: {%d}, y: {%d}", mx, my);
    update_and_redraw(s);
  }
  Close();
  return 0;
}
