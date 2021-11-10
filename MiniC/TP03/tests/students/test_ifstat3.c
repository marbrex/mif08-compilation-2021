#include "printlib.h"

int main(){
  bool cond;
  cond = false;
  if (cond) {
    println_string("in if block");
  }
  println_string("out of if/else statements");
  return 0;
}
  
// EXPECTED
// out of if/else statements
