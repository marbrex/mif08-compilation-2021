#include "printlib.h"

int main() {
    
    int x;
    int y;
    x = 42;
    y = 2;
    println_int(x / (y / x));
    return 0;
}

// SKIP TEST EXPECTED
// EXECCODE 1
// EXPECTED
// Division by 0