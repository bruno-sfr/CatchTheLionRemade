from enum import Enum


class Flag(Enum):
    EXACT = 0
    UPPERBOUND = 1
    LOWERBOUND = 2


"""flag = Flag.EXACT
flag_2 = Flag.LOWERBOUND
print(flag.name)
print(flag_2.name)
if flag == Flag.EXACT:
    print("Wow")
if flag == Flag.LOWERBOUND:
    print("Wow")"""