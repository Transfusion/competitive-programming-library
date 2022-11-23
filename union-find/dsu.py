class DSU_Recursive_By_Size:
    """Iterative find, rank by size, and path compression"""

    def __init__(self, n):
        self.par = list(range(n))
        self.size = [1] * n

    def find(self, x):
        if self.par[x] != x:
            self.par[x] = self.find(self.par[x])
        return self.par[x]

    def union(self, x, y):
        xr, yr = self.find(x), self.find(y)
        if xr == yr:
            return False
        else:
            if self.size[xr] < self.size[yr]:
                xr, yr = yr, xr
            self.par[yr] = xr
            self.size[xr] += self.size[yr]
            self.size[yr] = 0
            # self.par[self.find(x)] = self.find(y)
            return True


class DSU_Iterative_By_Size:
    """Iterative find, rank by size, and path compression
    https://judge.yosupo.jp/submission/113655"""

    def __init__(self, n):
        self.par = list(range(n))
        self.size = [1] * n

    def find(self, a):
        x = a
        while self.par[x] != x:
            x = self.par[x]
        while self.par[a] != x:
            self.par[a], a = x, self.par[a]
        return x

    def union(self, x, y):
        xr, yr = self.find(x), self.find(y)
        if xr == yr:
            return False
        else:
            if self.size[xr] < self.size[yr]:
                xr, yr = yr, xr
            self.par[yr] = xr
            self.size[xr] += self.size[yr]
            self.size[yr] = 0
            # self.par[self.find(x)] = self.find(y)
            return True
