#ifndef __STD_IOSTREAM__
#define __STD_IOSTREAM__
#include <iostream>
#endif

#ifndef __STD_VECTOR__
#define __STD_VECTOR__
#include <vector>
#endif

#define REP(i, n) for (int i = 0; (i) < (int)(n); ++(i))
template <typename T>
std::ostream &operator<<(std::ostream &out, std::vector<T> const &xs)
{
    REP(i, (int)xs.size() - 1)
    out << xs[i] << ' ';
    if (not xs.empty())
        out << xs.back();
    return out;
}
template <typename T>
void swap(T &a, T &b)
{
    T tmp;
    tmp = a;
    a = b;
    b = tmp;
}
#define dump(x) cerr << #x " = " << x << endl