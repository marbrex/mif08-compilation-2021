#include "printlib.h"

int main() {
    
    int x;
    int y;
    x = 42;
    y = 2;
    println_int(x / y);
    println_int(y / x);
    println_int(x * y);
    println_int(y * (x / 3));
    return 0;
}

// EXPECTED
// 21
// 0
// 84
// 28
