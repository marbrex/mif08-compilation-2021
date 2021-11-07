#include "printlib.h"

int main(){
  int n1, n2, n3;
  n2 = 2;
  n3 = 6;
  n1 = n3 - n2;
  println_int(n1);
  return 0;
}
  
// EXPECTED
// 4
