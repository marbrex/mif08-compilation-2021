#include "printlib.h"

int main(){
  int n1, n2;
  n1 = 3;
  n2 = n1 / 0;
  println_int(n2);
  return 0;
}
  
// EXPECTED
// EXITCODE 1
// Division by 0
