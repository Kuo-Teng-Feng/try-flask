from random import randint
from data import listcancelpaths

def ini(n, today, tomorrow, the_day_after_tomorrow): # n-digit cancelpath ini.
    
    l = [randomizer(n)]
    exist = listcancelpaths(today, tomorrow, the_day_after_tomorrow) # datetime objects.
    while l[0] in exist:
        l[0] = randomizer(n)
    return l[0]

def randomizer(n): # n-digit cancelpath ini.
    
    chs = []
    for ele in [(48, 58), (65, 91), (97, 123)]:
        for i in range(ele[0], ele[1]):
            chs.append(chr(i))
    s = ""
    while len(s) < n:
        s += chs[(randint(0, 62))]
    return s