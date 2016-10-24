source = input()
goal = input()

found = 0
for l in list(goal):
    if l != ' ' and goal.count(l) > source.count(l):
        print("NO")
        found = 1
        break

if(found == 0):
    print("YES")
