#include "printlib.h"

int main() {
    
    int x;
    int y;
    bool b;
    x = 42;
    y = 16;
    b = x > y;
    b = y < x;
    b = x >= y;
    b = y <= x;
    b = x == y;
    b = x != y;
    return 0;
}

// EXPECTED
