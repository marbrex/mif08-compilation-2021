#include "printlib.h"

int main(){
  println_int(122%3);
  println_int(16%3);
  println_int(0%1);
  return 0;
}
  
// EXPECTED
// 2
// 1
// 0
