N = int(input())

count = {}
lists = {}

for i in range(N):
    line = input().replace("dodaj ", "").split(" zanim dodasz ")

    count[line[1]] = count.get(line[1], 0) + 1
    count[line[0]] = count.get(line[0], 0)
    lists[line[0]] = lists.get(line[0], [])
    lists[line[0]].append(line[1])

zeros = []

for item in count:
    if (count.get(item) == 0):
        zeros.append(item)

for item in zeros:
    count.pop(item)

while (len(zeros) > 0):
    item = zeros[0]
    zeros.pop(0)
    for related in lists.get(item, []):
        count[related] -= 1
        if (count[related] == 0):
            count.pop(related)
            zeros.append(related)

if (len(count) > 0):
    print("NIE")
else:
    print("TAK")
