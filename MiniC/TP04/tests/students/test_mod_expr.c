#include "printlib.h"

int main() {
    
    int x;
    int y;
    x = 4;
    y = 3;
    println_int(x % y);
    println_int((-x) % y);
    println_int(x % (-y));
    println_int((-x) % (-y));
    return 0;
}

// EXPECTED
// 1
// -1
// 1
// -1
