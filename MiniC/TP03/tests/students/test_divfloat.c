#include "printlib.h"

int main(){
  float n1, n2;
  n1 = 3.3;
  n2 = n1 / 3.0;
  println_float(n2);
  return 0;
}
  
// EXPECTED
// 1.10
