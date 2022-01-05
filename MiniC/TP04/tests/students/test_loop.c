#include "printlib.h"

int main() {
    
    int a;

    a = 1;

    while(a <= 5) {

        if (a % 2 == 0) {
            println_int(2);
        }
        else {
            println_int(a);
        }

        a = a + 1;
    }

    return 0;
}

// EXPECTED
// 1
// 2
// 3
// 2
// 5
