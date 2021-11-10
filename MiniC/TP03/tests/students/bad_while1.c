#include "printlib.h"

int main(){
  float n;
  n = 3.14;
  while (n) {
    println_int(n);
    n = n + 1.0;
  }
  return 0;
}
  
// EXPECTED
// EXITCODE 2
// In function main: Line 6 col 2: invalid type for while condition: float
