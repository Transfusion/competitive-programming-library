#ifndef __STD_VECTOR__
#define __STD_VECTOR__
#include <vector>
#endif

/**
 * https://judge.yosupo.jp/submission/78809
 */
class DSU_Iterative_By_Size
{
private:
    std::vector<int> par;
    std::vector<int> size;

public:
    DSU_Iterative_By_Size(int sz) : par(sz), size(sz)
    {
        for (int i = 0; i < sz; i++)
        {
            par[i] = i;
            size[i] = 1;
        }
    }

    int find(int a)
    {
        int x = a;
        while (this->par[x] != x)
            x = this->par[x];
        while (this->par[a] != x)
        {
            this->par[a] = x;
            a = this->par[a];
        }
        return x;
    }

    bool un(int x, int y)
    {
        int tmp;
        int xr = this->find(x), yr = this->find(y);
        if (xr == yr)
            return false;
        else
        {
            if (this->size[xr] < this->size[yr])
            {
                // swap
                tmp = xr;
                xr = yr;
                yr = tmp;
            }
            this->par[yr] = xr;
            this->size[xr] += this->size[yr];
            return true;
        }
    }
};