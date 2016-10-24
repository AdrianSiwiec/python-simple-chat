calls = []
depth = 0


def monit(level):

    def h(func):

        def u(*args, **kwargs):
            global depth
            depth += 1
            calls.append((False, u, level, args, depth, func.__name__))

            ret = func(*args, **kwargs)

            calls.append((True, u, level, ret, depth))

            depth -= 1

            return ret

        return u

    return h


def report(level, indent = "->", limits = None):
    for i in calls:
        if( i[2] > level ):
            continue
        if (limits != None and i[1] in limits):
            p = limits[i[1]][0]
            q = limits[i[1]][1]
        else:
            p = -1
            q = -1
        if (p == -1 or (i[4] >= p and i[4] <= q)):
            for l in range(i[4] - 1):
                print(indent, end = "")

            if (not i[0]):
                print(i[5] + "(" + ",".join(map(str, i[3])) + ")")
            else:
                print("return " + str(i[3]))


def clear():
    global calls
    global depth
    calls = []
    depth = 0
