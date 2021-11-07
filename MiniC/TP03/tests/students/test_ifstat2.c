#include "printlib.h"

int main(){
  bool cond;
  cond = false;
  if (cond) {
    println_string("in if block");
  }
  else if (false) {
    println_string("in else block");
  }
  else {
    println_string("in else block 2");
  }
  return 0;
}
  
// EXPECTED
// in else block 2
