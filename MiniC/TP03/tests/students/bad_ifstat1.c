#include "printlib.h"

int main(){
  int n;
  if (n) {
    println_string("in if block");
  }
  else {
    println_string("in else block");
  }
  return 0;
}
  
// EXPECTED
// EXITCODE 2
// In function main: Line 5 col 2: invalid type for if condition: integer
