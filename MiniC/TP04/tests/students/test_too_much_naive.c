#include "printlib.h"

int main() {
    
    int x;
    int y;
    x = 42;
    y = 16;
    println_int(x + y);
    println_int(y + x);
    println_int(1 + x);
    println_int(1 + y);
    println_int(x + 1);
    println_int(y + 1);
    println_int(x - y);
    println_int(y - x);
    println_int(x - y + x - 2);
    return 0;
}

// EXPECTED
// 58
// 58
// 43
// 17
// 43
// 17
// 26
// -26
// 66
