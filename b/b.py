from datetime import datetime

data = []
N = int(input())

for i in range(N):
    line = input().split(" ", 2)
    data.append((datetime.strptime(line[0] + " " + line[1], "%d.%m.%Y %H:%M"), line[2]))

data = sorted(data)

for p in data:
    print(str.format("{}.{} {} {}", p[0].strftime("%d.%m"), str(p[0].year).zfill(4) ,p[0].strftime("%H:%M"), p[1]))
