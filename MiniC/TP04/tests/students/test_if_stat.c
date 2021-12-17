#include "printlib.h"

int main() {
    
    int x;
    int y;
    bool b;
    x = 42;
    y = 16;
    b = x > y;
    if (b) {
        println_int(x);
    }
    else {
        println_int(y);
    }
    return 0;
}

// EXPECTED
// 42
