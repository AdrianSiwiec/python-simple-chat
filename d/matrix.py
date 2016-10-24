import copy


class matrIter:

    def __init__(self, m):
        self.m = m
        self.i = 0
        self.j = 0
        self.N = m.N

    def __iter__(self):
        return self

    def __next__(self):
        if (self.j == self.N):
            self.j = 0
            self.i += 1
        if (self.i == self.N):
            raise StopIteration
        self.j += 1
        return self.m.tab[self.i][self.j - 1]


class Matrix:

    def __init__(self, N, default = None):
        self.N = N
        if (default == None):
            self.tab = [[0 for _ in range(N)] for _ in range(N)]
        else:
            self.tab = copy.deepcopy(default)

    def __getitem__(self, index):
        return self.tab[index]

    def __add__(self, item):
        res = Matrix(self.N)
        for i in range(self.N):
            for j in range(self.N):
                res[i][j] = self[i][j] + item[i][j]
        return res

    def __mul__(self, item):
        if (type(item) is Matrix):
            res = Matrix(self.N)
            for k in range(self.N):
                for i in range(self.N):
                    for j in range(self.N):
                        res[i][j] += self[i][k] * item[k][j]
        else:
            res = Matrix(self.N)
            for i in range(self.N):
                for j in range(self.N):
                    res[i][j] = self[i][j] * item
        return res

    def __mod__(self, item):
        res = Matrix(self.N)
        for i in range(self.N):
            for j in range(self.N):
                res[i][j] = self[i][j] % item
        return res

    def __pow__(self, item):
        res = Matrix(self.N, self.tab)

        if (item == 0):
            for i in range(self.N):
                for j in range(self.N):
                    res.tab[i][j] = 1 if i == j else 0
            return res
        for i in range(item - 1):
            res *= self
        return res

    def __iter__(self):
        return matrIter(self)

    def __next__(self):
        if (self.j == self.N):
            self.j = 0
            self.i += 1
        if (self.i == self.N):
            raise StopIteration
        self.j += 1
        return self.tab[self.i][self.j - 1]

    def __str__(self):
        res = str(self.N) + "\n"
        for line in self.tab:
            for c in line:
                res += str(c) + " "
            res += "\n"
        return res
