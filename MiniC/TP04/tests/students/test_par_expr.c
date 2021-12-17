#include "printlib.h"

int main() {
    
    int x;
    int y;
    x = 42;
    y = 16;
    println_int(106 - ((y + x) + (9 - 3)));
    return 0;
}

// EXPECTED
// 42
