#include "printlib.h"

int main() {

    int n;
    int a;
    int b;

    n = 2;
    a = 1;

    while(a <= n) {

        b = 1;

        while (b <= n) {

            println_int(a + b);

            b = b + 1;

        }

        a = a + 1;
    }

    return 0;
}

// EXPECTED
// 2
// 3
// 3
// 4
