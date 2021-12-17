#include "printlib.h"

int main() {
    
    int x;
    int y;
    x = 42;
    y = 16;
    println_int(-(x - y + x - 2));
    return 0;
}

// EXPECTED
// -66
