#include "printlib.h"

int main(){
  int n1, n2;
  n1 = 3;
  n2 = -n1;
  println_int(n2);
  return 0;
}
  
// EXPECTED
// -3
