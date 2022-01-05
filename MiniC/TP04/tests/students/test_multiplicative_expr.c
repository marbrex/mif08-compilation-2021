#include "printlib.h"

int main() {
    
    int a;
    int b;
    int c;

    a = 42;
    b = 2;

    c = (a/b)*b + a%b;

    if (c == a) {
        println_int(1);
    }
    else {
        println_int(0);
    }

    return 0;
}

// EXPECTED
// 1
