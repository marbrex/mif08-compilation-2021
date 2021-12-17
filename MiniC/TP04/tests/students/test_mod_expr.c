#include "printlib.h"

int main() {
    
    int x;
    int y;
    x = 42;
    y = 16;
    println_int(x % y);
    return 0;
}

// EXPECTED
// 10
