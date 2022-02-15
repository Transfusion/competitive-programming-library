#ifndef __STD_VECTOR__
#define __STD_VECTOR__
#include <vector>
#endif

/**
 * Partition(A, p, r)
1 x = A[r]
2 i = p-1
3 for j = p to r-1
4     do if A[j] <= x
5        then i = i+1
6            exchange A[i] and A[j] 
7 exchange A[i+1] and A[r]
8 returns the new position of the pivot
* https://onlinejudge.u-aizu.ac.jp/solutions/problem/ALDS1_6_B/review/6327055/Transfusion/C++17
*/
template <typename T>
int q_part(std::vector<T> &a, int l, int r)
{
    T pivot = a[r];
    int i = l - 1;
    T tmp;
    for (int j = l; j < r; j++)
    {
        if (a[j] <= pivot)
        {
            i++;
            // swap a[i] and a[j]
            tmp = a[i];
            a[i] = a[j];
            a[j] = tmp;
        }
    }
    tmp = a[i + 1];
    a[i + 1] = a[r];
    a[r] = tmp;
    return i + 1;
}

/**
 * Quicksort(A, p, r)
1 if p < r
2    then q = Partition(A, p, r)
3        run Quicksort(A, p, q-1)
4        run Quicksort(A, q+1, r)
* https://onlinejudge.u-aizu.ac.jp/solutions/problem/ALDS1_6_C/review/6327085/Transfusion/C++17
*/
template <typename T>
int q_sort(std::vector<T> &a, int l, int r)
{
    int q;
    if (l < r)
    {
        pvt_idx = q_part(a, l, r);
        q_sort(a, l, pvt_idx - 1);
        q_sort(a, pvt_idx + 1, r);
    }
}
