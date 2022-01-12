#include "printlib.h"

int main()
{
    int a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z;
    z = 6;
    while (z > 1)
    {
        a = 1;
        b = a*2;
        c = b*3;
        d = c*4;
        e = d*5;
        f = e*6;
        g = f*7;
        h = g*8;
        i = h*9;
        j = i*10;
        k = j*9;
        l = k*8;
        m = l*7;
        n = m*6;
        o = n*5;
        p = 3;
        q = 23;
        r = 12;
        s = 13;
        t = 15;
        u = 42;
        v = 12;
        w = 9;
        x = 64;
        y = a*2*b*3*c*4*d*5*e*6*f*7*g*8*h*9*i*10*j*9*k*8*l*7*m*6*n*5*o*4*p*3+q*2+r*1+s+2+t+3+u+4+v+5+w+6+x+7;
        z = z-1;
    }
    println_int(c);
    return 0;
}

// EXPECTED
// 6