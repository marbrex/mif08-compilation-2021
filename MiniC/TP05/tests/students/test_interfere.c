#include "printlib.h"

int main()
{
    int n, u, v, useless;
    n = 6;
    u = 0;
    while (n > 1)
    {
        n = n - 1;
        useless = 4;
        u = u + n;
    }
    println_int(u);
    return 0;
}

// EXPECTED
// 15