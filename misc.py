import os
import random as r

debug = True

# clear screen
def cls() -> int:
    return os.system("cls")

def gp_calc(score: int) -> int:
    gp = 0
    if 95 <= score <= 100:
        gp = 50
    elif score < 60:
        gp = 0
    else:
        gp = 15 + (score - 59) // 3 * 3
    return gp

def judge(chance: int) -> bool:
    dice = r.randint(1, 100)
    return dice <= chance

# if __name__ == "__main__":
#     print(".".join(str(int(input("score: ")))))