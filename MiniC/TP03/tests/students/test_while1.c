#include "printlib.h"

int main(){
  int n;
  n = 0;
  while (n < 5) {
    println_int(n);
    n = n + 1;
    if (n == 5) {
      println_string("end of while loop");
    }
  }
  return 0;
}
  
// EXPECTED
// 0
// 1
// 2
// 3
// 4
// end of while loop
